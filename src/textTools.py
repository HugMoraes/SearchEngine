print("Loading text tools...", flush=True)
import re
import os
import nltk
import spacy
from numpy import ndarray
from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.tokenize import word_tokenize
import ollama

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
        """
        Expande uma consulta jurídica usando o Llama 3 rodando localmente via Ollama.
        """
        # O prompt de sistema é o mesmo que você usou para o Groq
        prompt_sistema = """
            Você vai me ajudar a expandir consultas no contexto de um sistema de busca jurídico. 
            Vou lhe mandar textos e você expandirá os substantivos, verbos e adjetivos com 
            seus respectivos sinônimos. Escreva pelo menos três sinônimos para as palavras 
            mais importantes da consulta. Retorne apenas a consulta com os sinônimos, 
            sem caracteres especiais e sem vírgula onde houver os sinônimos adicionados. 
            não escreva mais nada além disso. Escreva em português!
            """

        # A mensagem do usuário também segue o mesmo padrão
        prompt_usuario = f'Em português. Expanda a seguinte query adicionando apenas 2 a 4 palavras importantes semelhantes para busca em um sistema de busca jurídico: "{query}"'

        # Chama a API do Ollama com os prompts e parâmetros
        response = ollama.chat(
            model='llama3',  # Ou o nome exato do seu modelo local
            messages=[
                {
                    'role': 'system',
                    'content': prompt_sistema.strip(),  # .strip() remove espaços/linhas em branco do início/fim
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

    @staticmethod
    def vectorize(text: str) -> ndarray:
        cleaned_text = Tools.lowercase_text(text)
        vector = _model_st.encode(cleaned_text)
        return vector
    
    def ai_text(text: str) -> str:
        """
        Otimiza textos para busca jurídica, extraindo termos e consultas
        usando o Llama 3 rodando localmente via Ollama.
        """

        prompt_sistema = """
                        Você vai me ajudar a otimizar textos em um contexto de busca por documentos jurídicos.
                        Vou te mandar textos e você vai me retornar termos e possíveis consultas sobre as coisas mais importantes de cada parágrafo do texto.
                        Me retorne em um formato padronizado que seja cada resultado separado por espaços, NÃO USE QUEBRA DE LINHA!.
                        Não escreva nada além do resultado. Escreva em português!
                        Escreva um longo texto com termos otimizados para busca jurídica
                        
                        """

        # O prompt do usuário que inclui o texto a ser analisado.
        prompt_usuario = f'Extraia termos e frases otimizadas para busca jurídica deste texto: "{text}"'

        # Chamada para a biblioteca ollama, com a mesma estrutura de antes
        response = ollama.chat(
            model='llama3',  # Use o nome do seu modelo local
            messages=[
                {
                    'role': 'system',
                    'content': prompt_sistema.strip(), # .strip() remove espaços/linhas em branco do início/fim
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

        # Retorna o conteúdo da resposta do modelo
        return response['message']['content']



# print(Tools.ai_text('''
#                     EMBARGOS A EXECUÇÃO FISCAL. MULTA APLICADA À EMBARGANTE POR UTILIZAÇÃO DE PRODUTO DA QUEIMA DE PALHA DE CANA DE AÇUCAR.
#                     PEDIDO JULGADO IMPROCEDENTE PELO MM. JUÍZO "A QUO". RECURSO DE APELAÇÃO INTERPOSTO PELA EMBARGANTE. PRETENSÃO RECURSAL ACOLHIDA. ENTENDIMENTO MAJORITÁRIO
#                     DA TURMA JULGADORA SOBRE O TEMA, A DESPEITO DA POSIÇÃO DESTE JULGADOR EM SENTIDO CONTRÁRIO. RESPONSABILIDADE ADMINISTRATIVA AMBIENTAL QUE É SUBJETIVA. AUSÊNCIA
#                     DE PROVA SEGURA DE QUE A EMBARGANTE TENHA PROMOVIDO O INCÊNDIO NO LOCAL OU DELE SE BENEFICIADO. COLHEITA REALIZADA DE FORMA MECANIZADA PELA USINA, QUE, ADEMAIS,
#                     PROCESSOU O PRODUTO DECORRENTE DA QUEIMA A FIM DE MINIMIZAR OS PREJUÍZOS (IMPORTANTE RESSALTAR QUE O ARTIGO 39 DO DECRETO-LEI Nº 3.855 /41 VEDA A EMPRESA PRODUTORA
#                     DE ÁLCOOL RECUSAR A COLHEITA DE SEU FORNECEDOR). ANULAÇÃO DO AUTO DE INFRAÇÃO E EXTINÇÃO DA EXECUÇÃO. SENTENÇA REFORMADA. RECURSO PROVIDO'''))