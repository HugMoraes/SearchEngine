from src.searchEngine import MyElasticsearch
from src.config import ELASTIC_SEARCH_ADDRESS, MAIN_INDEX_NAME

es = MyElasticsearch(hosts=ELASTIC_SEARCH_ADDRESS)

class DocumentResult:
    def __init__(self, doc_id: str, relevance: float):
        self.id: str = doc_id
        self.relevance: float = relevance

    def __str__(self) -> str:
        """Retorna uma representação em string do objeto DocumentResult."""
        # << MELHORIA: Formata a relevância para ter 2 casas decimais para melhor leitura.
        return f"ID do Documento: {self.id}, Relevância: {self.relevance:.2f}"

class Query:
    def __init__(self, text: str, documents: list[DocumentResult]):
        self.text: str = text
        self.documents: list[DocumentResult] = documents

    def __str__(self) -> str:
        """Retorna uma representação em string do objeto Query."""
        if not self.documents:
            return f"Query: {self.text}\nDocumentos:\n   (Nenhum resultado encontrado)"
            
        docs_str = '\n   '.join(str(doc) for doc in self.documents)
        return f"Query: {self.text}\nDocumentos:\n   {docs_str}"

def load_queries_from_file(path: str) -> list[Query]:
    """
    Lê um arquivo com consultas e seus documentos relevantes e retorna uma lista de objetos Query.
    """
    queries_dict = {}
    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    current_query_text = None
    current_relevance = None

    for line in lines:
        if line.startswith("Query:"):
            current_query_text = line.removeprefix("Query:").strip()
            # Garante que a mesma query não sobrescreva documentos se aparecer de novo
            if current_query_text not in queries_dict:
                queries_dict[current_query_text] = []
        elif line.startswith("Relevance:"):
            # << MELHORIA: Converte para float para consistência, embora no arquivo possa ser int.
            current_relevance = float(line.removeprefix("Relevance:").strip())
        elif line.startswith("Document ID:"):
            doc_id = line.removeprefix("Document ID:").strip()
            
            # << CORREÇÃO: Adiciona verificação para garantir que a query e a relevância foram definidas
            # antes de adicionar um documento. Isso torna o parser mais robusto.
            if current_query_text and current_relevance is not None:
                queries_dict[current_query_text].append(DocumentResult(doc_id, current_relevance))
                # Reseta a relevância para garantir que ela não seja reutilizada para o próximo ID
                # caso a linha "Relevance:" esteja faltando.
                current_relevance = None
            else:
                print(f"Aviso: Ignorando Document ID '{doc_id}' por falta de Query ou Relevância associada.")
    
    queries = [Query(text, docs) for text, docs in queries_dict.items()]
    return queries

def _to_document_results(search_hits: list[dict]) -> list[DocumentResult]:
    """
    Converte a lista de 'hits' de uma busca do Elasticsearch em uma lista de objetos DocumentResult.
    """
    document_results = []
    if not search_hits:
        return document_results

    for hit in search_hits:
        doc_id = hit.get('_id')
        relevance_score = hit.get('_score', 0.0)

        if doc_id:
            doc_result = DocumentResult(doc_id=doc_id, relevance=relevance_score)
            document_results.append(doc_result)
            
    return document_results


def query_elastic(index_name: str, queries: list[str], size: int = 20) -> list[Query]:
    """
    Executa uma lista de textos de consulta no Elasticsearch e retorna uma lista de objetos Query com os resultados.
    """
    results = []
    for query_text in queries:
        try:
            search_hits = es.search_documents(index_name, query=query_text, size=size)
            
            doc_results = _to_document_results(search_hits)
            
            results.append(Query(text=query_text, documents=doc_results))
        except Exception as e:
            print(f"Erro ao buscar pela query '{query_text}': {e}")
            results.append(Query(text=query_text, documents=[]))

    return results

queries_from_file = load_queries_from_file('data/query_eval')

query_texts_to_run = [query.text for query in queries_from_file]

print(query_texts_to_run)

# queries_from_elastic = query_elastic(MAIN_INDEX_NAME, query_texts_to_run)

# for query in queries_from_elastic:
#     print(query)
#     print("---")