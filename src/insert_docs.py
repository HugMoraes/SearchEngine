from src.searchEngine import MyElasticsearch
from SearchEngine.src.insertDocs.pipelineReader import PipelineReader
from src.schema import MAPPING
from src.config import DATABASE_PATH, ELASTIC_SEARCH_ADDRESS, MAIN_INDEX_NAME

def insert_docs():
    reader = PipelineReader(DATABASE_PATH)
    se = MyElasticsearch(hosts=ELASTIC_SEARCH_ADDRESS)

    se.create_index(MAIN_INDEX_NAME, MAPPING)
    all_docs = reader.documents_to_index_format()
    se.bulk_insert_documents(MAIN_INDEX_NAME, all_docs)
