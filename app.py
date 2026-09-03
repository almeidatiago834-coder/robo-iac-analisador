import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Robô Analisador IAC - Tiro das 15h", page_icon="🎯", layout="centered")

st.title("🎯 Robô Analisador IAC - Cruzamento Dois Horários (Tiro 15h)")
st.markdown("Cruzamento avançado: Penúltimo Horário + Último Horário para fechar o tiro das 15h.")

# Inicializar Histórico
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = []

# Tabela Oficial IAC Completa
TABELA_IAC_COMPLETA = {
    "Avestruz": {"grupo": 1, "alvos": ["Pavão", "Águia", "Camelo", "Urso"], "dezenas": ["01", "02", "03", "04"]},
    "Águia": {"grupo": 2, "alvos": ["Galo", "Avestruz", "Burro", "Coelho"], "dezenas": ["05", "06", "07", "08"]},
    "Burro": {"grupo": 3, "alvos": ["Cavalo", "Macaco", "Elefante", "Cobra"], "dezenas": ["09", "10", "11", "12"]},
    "Borboleta": {"grupo": 4, "alvos": ["Cabra", "Cavalo", "Leão", "Gato"], "dezenas": ["13", "14", "15", "16"]},
    "Cachorro": {"grupo": 5, "alvos": ["Gato", "Cabra", "Burro", "Vaca"], "dezenas": ["17", "18", "19", "20"]},
    "Cabra": {"grupo": 6, "alvos": ["Carneiro", "Cachorro", "Burro", "Touro"], "dezenas": ["21", "22", "23", "24"]},
    "Carneiro": {"grupo": 7, "alvos": ["Camelo", "Cabra", "Macaco", "Peru"], "dezenas": ["25", "26", "27", "28"]},
    "Camelo": {"grupo": 8, "alvos": ["Urso", "Carneiro", "Avestruz", "Jacaré"], "dezenas": ["29", "30", "31", "32"]},
    "Cobra": {"grupo": 9, "alvos": ["Touro", "Camelo", "Cabra", "Leão"], "dezenas": ["33", "34", "35", "36"]},
    "Coelho": {"grupo": 10, "alvos": ["Leão", "Cobra", "Tigre", "Águia"], "dezenas": ["37", "38", "39", "40"]},
    "Cavalo": {"grupo": 11, "alvos": ["Elefante", "Borboleta", "Gato", "Burro"], "dezenas": ["41", "42", "43", "44"]},
    "Elefante": {"grupo": 12, "alvos": ["Jacaré", "Cavalo", "Leão", "Macaco"], "dezenas": ["45", "46", "47", "48"]},
    "Galo": {"grupo": 13, "alvos": ["Águia", "Pavão", "Peru", "Avestruz"], "dezenas": ["49", "50", "51", "52"]},
    "Gato": {"grupo": 14, "alvos": ["Cachorro", "Leão", "Coelho", "Borboleta"], "dezenas": ["53", "54", "55", "56"]},
    "Jacaré": {"grupo": 15, "alvos": ["Macaco", "Elefante", "Porco", "Camelo"], "dezenas": ["57", "58", "59", "60"]},
    "Leão": {"grupo": 16, "alvos": ["Tigre", "Gato", "Elefante", "Cobra"], "dezenas": ["61", "62", "63", "64"]},
    "Macaco": {"grupo": 17, "alvos": ["Porco", "Burro", "Jacaré", "Carneiro"], "dezenas": ["65", "66", "67", "68"]},
    "Porco": {"grupo": 18, "alvos": ["Peru", "Macaco", "Touro", "Elefante"], "dezenas": ["69", "70", "71", "72"]},
    "Pavão": {"grupo": 19, "alvos": ["Avestruz", "Galo", "Urso", "Galo"], "dezenas": ["73", "74", "75", "76"]},
    "Peru": {"grupo": 20, "alvos": ["Veado", "Porco", "Galo", "Carneiro"], "dezenas": ["77", "78", "79", "80"]},
    "Touro": {"grupo": 21, "alvos": ["Cobra", "Porco", "Vaca", "Cabra"], "dezenas": ["81", "82", "83", "84"]},
    "Tigre": {"grupo": 22, "alvos": ["Leão", "Coelho", "Urso", "Coelho"], "dezenas": ["85", "86", "87", "88"]},
    "Urso": {"grupo": 23, "alvos": ["Camelo", "Tigre", "Pavão", "Avestruz"], "dezenas": ["89", "90", "91", "92"]},
    "Veado": {"grupo": 24, "alvos": ["Peru", "Avestruz", "Cobra", "Peru"], "dezenas": ["93", "94", "95", "96"]},
    "Vaca": {"grupo": 25, "alvos": ["Touro", "Cobra", "Jacaré", "Cachorro"], "dezenas": ["97", "98", "99", "00"]}
}

lista_bichos = sorted(list(TABELA_IAC_COMPLETA.keys()))

st.subheader("⏱️ Passo 1: Penúltimo Horário (1º ao 5º Prémio)")
col1, col2 = st.columns(2)
with col1:
    p1_cabeca = st.selectbox("1º Prémio (Penúltimo):", lista_bichos, index=0, key="p1_c")
    p1_p2 = st.selectbox("2º Prémio (Penúltimo):", lista_bichos, index=1, key="p1_2")
    p1_p3 = st.selectbox("3º Prémio (Penúltimo):", lista_bichos, index=2, key="p1_3")
with col2:
    p1_p4 = st.selectbox("4º Prémio (Penúltimo):", lista_bichos, index=3, key="p1_4")
    p1_p5 = st.selectbox("5º Prémio (Penúltimo):", lista_bichos, index=4, key="p1_5")

st.markdown("---")
st.subheader("⏱️ Passo 2: Último Horário / Atual (1º ao 5º Prémio)")
col3, col4 = st.columns(2)
with col3:
    u1_cabeca = st.selectbox("1º Prémio (Último/Cabeça):", lista_bichos, index=10, key="u1_c")
    u1_p2 = st.selectbox("2º Prémio (Último):", lista_bichos, index=5, key="u1_2")
    u1_p3 = st.selectbox("3º Prémio (Último):", lista_bichos, index=6, key="u1_3")
with col4:
    u1_p4 = st.selectbox("4º Prémio (Último):", lista_bichos, index=7, key="u1_4")
    u1_p5 = st.selectbox("5º Prémio (Último/Elástico):", lista_bichos, index=12, key="u1_5")

if st.button("🚀 Processar Tiro Certeiro para as 15h"):
    # Consolida todos os 10 bichos que saíram nos dois horários para blindagem total
    penultimo_sorteio = [p1_cabeca, p1_p2, p1_p3, p1_p4, p1_p5]
    ultimo_sorteio = [u1_cabeca, u1_p2, u1_p3, u1_p4, u1_p5]
    todos_sorteados = penultimo_sorteio + ultimo_sorteio
    
    candidatos_pontuados = {}
    
    # Processa o penúltimo horário (peso menor de histórico)
    for idx, bicho in enumerate(penultimo_sorteio):
        peso = 2 if idx == 0 else 1
        for alvo in TABELA_IAC_COMPLETA[bicho]["alvos"]:
            if alvo not in todos_sorteados:
                candidatos_pontuados[alvo] = candidatos_pontuados.get(alvo, 0) + peso

    # Processa o último horário (peso máximo na cabeça e no 5º prêmio por ser transição direta)
    for idx, bicho in enumerate(ultimo_sorteio):
        peso = 4 if idx == 0 else (3 if idx == 4 else 2)
        for alvo in TABELA_IAC_COMPLETA[bicho]["alvos"]:
            if alvo not in todos_sorteados:
                candidatos_pontuados[alvo] = candidatos_pontuados.get(alvo, 0) + peso

    # Ordena os melhores alvos cruzados
    alvos_ordenados = sorted(candidatos_pontuados.keys(), key=lambda x: candidatos_pontuados[x], reverse=True)

    while len(alvos_ordenados) < 3:
        alvos_ordenados.append("")

    alvo_1 = alvos_ordenados[0]
    alvo_2 = alvos_ordenados[1]
    alvo_3 = alvos_ordenados[2]

    d_1 = TABELA_IAC_COMPLETA[alvo_1]
    d_2 = TABELA_IAC_COMPLETA[alvo_2]
    d_3 = TABELA_IAC_COMPLETA[alvo_3]

    st.markdown("---")
    st.subheader("🎫 PULE DE OURO — TIRO CERTEIRO DAS 15H")
    
    st.markdown(f"""
    * **Base Cruzada (10 Prêmios Bloqueados):** Analisado o fluxo do penúltimo e último horários.
    
    ---
    ### 📊 Os 3 Alvos Definitivos para as 15h:
    
    1. **1º Alvo Principal (Máxima Convergência de Fluxo) [R$ 1,50]:**
       * **{alvo_1}** (Grupo {d_1['grupo']:02d}) | Dezenas: `{', '.join(d_1['dezenas'])}`
    
    2. **2º Alvo de Transição & Inversão [R$ 1,50]:**
       * **{alvo_2}** (Grupo {d_2['grupo']:02d}) | Dezenas: `{', '.join(d_2['dezenas'])}`
    
    3. **3º Alvo Elástico de Fechamento [R$ 1,00]:**
       * **{alvo_3}** (Grupo {d_3['grupo']:02d}) | Dezenas: `{', '.join(d_3['dezenas'])}`
    
    4. **Duques e Terno Combinados:**
       * **Duque:** {alvo_1} x {alvo_2} | **Terno de Grupo:** {alvo_1} x {alvo_2} x {alvo_3}
    """)

    st.session_state.historico_apostas.append({
        "horario_alvo": "15:00",
        "alvos_15h": f"{alvo_1}, {alvo_2}, {alvo_3}"
    })

st.markdown("---")
st.subheader("📊 Histórico de Tiros")
if st.session_state.historico_apostas:
    st.dataframe(pd.DataFrame(st.session_state.historico_apostas))
