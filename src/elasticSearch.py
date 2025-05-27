from elasticsearch import Elasticsearch, exceptions

class MyElasticsearch (Elasticsearch):
    def __init__(self, address="http://localhost:9200"):
        self.start_connection(address)
        
    def start_connection(self, address):
        """
        Start the connection to Elasticsearch.
        """

        print(f"Starting connection to Elasticsearch ({address})...")
        try:
            super().__init__(address)
        except exceptions.ConnectionError as e:
            print(f"Conection error!\n\nTry to modify config/elasticsearch.yaml file changing xpack.security.enabled to false and restart elastic search\n\n Error:\n {e}")
            exit(1)
        
        client_info = self.info()
        print("Connected to Elasticsearch:", client_info)
        print(client_info.body)

        print("\nConnection established successfully.\n")

    def create_index(self, index_name):
        """
        Create an index in Elasticsearch if it does not already exist.
        """
        if not self.indices.exists(index=index_name):
            self.indices.create(index=index_name)
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")

    def insert_document(self, index_name, document):
        """
        Insert a document into the specified index.
        """
        try:
            response = self.index(index=index_name, body=document)
            print(f"Document inserted with ID: {response['_id']}")
        except exceptions.ElasticsearchException as e:
            print(f"Error inserting document: {e}")

