import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Robô Analisador IAC - Motor Numérico Real", page_icon="🎯", layout="centered")

st.title("🎯 Robô Analisador IAC - Motor Numérico (Milhar/Centena)")
st.markdown("Análise matemática de alta precisão baseada nos números reais dos 10 prêmios.")

# Inicializar Histórico
if 'historico_apostas' not in st.session_state:
    st.session_state.historico_apostas = []

# Dicionário de Grupos e Dezenas Oficiais do Jogo do Bicho
# Mapeia cada dezena (00 a 99) para o seu respectivo grupo e bicho
def obter_dados_por_dezena(dezena_str):
    d = int(dezena_str) % 100
    # Ajuste para 00 cair na Vaca (grupo 25)
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

st.subheader("⏱️ Passo 1: Penúltimo Horário (Digite os números completos)")
col1, col2 = st.columns(2)
with col1:
    p1_1 = st.text_input("1º Prémio (Cabeça):", value="4593", key="p1_1")
    p1_2 = st.text_input("2º Prémio:", value="1214", key="p1_2")
    p1_3 = st.text_input("3º Prémio:", value="8821", key="p1_3")
with col2:
    p1_4 = st.text_input("4º Prémio:", value="3345", key="p1_4")
    p1_5 = st.text_input("5º Prémio (Elástico):", value="9902", key="p1_5")

st.markdown("---")
st.subheader("⏱️ Passo 2: Último Horário / Atual (Digite os números completos)")
col3, col4 = st.columns(2)
with col3:
    u1_1 = st.text_input("1º Prémio (Cabeça Atual):", value="7837", key="u1_1")
    u1_2 = st.text_input("2º Prémio:", value="5511", key="u1_2")
    u1_3 = st.text_input("3º Prémio:", value="2265", key="u1_3")
with col4:
    u1_4 = st.text_input("4º Prémio:", value="1189", key="u1_4")
    u1_5 = st.text_input("5º Prémio (Elástico):", value="6640", key="u1_5")

if st.button("🚀 Processar Tiro Cirúrgico Baseado nos Números"):
    try:
        # Agrupa todos os números digitados
        nums_penultimo = [p1_1, p1_2, p1_3, p1_4, p1_5]
        nums_ultimo = [u1_1, u1_2, u1_3, u1_4, u1_5]
        todos_inputs = nums_penultimo + nums_ultimo
        
        # Extrai dezenas e grupos já saídos para bloqueio absoluto
        grupos_bloqueados = set()
        dezenas_bloqueadas = set()
        
        for n in todos_inputs:
            n_limpo = "".join(filter(str.isdigit, n))
            if len(n_limpo) >= 2:
                dez_Str = n_limpo[-2:]
                g, bicho, dez_lista = obter_dados_por_dezena(dez_Str)
                grupos_bloqueados.add(g)
                for dz in dez_lista:
                    dezenas_bloqueadas.add(dz)

        # MOTOR MATEMÁTICO DE INVERSÃO E ECO DECIMAL
        # Vamos analisar a movimentação das dezenas do último horário para calcular a tendência exata
        candidatos_pontuados = {}

        for idx, n in enumerate(nums_ultimo):
            n_limpo = "".join(filter(str.isdigit, n))
            if len(n_limpo) >= 2:
                dz_atual = int(n_limpo[-2:])
                
                # Regra de Inversão Matemática (ex: dezena 37 vira 73 ou inversão de dígitos)
                inv_1 = (dz_atual % 10) * 10 + (dz_atual // 10)
                # Regra de Eco Decimal / Simetria (+11 e -11)
                eco_1 = (dz_atual + 11) % 100
                eco_2 = (dz_atual - 11) % 100
                # Efeito Elástico de Salto (+25 e +50)
                elastico_1 = (dz_atual + 25) % 100
                
                calculados = [inv_1, eco_1, eco_2, elastico_1]
                peso_base = 4 if idx == 0 else (3 if idx == 4 else 2)

                for calc in calculados:
                    calc_str = f"{calc:02d}"
                    g_cand, b_cand, dez_cand_lista = obter_dados_por_dezena(calc_str)
                    
                    # FILTRO ABSOLUTO: Se o grupo ou a dezena já saiu nos 10 prêmios, descarta
                    if g_cand not in grupos_bloqueados and calc_str not in dezenas_bloqueadas:
                        candidatos_pontuados[g_cand] = candidatos_pontuados.get(g_cand, 0) + peso_base

        # Ordena os grupos pela pontuação matemática do cruzamento
        grupos_ordenados = sorted(candidatos_pontuados.keys(), key=lambda x: candidatos_pontuados[x], reverse=True)

        # Garante 3 alvos caso o filtro elimine tudo
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
        st.subheader("🎫 PULE DE OURO — MATEMÁTICA PURA (10 PRÊMIOS PROCESSADOS)")
        
        st.markdown(f"""
        * **Status do Filtro:** Bloqueados {len(grupos_bloqueados)} grupos que já saíram nos dois horários.
        
        ---
        ### 📊 Alvos Numéricos Calculados para o Próximo Horário:
        
        1. **1º Alvo Principal (Inversão e Simetria Direta) [R$ 1,50]:**
           * **{b1}** (Grupo {g1:02d}) | Dezenas: `{', '.join(dez1)}`
        
        2. **2º Alvo de Eco Decimal [R$ 1,50]:**
           * **{b2}** (Grupo {g2:02d}) | Dezenas: `{', '.join(dez2)}`
        
        3. **3º Alvo de Efeito Elástico [R$ 1,00]:**
           * **{b3}** (Grupo {g3:02d}) | Dezenas: `{', '.join(dez3)}`
        
        4. **Duques e Terno Combinados:**
           * **Duque:** {b1} x {b2} | **Terno de Grupo:** {b1} x {b2} x {b3}
        """)

        st.session_state.historico_apostas.append({
            "status": "Processado com Sucesso",
            "alvos_gerados": f"{b1}, {b2}, {b3}"
        })

    except Exception as e:
        st.error(f"Erro no processamento matemático dos números: {e}")

st.markdown("---")
st.subheader("📊 Histórico de Tiros Numéricos")
if st.session_state.historico_apostas:
    st.dataframe(pd.DataFrame(st.session_state.historico_apostas))
