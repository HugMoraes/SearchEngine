from src.searchEngine import MyElasticsearch
from src.pipelineReader import PipelineReader
from src.schema import MAPPING

DATABASE_PATH = 'data/baseDocumentos'
ELASTIC_SEARCH_ADDRESS = 'http://localhost:9200'

reader = PipelineReader(DATABASE_PATH)

se = MyElasticsearch(ELASTIC_SEARCH_ADDRESS)

se.create_index('test', MAPPING)
se.list_indices()

row = reader.df.iloc[0]
doc = reader._create_document_from_row(row)
print(doc)
se.insert_document('test', doc)
se.count_documents('test')


# se.delete_index('test')
# se.list_indices()
