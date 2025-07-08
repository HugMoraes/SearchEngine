from src.insertDocs.searchEngine import MyElasticsearch
from src.insertDocs.pipelineReader import PipelineReader
from src.config import DATABASE_PATH, ELASTIC_SEARCH_ADDRESS, MAIN_INDEX_NAME
from src.insertDocs.SearchFieldsModels import SearchFieldsConfig
from src.insertDocs.utils import generate_search_field_combinations

def insert_docs_without_processing():
    reader = PipelineReader(DATABASE_PATH)
    se = MyElasticsearch(hosts=ELASTIC_SEARCH_ADDRESS)

    se.create_index(MAIN_INDEX_NAME)
    all_docs = reader.documents_to_index_format()
    se.bulk_insert_documents(MAIN_INDEX_NAME, all_docs)

def insert_docs_one_by_one():
    reader = PipelineReader(DATABASE_PATH)
    se = MyElasticsearch(hosts=ELASTIC_SEARCH_ADDRESS)

    index_name = "test_index"

    se.create_index(index_name)

    total_docs = len(reader.df.index)
        
    for i, row in enumerate(reader.df.to_dict('records')):

        print(f"Processando documento: {i + 1}/{total_docs}", end="\r")

        doc_id = row.get("id")

        query = {
            "query": {
                "term": {
                    "_id": doc_id # Em muitos sistemas (como Elasticsearch), o campo de ID padrão é '_id'
                }
            },
            "size": 1 # Só precisamos saber se existe, então 1 resultado é suficiente
        }
        
        # Executa a busca
        search_result = se.search(index=index_name, body=query)

        if search_result['hits']['total']['value'] > 0:
            # Pula para a próxima iteração do loop
            continue


        doc = reader._create_document_from_row(row)
        doc = reader._insert_search_fields(doc, generate_search_field_combinations(SearchFieldsConfig))
        doc = reader._insert_ai_text_search_field(doc)

        se.insert_document(index_name, doc)

insert_docs_one_by_one()