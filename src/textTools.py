print("Loading text tools...", flush=True)
import re
import os
import nltk
import spacy
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
import ollama

try:
    _stop_words = set(stopwords.words('portuguese'))
except LookupError:
    nltk.download('stopwords')
    _stop_words = set(stopwords.words('portuguese'))

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('stemmers/rslp')
except LookupError:
    nltk.download('rslp')

try:
    nlp_pt = spacy.load("pt_core_news_sm")
    nlp_pt.max_length = 5000000
except OSError:
    os.system("python -m spacy download pt_core_news_sm")
    nlp_pt = spacy.load("pt_core_news_sm")

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
        prompt_sistema = """
            Você vai me ajudar a expandir consultas no contexto de um sistema de busca jurídico. 
            Vou lhe mandar textos e você expandirá os substantivos, verbos e adjetivos com 
            seus respectivos sinônimos. Escreva pelo menos três sinônimos para as palavras 
            mais importantes da consulta. Retorne apenas a consulta com os sinônimos, 
            sem caracteres especiais e sem vírgula onde houver os sinônimos adicionados. 
            não escreva mais nada além disso. Escreva em português!
            """

        prompt_usuario = f'Em português. Expanda a seguinte query adicionando apenas 2 a 4 palavras importantes semelhantes para busca em um sistema de busca jurídico: "{query}"'

        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'system',
                    'content': prompt_sistema.strip(),
                },
                {
                    'role': 'user',
                    'content': prompt_usuario,
                },
            ],
            options={
                'temperature': 0.5,
            }
        )

        return response['message']['content']
    
    def ai_text(text: str) -> str:
        prompt_sistema = """
                        Você vai me ajudar a otimizar textos em um contexto de busca por documentos jurídicos.
                        Vou te mandar textos e você vai me retornar termos e possíveis consultas sobre as coisas mais importantes de cada parágrafo do texto.
                        Me retorne em um formato padronizado que seja cada resultado separado por espaços, NÃO USE QUEBRA DE LINHA!.
                        Não escreva nada além do resultado. Escreva em português!
                        Escreva um longo texto com termos otimizados para busca jurídica
                        
                        """
        
        prompt_usuario = f'Extraia termos e frases otimizadas para busca jurídica deste texto: "{text}"'

        response = ollama.chat(
            model='llama3',
            messages=[
                {
                    'role': 'system',
                    'content': prompt_sistema.strip(),
                },
                {
                    'role': 'user',
                    'content': prompt_usuario,
                },
            ],
            options={
                'temperature': 0.5,
            }
        )


        return response['message']['content']
