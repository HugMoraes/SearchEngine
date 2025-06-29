from src.searchEngine import MyElasticsearch
from src.pipelineReader import PipelineReader
from src.schema import MAPPING

DATABASE_PATH = 'data/baseDocumentos'
ELASTIC_SEARCH_ADDRESS = 'http://localhost:9200'

reader = PipelineReader(DATABASE_PATH)

se = MyElasticsearch(hosts=ELASTIC_SEARCH_ADDRESS)

se.create_index('test', MAPPING)
se.list_indices()

all_docs = reader.documents_to_index_format()
se.bulk_insert_documents('test', all_docs)

se.count_documents('test')


# se.delete_index('test')
# se.list_indices()
