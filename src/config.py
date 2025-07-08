import os
from src.app.QueryConfig import QueryConfig

DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/baseDocumentos')
IDEAL_QUERY_PATH = os.getenv('IDEAL_QUERY_PATH', 'data/query_eval')
ELASTIC_SEARCH_ADDRESS = os.getenv('ELASTICSEARCH_HOSTS', 'http://localhost:9200')
MAIN_INDEX_NAME = os.getenv('MAIN_INDEX_NAME', 'test_index')

BEST_QUERY_CONFIG = QueryConfig(text_techniques_list=['lowercase_text', 'remove_stopwords'])