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
        print(f"Reading parquet file from {self.filepath}...")
        start_time = time.time()
        
        try:
            df = pd.read_parquet(self.filepath)
        except FileNotFoundError:
            print(f"Error: The file was not found at {self.filepath}")
            return
        except Exception as e:
            # Captura outras exceções de leitura
            print(f"Error reading parquet file: {e}")
            return
    
        self.df = df
        print(f"DataFrame loaded successfully with {len(df)} rows and {len(df.columns)} columns.")
        print(f"Time taken to read the file: {time.time() - start_time:.2f} seconds")
    
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

    def documents_to_index_format(self, transformations=None):
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
            
            if transformations:
                doc = self._apply_transformations(doc, transformations)
                
            documents.append(doc)
        
        # 4. (Opcional, mas recomendado) Imprima uma linha em branco no final 
        #    para que o próximo output do terminal não sobrescreva sua linha de progresso.
        print() 
        print("Processamento concluído!")
        
        return documents

    def _get_nested_value(self, dictionary, keys):
        """Acessa um valor aninhado em um dicionário usando uma lista de chaves."""
        try:
            return reduce(operator.getitem, keys, dictionary)
        except (KeyError, TypeError):
            return None

    def _set_nested_value(self, dictionary, keys, value):
        """
        Define um valor em um campo aninhado APENAS SE O CAMINHO COMPLETO JÁ EXISTIR.
        Não cria novas chaves para evitar inconsistências com o schema.
        """
        # Copia a referência do dicionário para uma variável temporária
        d = dictionary
        
        # 1. Navega até o dicionário que contém o campo final
        for key in keys[:-1]:
            d = d.get(key)
            
            # Se em qualquer ponto o caminho não for encontrado ou o valor não for
            # um dicionário, a função é interrompida para evitar erros.
            if not isinstance(d, dict):
                #Opcional: Adicionar um log para alertar sobre caminhos inválidos.
                print(f"Aviso: O caminho '{".".join(keys)}' é inválido e não será atualizado.")
                return

        # 2. No dicionário final, verifica se a chave-alvo existe.
        #    Só então o valor é atualizado.
        if keys[-1] in d:
            d[keys[-1]] = value
        else:
            # Opcional: Alerta se o campo final não existe no dicionário pai.
            print(f"Aviso: O campo final '{keys[-1]}' não existe e não será criado.")

    def _apply_transformations(self, doc, transformations):
        """Aplica as transformações especificadas a um documento."""
        if not transformations:
            return doc

        for field_path, funcs in transformations.items():
            keys = field_path.split('.')
            original_value = self._get_nested_value(doc, keys)

            if not isinstance(original_value, str):
                continue

            if not isinstance(funcs, list):
                funcs = [funcs]
            
            transformed_value = original_value
            for func in funcs:
                transformed_value = func(transformed_value)
            
            self._set_nested_value(doc, keys, transformed_value)
            
        return doc