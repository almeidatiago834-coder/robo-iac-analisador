import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Robô Analisador IAC - Estratégia Oficial", page_icon="🎯", layout="centered")

st.title("🎯 Robô Analisador IAC - Estratégia Cirúrgica")
st.markdown("Envie os prints, informe a data da análise e gere sua pule cirúrgica baseada nas puxadas oficiais.")

# Inicializar Histórico de Apostas
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = []

# Tabela Oficial IAC de Puxadas e Famílias Completa
TABELA_FAMILIAS_IAC = {
    "01": {"bicho": "Avestruz", "grupo": "01", "alvo": "Pavão", "dezenas": ["01", "02", "03", "04"]},
    "02": {"bicho": "Águia", "grupo": "02", "alvo": "Galo", "dezenas": ["05", "06", "07", "08"]},
    "03": {"bicho": "Burro", "grupo": "03", "alvo": "Cavalo", "dezenas": ["09", "10", "11", "12"]},
    "04": {"bicho": "Borboleta", "grupo": "04", "alvo": "Cabra", "dezenas": ["13", "14", "15", "16"]},
    "05": {"bicho": "Cachorro", "grupo": "05", "alvo": "Gato", "dezenas": ["17", "18", "19", "20"]},
    "06": {"bicho": "Cabra", "grupo": "06", "alvo": "Carneiro", "dezenas": ["21", "22", "23", "24"]},
    "07": {"bicho": "Carneiro", "grupo": "07", "alvo": "Camelo", "dezenas": ["25", "26", "27", "28"]},
    "08": {"bicho": "Camelo", "grupo": "08", "alvo": "Urso", "dezenas": ["29", "30", "31", "32"]},
    "09": {"bicho": "Cobra", "grupo": "09", "alvo": "Touro", "dezenas": ["33", "34", "35", "36"]},
    "10": {"bicho": "Coelho", "grupo": "10", "alvo": "Leão", "dezenas": ["37", "38", "39", "40"]},
    "11": {"bicho": "Cavalo", "grupo": "11", "alvo": "Elefante", "dezenas": ["41", "42", "43", "44"]},
    "12": {"bicho": "Elefante", "grupo": "12", "alvo": "Jacaré", "dezenas": ["45", "46", "47", "48"]},
    "13": {"bicho": "Galo", "grupo": "13", "alvo": "Águia", "dezenas": ["49", "50", "51", "52"]},
    "14": {"bicho": "Gato", "grupo": "14", "alvo": "Cachorro", "dezenas": ["53", "54", "55", "56"]},
    "15": {"bicho": "Jacaré", "grupo": "15", "alvo": "Macaco", "dezenas": ["57", "58", "59", "60"]},
    "16": {"bicho": "Leão", "grupo": "16", "alvo": "Tigre", "dezenas": ["61", "62", "63", "64"]},
    "17": {"bicho": "Macaco", "grupo": "17", "alvo": "Porco", "dezenas": ["65", "66", "67", "68"]},
    "18": {"bicho": "Porco", "grupo": "18", "alvo": "Peru", "dezenas": ["69", "70", "71", "72"]},
    "19": {"bicho": "Pavão", "grupo": "19", "alvo": "Avestruz", "dezenas": ["73", "74", "75", "76"]},
    "20": {"bicho": "Peru", "grupo": "20", "alvo": "Veado", "dezenas": ["77", "78", "79", "80"]},
    "21": {"bicho": "Touro", "grupo": "21", "alvo": "Cobra", "dezenas": ["81", "82", "83", "84"]},
    "22": {"bicho": "Tigre", "grupo": "22", "alvo": "Leão", "dezenas": ["85", "86", "87", "88"]},
    "23": {"bicho": "Urso", "grupo": "23", "alvo": "Camelo", "dezenas": ["89", "90", "91", "92"]},
    "24": {"bicho": "Veado", "grupo": "24", "alvo": "Peru", "dezenas": ["93", "94", "95", "96"]},
    "25": {"bicho": "Vaca", "grupo": "25", "alvo": "Touro", "dezenas": ["97", "98", "99", "00"]}
}

st.sidebar.header("⚙️ Painel de Controle IAC")

# TAXA/SELETOR PARA DIGITAR OU ESCOLHER A DATA DO DIA
data_selecionada = st.sidebar.date_input("📅 Data da Análise:", datetime.now())
string_data = data_selecionada.strftime("%d%m%Y")

# Cálculo dinâmico da Cruz do Dia com base na data escolhida por você
soma_digitos = sum(int(d) for d in string_data)
segunda_soma = sum(int(d) for d in str(soma_digitos))
digitos_cruz = list(string_data) + list(str(soma_digitos)) + list(str(segunda_soma))
digitos_unicos = [d for d in digitos_cruz if d != '0']

cruz_gerada = []
for d in digitos_unicos:
    if d not in cruz_gerada:
        cruz_gerada.append(d)
    if len(cruz_gerada) == 4:
        break
if len(cruz_gerada) < 4:
    cruz_gerada = ["1", "4", "7", "9"]

st.sidebar.markdown(f"**Cruz do Dia Gerada:** `{' '.join(cruz_gerada)}`")
forcar_repeticao = st.sidebar.checkbox("🔄 Forçar Repetição (Matriz de Saturação)")

st.subheader("📸 1. Envie os Prints dos Horários")
fotos_carregadas = st.file_uploader(
    "Carregue múltiplos prints (ex: 11h, 12h, etc.):", 
    type=["png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if fotos_carregadas:
    st.success(f"{len(fotos_carregadas)} print(s) carregado(s) com sucesso!")
    cols = st.columns(len(fotos_carregadas) if len(fotos_carregadas) <= 3 else 3)
    for idx, foto in enumerate(fotos_carregadas):
        with cols[idx % len(cols)]:
            st.image(foto, caption=f"Print {idx+1}", use_container_width=True)

st.markdown("---")
st.subheader("🐾 2. Confirme o Bicho que Saiu na Cabeça (Conforme o Print)")
lista_bichos_nomes = [v["bicho"] for v in TABELA_FAMILIAS_IAC.values()]
bicho_escolhido = st.selectbox("Selecione o Bicho da Cabeça do último resultado:", lista_bichos_nomes, index=23) # Padrão Veado

# Botão de Execução Estratégica
if st.button("🚀 Executar Análise Cirúrgica Completa"):
    # Encontra o grupo e informações do bicho escolhido
    grupo_cabeca = "24"
    for k, v in TABELA_FAMILIAS_IAC.items():
        if v["bicho"] == bicho_escolhido:
            grupo_cabeca = k
            break
            
    bicho_cabeca_info = TABELA_FAMILIAS_IAC[grupo_cabeca]
    bicho_alvo_nome = bicho_cabeca_info["alvo"]
    
    # Descobre o número do grupo alvo
    grupo_alvo = "20"
    for k, v in TABELA_FAMILIAS_IAC.items():
        if v["bicho"] == bicho_alvo_nome:
            grupo_alvo = k
            break

    # Apoio Cruz do Dia
    digito_cruz_int = int(cruz_gerada[0])
    grupo_cruz_num = f"{((digito_cruz_int - 1) % 25) + 1:02d}"
    bicho_cruz_nome = TABELA_FAMILIAS_IAC[grupo_cruz_num]["bicho"]

    dezena_base = bicho_cabeca_info["dezenas"][0]
    
    if forcar_repeticao:
        status_transicao = "⚠️ Saturação Ativada: Trabalhando na linha de repetição direta."
        dezena_final = dezena_base
        milhar_puxada = f"4{bicho_cabeca_info['dezenas'][0]}6"
    else:
        status_transicao = "🔒 Blindagem Ativa: Avanço tático de transição aplicado."
        dezena_trans = (int(dezena_base) + 3) % 100
        dezena_final = f"{dezena_trans:02d}"
        milhar_puxada = f"7{dezena_final}2"

    st.markdown("---")
    st.subheader(f"🎫 PULE CIRÚRGICA IAC — Data: {data_selecionada.strftime('%d/%m/%Y')}")
    
    st.markdown(f"""
    * **Status do Algoritmo:** {status_transicao}
    * **Cruz do Dia Calculada:** `{' - '.join(cruz_gerada)}`
    * **Cabeça Analisada:** **{bicho_escolhido} (Grupo {grupo_cabeca})**
    * **Alvo de Puxada Oficial IAC:** **{bicho_alvo_nome} (Grupo {grupo_alvo})**
    * **Apoio Cruz do Dia:** **{bicho_cruz_nome} (Grupo {grupo_cruz_num})**
    
    ---
    ### 📊 Distribuição Tática da Pule Cirúrgica (R$ 5,00):
    
    1. **Cabeça Seca (1º Prêmio) [R$ 1,00]:** 
       * Grupo {grupo_cabeca} ({bicho_escolhido})
    
    2. **Cercado Parcial (1º ao 3º) [R$ 1,00]:** 
       * Grupo {grupo_cabeca} ({bicho_escolhido})
    
    3. **Cercado Amplo (1º ao 5º) [R$ 1,00]:** 
       * Grupos de Puxada e Cruz: **{bicho_alvo_nome}** e **{bicho_cruz_nome}**
    
    4. **Dezenas de Alta Precisão [R$ 0,60]:** 
       * Dezenas do bloco principal e dezena **{dezena_final}**
    
    5. **Duques Combinados [R$ 0,60]:** 
       * {bicho_escolhido} x {bicho_alvo_nome} / {bicho_escolhido} x {bicho_cruz_nome}
    
    6. **Centena e Milhar Cirúrgica [R$ 0,80]:** 
       * Milhar Principal: **{milhar_puxada}**
    """)
    
    st.session_state.historico_apostas.append({
        "data": data_selecionada.strftime('%d/%m/%Y'),
        "bicho_cabeca": bicho_escolhido,
        "alvo": bicho_alvo_nome,
        "status": "Repetido" if forcar_repeticao else "Transição"
    })

st.markdown("---")
st.subheader("📊 Histórico de Pules Executadas")
if st.session_state.historico_apostas:
    df_h = pd.DataFrame(st.session_state.historico_apostas)
    st.dataframe(df_h)
else:
    st.info("Nenhuma pule registrada nesta sessão.")
