import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Robô Analisador IAC - Entrada Real", page_icon="🎯", layout="centered")

st.title("🎯 Robô Analisador IAC - Estratégia Oficial")
st.markdown("Insira os resultados reais para o motor calcular o cruzamento exato.")

# Inicializar Histórico
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = []

# Tabela Oficial IAC Completa
TABELA_IAC_COMPLETA = {
    "Avestruz": {"grupo": 1, "alvos": ["Pavão", "Águia", "Camelo"], "dezenas": ["01", "02", "03", "04"]},
    "Águia": {"grupo": 2, "alvos": ["Galo", "Avestruz", "Burro"], "dezenas": ["05", "06", "07", "08"]},
    "Burro": {"grupo": 3, "alvos": ["Cavalo", "Macaco", "Elefante"], "dezenas": ["09", "10", "11", "12"]},
    "Borboleta": {"grupo": 4, "alvos": ["Cabra", "Cavalo", "Leão"], "dezenas": ["13", "14", "15", "16"]},
    "Cachorro": {"grupo": 5, "alvos": ["Gato", "Cabra", "Burro"], "dezenas": ["17", "18", "19", "20"]},
    "Cabra": {"grupo": 6, "alvos": ["Carneiro", "Cachorro", "Burro"], "dezenas": ["21", "22", "23", "24"]},
    "Carneiro": {"grupo": 7, "alvos": ["Camelo", "Cabra", "Macaco"], "dezenas": ["25", "26", "27", "28"]},
    "Camelo": {"grupo": 8, "alvos": ["Urso", "Carneiro", "Avestruz"], "dezenas": ["29", "30", "31", "32"]},
    "Cobra": {"grupo": 9, "alvos": ["Touro", "Camelo", "Cabra"], "dezenas": ["33", "34", "35", "36"]},
    "Coelho": {"grupo": 10, "alvos": ["Leão", "Cobra", "Tigre"], "dezenas": ["37", "38", "39", "40"]},
    "Cavalo": {"grupo": 11, "alvos": ["Elefante", "Borboleta", "Gato"], "dezenas": ["41", "42", "43", "44"]},
    "Elefante": {"grupo": 12, "alvos": ["Jacaré", "Cavalo", "Leão"], "dezenas": ["45", "46", "47", "48"]},
    "Galo": {"grupo": 13, "alvos": ["Águia", "Pavão", "Peru"], "dezenas": ["49", "50", "51", "52"]},
    "Gato": {"grupo": 14, "alvos": ["Cachorro", "Leão", "Coelho"], "dezenas": ["53", "54", "55", "56"]},
    "Jacaré": {"grupo": 15, "alvos": ["Macaco", "Elefante", "Porco"], "dezenas": ["57", "58", "59", "60"]},
    "Leão": {"grupo": 16, "alvos": ["Tigre", "Gato", "Elefante"], "dezenas": ["61", "62", "63", "64"]},
    "Macaco": {"grupo": 17, "alvos": ["Porco", "Burro", "Jacaré"], "dezenas": ["65", "66", "67", "68"]},
    "Porco": {"grupo": 18, "alvos": ["Peru", "Macaco", "Touro"], "dezenas": ["69", "70", "71", "72"]},
    "Pavão": {"grupo": 19, "alvos": ["Avestruz", "Galo", "Urso"], "dezenas": ["73", "74", "75", "76"]},
    "Peru": {"grupo": 20, "alvos": ["Veado", "Porco", "Galo"], "dezenas": ["77", "78", "79", "80"]},
    "Touro": {"grupo": 21, "alvos": ["Cobra", "Porco", "Vaca"], "dezenas": ["81", "82", "83", "84"]},
    "Tigre": {"grupo": 22, "alvos": ["Leão", "Coelho", "Urso"], "dezenas": ["85", "86", "87", "88"]},
    "Urso": {"grupo": 23, "alvos": ["Camelo", "Tigre", "Pavão"], "dezenas": ["89", "90", "91", "92"]},
    "Veado": {"grupo": 24, "alvos": ["Peru", "Avestruz", "Cobra"], "dezenas": ["93", "94", "95", "96"]},
    "Vaca": {"grupo": 25, "alvos": ["Touro", "Cobra", "Jacaré"], "dezenas": ["97", "98", "99", "00"]}
}

lista_bichos = sorted(list(TABELA_IAC_COMPLETA.keys()))

st.subheader("📝 Digitação dos Resultados Reais (1º ao 5º Prémio)")

col1, col2 = st.columns(2)
with col1:
    b1 = st.selectbox("1º Prémio (Cabeça):", lista_bichos, index=0)
    b2 = st.selectbox("2º Prémio:", lista_bichos, index=1)
    b3 = st.selectbox("3º Prémio:", lista_bichos, index=2)
with col2:
    b4 = st.selectbox("4º Prémio:", lista_bichos, index=3)
    b5 = st.selectbox("5º Prémio (Elástico):", lista_bichos, index=4)

if st.button("🚀 Processar Estratégia Oficial"):
    # Cruza a cabeça (1º) e o 5º prêmio com a matriz IAC oficial
    alvos_1 = TABELA_IAC_COMPLETA[b1]["alvos"]
    alvos_5 = TABELA_IAC_COMPLETA[b5]["alvos"]
    
    alvo_principal = alvos_1[0]
    alvo_secundario = alvos_1[1]
    alvo_elastico = alvos_5[0]

    d_1 = TABELA_IAC_COMPLETA[alvo_principal]
    d_2 = TABELA_IAC_COMPLETA[alvo_secundario]
    d_3 = TABELA_IAC_COMPLETA[alvo_elastico]

    st.markdown("---")
    st.subheader("🎫 PULE CIRÚRGICA DE ALTA PRECISÃO")
    
    st.markdown(f"""
    * **Base Analisada:** Cabeça (`{b1}`) | 5º Prêmio (`{b5}`)
    
    ---
    ### 📊 Alvos Validados para o Próximo Horário:
    
    1. **1º Alvo Principal (Puxada Direta da Cabeça) [R$ 1,50]:**
       * **{alvo_principal}** (Grupo {d_1['grupo']:02d}) | Dezenas: `{', '.join(d_1['dezenas'])}`
    
    2. **2º Alvo de Inversão & Família [R$ 1,50]:**
       * **{alvo_secundario}** (Grupo {d_2['grupo']:02d}) | Dezenas: `{', '.join(d_2['dezenas'])}`
    
    3. **3º Alvo de Cobertura do Efeito Elástico (5º Prêmio) [R$ 1,00]:**
       * **{alvo_elastico}** (Grupo {d_3['grupo']:02d}) | Dezenas: `{', '.join(d_3['dezenas'])}`
    
    4. **Duques e Terno Combinados:**
       * **Duque:** {alvo_principal} x {alvo_secundario} | **Terno de Grupo:** {alvo_principal} x {alvo_secundario} x {alvo_elastico}
    """)

    st.session_state.historico_apostas.append({
        "cabeca": b1,
        "quinto": b5,
        "alvos": f"{alvo_principal}, {alvo_secundario}, {alvo_elastico}"
    })

st.markdown("---")
st.subheader("📊 Histórico")
if st.session_state.historico_apostas:
    st.dataframe(pd.DataFrame(st.session_state.historico_apostas))
