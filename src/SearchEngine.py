from elasticsearch import Elasticsearch, exceptions, helpers
import time

class MyElasticsearch(Elasticsearch):
    """
    Uma subclasse customizada do cliente Elasticsearch para adicionar
    métodos de conveniência e tratamento de erros padronizado.
    """
    def __init__(self, *args, **kwargs):
        """
        Inicializa a conexão com o Elasticsearch com múltiplas tentativas.

        Este construtor tenta estabelecer uma conexão até 100 vezes, com um
        intervalo de 10 segundos entre cada tentativa. Ele aceita os mesmos 
        argumentos que a classe base 'Elasticsearch' (ex: hosts, cloud_id, 
        api_key, etc.) e os repassa, garantindo total compatibilidade com os 
        helpers da biblioteca.

        ATENÇÃO: USE hosts={url do elastic} !!!!!!!
        """
        print("Iniciando processo de conexão com o Elasticsearch...")

        max_tentativas = 100
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

    def create_index(self, index_name, mapping=None):
        """
        Create an index in Elasticsearch if it does not already exist.
        """
        if not self.indices.exists(index=index_name):
            if mapping:
                self.indices.create(index=index_name, mappings=mapping)
            else:
                self.indices.create(index=index_name)
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")

    def delete_index(self, index_name):
        """
        Delete an index in Elasticsearch if it exists.
        """
        try:
            if self.indices.exists(index=index_name):
                self.indices.delete(index=index_name)
                print(f"Index '{index_name}' deleted.")
            else:
                print(f"Index '{index_name}' does not exist.")
        except Exception as e:
            print(f"Error deleting index: {e}")

    def list_indices(self):
        """
        Retorna uma lista de todos os índices no Elasticsearch.
        """
        try:
            indices = list(self.indices.get_alias(index="*").keys())
            
            indices_reais = [idx for idx in indices if not idx.startswith('.')]
            print("Índices encontrados:", indices_reais)
            return indices_reais
        except Exception as e:
            print(f"Erro ao tentar obter os índices: {e}")
            return []


    def insert_document(self, index_name, document):
        """
        Insert a document into the specified index.
        """
        try:
            response = self.index(index=index_name, body=document)
            print(f"Document inserted with ID: {response['_id']}")
        except Exception as e:
            print(f"Error inserting document: {e}")

    def delete_document(self, index_name, doc_id):
        """
        Delete a document from the specified index by its ID.
        """
        try:
            response = self.delete(index=index_name, id=doc_id)
            print(f"Document with ID '{doc_id}' deleted from '{index_name}'.")
            return response
        except Exception as e:
            print(f"Error deleting document: {e}")
            return None

    def search_documents(self, index_name, query, size=10):
        """
        Busca por documentos no índice especificado usando a consulta (query) fornecida.
        Retorna uma lista de documentos correspondentes.

        Args:
            index_name (str): O nome do índice para buscar.
            query (str): O termo ou a string de busca.
            size (int, optional): O número máximo de documentos a serem retornados. Padrão é 10.

        Returns:
            list: Uma lista dos dicionários '_source' dos documentos encontrados.
                  Retorna uma lista vazia se nenhum documento for encontrado ou em caso de erro.
        """
        print(f"\nBuscando por: {query}")
        try:
            request_body = {
                "size": size,
                "query": {
                    "query_string": {
                        "query": query
                    }
                }
            }

            response = self.search(index=index_name, body=request_body)

            documents = [hit["_source"] for hit in response["hits"]["hits"]]
            print(f"Encontrados {len(documents)} documentos em '{index_name}'.")
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
            return total
        except exceptions.NotFoundError:
            return -1
        except Exception as e:
            print(f"Error counting documents: {e}")
            raise Exception

    def bulk_insert_documents(self, index_name: str, docs: list[dict]):
        """
        Insere uma lista de documentos em lote (bulk) no índice especificado.

        Este método é altamente otimizado para inserir um grande volume de
        documentos de uma só vez, sendo muito mais performático do que
        inserir um por um.

        Args:
            index_name (str): O nome do índice onde os documentos serão inseridos.
            docs (list[dict]): Uma lista de dicionários, onde cada dicionário
                               é um documento a ser indexado. É recomendado que
                               cada dicionário tenha uma chave 'id' para usar como
                               o _id do documento no Elasticsearch.

        Returns:
            tuple[int, list]: Uma tupla contendo:
                - O número de documentos inseridos com sucesso.
                - Uma lista de erros, se houver. Cada erro é um dicionário
                  detalhando a falha.
        """
        if not docs:
            print("A lista de documentos está vazia. Nenhuma ação foi tomada.")
            return 0, []

        actions = (
            {
                "_index": index_name,
                "_id": doc.get("id"),  # Usa o 'id' do doc como _id. Se não houver, o ES gera um.
                "_source": doc
            }
            for doc in docs
        )

        print(f"Usando helper com NOVA CONEXÃO. Iniciando a inserção em lote de {len(docs)} documentos no índice '{index_name}'...")
        start_time = time.time()
        
        try:
            success, errors = helpers.bulk(client=self, actions=actions)
            
            duration = time.time() - start_time
            print(f"Inserção em lote finalizada em {duration:.2f} segundos.")
            print(f"Documentos inseridos com sucesso: {success}")

            if errors:
                print(f"Ocorreram {len(errors)} erros durante a inserção:")
                # Imprime os primeiros 5 erros para não poluir o console
                for i, error in enumerate(errors[:5]):
                    print(f"  Erro {i+1}: {error}")
                if len(errors) > 5:
                    print(f"  ... e mais {len(errors) - 5} erros.")

            return success, errors

        except exceptions.ConnectionError as e:
            print(f"Erro de conexão durante a operação em lote: {e}")
            return 0, [str(e)]
        except Exception as e:
            print(f"Ocorreu um erro inesperado durante a operação em lote: {e}")
            return 0, [str(e)]