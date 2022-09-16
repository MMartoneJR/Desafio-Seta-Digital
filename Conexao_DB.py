from datetime import date
import psycopg2
import Funcoes

hostname = 'localhost'
database = 'desafio_seta'
username = 'postgres'
pwd = 'root'
port_id = '5433'
conn = None
cursor = None


try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)
    cursor = conn.cursor()
   
except Exception as error:
    print("Falha ao conectar ao banco de dados")

def Create_Tables():
    create_cliente = '''CREATE TABLE IF NOT EXISTS clientes(
                 id_cliente SERIAL PRIMARY KEY,
                 nome VARCHAR(15) NOT NULL,
                 sobrenome VARCHAR(15) NOT NULL,
                 cpf INT NOT NULL,
                 email VARCHAR(40) NOT NULL,
                 celular INT NOT NULL)'''
    create_emprestimo = '''CREATE TABLE IF NOT EXISTS emprestimos(
                           id_emprestimo SERIAL PRIMARY KEY,
                           id_cliente INT,
                           data_emprestimo DATE,
                           moeda VARCHAR(15) NOT NULL,
                           valor_emprestimo FLOAT(2) NOT NULL,
                           taxa_conversao FLOAT(2) NOT NULL,
                           data_vencimento DATE NOT NULL,
                           CONSTRAINT fk_cliente FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente))'''
    cursor.execute(create_cliente)
    cursor.execute(create_emprestimo)
    conn.commit()

def cadastro_cliente():
    nome = input("Digite o primeiro nome: ").upper()
    sobrenome = input("Digite o sobrenome: ").upper()
    cpf = input("Digite os números do CPF: ")
    email = input("Digite o e-mail: ")
    celular = input("Digite o celular: ")
    insert_cliente = '''INSERT INTO clientes (nome, sobrenome, cpf, email, celular) VALUES
                        (%s, %s, %s, %s, %s)'''
    valores_insert = (nome, sobrenome, cpf, email, celular)
    cursor.execute(insert_cliente, valores_insert)
    conn.commit()

def check_id(id_cliente):
    query = '''SELECT EXISTS (
            SELECT 1 FROM clientes
            WHERE id_cliente = %s)'''
    cursor.execute(query, id_cliente)
    if cursor.fetchone()[0]:
        return True
    else:
        return False

def nome_completo(id_cliente):
    query = '''SELECT 
            nome,
            sobrenome
            FROM
            clientes
            WHERE
            id_cliente = %s'''
    cursor.execute(query, id_cliente)
    return cursor.fetchall()

def cadastro_emprestimo():
    while True:
        id_cliente = input("Digite o ID do cliente que receberá o emprestimo: ")
        if check_id(id_cliente) == True:
            break
        else:
            print("ID não localizado, tente novamente")
    while True:
        moeda = input("Qual a moeda a fazer o emprestimo? ").upper()
        if Funcoes.moedas_bcb(moeda) == True:
            break
    valor_emprestimo = float(input("Digite o valor do emprestimo: "))
    data_vencimento = input("Qual a data do vencimento(AAAA/MM/DD)? ")
    
    valor_total = ((float(valor_emprestimo) * float(Funcoes.cotacao_moedas(moeda))))
    taxa_conversao = float(Funcoes.cotacao_moedas(moeda))
    data_emprestimo = date.today().strftime("%Y-%m-%d")

    print("Resumo da requisição...........:")
    print("Nome do solicitante............: ", nome_completo(id_cliente))
    print("Moeda..........................: ", moeda)
    print(f"Valor do emprestimo em {moeda}.....: ", round(valor_emprestimo,2))
    print("Taxa de conversão..............: R$", round(taxa_conversao,2))
    print("Valor Total em R$..............: ", round(valor_total,2))
    print("Data de vencimento.............: ", data_vencimento)
    opc = int(input("Deseja finalizar a solicitação? \n1 - Sim \n2 - Não \n"))
    match opc:
        case 1:
            insert_emprestimo = '''INSERT INTO emprestimos(id_cliente, data_emprestimo, moeda, valor_emprestimo, taxa_conversao, data_vencimento)
                                    VALUES (%s, %s, %s, %s, %s, %s)'''
            valores_insert = (id_cliente, str(data_emprestimo), moeda, round(valor_emprestimo,2), round(taxa_conversao,2), str(data_vencimento))       
            cursor.execute(insert_emprestimo, valores_insert)                 
            conn.commit()
            print("Cadastro realizado com sucesso!")

def consulta_emprestimos():
    cursor.execute('select * from emprestimos')

    for item in cursor.fetchall():
        meses = (12 * item[2].year + item[2].month) - (12 * item[6].year + item[6].month)
        meses = meses * (-1)

        valor_em_real = (float(item[4])*float(item[5]))
        taxa = 0.1
        juros_composto = valor_em_real*(1+taxa)**2
        print("ID do emprestimo..............: ", item[0])
        print("ID do cliente.................: ", item[1])
        print("Valor do emprestimo(em R$)....: ", valor_em_real)
        print("Data do emprestimo............: ", item[2])
        print("Data do vencimento............: ", item[6])
        print("Total Meses...................: ", meses)
        print("Valor total a ser pago(em R$).: ", juros_composto)
        print("")

def consulta_intervalo_emprestimos():
    data_inicial = input("Digite a data inicial(AAAA/MM/DD): ")
    data_final = input("Digite a data final(AAAA/MM/DD): ")
    
    select_query = '''SELECT * FROM emprestimos WHERE data_emprestimo BETWEEN SYMMETRIC %s AND %s'''
    valores_query = (data_inicial, data_final)
    cursor.execute(select_query, valores_query)

    for item in cursor.fetchall():
        meses = (12 * item[2].year + item[2].month) - (12 * item[6].year + item[6].month)
        meses = meses * (-1)

        valor_em_real = (float(item[4])*float(item[5]))
        taxa = 0.1
        juros_composto = valor_em_real*(1+taxa)**2
        print("ID do emprestimo..............: ", item[0])
        print("ID do cliente.................: ", item[1])
        print("Valor do emprestimo(em R$)....: ", valor_em_real)
        print("Data do emprestimo............: ", item[2])
        print("Data do vencimento............: ", item[6])
        print("Total Meses...................: ", meses)
        print("Valor total a ser pago(em R$).: ", juros_composto)
        print("")

        

def close_sql_conn():
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()

