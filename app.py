import streamlit as st

def calcular_metodo_bahia_corrigido(resultados_10h, resultados_12h):
    historico_proibido = set(resultados_10h + resultados_12h)
    
    cabeca_12h = resultados_12h[0]           # Ex: '9459'
    dezena_cabeca_12h = cabeca_12h[2:]      # Ex: '59'
    
    elastico_12h = resultados_12h[4]         # 5º prêmio das 12h
    
    # Rotação baseada no espelho/inversão e ciclo de soma decimal
    dezena_invertida = int(dezena_cabeca_12h[::-1])
    soma_digitos = (int(dezena_cabeca_12h[0]) + int(dezena_cabeca_12h[1])) * 5 % 100
    
    bicho_1_dezena = dezena_invertida                # O espelho exato (ex: 59 vira 95)
    bicho_2_dezena = int(elastico_12h[2:])           # O elástico do 5º prêmio
    bicho_3_dezena = soma_digitos                    # O resultado do ciclo de soma
    
    dezenas_alvo = [bicho_1_dezena, bicho_2_dezena, bicho_3_dezena]
    palpites_finais = []
    
    prefixo_base = int(cabeca_12h[0]) 
    
    for dez in dezenas_alvo:
        dez_str = f"{dez:02d}"
        milhar_principal = f"{prefixo_base}{elastico_12h[1]}{dez_str}"
        milhar_alternativa = f"{elastico_12h[0]}{prefixo_base}{dez_str}"
        
        status = "CERCA / FUNDO" if milhar_principal in historico_proibido else "LINHA DE CABEÇA"
        
        palpites_finais.append({
            "Dezena": dez_str,
            "Milhar Sugerida": milhar_principal,
            "Alternativa": milhar_alternativa,
            "Posição Estratégica": status
        })
        
    return palpites_finais

# --- INTERFACE GRÁFICA DO STREAMLIT ---
st.title("🎯 Robô Analisador - Método Bahia (Corrigido)")
st.write("Insira os resultados dos sorteios para gerar os palpites com a nova lógica de rotação e espelho.")

st.subheader("Resultados das 10h (10 prêmios)")
res_10h_input = st.text_area(
    "Digite os 10 números das 10h (separados por vírgula):",
    "0404, 0849, 9205, 2618, 6701, 4642, 9645, 3869, 3738, 4358",
    key="input_10h"
)

st.subheader("Resultados das 12h (10 prêmios)")
res_12h_input = st.text_area(
    "Digite os 10 números das 12h (separados por vírgula):",
    "9459, 6410, 6888, 4923, 0799, 8774, 1846, 6476, 5891, 3382",
    key="input_12h"
)

if st.button("Gerar Palpites Corrigidos"):
    r10 = [x.strip() for x in res_10h_input.replace("\n", ",").split(",") if x.strip()]
    r12 = [x.strip() for x in res_12h_input.replace("\n", ",").split(",") if x.strip()]
    
    if len(r10) >= 5 and len(r12) >= 5:
        saida_robo = calcular_metodo_bahia_corrigido(r10, r12)
        
        st.success("Análise recalculada com sucesso!")
        for i, p in enumerate(saida_robo, 1):
            st.markdown(f"**Palpite {i}**")
            st.write(f"• **Dezena:** {p['Dezena']}")
            st.write(f"• **Milhar Sugerida:** {p['Milhar Sugerida']}")
            st.write(f"• **Alternativa:** {p['Alternativa']}")
            st.write(f"• **Status:** {p['Posição Estratégica']}")
            st.markdown("---")
    else:
        st.error("Por favor, insira pelo menos 5 resultados válidos para cada horário.")
