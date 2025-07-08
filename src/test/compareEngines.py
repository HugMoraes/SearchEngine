import math
from src.test.query import load_queries_from_file, DocumentResult
from src.config import IDEAL_QUERY_PATH
from src.app.QueryConfig import QueryConfig
from src.insertDocs.utils import generate_search_field_combinations
from src.insertDocs.SearchFieldsModels import SearchFieldsConfig
from src.app.MySearchEngine import MySearchEngine
import pandas as pd


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

def compare_engines(idealQueryResults: dict[str, list[DocumentResult]]):
    techniques = generate_search_field_combinations(SearchFieldsConfig)

    results_df = pd.DataFrame(columns=["ai_text", "global_expansion", "techniques", "ndcg", "map"])

    

    num_techniques = len(techniques)
    num_queries = len(idealQueryResults.keys())
    print("Número total de queries:", num_queries)
    total_consultas = 2 * 1 * num_techniques * num_queries
    consultas_feitas = 0

    for ai_text in [True, False]:
        for ai_global_expasion in [False]:
            for techniques_combination in techniques:
                config = QueryConfig(
                    ai_text=ai_text,
                    ai_global_expansion=ai_global_expasion,
                    text_techniques_list=techniques_combination.techniques
                )

                print(f"Comparando com configuração: {config}")
                
                se = MySearchEngine(hosts='http://localhost:9200',config=config)

                currentQueryResults = {}

                for currentQuery in idealQueryResults.keys():
                    consultas_feitas += 1

                    status_text = (
                        f"ai_text: {str(ai_text):<5} | "
                        f"ai_global_expasion: {str(ai_global_expasion):<5} | "
                        f"Techniques: {'_'.join(techniques_combination.techniques):<25} | "
                        f"Consulta: {consultas_feitas}/{total_consultas}"
                    )

                    print(status_text, end='\r', flush=True)

                    
                    results = se.search_documents(
                        index_name="test_index",
                        query=currentQuery,
                        size=len(idealQueryResults[currentQuery])
                    )

                    currentQueryResults[currentQuery] = [DocumentResult(doc['id'], 0) for doc in results]

                ndcg = calculate_NDCG(idealQueryResults, currentQueryResults)
                map_score = calculate_MAP(idealQueryResults, currentQueryResults)

                results_df = pd.concat([results_df, pd.DataFrame([{"ai_text": ai_text, "global_expansion": ai_global_expasion, "techniques": "_".join(techniques_combination.techniques), "ndcg": ndcg, "map": map_score}])], ignore_index=True)

    print("\nComparação concluída.")
    results_df.to_csv('results.csv', index=False)

def get_baseline(idealQueryResults: dict[str, list[DocumentResult]]):


    se = MySearchEngine(hosts='http://localhost:9200')

    currentQueryResults = {}

    for currentQuery in idealQueryResults.keys():
        results = se.search_documents(
            index_name="test_index",
            query=currentQuery,
            size=len(idealQueryResults[currentQuery])
        )

        currentQueryResults[currentQuery] = [DocumentResult(doc['id'], 0) for doc in results]

    ndcg = calculate_NDCG(idealQueryResults, currentQueryResults)
    map_score = calculate_MAP(idealQueryResults, currentQueryResults)

    print(f"Baseline NDCG: {ndcg}, MAP: {map_score}")

def get_ai_global_expansion(idealQueryResults: dict[str, list[DocumentResult]]):

    config = QueryConfig(ai_global_expansion=True, text_techniques_list=['lowercase_text', 'remove_stopwords'])


    se = MySearchEngine(hosts='http://localhost:9200', config=config)

    currentQueryResults = {}

    for currentQuery in idealQueryResults.keys():
        results = se.search_documents(
            index_name="test_index",
            query=currentQuery,
            size=len(idealQueryResults[currentQuery])
        )

        currentQueryResults[currentQuery] = [DocumentResult(doc['id'], 0) for doc in results]

    ndcg = calculate_NDCG(idealQueryResults, currentQueryResults)
    map_score = calculate_MAP(idealQueryResults, currentQueryResults)

    print(f"expansão global NDCG: {ndcg}, MAP: {map_score}")
