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

    def delete_index(self, index_name):
        """
        Delete an index in Elasticsearch if it exists.
        """
        try:
            if self.indices.exists(index=index_name):
                self.indices.delete(index=index_name)
                print(f"Index '{index_name}' deleted.")
            else:
                print(f"Index '{index_name}' does not exist.")
        except exceptions.ElasticsearchException as e:
            print(f"Error deleting index: {e}")

    def get_indices(self):
        """
        Return a list of all indices in Elasticsearch.
        """
        try:
            indices = list(self.indices.get_alias("*").keys())
            print("Found indices:", indices)
            return indices
        except exceptions.ElasticsearchException as e:
            print(f"Error trying to get indices: {e}")
            return []


    def insert_document(self, index_name, document):
        """
        Insert a document into the specified index.
        """
        try:
            response = self.index(index=index_name, body=document)
            print(f"Document inserted with ID: {response['_id']}")
        except exceptions.ElasticsearchException as e:
            print(f"Error inserting document: {e}")

    def delete_document(self, index_name, doc_id):
        """
        Delete a document from the specified index by its ID.
        """
        try:
            response = self.delete(index=index_name, id=doc_id)
            print(f"Document with ID '{doc_id}' deleted from '{index_name}'.")
            return response
        except exceptions.ElasticsearchException as e:
            print(f"Error deleting document: {e}")
            return None

    def search_documents(self, index_name, query, size=10):
        """
        Search for documents in the specified index using the given query.
        Returns a list of matching documents.
        """
        try:
            response = self.search(index=index_name, body={"query": query}, size=size)
            documents = [hit["_source"] for hit in response["hits"]["hits"]]
            print(f"Found {len(documents)} documents in '{index_name}'.")
            return documents
        except exceptions.ElasticsearchException as e:
            print(f"Error searching documents: {e}")
            return []

    def count_documents(self, index_name):
        """
        Return the total number of documents indexed in the specified index.
        """
        try:
            response = self.count(index=index_name)
            total = response['count']
            print(f"Total documents in '{index_name}': {total}")
            return total
        except exceptions.ElasticsearchException as e:
            print(f"Error counting documents: {e}")
            return 0

