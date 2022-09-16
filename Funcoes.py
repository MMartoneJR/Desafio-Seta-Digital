import pandas as pd
from datetime import date

def main_menu():
    print("1 - Cadastro de cliente")
    print("2 - Aquisição de emprestimo")
    print("3 - Consultar empréstimos")
    print("0 - Sair")

def moedas_bcb(moeda):
    url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=100&$format=text/csv&$select=simbolo,nomeFormatado"
    df = pd.read_csv(url)

    listagem_moedas_bcb = [df]
    moedas_simbolos = df.simbolo.to_list()
    #moedas_nome = df.nomeFormatado.to_list()
    #moedas_tipo =df.tipoMoeda.to_list()
    if moeda in moedas_simbolos:
        return True
    else:
        print("Valor inválido, selecione um dos símbolos abaixo:")
        for item in listagem_moedas_bcb:
            print(item)

def cotacao_moedas(moeda):
    hoje = date.today().strftime("%m-%d-%Y")
    url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda='{moeda}'&@dataCotacao='09-14-2022'&$top=100&$format=text/csv&$select=cotacaoCompra,dataHoraCotacao"
    df = pd.read_csv(url)
    cotacao = df.cotacaoCompra.to_list()
    #cotacao_atual = cotacao[-1]
    cotacao_atual = float(str(cotacao[-1]).replace(',', '.'))
    return (cotacao_atual)