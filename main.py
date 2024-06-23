from ocorrencias import SistemaOcorrencias
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ocorrencias_db"]
collection = db["ocorrencias"]

def exibir_menu():
    print("Bem-vindo ao Menu de Opções:")
    print("1. Listar Ocorrências")
    print("2. Adicionar Ocorrência")
    print("3. Exibir Ocorrências por Tipo")
    print("4. Deletar todas as ocorrências")
    print("5. Deletar ocorrência específica")
    print("6. Sair do Programa")

def main():
    sistema = SistemaOcorrencias()  # Cria uma instância do SistemaOcorrencias

    while True:
        exibir_menu()
        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            sistema.exibir_ocorrencias()  # Chama o método para listar ocorrências
        elif escolha == "2":
            nome = input("Digite o nome: ")
            tipo = input("Digite o tipo (crítica, elogio ou sugestão): ")
            descricao = input("Digite a descrição: ")
            sistema.adicionar_ocorrencia(nome, tipo, descricao)  # Chama o método para adicionar ocorrência
        elif escolha == "3":
            tipo = input("Digite o tipo (crítica, elogio ou sugestão): ")
            sistema.exibir_ocorrencias_por_cpf(tipo)  # Chama o método para exibir ocorrências por tipo
        elif escolha == "4":
            collection.delete_many({})  # Deleta todas as ocorrências
            print("Todas as ocorrências foram excluídas.")
        elif escolha == "5":
            nome_ocorrencia = input("Digite o nome da ocorrência a ser excluída: ")
            collection.delete_one({"nome": nome_ocorrencia})
            print(f"Ocorrência '{nome_ocorrencia}' foi excluída.")
        elif escolha == "6":
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()

