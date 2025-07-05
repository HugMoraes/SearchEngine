from typing import Set, Dict, Any

ALLOWED_OPTIONS: Dict[str, Set[Any]] = {
    "global-expansion-strategy": {
        "thesaurus",
        "word-embeddings",
        "wordnet",
        None  # 'None' ou 'null' é uma opção válida para desativar
    },
    "local-expansion-strategy": {
        "relevance-feedback",
        "cluster-analysis",
        "rocchio",
        None  # 'None' ou 'null' é uma opção válida para desativar
    },
    "transformations": {
        "case-normalization",
        "remove-punctuation",
        "remove-special-characters",
        "remove-stopwords",
        "stemming",
        "lematization",
        "ascii-folding",
        "synonym-expansion",
        "ai-expand-text"
    }
}