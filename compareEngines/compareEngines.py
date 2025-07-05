from compareEngines.query import Query, load_queries_from_file, DocumentResult
from src.config import IDEAL_QUERY_PATH

idealQueryResults = load_queries_from_file(IDEAL_QUERY_PATH)

def calculate_NDCG(idealQueryResults:dict[str, DocumentResult], currentQueryResults:dict[DocumentResult]):
    totalNDCG = 0
    for query in idealQueryResults:
        idealDCG = [doc.relevance for doc in idealQueryResults[query]]
        currentDCG = [doc.relevance for doc in currentQueryResults[query]]

        totalNDCG += currentDCG/idealDCG

    engineNDCG = totalNDCG/len(idealQueryResults)

    return engineNDCG


