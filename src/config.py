import os

DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/baseDocumentos')
ELASTIC_SEARCH_ADDRESS = os.getenv('ELASTICSEARCH_HOSTS', 'http://localhost:9200')
MAIN_INDEX_NAME = os.getenv('MAIN_INDEX_NAME', 'main_index')