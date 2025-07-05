import re
import os
import nltk
import spacy
from numpy import ndarray
from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
from groq import Groq

_model_st = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

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

        return stream.choices[0].message.content

    @staticmethod
    def vectorize(text: str) -> ndarray:
        cleaned_text = Tools.lowercase_text(text)
        vector = _model_st.encode(cleaned_text)
        return vector
    
    def ai_text(text: str) -> str:
        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    Você vai me ajudar a otimizar textos em um contexto de busca por documentos jurídicos.
                    Vou te mandar textos e você vai me retornar termos e possíveis consultas sobre as coisas mais importantes de cada parágrafo do texto.
                    Me retorne em um formato padronizado que seja cada resultado separado por quebras de linha.
                    Não escreva nada além do resultado.
                    Para cada texto, leia todos os parágrafos e gere pelo menos 10 resultados e no máximo 50.
                    """
                },
                {
                    "role": "user",
                    "content": f'Extraia termos otimizados para busca jurídica deste texto: "{text}"'
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )

        return stream.choices[0].message.content


# print(Tools.ai_text('''
#                     EMBARGOS A EXECUÇÃO FISCAL. MULTA APLICADA À EMBARGANTE POR UTILIZAÇÃO DE PRODUTO DA QUEIMA DE PALHA DE CANA DE AÇUCAR.
#                     PEDIDO JULGADO IMPROCEDENTE PELO MM. JUÍZO "A QUO". RECURSO DE APELAÇÃO INTERPOSTO PELA EMBARGANTE. PRETENSÃO RECURSAL ACOLHIDA. ENTENDIMENTO MAJORITÁRIO
#                     DA TURMA JULGADORA SOBRE O TEMA, A DESPEITO DA POSIÇÃO DESTE JULGADOR EM SENTIDO CONTRÁRIO. RESPONSABILIDADE ADMINISTRATIVA AMBIENTAL QUE É SUBJETIVA. AUSÊNCIA
#                     DE PROVA SEGURA DE QUE A EMBARGANTE TENHA PROMOVIDO O INCÊNDIO NO LOCAL OU DELE SE BENEFICIADO. COLHEITA REALIZADA DE FORMA MECANIZADA PELA USINA, QUE, ADEMAIS,
#                     PROCESSOU O PRODUTO DECORRENTE DA QUEIMA A FIM DE MINIMIZAR OS PREJUÍZOS (IMPORTANTE RESSALTAR QUE O ARTIGO 39 DO DECRETO-LEI Nº 3.855 /41 VEDA A EMPRESA PRODUTORA
#                     DE ÁLCOOL RECUSAR A COLHEITA DE SEU FORNECEDOR). ANULAÇÃO DO AUTO DE INFRAÇÃO E EXTINÇÃO DA EXECUÇÃO. SENTENÇA REFORMADA. RECURSO PROVIDO'''))