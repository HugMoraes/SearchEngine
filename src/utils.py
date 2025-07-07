from src.app.MySearchEngine import MySearchEngine
from src.config import ELASTIC_SEARCH_ADDRESS, MAIN_INDEX_NAME
import sys
from SearchEngine.src.insertDocs.insert_docs import insert_docs

def check_index_elasticSearch():
    """
    Verifica a conexão com o Elasticsearch e a existência do índice principal.
    Se o índice não existir ou estiver vazio, chama a função insere_docs para populá-lo.
    """
    try:
        es = MySearchEngine(hosts=ELASTIC_SEARCH_ADDRESS)
        
        print("Verificando conexão com Elasticsearch...")
        # O método ping() é uma forma leve de verificar se o cluster está disponível.
        if not es.ping():
            raise ConnectionError("Ping para o Elasticsearch falhou. Verifique se o serviço está no ar.")
        print("✅ Conexão com o Elasticsearch bem-sucedida.")
        
        print(f"Verificando se o índice '{MAIN_INDEX_NAME}' existe e tem documentos...")
        # Tentamos contar os documentos. Se o índice não existir, um NotFoundError será levantado.
        total_docs = es.count_documents(MAIN_INDEX_NAME)

        if total_docs < 0:
            print(f"⚠️  O índice '{MAIN_INDEX_NAME}' não foi encontrado.")
            print("Iniciando a criação do índice e inserção de documentos...")
            try:
                # A função insere_docs deve ser responsável por criar o índice (se necessário) e inserir os dados.
                insert_docs()
                print(f"✅ Índice '{MAIN_INDEX_NAME}' criado e populado com sucesso.")
            except Exception as e_insert:
                print(f"❌ ERRO CRÍTICO: Falha ao tentar criar e popular o índice.")
                print(f"Detalhes: {e_insert}")
                sys.exit(1) # Encerra o programa se a inserção de dados falhar.

        elif total_docs > 0:
            print(f"✅ Índice '{MAIN_INDEX_NAME}' encontrado com {total_docs} documentos.")
        else:
            # O índice existe, mas está vazio.
            print(f"⚠️  O índice '{MAIN_INDEX_NAME}' existe, mas está vazio. Iniciando a inserção de documentos...")
            insert_docs()
            print(f"✅ Documentos inseridos no índice '{MAIN_INDEX_NAME}' com sucesso.")

    except ConnectionError as e_conn:
        # Captura erros de conexão de forma mais específica.
        print(f"❌ ERRO CRÍTICO: Não foi possível conectar ao Elasticsearch.")
        print(f"Detalhes: {e_conn}")
        print("--- Servidor Flask NÃO será iniciado. ---")
        sys.exit(1)

    except Exception as e:
        # Captura qualquer outra exceção inesperada durante a inicialização.
        print(f"❌ ERRO CRÍTICO: Não foi possível inicializar o app.")
        print(f"Detalhes: {e}")
        print("--- Servidor Flask NÃO será iniciado. ---")
        sys.exit(1)
