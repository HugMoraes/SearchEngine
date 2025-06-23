import pandas as pd
import time
import numpy as np

class PipelineReader:
    def __init__(self, filepath:str):
        self.filepath = filepath
        self.df = None

        self.load_file()
        
    def load_file(self) -> None:
        """        
        Reads a parquet file and returns a pandas DataFrame.
        Args:
            filepath (str): Path to the parquet file.
        Returns:
            pd.DataFrame: DataFrame containing the data from the parquet file.
        """

        print(f"Reading parquet file from {self.filepath}...")
        start_time = time.time()
        
        try:
            df = pd.read_parquet(self.filepath)

        except Exception as e:
            print(f"Error reading parquet file: {e}")
            return None
    
        else:
            self.df = df
            print(f"DataFrame loaded successfully with {len(df)} rows and {len(df.columns)} columns.")
            print(f"Time taken to read the file: {time.time() - start_time:.2f} seconds")
    
    def _create_document_from_row(self, row):
        """
        Cria um único dicionário de documento a partir de uma linha do DataFrame,
        tratando de forma segura os campos que podem ser nulos ou vazios.

        Args:
            row: Uma linha do DataFrame (pd.Series).

        Returns:
            Um dicionário formatado para indexação.
        """
        # Acesso seguro aos metadados e ao documento principal
        metadata = row.get("metadata", {}) or {}
        document_data = row.get("document", {}) or {}
        author_data = metadata.get("author", {}) or {}
        
        # Tratamento seguro para campos que serão divididos (split)
        related_judges_str = metadata.get("related_judges")
        related_judges_list = related_judges_str.split() if isinstance(related_judges_str, str) else []

        addons_str = metadata.get("addons")
        addons_list = addons_str.splitlines() if isinstance(addons_str, str) else []

        # --- CORREÇÃO APLICADA AQUI ---
        # Em vez de usar 'or []', verificamos explicitamente se o dado é uma lista ou array.
        citations_data = metadata.get("document_citations")
        if isinstance(citations_data, (list, np.ndarray)):
            citations_list = citations_data
        else:
            citations_list = []
        
        doc = {
            "id": row.get("id"),
            "document": {
                "title": document_data.get("title"),
                "body": document_data.get("body"),
                "highlight": document_data.get("highlight"),
                "date": document_data.get("date")
            },
            "metadata": {
                "author": {
                    "name": author_data.get("name"),
                    "username": author_data.get("username")
                },
                "court": metadata.get("court"),
                "jurisprudence_type": metadata.get("jurisprudence_type"),
                "degree": metadata.get("degree"),
                "rapporteur_name": metadata.get("rapporteur_name"),
                "judging_organ": metadata.get("judging_organ"),
                "related_judges": related_judges_list,
                "document_citations": [
                    {
                        "id": cit.get("id"),
                        "kind": cit.get("kind"),
                        "count": cit.get("count")
                    }
                    for cit in citations_list
                ],
                "addons": addons_list
            },
            "phrasal_terms": row.get("phrasal_terms", [])
        }
        return doc

    def documents_to_index_format(self):
        """
        Converte o DataFrame para uma lista de dicionários no formato requerido para indexação.

        Returns:
            Lista de dicionários com o formato requerido.
        """
        if self.df is None:
            print("DataFrame está vazio. Por favor, carregue o arquivo primeiro.")
            return []
        
        documents = []
        for _, row in self.df.iterrows():
            # Chama a função auxiliar para criar cada documento individualmente
            doc = self._create_document_from_row(row)
            documents.append(doc)
        
        return documents





