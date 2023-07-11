def gerar_trade(quantidade, preço, operação):
    
    return {"quantidade": quantidade, "preço": preço, "operação": operação}

def gerar_div(ativos, preços, operações, datas):

    for i in range(0, len(ativos)):

        data = str(datas[i])
        ticker = str(ativos[i])
        operação = str(operações[i])
        preço = float(preço[i])
        

    return {"data": data, "preço": preço, "operação": operação}

def gerar_fifo(ativo, operações, quantidade, preço):
    
    portifolio = {}
    dividendos = {}

# ============================================== INÍCIO DO FOR QUE PERCORRE CADA TRANSAÇÃO ==============================================

    for i in range(0, len(ativo)):

        # print(f"TRANSAÇÃO {i:03} | {ativo[i]}")

        ticker = str(ativo[i])
        operação = str(operações[i])
        quantidade_ativo = float(quantidade[i])
        preço_ativo = float(preço[i])

        trade = gerar_trade(quantidade_ativo, preço_ativo, operação)

        div = gerar_trade(quantidade_ativo, preço_ativo, operação)

# ============================================== COMPUTANDO TRANSAÇÃO DE COMPRA ==============================================

        if operação.upper() == "COMPRA":

            # print(f"TRANSAÇÃO COMPRA GERADA | {trade}")
            
            trade_ativo = portifolio.get(ticker)

            if trade_ativo == None:
                portifolio[f"{ticker}"] = [trade]
            else:
                trade_ativo.append(trade)

# ============================================== TRANSAÇÃO DE COMPRA COMPUTADA ==============================================

# ============================================== COMPUTANDO TRANSAÇÃO DE DIVIDENDOS ==============================================        

        if operação.upper() == "DIVIDENDO" or operação.upper() == "JSCP" or operação.upper() == "RENDIMENTO":

            div_ativo = dividendos.get(ticker)

            if div_ativo == None:
                dividendos[f"{ticker}"] = [trade]
            else:
                div_ativo.append(trade)

        #     # print(f"TRANSAÇÃO {i} | {trade_ativo}")

# ============================================== TRANSAÇÃO DE DIVIDENDOS COMPUTADA ==============================================

# ============================================== COMPUTANDO TRANSAÇÃO DE VENDA ==============================================

        if operação.upper() == "VENDA":
            
            trade_ativo = portifolio.get(ticker)
            precisão = 2

            # print(f"TRANSAÇÃO VENDA GERADA | {trade}")

            if trade_ativo != None:

                quantidade_venda = round(trade["quantidade"],precisão)

# ============================================== INÍCIO DO WHILE QUE VERIFICA QUANTIDADDE DE VENDA ==============================================

                while quantidade_venda > 0:

                    if len(trade_ativo) > 0:
                        
                        item_venda = trade_ativo[0]
                        item_venda["quantidade"] = round(item_venda["quantidade"], precisão)

                        # print(f"TENHO QUE VENDER {quantidade_venda} DA TRANSAÇÃO {item_venda}")

                        if item_venda["quantidade"] == quantidade_venda:

                            del trade_ativo[0]
                            quantidade_venda = 0

                        elif item_venda["quantidade"] < quantidade_venda:

                            quantidade_venda -= round(item_venda["quantidade"], precisão)
                            quantidade_venda = round(quantidade_venda, precisão)
                            
                            del trade_ativo[0]

                        else:
                            
                            item_venda["quantidade"] -= round(quantidade_venda, precisão)
                            quantidade_venda = 0

                        # print(f"ME RESTARAM {quantidade_venda} PARA VENDER")

# ============================================== FIM DO WHILE QUE VERIFICA QUANTIDADDE DE VENDA ==============================================                             
                
                if len(trade_ativo) == 0:
                    portifolio.pop(ticker)

# ============================================== TRANSAÇÃO DE VENDA COMPUTADA ==============================================



# ============================================== FIM DO FOR QUE PERCORRE CADA TRANSAÇÃO ==============================================

    return portifolio, dividendos

def mypositions (arquivo, data_final = ""):

# ============================================== IMPORTANDO BIBLIOTECAS ==============================================
    
    import pandas as pd

# ============================================== IMPORTANDO BIBLIOTECAS ==============================================

# ============================================== CRIACÃO DAS VARIÁVEIS ==============================================

    # Abrir arquivo excel
    dados = pd.read_excel(arquivo)
    data_final = pd.to_datetime(data_final, dayfirst = True)

    if data_final != "":
        try:
            filtro = (dados["Data"] <= data_final)
            dados = dados[filtro]            
        except:
            print("Digite uma data válida no formato 'dd-mm-yyyy'")
        
    # Criar portifolio através da função fifo
    portifolio, dividendos = gerar_fifo(dados["Ticker"], dados["Operação"], dados["Quantidade"], dados["Preço"])

    # Lista que conterá os trades ativos restantes
    resultado = []
    
# ============================================== CRIACÃO DAS VARIÁVEIS ==============================================

# ============================================== INICIO DO FOR QUE PERCORRE CADA TICKER DO PORTIFOLIO ==============================================

    for chave, valor in portifolio.items():
        quantidade = 0
        custo_total = 0
        custo_médio = 0

        for i in range(0, len(valor)):
            # print(chave, valor[i], len(valor))

            quantidade += valor[i]["quantidade"]
            custo_total += valor[i]["quantidade"] * valor[i]["preço"]
        
        custo_médio = round((custo_total/quantidade), 2)

        if "Tesouro" in chave:
            resultado.append([chave, f"{quantidade:.2f}", custo_médio])
        else:
            resultado.append([chave, f"{quantidade:.0f}", custo_médio])

# ============================================== FIM DO FOR QUE PERCORRE CADA TICKER DO PORTIFOLIO ==============================================

    div = mydividends(dividendos)

    carteira = pd.DataFrame(data = resultado, columns = ["Ticker", "Quantidade", "Preço Médio"]).sort_values(by = "Ticker").reset_index(drop = True)
    meus_dividendos = pd.DataFrame(data = div, columns = ["Ticker", "Rendimento Total", "Último Rendimento"]).sort_values(by = "Ticker").reset_index(drop = True)
    
    
    
    meus_dividendos["DY"] = list(" " * len(dividendos))
    carteira["DY 12M"] = list(" " * len(carteira))


    return carteira, meus_dividendos

def mydividends(arquivo):

    resultado = []

    for chave, valor in arquivo.items():

        rendimento_total = 0
        ultimo_rendimento = valor[-1]["preço"]

        for i in range(0, len(valor)):

            rendimento_total += valor[i]["quantidade"] * valor[i]["preço"]


        resultado.append([chave, rendimento_total, ultimo_rendimento])

    return resultado