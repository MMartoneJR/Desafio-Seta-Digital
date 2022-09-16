import Conexao_DB
import Funcoes

Conexao_DB.Create_Tables()

while True:
    Funcoes.main_menu()
    opc = int(input())
    match opc:
        case 1:
            Conexao_DB.cadastro_cliente()
        case 2:
            Conexao_DB.cadastro_emprestimo()
        case 3:
            opc2 = int(input("Consultar: \n1 - Todos os emprestimos\n2 - especificar período\n"))
            match opc2:
                case 1:
                    Conexao_DB.consulta_emprestimos()
                case 2:
                    Conexao_DB.consulta_intervalo_emprestimos()
        case 0:
            print("Encerrando aplicação")
            Conexao_DB.close_sql_conn()
            break
        case _:
            print("Opção inválida")
