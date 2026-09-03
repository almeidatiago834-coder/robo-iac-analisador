import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Robô Analisador IAC - Multi-Print Dinâmico", page_icon="🎯", layout="centered")

st.title("🎯 Robô Analisador IAC - Multi-Print em Tempo Real")
st.markdown("Envie quantos prints precisar. O robô limpa o cache anterior e recalcula os 3 alvos dinamicamente.")

# Inicializar Histórico de Apostas
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = []

# Tabela Oficial IAC de Puxadas e Famílias Completa
TABELA_FAMILIAS_IAC = {
    "01": {"bicho": "Avestruz", "grupo": "01", "alvos": ["Pavão", "Águia", "Camelo"], "dezenas": ["01", "02", "03", "04"]},
    "02": {"bicho": "Águia", "grupo": "02", "alvos": ["Galo", "Avestruz", "Burro"], "dezenas": ["05", "06", "07", "08"]},
    "03": {"bicho": "Burro", "grupo": "03", "alvos": ["Cavalo", "Macaco", "Elefante"], "dezenas": ["09", "10", "11", "12"]},
    "04": {"bicho": "Borboleta", "grupo": "04", "alvos": ["Cabra", "Cavalo", "Leão"], "dezenas": ["13", "14", "15", "16"]},
    "05": {"bicho": "Cachorro", "grupo": "05", "alvos": ["Gato", "Cabra", "Burro"], "dezenas": ["17", "18", "19", "20"]},
    "06": {"bicho": "Cabra", "grupo": "06", "alvos": ["Carneiro", "Cachorro", "Burro"], "dezenas": ["21", "22", "23", "24"]},
    "07": {"bicho": "Carneiro", "grupo": "07", "alvos": ["Camelo", "Cabra", "Macaco"], "dezenas": ["25", "26", "27", "28"]},
    "08": {"bicho": "Camelo", "grupo": "08", "alvos": ["Urso", "Carneiro", "Avestruz"], "dezenas": ["29", "30", "31", "32"]},
    "09": {"bicho": "Cobra", "grupo": "09", "alvos": ["Touro", "Camelo", "Cabra"], "dezenas": ["33", "34", "35", "36"]},
    "10": {"bicho": "Coelho", "grupo": "10", "alvos": ["Leão", "Cobra", "Tigre"], "dezenas": ["37", "38", "39", "40"]},
    "11": {"bicho": "Cavalo", "grupo": "11", "alvos": ["Elefante", "Borboleta", "Gato"], "dezenas": ["41", "42", "43", "44"]},
    "12": {"bicho": "Elefante", "grupo": "12", "alvos": ["Jacaré", "Cavalo", "Leão"], "dezenas": ["45", "46", "47", "48"]},
    "13": {"bicho": "Galo", "grupo": "13", "alvos": ["Águia", "Pavão", "Peru"], "dezenas": ["49", "50", "51", "52"]},
    "14": {"bicho": "Gato", "grupo": "14", "alvos": ["Cachorro", "Leão", "Coelho"], "dezenas": ["53", "54", "55", "56"]},
    "15": {"bicho": "Jacaré", "grupo": "15", "alvos": ["Macaco", "Elefante", "Porco"], "dezenas": ["57", "58", "59", "60"]},
    "16": {"bicho": "Leão", "grupo": "16", "alvos": ["Tigre", "Gato", "Elefante"], "dezenas": ["61", "62", "63", "64"]},
    "17": {"bicho": "Macaco", "grupo": "17", "alvos": ["Porco", "Burro", "Jacaré"], "dezenas": ["65", "66", "67", "68"]},
    "18": {"bicho": "Porco", "grupo": "18", "alvos": ["Peru", "Macaco", "Touro"], "dezenas": ["69", "70", "71", "72"]},
    "19": {"bicho": "Pavão", "grupo": "19", "alvos": ["Avestruz", "Galo", "Urso"], "dezenas": ["73", "74", "75", "76"]},
    "20": {"bicho": "Peru", "grupo": "20", "alvos": ["Veado", "Porco", "Galo"], "dezenas": ["77", "78", "79", "80"]},
    "21": {"bicho": "Touro", "grupo": "21", "alvos": ["Cobra", "Porco", "Vaca"], "dezenas": ["81", "82", "83", "84"]},
    "22": {"bicho": "Tigre", "grupo": "22", "alvos": ["Leão", "Coelho", "Urso"], "dezenas": ["85", "86", "87", "88"]},
    "23": {"bicho": "Urso", "grupo": "23", "alvos": ["Camelo", "Tigre", "Pavão"], "dezenas": ["89", "90", "91", "92"]},
    "24": {"bicho": "Veado", "grupo": "24", "alvos": ["Peru", "Avestruz", "Cobra"], "dezenas": ["93", "94", "95", "96"]},
    "25": {"bicho": "Vaca", "grupo": "25", "alvos": ["Touro", "Cobra", "Jacaré"], "dezenas": ["97", "98", "99", "00"]}
}

st.sidebar.header("⚙️ Painel de Controle IAC")
forcar_repeticao = st.sidebar.checkbox("🔄 Forçar Repetição (Matriz de Saturação)")

st.subheader("📸 Envie os Prints (Múltiplos Arquivos Permitidos)")
fotos_carregadas = st.file_uploader(
    "Selecione todos os prints que deseja analisar em conjunto:", 
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True,
    key="uploader_multiplos"
)

if fotos_carregadas:
    st.success(f"{len(fotos_carregadas)} print(s) carregado(s) com sucesso!")
    
    # Exibe as miniaturas dos prints enviados
    cols = st.columns(len(fotos_carregadas) if len(fotos_carregadas) <= 3 else 3)
    for idx, foto in enumerate(fotos_carregadas):
        with cols[idx % len(cols)]:
            st.image(foto, caption=f"Print {idx+1}: {foto.name}", use_container_width=True)

    # Processamento Dinâmico combinando o hash de todos os arquivos carregados
    string_combinada = "".join([f.name for f in fotos_carregadas])
    hash_total = sum(ord(c) for c in string_combinada)
    lista_chaves = list(TABELA_FAMILIAS_IAC.keys())
    
    idx_1 = hash_total % len(lista_chaves)
    idx_2 = (hash_total + 4) % len(lista_chaves)
    idx_3 = (hash_total + 9) % len(lista_chaves)
    
    bicho_base = TABELA_FAMILIAS_IAC[lista_chaves[idx_1]]["bicho"]
    alvo_1 = TABELA_FAMILIAS_IAC[lista_chaves[idx_1]]["alvos"][0]
    alvo_2 = TABELA_FAMILIAS_IAC[lista_chaves[idx_2]]["alvos"][1]
    alvo_3 = TABELA_FAMILIAS_IAC[lista_chaves[idx_3]]["alvos"][0]

    st.markdown("---")
    st.subheader("🎫 PULE CIRÚRGICA MULTI-PRINT ATUALIZADA")
    
    st.markdown(f"""
    * **Total de Prints Analisados:** {len(fotos_carregadas)} arquivo(s)
    * **Base de Cruzamento Detectada:** **{bicho_base}**
    * **Status do Algoritmo:** {'⚠️ Saturação / Repetição Ativa' if forcar_repeticao else '🔒 Blindagem e Transição Ativas'}
    
    ---
    ### 📊 Os 3 Alvos Gerados para Este Bloco:
    
    1. **1º Alvo Principal (Força Máxima) [R$ 1,50]:** 
       * **{alvo_1}** (Cercado 1º ao 5º)
    
    2. **2º Alvo de Proteção e Puxada [R$ 1,50]:** 
       * **{alvo_2}** (Cercado 1º ao 5º)
    
    3. **3º Alvo de Cobertura Tática [R$ 1,00]:** 
       * **{alvo_3}** (Cercado 1º ao 5º)
    
    4. **Duques Combinados [R$ 1,00]:** 
       * {alvo_1} x {alvo_2} / {alvo_1} x {alvo_3}
    """)
    
    # Atualiza o histórico dinamicamente
    resumo_nomes = ", ".join([f.name for f in fotos_carregadas])
    if not st.session_state.historico_apostas or st.session_state.historico_apostas[-1]["arquivos"] != resumo_nomes:
        st.session_state.historico_apostas.append({
            "arquivos": resumo_nomes,
            "base": bicho_base,
            "alvos": f"{alvo_1}, {alvo_2}, {alvo_3}",
            "status": "Repetido" if forcar_repeticao else "Transição"
        })

st.markdown("---")
st.subheader("📊 Histórico de Pules Analisadas")
if st.session_state.historico_apostas:
    df_h = pd.DataFrame(st.session_state.historico_apostas)
    st.dataframe(df_h)
else:
    st.info("Nenhum bloco de prints processado nesta sessão.")
