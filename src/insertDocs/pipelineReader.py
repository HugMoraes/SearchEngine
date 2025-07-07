import pandas as pd
import time
import numpy as np
from src.config import DATABASE_PATH
from src.insertDocs.SearchFieldsModels import SearchField, TEXT_FUNCTIONS, SearchFieldsConfig
from src.insertDocs.utils import generate_search_field_combinations
from src.textTools import Tools

class PipelineReader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.df = None
        self.load_file()
    
    def load_file(self) -> None:
        print(f"Lendo arquivo parquet {self.filepath}...")
        start_time = time.time()
        
        try:
            df = pd.read_parquet(self.filepath)
        except FileNotFoundError:
            print(f"Error: The file was not found at {self.filepath}")
            return
        except Exception as e:
            print(f"Error reading parquet file: {e}")
            return
    
        self.df = df
        print(f"DataFrame carregado com sucesso com {len(df)} linhas e {len(df.columns)} colunas.")
        print(f"Tempo gasto para ler o arquivo: {time.time() - start_time:.2f} segundos")
    
    def _create_document_from_row(self, row: dict):
        """Cria um único dicionário de documento a partir de uma linha (em formato de dict)."""

        metadata = row.get("metadata", {}) or {}
        document_data = row.get("document", {}) or {}
        author_data = metadata.get("author", {}) or {}
        related_judges_str = metadata.get("related_judges")
        related_judges_list = related_judges_str.split() if isinstance(related_judges_str, str) else []
        addons_str = metadata.get("addons")
        addons_list = addons_str.splitlines() if isinstance(addons_str, str) else []
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
                        "id": cit.get("id", {}).get("id"),
                        "kind": cit.get("id", {}).get("kind"),
                        "count": cit.get("count")
                    }
                    for cit in citations_list
                ],
                "addons": addons_list
            },
            "phrasal_terms": row.get("phrasal_terms", [])
        }
        return doc

    def _insert_search_fields(self, doc:dict, searchFields:list[SearchField]):

        search_fields = {}

        try:

            for field in searchFields:
                
                field_text = doc["document"][field.from_field]
                if field_text == None or field_text == "":
                    search_fields[field.from_field + "_" + "_".join(field.techniques)] = ""
                    continue

                for technique_name in field.techniques:
                    field_text = TEXT_FUNCTIONS[technique_name](field_text)

                search_fields[field.from_field + "_" + "_".join(field.techniques)] = field_text

        except Exception as e:
            print("Error transformando texto")
            print(f"texto do campo: {field_text}")
            print("Documento:\n")
            print(doc)
            print()
            print(e)
            exit()


        doc["search_fields"] = search_fields

        return doc

    def _insert_ai_text_search_field(self, doc):

        if doc["document"]["highlight"] is None or doc["document"]["highlight"] == "":
            doc["search_fields"]["ai_text"] = ""
        else:
            doc["search_fields"]["ai_text"] = Tools.ai_text(doc["document"]["highlight"])

        return doc

    def documents_to_index_format(self):
        """Converte o DataFrame para uma lista de dicionários no formato para indexação.
        """
        if self.df is None:
            print("DataFrame está vazio. Por favor, carregue o arquivo primeiro.")
            return []
        
        documents = []

        total_docs = len(self.df.index)
        
        for i, row in enumerate(self.df.to_dict('records')):

            print(f"Processando documento: {i + 1}/{total_docs}", end="\r")

            doc = self._create_document_from_row(row)
            doc = self._insert_search_fields(doc, generate_search_field_combinations(SearchFieldsConfig))
            doc = self._insert_ai_text_search_field(doc)

            documents.append(doc)

        print() 
        print("Processamento concluído!")
        
        return documents

# doc = {
#     "id": 123,
#     "document": {
#         "title": "TITUlo1",
#         "body": "corpo do documento",
#         "highlight": "resumo",
#         "date": "data"
#     },
#     "metadata": {
#         "author": {
#             "name": "nome autor",
#             "username": "nickname autor"
#         },
#         "court": "corte",
#         "jurisprudence_type": "tipo de jurisprudencia",
#         "degree": "grau",
#         "rapporteur_name": "nome do rapporteur",
#         "judging_organ": "orgão juridico",
#         "related_judges": "lista de juizes relacionados",
#         "document_citations": [
#             {
#                 "id": "2",
#                 "kind": "tipo de documento citadpl",
#                 "count": "contagem"
#             }
#         ],
#         "addons": "lista de addons"
#     },
#     "phrasal_terms": "termos frasais"
# }


# pr = PipelineReader(DATABASE_PATH)

# print(pr._insert_search_fields(doc, generate_search_field_combinations(SearchFieldsConfig)))