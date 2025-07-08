from src.app.MySearchEngine import MySearchEngine
from src.config import ELASTIC_SEARCH_ADDRESS, MAIN_INDEX_NAME

es = MySearchEngine(hosts=ELASTIC_SEARCH_ADDRESS)

class DocumentResult:
    def __init__(self, doc_id: str, relevance: float):
        self.id: str = doc_id
        self.relevance: float = relevance

    def __str__(self) -> str:
        return f"ID do Documento: {self.id}, Relevância: {self.relevance:.2f}"

def load_queries_from_file(path: str) -> dict[str, DocumentResult]:
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
    
    return queries_dict

