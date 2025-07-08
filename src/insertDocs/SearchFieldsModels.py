from src.textTools import Tools

class SearchFieldsConfig:
    COMMON_TECHNIQUES= [
        "remove_stopwords",
        "lowercase_text",
    ]

    EXCLUSIVE_OPTIONAL_TECHNIQUES = [
        ["stemming", "lemmatization"]
    ]

    FIELDS = [
        "title", "body", "highlight"
    ]


class SearchField:
    def __init__(self, techniques:list[str], from_field:str):
        self.techniques = techniques
        self.from_field = from_field

    def __repr__(self):
        """Retorna uma representação legível do objeto."""
        return f"SearchField(from_field='{self.from_field}', techniques={self.techniques})"

TEXT_FUNCTIONS = {
    "remove_stopwords": Tools.remove_stopwords,
    "lowercase_text": Tools.lowercase_text,
    "lemmatization": Tools.apply_lemmatization,
    "stemming": Tools.apply_stemming
}

