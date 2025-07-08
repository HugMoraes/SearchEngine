import os

DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/baseDocumentos')
IDEAL_QUERY_PATH = os.getenv('IDEAL_QUERY_PATH', 'data/query_eval')
ELASTIC_SEARCH_ADDRESS = os.getenv('ELASTICSEARCH_HOSTS', 'http://localhost:9200')
MAIN_INDEX_NAME = os.getenv('MAIN_INDEX_NAME', 'test_index')