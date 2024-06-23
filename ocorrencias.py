from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ocorrencias_db"]
collection = db["ocorrencias"]

class Ocorrencia:
    def __init__(self, nome, tipo, descricao):
        self.nome = nome
        self.tipo = tipo
        self.descricao = descricao

    def __str__(self):
        return f"Nome: {self.nome}\nTipo: {self.tipo.capitalize()}\nDescrição: {self.descricao}\n"

class SistemaOcorrencias:
    def __init__(self):
        # self.ocorrencias = []
        pass

    def adicionar_ocorrencia(self, nome, tipo, descricao):
        tipo = tipo.lower()
        if tipo in ['crítica', 'elogio', 'sugestão']:
            nova_ocorrencia = Ocorrencia(nome, tipo, descricao)
            collection.insert_one({
                "nome": nova_ocorrencia.nome,
                "tipo": nova_ocorrencia.tipo,
                "descricao": nova_ocorrencia.descricao
            })
            print("Ocorrência adicionada com sucesso.")
        else:
            print("Tipo de ocorrência inválido. Use 'crítica', 'elogio' ou 'sugestão'.")

    def exibir_ocorrencias(self):
        todas_ocorrencias = collection.find()
        num_ocorrencias = collection.count_documents({})  # Conta o número de documentos

        if num_ocorrencias == 0:
            print("Nenhuma ocorrência registrada.")
        else:
            for ocorrencia in todas_ocorrencias:
                # Crie um objeto Ocorrencia com os dados do documento
                ocorrencia_obj = Ocorrencia(ocorrencia["nome"], ocorrencia["tipo"], ocorrencia["descricao"])
                print(ocorrencia_obj)

    def exibir_ocorrencias_por_cpf(self, cpf):
        # Busca todas as ocorrências associadas ao CPF
        ocorrencias_usuario = collection.find({"cpf": cpf})

        if ocorrencias_usuario.count() == 0:
            print(f"Nenhuma ocorrência registrada para o CPF '{cpf}'.")
        else:
            for ocorrencia in ocorrencias_usuario:
                # Crie um objeto Ocorrencia com os dados do documento
                ocorrencia_obj = Ocorrencia(ocorrencia["nome"], ocorrencia["tipo"], ocorrencia["descricao"])
                print(ocorrencia_obj)
