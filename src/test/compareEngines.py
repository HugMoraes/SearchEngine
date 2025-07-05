from SearchEngine.src.test.query import Query, load_queries_from_file, DocumentResult
from src.config import IDEAL_QUERY_PATH

idealQueryResults = load_queries_from_file(IDEAL_QUERY_PATH)

def calculate_NDCG(idealQueryResults:dict[str, DocumentResult], currentQueryResults:dict[str, DocumentResult]):
    pass

def calculate_MAP(idealQueryResults:dict[str, DocumentResult], currentQueryResults:dict[str, DocumentResult]):
    pass
