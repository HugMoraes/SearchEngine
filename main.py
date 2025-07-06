from src.utils import check_index_elasticSearch, remove_search_fields
from src.searchEngine import MyElasticsearch
from src.config import MAIN_INDEX_NAME, ELASTIC_SEARCH_ADDRESS # to initialize env vars
from flask import Flask, request, jsonify
from flask_cors import CORS

if __name__ == '__main__':
    
    """
    Esta é a "Application Factory".
    Nenhum app é criado até que esta função seja chamada.
    Ela configura e retorna uma nova instância da aplicação.
    """

    print("\n--- INICIANDO VERIFICAÇÃO DE PRÉ-REQUISITOS ---")
    check_index_elasticSearch()
    print("--- VERIFICAÇÃO CONCLUÍDA. APP PRONTO PARA INICIAR. ---\n")

    app = Flask(__name__)

    CORS(app)

    try:
        es = MyElasticsearch(hosts=ELASTIC_SEARCH_ADDRESS)
    except Exception as e:
        print(f"   - Erro ao conectar com o Elasticsearch: {e}")
        es = None

    @app.route('/api/search', methods=['GET'])
    def rota_de_busca():
        if es is None:
            return jsonify({"erro": "Não foi possível conectar ao servidor Elasticsearch."}), 500

        termo_de_busca = request.args.get('q')
        if not termo_de_busca:
            return jsonify({"erro": "O parâmetro de busca 'q' é obrigatório."}), 400

        try:
            resultados = es.search_documents(MAIN_INDEX_NAME, termo_de_busca, size=20)
            map(lambda doc: remove_search_fields(doc), resultados)
            return jsonify(resultados)
        except Exception as e:
            print(f"Erro durante a busca: {e}")
            return jsonify({"erro": f"Ocorreu um erro durante a busca: {e}"}), 500

    print("🚀 Iniciando o servidor de desenvolvimento Flask...")
    
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    