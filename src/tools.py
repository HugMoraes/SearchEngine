import re
import nltk
from nltk.corpus import stopwords

class Tools:
    @staticmethod
    def remove_stopwords(text: str) -> str:
        try:
            stopwords.words('portuguese')
        except LookupError:
            nltk.download('stopwords')
        stop_words = set(stopwords.words('portuguese'))
        words = text.split()
        filtered = [word for word in words if word.lower() not in stop_words]
        return ' '.join(filtered)

    @staticmethod
    def remove_special_characters(text: str) -> str:
        return re.sub(r'[^\w\sÀ-ÿ]', ' ', text, flags=re.UNICODE)

    @staticmethod
    def lowercase_text(text: str) -> str:
        return text.lower()

    @staticmethod
    def apply_text_processing(text:str, functions:list) -> str:
        """
        Applies a series of text processing functions to the input text.
        
        Args:
            text (str): The input text to be processed.
            functions (list): A list of functions to apply to the text.
        
        Returns:
            str: The processed text.
        """
        for func in functions:
            text = func(text)
        return text