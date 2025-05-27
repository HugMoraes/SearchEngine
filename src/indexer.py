# This file will read the parquet file and index the documents into Elasticsearch.
import pandas as pd
from elasticSearch import MyElasticsearch
from config import Config
def index_documents():
    # Read the parquet file
    df = pd.read_parquet('data/baseDocumentos')

    # Initialize Elasticsearch client
    es = MyElasticsearch(address=Config.address)

    # Create index if it does not exist
    es.create_index(Config.index_name)

    # Iterate over DataFrame rows and index documents
    for index, row in df.iterrows():
        document = {
            'metadata': row['metadata'],
            'document': row['document']
        }
        es.insert_document(Config.index_name, document)

        if index % 100 == 0:  # Print status every 100 documents
            print(f"Indexed {index + 1} documents...")

    print("Indexing completed.")