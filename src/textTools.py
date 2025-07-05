import re
import nltk
import os
import spacy
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
from groq import Groq
import time
# Inicialização segura dos recursos externos
try:
    _stop_words = set(stopwords.words('portuguese'))
except LookupError:
    nltk.download('stopwords')
    _stop_words = set(stopwords.words('portuguese'))

# Garante que os recursos do NLTK estejam disponíveis
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('stemmers/rslp')
except LookupError:
    nltk.download('rslp')

# Carrega o modelo do spaCy para português
try:
    nlp_pt = spacy.load("pt_core_news_sm")
except OSError:
    os.system("python -m spacy download pt_core_news_sm")
    nlp_pt = spacy.load("pt_core_news_sm")

client = Groq(api_key="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")

class Tools:

    @staticmethod
    def remove_stopwords(text: str) -> str:
        words = text.split()
        filtered = [word for word in words if word.lower() not in _stop_words]
        return ' '.join(filtered)

    @staticmethod
    def remove_special_characters(text: str) -> str:
        return re.sub(r'[^\w\sÀ-ÿ]', ' ', text)

    @staticmethod
    def lowercase_text(text: str) -> str:
        return text.lower()

    @staticmethod
    def remove_extra_spaces(text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def apply_lemmatization(text: str) -> str:
        doc = nlp_pt(text)
        lemmatized_words = [token.lemma_ for token in doc]
        return ' '.join(lemmatized_words)
    
    @staticmethod
    def tokenize(text: str) -> list[str]:            
        return word_tokenize(text, language='portuguese')
    
    @staticmethod
    def apply_stemming(text: str) -> str:               
        stemmer = RSLPStemmer()
        words = text.split()
        return ' '.join([stemmer.stem(word) for word in words])
    
    @staticmethod
    def expand_query(query: str) -> str:
        start_time = time.time()
        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você vai me ajudar a expandir consultas no contexto de um sistema de busca jurídico. Vou lhe mandar textos e você expandirá os substantivos, verbos e adjetivos com seus respectivos sinônimos. Escreva pelo menos três sinônimos para as palavras mais importantes da consulta. Retorne apenas a consulta com os sinônimos, sem caracteres especiais e sem vírgula onde houver os sinônimos adicionados. não escreva mais nada além disso."
                },
                {
                    "role": "user",
                    "content": f'Expanda a seguinte query: "{query}"'
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )

        print(f"Tempo chamando Groq para adicionar sinônimos: {int(time.time() - start_time)}s")
        return stream.choices[0].message.content
    

# print(Tools.expand_query("ação para tutela da saúde mental"))