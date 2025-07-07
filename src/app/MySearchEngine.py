from elasticsearch import Elasticsearch, exceptions
from src.app.QueryConfig import QueryConfig
from src.insertDocs.SearchFieldsModels import TEXT_FUNCTIONS
from src.textTools import Tools
import time

class MySearchEngine(Elasticsearch):
    """
    Uma subclasse customizada do cliente Elasticsearch para adicionar
    métodos de conveniência e tratamento de erros padronizado.
    """
    def __init__(self, config:QueryConfig=None,*args, **kwargs):
        """
        Inicializa a conexão com o Elasticsearch com múltiplas tentativas.

        Este construtor tenta estabelecer uma conexão até 20 vezes, com um
        intervalo de 10 segundos entre cada tentativa. Ele aceita os mesmos 
        argumentos que a classe base 'Elasticsearch' (ex: hosts, cloud_id, 
        api_key, etc.) e os repassa, garantindo total compatibilidade com os 
        helpers da biblioteca.

        ATENÇÃO: USE hosts={url do elastic} !!!!!!!
        """

        self.config = config

        print("Iniciando processo de conexão com o Elasticsearch...")

        if 'hosts' not in kwargs:
            raise ValueError(
                "O argumento 'hosts' é obrigatório para a inicialização. "
                "Forneça o endereço do Elasticsearch. Exemplo: hosts=['http://localhost:9200'] ou hosts='http://localhost:9200'"
            )

        max_tentativas = 20
        intervalo_segundos = 10

        for tentativa in range(max_tentativas):
            try:
                print(f"\n[Tentativa {tentativa + 1}/{max_tentativas}] Conectando ao Elasticsearch...")
                
                # Tenta inicializar a conexão com a classe pai
                super().__init__(*args, **kwargs)
                
                # Verifica se a conexão está realmente ativa enviando um ping
                self.info()

                # Se chegou até aqui, a conexão foi bem-sucedida
                print("\nConexão estabelecida com sucesso.\n")
                # Sai do laço de tentativas, pois não precisa mais tentar
                break

            except exceptions.ConnectionError as e:
                print(f"Erro de conexão na tentativa {tentativa + 1}: {e}")
            except Exception as e:
                print(f"Ocorreu um erro inesperado na tentativa {tentativa + 1}: {e}")

            # Se a conexão falhou e não é a última tentativa, aguarda antes de tentar novamente
            if tentativa < max_tentativas - 1:
                print(f"Aguardando {intervalo_segundos} segundos para a próxima tentativa...")
                time.sleep(intervalo_segundos)
        
        # O bloco 'else' de um laço 'for' só é executado se o laço terminar
        # naturalmente (ou seja, sem um 'break').
        # Isso significa que todas as 100 tentativas falharam.
        else:
            print(f"\nFalha ao conectar ao Elasticsearch após {max_tentativas} tentativas.")
            print("\nPor favor, verifique se o serviço Elasticsearch está no ar e acessível.")
            print("Tente modificar o arquivo config/elasticsearch.yml mudando xpack.security.enabled para false e reinicie o Elasticsearch.")
            exit(1)

    def search_documents(self, index_name, query, size=20):
        """
        Busca por documentos no índice especificado usando a consulta (query) fornecida.
        Retorna uma lista de documentos correspondentes.

        Args:
            index_name (str): O nome do índice para buscar.
            query (str): O termo ou a string de busca.
            size (int, optional): O número máximo de documentos a serem retornados. Padrão é 20.

        Returns:
            list: Uma lista dos dicionários '_source' dos documentos encontrados.
                  Retorna uma lista vazia se nenhum documento for encontrado ou em caso de erro.
        """
        #print(f"\nBuscando por: {query}")

        for technique in self.config.text_techniques:
            if technique not in TEXT_FUNCTIONS:
                raise ValueError(f"Técnica de texto desconhecida: {technique}. Verifique a configuração.")
            
            query = TEXT_FUNCTIONS[technique](query)
            
        if self.config.ai_global_expansion:
            query += Tools.expand_query(query)

        try:
            request_body = {
                "_source": {
                    "excludes": ["search_fields"]
                },
                "size": size,
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": self.config.fields
                    }
                }
            }

            response = self.search(index=index_name, body=request_body)

            documents = [hit["_source"] for hit in response["hits"]["hits"]]
            #print(f"Encontrados {len(documents)} documentos em '{index_name}'.")
            return documents

        except Exception as e:
            print(f"Erro ao buscar documentos: {e}")
            return []
        

    def count_documents(self, index_name):
        """
        Return the total number of documents indexed in the specified index.
        """
        try:
            response = self.count(index=index_name)
            total = response['count']
            #print(f"Total documents in '{index_name}': {total}")
            return total
        except exceptions.NotFoundError:
            return -1
        except Exception as e:
            print(f"Error counting documents: {e}")
            raise Exception
        