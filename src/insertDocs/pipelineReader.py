import pandas as pd
import time
import numpy as np
from functools import reduce
import operator

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

    def _insert_search_fields(self):
        pass

    def documents_to_index_format(self):
        """Converte o DataFrame para uma lista de dicionários no formato para indexação.

        Este método itera sobre cada linha do DataFrame, converte-a para um dicionário
        estruturado e, opcionalmente, aplica uma série de funções de processamento de
        texto a campos específicos do dicionário gerado.

        Args:
            transformations (dict, optional): Um dicionário para especificar as
                transformações de texto a serem aplicadas. Se None, nenhuma
                transformação é realizada.

                A estrutura do dicionário deve ser:
                - Chave (str): O caminho para o campo a ser transformado, usando '.'
                como separador (ex: 'document.body').
                - Valor (callable ou list[callable]): A função ou lista de funções
                a serem aplicadas ao campo. Se for uma lista, as funções são
                aplicadas em sequência (pipeline).

        Returns:
            list[dict]: Uma lista de dicionários, onde cada dicionário representa
                        um documento pronto para indexação, com as transformações
                        devidamente aplicadas.

        Examples:
            # 1. Uso básico, sem aplicar nenhuma transformação:
            documentos = reader.documents_to_index_format()

            # 2. Aplicando uma única transformação (lowercase) ao título:
            transform_simples = {
                'document.title': tool.lowercase_text
            }
            documentos_lower = reader.documents_to_index_format(
                transformations=transform_simples
            )

            # 3. Aplicando transformações diferentes a campos diferentes:
            transform_multi = {
                'document.title': tool.lowercase_text,
                'document.highlight': tool.remove_special_characters
            }
            documentos_multi = reader.documents_to_index_format(
                transformations=transform_multi
            )

            # 4. Aplicando um pipeline de transformações ao corpo do documento.
            #    As funções são aplicadas na ordem da lista:
            #    1º -> remove_special_characters
            #    2º -> lowercase_text
            #    3º -> remove_stopwords
            pipeline_completo = {
                'document.body': [
                    tool.remove_special_characters,
                    tool.lowercase_text,
                    tool.remove_stopwords
                ]
            }
            documentos_processados = reader.documents_to_index_format(
                transformations=pipeline_completo
            )
        """
        if self.df is None:
            print("DataFrame está vazio. Por favor, carregue o arquivo primeiro.")
            return []
        
        documents = []

        total_docs = len(self.df.index)
        
        for i, row in enumerate(self.df.to_dict('records')):

            print(f"Processando documento: {i + 1}/{total_docs}", end="\r")

            doc = self._create_document_from_row(row)
            doc = self._insert_search_fields(doc)
                
            documents.append(doc)

        print() 
        print("Processamento concluído!")
        
        return documents

