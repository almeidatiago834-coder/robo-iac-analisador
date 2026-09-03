def calcular_metodo_bahia(resultados_10h, resultados_12h):
    """
    resultados_10h e resultados_12h devem ser listas com os números sorteados (ex: ['0404', '0849', ...])
    """
    
    # 1. BLOCO DE CORTE ABSOLUTO (Tudo o que já saiu não vai na cabeça principal)
    historico_proibido = set(resultados_10h + resultados_12h)
    
    # Extração de referências-chave
    cabeca_12h = resultados_12h[0]       # Ex: '9459'
    dezena_cabeca_12h = int(cabeca_12h[2:]) # Ex: 59
    
    elastico_10h = resultados_10h[4]     # 5º prêmio das 10h
    elastico_12h = resultados_12h[4]     # 5º prêmio das 12h
    
    # 2. SELEÇÃO DOS 3 BICHOS (O Triângulo Base)
    # Bicho 1: Derivado da inversão/eco da cabeça das 12h
    bicho_1_dezena = (dezena_cabeca_12h * 3) % 100 # Fator de rotação decimal testado
    
    # Bicho 2: O Elástico do 5º prêmio (âncora magnética)
    bicho_2_dezena = int(elastico_12h[2:])
    
    # Bicho 3: O Retorno de Fundo (A cabeça das 10h que desce)
    bicho_3_dezena = int(resultados_10h[0][2:])
    
    dezenas_alvo = [bicho_1_dezena, bicho_2_dezena, bicho_3_dezena]
    
    palpites_finais = []
    
    # 3. LAPIDAÇÃO DE MILHAR E CENTENA (Física do Elástico)
    prefixo_base = int(cabeca_12h[0]) # Dígito inicial da cabeça das 12h
    
    for dez in dezenas_alvo:
        # Garante o formato de dezena com 2 dígitos (ex: '07', '22')
        dez_str = f"{dez:02d}"
        
        # Monta as milhar/centena cruzando o prefixo base e variações do elástico
        milhar_principal = f"{prefixo_base}{elastico_12h[1]}{dez_str}"
        milhar_alternativa = f"{elastico_12h[0]}{prefixo_base}{dez_str}"
        
        # Validação de Blindagem (Se já saiu exato nos blocos anteriores, vira apenas opção de fundo/cercado)
        status = "CERCA / FUNDO" if milhar_principal in historico_proibido else "LINHA DE CABEÇA"
        
        palpites_finais.append({
            "Dezena": dez_str,
            "Milhar Sugerida": milhar_principal,
            "Alternativa": milhar_alternativa,
            "Posição Estratégica": status
        })
        
    return palpites_finais

# Exemplo de teste com o bloco do dia 31/08 que analisamos:
res_10h = ['0404', '0849', '9205', '2618', '6701', '4642', '9645', '3869', '3738', '4358']
res_12h = ['9459', '6410', '6888', '4923', '0799', '8774', '1846', '6476', '5891', '3382']

saida_robo = calcular_metodo_bahia(res_10h, res_12h)
for p in saida_robo:
    print(p)
