# Search Engine
O arquivo baseDocumentos é do tipo parquet. Dentro dele temos os seguintes campos

```bash
{
    'id':str                #identificador do documento
    'kind':str              #Tipo do documento, nessa base só existe 'JURISPRUDENCE'
    'document': 
    {
        'title':str         # Titulo do documento
        'body':str          # Conteúdo do documento
        'highlight':str     # Resumo do documento
        'date':str          # Data do documento
    }

    'metadata': 
    {
        'author': 
        {         # Autor nesse caso é qual Tribunal o documento está
            'id':str        # id do tribunal
            'name':str      # Nome do tribunal
            'username':str  # Nome simplificado
            'avatar':str    # Path imagem
        }
        'legacy': 
        {
            'url':str       # refencia da url do documento
        }
        'court':str         # Identificador do tribunal
        'jurisprudence_type'str             # Tipo de jurisprudencia
        'degree':str # Grau de algo???
        'party_name':array[str] # Membros do documento
        'rapporteur_name':str # Nome do relator
        'summary_status':str # None?
        'guidance_status':str # None?
        'is_mandatory_precedent':bool # É precedente obrigatório?
        'is_decision_merit':bool # Tem decição de merito?
        'is_decision_admissibility':bool # Possui decisão de admissibilidade?
        'judging_organ':str                 # Orgão jurídico
        'thesis_type':str                   # Tipo de tese
        'thesis':str                        # Tese vazio?
        'theme_number':str                  # vazio?
        'theme':str                         # vazio?
        'has_gdpr_citation':bool            # Tem citação gdpr
        'lawsuit_number':str                 # Número do processo
        'related_judges':array[str]         # Juízes relacionados, vazio???
        "document_entities": [{
            "entity_type": "str",           # Tipo da entidade (ex: "NORMATIVE_ACT")
            "title": "str|null",            # Título da entidade, se houver
            "body": 
                {
                "entity_type": "str",       # Tipo da entidade (repetido)
                "matches": [
                {
                    "offsets": [
                    {
                        "length": "int",    # Tamanho do trecho identificado
                        "position": "int"   # Posição inicial no texto
                    }
                    # ...mais offsets...
                    ],
                    "aliases": ["str"]      # Lista de identificadores únicos da entidade
                }
                # ...mais matches...
                ]
            },
            "highlight": "str|null",        # Destaque, se houver
            "extensions": 
            {
                "key_value": []             # Extensões adicionais (array de pares chave-valor)
            },
            "updated_at": "str|null"        # Data/hora da última atualização, se houver
            }
            # ...mais entidades...
        ]
        "document_citations": [
            {
                "id": 
                    {
                        "id": "str",           # Identificador único da citação (ex: número da lei ou jurisprudência)
                        "kind": "str"          # Tipo da citação (ex: "LAW", "JURISPRUDENCE")
                    },
                "count": "int"           # Quantidade de vezes que essa citação aparece no documento
            }
            # ...mais citações...
        ]
        "addons": 
        {
            "key_value": [
            {
                "key": "str",     # Nome ou identificador do dado adicional (ex: "plain_facts")
                "value": "str"    # Valor associado à chave, geralmente um texto explicativo ou informativo
            }
            # ...mais pares chave-valor...
            ]
        }

    }

    "boosts": 
    {
        "recency": "float",                # Valor de atualidade do documento
        "authority": "float",              # Valor de autoridade do documento
        "overall": "float",                # Valor geral calculado
        "experiments": {
            "key_value": []                  # Lista de pares chave-valor de experimentos (pode estar vazia)
        },
        "updated_at": "str"                # Data/hora da última atualização (formato datetime ou string)
    }


}
``` 