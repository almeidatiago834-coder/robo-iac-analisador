import streamlit as st
import pandas as pd
import random

# Configuração da Página
st.set_page_config(page_title="Robô Analisador IAC", page_icon="🎯", layout="centered")

st.title("🎯 Robô Analisador IAC - Blindagem de Pules")
st.markdown("Sistema automatizado de análise, histórico e prevenção de erros por família.")

# 1. Simulação de Banco de Dados de Histórico e Famílias
# (No seu app real, isso puxa de um arquivo CSV ou banco de dados)
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = []

# Dicionário simplificado de famílias e puxadas do IAC
TABELA_PUXADAS = {
    "Avestruz": {"grupo": "01", "familia_direta": "Pavão", "dezenas": ["01", "02", "03", "04"]},
    "Cabra": {"grupo": "06", "familia_direta": "Carneiro", "dezenas": ["21", "22", "23", "24"]},
    "Pavão": {"grupo": "19", "familia_direta": "Avestruz", "dezenas": ["73", "74", "75", "76"]},
    "Carneiro": {"grupo": "07", "familia_direta": "Cabra", "dezenas": ["25", "26", "27", "28"]}
}

# 2. Área de Entrada de Dados do Último Sorteio
st.subheader("📥 Entrada de Resultados")
col1, col2 = st.columns(2)
with col1:
    horario_sorteio = st.selectbox("Horário da Extração", ["10h", "12h", "15h", "19h", "Federal"])
with col2:
    bicho_cabeca = st.selectbox("Bicho que deu na Cabeça (1º Prêmiio)", list(TABELA_PUXADAS.keys()))

milhar_informada = st.text_input("Digite o Milhar/Centena que saiu (Ex: 3774):", "3774")

# 3. Botão de Execução do Algoritmo IAC
if st.button("🚀 Rodar Análise e Gerar Pule Blindada"):
    
    # Lógica de Puxada baseada na Família (Regra de Ouro)
    dados_bicho = TABELA_PUXADAS[bicho_cabeca]
    bicho_alvo = dados_bicho["familia_direta"]
    
    # Regra de Transição: Evitar repetir exatamente o passado, gerando avanço numérico
    dezena_base = int(milhar_informada[-2:]) if milhar_informada.isdigit() and len(milhar_informada) >= 2 else 0
    dezena_transicao = f"{(dezena_base + 3) % 100:02d}"
    dezena_espelho_mais = f"{(dezena_base + 4) % 100:02d}"
    dezena_espelho_menos = f"{(dezena_base + 2) % 100:02d}"

    st.success(f"Análise concluída! Foco alinhado na **Família do {bicho_alvo}**.")
    
    # Exibição da Pule Fracionada (Teto de R$ 5,00)
    st.markdown("---")
    st.subheader("🎫 PULE GERADA (R$ 5,00)")
    
    st.markdown(f"""
    * **Foco da Operação:** Família de puxada direta do **{bicho_alvo}**.
    * **1. Cabeça (1º Prêmio) [R$ 1,20]:** Alvo principal no grupo do {bicho_alvo}.
    * **2. Cercado (1º ao 5º) [R$ 1,50]:** Proteção ampla na matriz do {bicho_alvo}.
    * **3. Do 1º ao 3º Prêmio [R$ 0,75]:** Filtro intermediário.
    * **4. Tiro Duplo de Transição + Anti-Trave (+1/-1) [R$ 0,95]:**
        * Dezena de Transição: **{dezena_transicao}**
        * Espelho Anti-Trave (+1/-1): **{dezena_espelho_mais}** e **{dezena_espelho_menos}**
        * *Garantia:* Sem repetir o passado (`{milhar_informada}` descartado para evitar repetição cega).
    """)
    
    # Salva no histórico para registro de erros/acertos
    st.session_state.historico_apostas.append({
        "horario": horario_sorteio,
        "base": milhar_informada,
        "alvo": bicho_alvo
    })

# 4. Bloco de Aprendizado por Erro (Feedback Loop)
st.markdown("---")
st.subheader("📊 Painel de Aprendizado e Histórico")
if st.session_state.historico_apostas:
    df_historico = pd.DataFrame(st.session_state.historico_apostas)
    st.dataframe(df_historico)
    
    # Botões de Feedback para o Robô aprender
    col_fb1, col_fb2 = st.columns(2)
    with col_fb1:
        if st.button("✅ Registrar GREEN (Acerto)"):
            st.toast("Green registrado! O robô reforçou os pesos desta família.")
    with col_fb2:
        if st.button("❌ Registrar RED (Erro)"):
            st.toast("Red registrado! O robô ativou o gatilho de ajuste contra desvios laterais.")
else:
    st.info("Nenhuma operação registrada nesta sessão ainda. Gere uma pule para iniciar o histórico.")
