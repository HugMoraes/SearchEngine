class DocumentResult:
    def __init__(self, doc_id:str, relevance:int):
        self.id = doc_id
        self.relevance = relevance

class Query:
    def __init__(self, text:str, documents:list[DocumentResult]):
        self.text = text
        self.documents = documents


def load_queries_from_file(path: str) -> list[Query]:
    """
    Reads a file with queries and document results, and returns a list of Query objects.
    If a query with the same text appears multiple times, its documents are merged.
    """
    queries_dict = {}
    with open(path, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    current_query_text = None
    current_relevance = None

    for line in lines:
        if line.startswith("Query:"):
            current_query_text = line[len("Query:"):].strip()
        elif line.startswith("Relevance:"):
            current_relevance = int(line[len("Relevance:"):].strip())
        elif line.startswith("Document ID:"):
            doc_id = line[len("Document ID:"):].strip()
            if current_query_text not in queries_dict:
                queries_dict[current_query_text] = []
            queries_dict[current_query_text].append(DocumentResult(doc_id, current_relevance))
        # Ignore separator lines

    queries = [Query(text, docs) for text, docs in queries_dict.items()]
    return queries

