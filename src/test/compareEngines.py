import math
from src.test.query import load_queries_from_file, DocumentResult
from src.config import IDEAL_QUERY_PATH


idealQueryResults = load_queries_from_file(IDEAL_QUERY_PATH)

def dcg(results: list) -> float:
    dcg_value = 0.0
    for i, doc in enumerate(results):
        gain = (2 ** doc.relevance - 1)
        discount = math.log2(i + 2)
        dcg_value += gain / discount
    return dcg_value

def calculate_NDCG(idealQueryResults: dict[str, list[DocumentResult]], currentQueryResults: dict[str, list[DocumentResult]]) -> float:
    total_ndcg = 0
    count = 0

    for query in idealQueryResults:
        if query not in currentQueryResults:
            continue

        ideal_docs = idealQueryResults[query]
        retrieved_docs = currentQueryResults[query]

        rel_dict = {doc.id: doc.relevance for doc in ideal_docs}

        scored_docs = []
        for doc in retrieved_docs:
            rel = rel_dict.get(doc.id, 0.0)
            scored_docs.append(DocumentResult(doc.id, rel))

        dcg_val = dcg(scored_docs)
        idcg_val = dcg(sorted(ideal_docs, key=lambda d: d.relevance, reverse=True))

        ndcg = dcg_val / idcg_val if idcg_val > 0 else 0.0
        total_ndcg += ndcg
        count += 1

    return total_ndcg / count if count > 0 else 0.0



def calculate_MAP(idealQueryResults: dict[str, list[DocumentResult]],
                  currentQueryResults: dict[str, list[DocumentResult]]) -> float:
    total_ap = 0
    query_count = 0

    for query, ideal_docs in idealQueryResults.items():
        if query not in currentQueryResults:
            continue

        current_docs = currentQueryResults[query]
        relevant_ids = {doc.id for doc in ideal_docs}
        num_relevant = 0
        sum_precisions = 0

        for idx, doc in enumerate(current_docs):
            if doc.id in relevant_ids:
                num_relevant += 1
                precision_at_k = num_relevant / (idx + 1)
                sum_precisions += precision_at_k

        ap = sum_precisions / len(relevant_ids) if relevant_ids else 0.0
        total_ap += ap
        query_count += 1

    return total_ap / query_count if query_count > 0 else 0.0
