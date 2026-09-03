import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Robô Analisador IAC - Estratégia Blindada", page_icon="🎯", layout="centered")

st.title("🎯 Robô Analisador IAC - Motor de Cruzamento Blindado")
st.markdown("Exclusão absoluta dos sorteados: o robô só traz bichos novos puxados pela matriz.")

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

st.subheader("📝 Digitação dos Resultados Reais (1º ao 5º Prémio)")

col1, col2 = st.columns(2)
with col1:
    b1 = st.selectbox("1º Prémio (Cabeça):", lista_bichos, index=23)
    b2 = st.selectbox("2º Prémio:", lista_bichos, index=0)
    b3 = st.selectbox("3º Prémio:", lista_bichos, index=1)
with col2:
    b4 = st.selectbox("4º Prémio:", lista_bichos, index=14)
    b5 = st.selectbox("5º Prémio (Elástico):", lista_bichos, index=12)

if st.button("🚀 Processar Estratégia com Exclusão Absoluta"):
    # Lista de tudo o que saiu no sorteio (para NUNCA aparecer como palpite)
    bichos_sorteados = [b1, b2, b3, b4, b5]
    
    candidatos_pontuados = {}
    
    for idx, bicho in enumerate(bichos_sorteados):
        peso = 3 if idx == 0 else (2 if idx == 4 else 1)
        alvos_puxada = TABELA_IAC_COMPLETA[bicho]["alvos"]
        
        for alvo in alvos_puxada:
            # BLOQUEIO RIGOROSO: Só pontua se o alvo NÃO estiver entre os 5 prêmios sorteados
            if alvo not in bichos_sorteados:
                candidatos_pontuados[alvo] = candidatos_pontuados.get(alvo, 0) + peso

    # Ordena os candidatos limpos (que não saíram no print)
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
    st.subheader("🎫 PULE CIRÚRGICA 100% LIMPA")
    
    st.markdown(f"""
    * **Sorteio Base (Bloqueados):** {', '.join(bichos_sorteados)}
    
    ---
    ### 📊 Alvos Exclusivos para o Próximo Horário:
    
    1. **1º Alvo Principal [R$ 1,50]:**
       * **{alvo_1}** (Grupo {d_1['grupo']:02d}) | Dezenas: `{', '.join(d_1['dezenas'])}`
    
    2. **2º Alvo de Inversão [R$ 1,50]:**
       * **{alvo_2}** (Grupo {d_2['grupo']:02d}) | Dezenas: `{', '.join(d_2['dezenas'])}`
    
    3. **3º Alvo Elástico [R$ 1,00]:**
       * **{alvo_3}** (Grupo {d_3['grupo']:02d}) | Dezenas: `{', '.join(d_3['dezenas'])}`
    
    4. **Duques e Terno Combinados:**
       * **Duque:** {alvo_1} x {alvo_2} | **Terno de Grupo:** {alvo_1} x {alvo_2} x {alvo_3}
    """)

    st.session_state.historico_apostas.append({
        "base": f"{b1} até {b5}",
        "alvos_limpos": f"{alvo_1}, {alvo_2}, {alvo_3}"
    })

st.markdown("---")
st.subheader("📊 Histórico")
if st.session_state.historico_apostas:
    st.dataframe(pd.DataFrame(st.session_state.historico_apostas))
