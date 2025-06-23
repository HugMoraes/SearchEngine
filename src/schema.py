MAPPING = {
    "properties": {
        "id": {"type": "keyword"},
        "document": {
            "properties": {
                "title": {"type": "text"},
                "body": {"type": "text"},
                "highlight": {"type": "text"},
                "date": {"type": "date"}
            }
        },
        "metadata": {
            "properties": {
                "author": {
                    "properties": {
                        "name": {"type": "text"},
                        "username": {"type": "keyword"}
                    }
                },
                "court": {"type": "text"},
                "jurisprudence_type": {"type": "keyword"},
                "degree": {"type": "keyword"},
                "rapporteur_name": {"type": "text"},
                "judging_organ": {"type": "text"},
                "related_judges": {"type": "flattened"},
                "document_citations": {
                    "type": "nested",
                    "properties": {
                        "id": {"type": "keyword"},
                        "kind": {"type": "keyword"},
                        "count": {"type": "integer"}
                    }
                },
                "addons": {"type": "text"}  # Addons should be a list of strings, separated by line breaks
            }
        },
        "phrasal_terms": {
            "type": "nested"
        }
    }
}
