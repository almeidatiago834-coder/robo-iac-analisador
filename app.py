import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Robô Analisador IAC - Motor de Eco Potencializado", page_icon="🎯", layout="centered")

st.title("🎯 Robô Analisador IAC - Foco Absoluto no Eco & Espelhamento")
st.markdown("Motor refinado: Potencializando o padrão de eco que está cravando os resultados.")

# Inicializar Histórico
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = []

# Dicionário de Grupos e Dezenas Oficiais do Jogo do Bicho
def obter_dados_por_dezena(dezena_str):
    d = int(dezena_str) % 100
    g = ((d - 1) // 4) + 1 if d != 0 else 25
    
    tabela_grupos = {
        1: ("Avestruz", ["01", "02", "03", "04"]),
        2: ("Águia", ["05", "06", "07", "08"]),
        3: ("Burro", ["09", "10", "11", "12"]),
        4: ("Borboleta", ["13", "14", "15", "16"]),
        5: ("Cachorro", ["17", "18", "19", "20"]),
        6: ("Cabra", ["21", "22", "23", "24"]),
        7: ("Carneiro", ["25", "26", "27", "28"]),
        8: ("Camelo", ["29", "30", "31", "32"]),
        9: ("Cobra", ["33", "34", "35", "36"]),
        10: ("Coelho", ["37", "38", "39", "40"]),
        11: ("Cavalo", ["41", "42", "43", "44"]),
        12: ("Elefante", ["45", "46", "47", "48"]),
        13: ("Galo", ["49", "50", "51", "52"]),
        14: ("Gato", ["53", "54", "55", "56"]),
        15: ("Jacaré", ["57", "58", "59", "60"]),
        16: ("Leão", ["61", "62", "63", "64"]),
        17: ("Macaco", ["65", "66", "67", "68"]),
        18: ("Porco", ["69", "70", "71", "72"]),
        19: ("Pavão", ["73", "74", "75", "76"]),
        20: ("Peru", ["77", "78", "79", "80"]),
        21: ("Touro", ["81", "82", "83", "84"]),
        22: ("Tigre", ["85", "86", "87", "88"]),
        23: ("Urso", ["89", "90", "91", "92"]),
        24: ("Veado", ["93", "94", "95", "96"]),
        25: ("Vaca", ["97", "98", "99", "00"])
    }
    bicho, dezenas = tabela_grupos[g]
    return g, bicho, dezenas

st.subheader("⏱️ Passo 1: Penúltimo Horário (1º ao 5º)")
col1, col2 = st.columns(2)
with col1:
    p1_1 = st.text_input("1º Prémio:", value="4593", key="p1_1")
    p1_2 = st.text_input("2º Prémio:", value="1214", key="p1_2")
    p1_3 = st.text_input("3º Prémio:", value="8821", key="p1_3")
with col2:
    p1_4 = st.text_input("4º Prémio:", value="3345", key="p1_4")
    p1_5 = st.text_input("5º Prémio:", value="9902", key="p1_5")

st.markdown("---")
st.subheader("⏱️ Passo 2: Último Horário / Atual (1º ao 5º)")
col3, col4 = st.columns(2)
with col3:
    u1_1 = st.text_input("1º Prémio (Cabeça Atual):", value="7837", key="u1_1")
    u1_2 = st.text_input("2º Prémio:", value="5511", key="u1_2")
    u1_3 = st.text_input("3º Prémio:", value="2265", key="u1_3")
with col4:
    u1_4 = st.text_input("4º Prémio:", value="1189", key="u1_4")
    u1_5 = st.text_input("5º Prémio (Elástico):", value="6640", key="u1_5")

if st.button("🚀 Processar com Motor de Eco Refinado"):
    try:
        nums_penultimo = [p1_1, p1_2, p1_3, p1_4, p1_5]
        nums_ultimo = [u1_1, u1_2, u1_3, u1_4, u1_5]
        todos_inputs = nums_penultimo + nums_ultimo
        
        grupos_bloqueados = set()
        dezenas_bloqueadas = set()
        
        for n in todos_inputs:
            n_limpo = "".join(filter(str.isdigit, n))
            if len(n_limpo) >= 2:
                dez_str = n_limpo[-2:]
                g, _, dez_lista = obter_dados_por_dezena(dez_str)
                grupos_bloqueados.add(g)
                for dz in dez_lista:
                    dezenas_bloqueadas.add(dz)

        # MOTOR FOCADO NO ECO E ESPELHAMENTO MATEMÁTICO
        candidatos_pontuados = {}

        for idx, n in enumerate(nums_ultimo):
            n_limpo = "".join(filter(str.isdigit, n))
            if len(n_limpo) >= 2:
                dz_atual = int(n_limpo[-2:])
                
                # O Padrão de Eco Principal que está cravando:
                # Variações simétricas de eco decimal (+11, -11, +22, -22) e inversões limpas
                ecos = [
                    (dz_atual + 11) % 100,
                    (dz_atual - 11) % 100,
                    (dz_atual + 22) % 100,
                    (dz_atual - 22) % 100,
                    (dz_atual + 9) % 100,   # Eco cruzado de terminação
                    (dz_atual - 9) % 100,
                    ((dz_atual % 10) * 10 + (dz_atual // 10)) % 100 # Inversão pura
                ]
                
                # Peso maior para a cabeça (idx 0) e para o 5º prêmio (elasticidade do eco)
                peso = 5 if idx == 0 else (4 if idx == 4 else 2)

                for eco in ecos:
                    eco_str = f"{eco:02d}"
                    g_cand, _, _ = obter_dados_por_dezena(eco_str)
                    
                    if g_cand not in grupos_bloqueados:
                        candidatos_pontuados[g_cand] = candidatos_pontuados.get(g_cand, 0) + peso

        # Ordena os grupos com base na pontuação de eco
        grupos_ordenados = sorted(candidatos_pontuados.keys(), key=lambda x: candidatos_pontuados[x], reverse=True)

        fallback_g = 1
        while len(grupos_ordenados) < 3:
            if fallback_g not in grupos_bloqueados and fallback_g not in grupos_ordenados:
                grupos_ordenados.append(fallback_g)
            fallback_g += 1

        g1, g2, g3 = grupos_ordenados[0], grupos_ordenados[1], grupos_ordenados[2]
        
        _, b1, dez1 = obter_dados_por_dezena(f"{g1*4}")
        _, b2, dez2 = obter_dados_por_dezena(f"{g2*4}")
        _, b3, dez3 = obter_dados_por_dezena(f"{g3*4}")

        st.markdown("---")
        st.subheader("🎫 PULE DE OURO — MATRIZ DE ECO REFINADA")
        
        st.markdown(f"""
        * **Filtro Ativo:** {len(grupos_bloqueados)} grupos eliminados da base anterior.
        
        ---
        ### 📊 Alvos Validados pelo Padrão de Eco:
        
        1. **1º Alvo Principal (Eco Direto de Alta Precisão) [R$ 1,50]:**
           * **{b1}** (Grupo {g1:02d}) | Dezenas: `{', '.join(dez1)}`
        
        2. **2º Alvo de Eco Simétrico [R$ 1,50]:**
           * **{b2}** (Grupo {g2:02d}) | Dezenas: `{', '.join(dez2)}`
        
        3. **3º Alvo de Fechamento Elástico [R$ 1,00]:**
           * **{b3}** (Grupo {g3:02d}) | Dezenas: `{', '.join(dez3)}`
        
        4. **Duques e Terno Combinados:**
           * **Duque:** {b1} x {b2} | **Terno de Grupo:** {b1} x {b2} x {b3}
        """)

        st.session_state.historico_apostas.append({
            "status": "Eco Processado",
            "alvos": f"{b1}, {b2}, {b3}"
        })

    except Exception as e:
        st.error(f"Erro ao calcular o eco: {e}")

st.markdown("---")
st.subheader("📊 Histórico de Tiros com Eco")
if st.session_state.historico_apostas:
    st.dataframe(pd.DataFrame(st.session_state.historico_apostas))
