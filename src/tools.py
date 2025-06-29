import re
import nltk
from nltk.corpus import stopwords

class Tools:
    try:
        _stop_words = set(stopwords.words('portuguese'))
    except LookupError:
        print("NLTK stopwords not found. Downloading...")
        nltk.download('stopwords')
        _stop_words = set(stopwords.words('portuguese'))

    @staticmethod
    def remove_stopwords(text: str) -> str:
        words = text.split()
        # Usa o set de stopwords já carregado na classe
        filtered = [word for word in words if word.lower() not in Tools._stop_words]
        return ' '.join(filtered)

    @staticmethod
    def remove_special_characters(text: str) -> str:
        # A flag re.UNICODE é padrão no Python 3, então pode ser omitida.
        return re.sub(r'[^\w\sÀ-ÿ]', ' ', text)

    @staticmethod
    def lowercase_text(text: str) -> str:
        return text.lower()