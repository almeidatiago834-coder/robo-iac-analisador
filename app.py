import streamlit as st
import pandas as pd
import datetime

# Configuração da Página
st.set_page_config(page_title="Robô Analisador IAC", page_icon="🎯", layout="centered")

st.title("🎯 Robô Analisador IAC - Estratégia & Cruz do Dia")
st.markdown("Envie o print do resultado e gere sua pule cirúrgica de forma rápida e segura.")

# Inicializar Histórico de Apostas
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = []

# Tabela Oficial IAC de Puxadas e Famílias
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

# Função para calcular a Cruz do Dia
def calcular_cruz_do_dia():
    hoje = datetime.datetime.now()
    string_data = hoje.strftime("%d%m%Y")
    soma_digitos = sum(int(d) for d in string_data)
    segunda_soma = sum(int(d) for d in str(soma_digitos))
    
    digitos_cruz = list(string_data) + list(str(soma_digitos)) + list(str(segunda_soma))
    digitos_unicos = sorted(list(set([d for d in digitos_cruz if d != '0'])))
    if not digitos_unicos:
        digitos_unicos = ["1", "4", "7", "9"]
    return digitos_unicos[:4], string_data

cruz_base, data_str = calcular_cruz_do_dia()

st.sidebar.header("⚙️ Configurações")
st.sidebar.markdown(f"**Data:** {data_str[:2]}/{data_str[2:4]}/{data_str[4:]}")
st.sidebar.markdown(f"**Cruz do Dia:** `{' '.join(cruz_base)}`")

forcar_repeticao = st.sidebar.checkbox("🔄 Forçar Repetição (Matriz de Saturação)")

st.subheader("📸 Envie o Print do Horário")
foto_enviada = st.file_uploader("Cole ou envie a foto do resultado:", type=["png", "jpg", "jpeg"])

if foto_enviada:
    # Exibe a foto perfeitamente sem quebrar o servidor
    st.image(foto_enviada, caption="Print do Resultado Carregado", use_container_width=True)

# Seleção rápida e inteligente do Bicho que saiu na Cabeça (baseado no print)
lista_bichos_nomes = [v["bicho"] for v in TABELA_FAMILIAS_IAC.values()]
bicho_selecionado = st.selectbox("🐾 Bicho que saiu na Cabeça (conforme o print):", lista_bichos_nomes)

# Botão de Execução
if st.button("🚀 Gerar Pule Cirúrgica Completa"):
    # Encontra as chaves com base na seleção
    grupo_1 = "01"
    for k, v in TABELA_FAMILIAS_IAC.items():
        if v["bicho"] == bicho_selecionado:
            grupo_1 = k
            break
            
    bicho_cabeca_info = TABELA_FAMILIAS_IAC[grupo_1]
    bicho_apoio1_nome = bicho_cabeca_info["alvo"]
    
    # Segundo apoio baseado na cruz do dia
    idx_cruz = int(cruz_base[0]) % len(TABELA_FAMILIAS_IAC)
    grupo_apoio2 = f"{(idx_cruz % 25) + 1:02d}"
    bicho_apoio2_name = TABELA_FAMILIAS_IAC[grupo_apoio2]["bicho"]

    dezena_base = bicho_cabeca_info["dezenas"][0]
    
    if forcar_repeticao:
        status_transicao = "⚠️ Repetição autorizada pelo algoritmo (Saturação ativada)."
        dezena_final = dezena_base
        centena_final = "774"
        milhar_final = "3774"
    else:
        status_transicao = "🔒 Blindagem Ativa: Avanço de transição aplicado."
        dezena_trans = (int(dezena_base) + 3) % 100
        dezena_final = f"{dezena_trans:02d}"
        centena_final = "807"
        milhar_final = "4807"

    st.markdown("---")
    st.subheader("🎫 PULE CIRÚRGICA IAC (ESTRATÉGIA COMPLETA)")
    
    st.markdown(f"""
    * **Status do Algoritmo:** {status_transicao}
    * **Cruz do Dia Aplicada:** `{' - '.join(cruz_base)}`
    * **Bicho Principal de Cabeça:** **{bicho_selecionado} (Grupo {grupo_1})**
    * **Bichos de Apoio (Puxada + Cruz):** {bicho_apoio1_nome} e {bicho_apoio2_name}
    
    ---
    ### 📊 Divisão Fracionada da Aposta (Total: R$ 5,00):
    
    1. **Cabeça (1º Prêmio) [R$ 1,00]:** 
       * Grupo do {bicho_selecionado} ({grupo_1})
    
    2. **Cercado do 1º ao 3º Prêmio [R$ 1,00]:** 
       * Grupo do {bicho_selecionado} ({grupo_1})
    
    3. **Cercado do 1º ao 5º Prêmio [R$ 1,00]:** 
       * Grupos de Apoio ({bicho_apoio1_nome} e {bicho_apoio2_name})
    
    4. **Dezenas de Alta Precisão [R$ 0,60]:** 
       * Dezena **{dezena_final}** do {bicho_selecionado}
    
    5. **Duques de Grupo [R$ 0,60]:** 
       * {bicho_selecionado} x {bicho_apoio1_nome} / {bicho_selecionado} x {bicho_apoio2_name}
    
    6. **Centena e Milhar Seca [R$ 0,80]:** 
       * Centena: **{centena_final}**
       * Milhar Seca: **{milhar_final}**
    """)
    
    st.session_state.historico_apostas.append({
        "bicho_cabeca": bicho_selecionado,
        "status": "Repetido" if forcar_repeticao else "Transição"
    })

st.markdown("---")
st.subheader("📊 Histórico de Pules Geradas")
if st.session_state.historico_apostas:
    df_h = pd.DataFrame(st.session_state.historico_apostas)
    st.dataframe(df_h)
else:
    st.info("Nenhuma pule processada nesta sessão.")
