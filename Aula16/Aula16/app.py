# =============================================================================
# Aula 16 — ponto de entrada da aplicação Flask
# =============================================================================
# Diferente da Aula 15: aqui NÃO há banco SQLite. Os dados vêm de um site
# externo (ESPN Futebol) no momento da requisição — o Service faz o download.
# Resposta sempre JSON (jsonify), sem render_template.
#
# TYPE HINT (revisão):
#   def criar_app() -> Flask:
#   O "-> Flask" promete que a função devolve um objeto Flask.
#   Não muda o comportamento em runtime — ajuda você e o VS Code/Cursor.

from flask import Flask, jsonify

from controllers import selecao_api_bp

# Lista exibida em GET / para o aluno saber qual rota testar no Postman.
# Cada item é um dict com chaves str; o valor de "query" também é str.
ENDPOINTS: list[dict[str, str]] = [
    {
        "metodo": "GET",
        "rota": "/api/selecao",
        "descricao": "Lista textos do ESPN Futebol que citam Brasileirão (busca ao vivo no site)",
        "query": "?modo=substring (padrão) ou ?modo=palavra",
    },
]


def criar_app() -> Flask:
    # Factory pattern: mesma ideia das aulas anteriores — facilita testes.
    app = Flask(__name__)

    # SECRET_KEY é obrigatória no Flask; nesta API simples quase não usamos sessão,
    # mas o framework exige a configuração.
    app.config["SECRET_KEY"] = "aula16-ge-globo-dev"

    # Registra o Blueprint das rotas /api/... (arquivo controllers/selecao_api.py).
    app.register_blueprint(selecao_api_bp)

    @app.route("/")
    def index():
        # Rota de ajuda — também é JSON, não é página HTML.
        return jsonify(
            {
                "aula": "16 — API + site externo (ESPN Futebol)",
                "fonte": "https://www.espn.com.br/futebol/",
                "mensagem": "Use GET /api/selecao no Postman ou navegador.",
                "endpoints": ENDPOINTS,
            }
        )

    return app


# Instância usada pelo `python app.py` e por testes automatizados.
app = criar_app()

if __name__ == "__main__":
    # debug=True recarrega ao salvar arquivo — só para desenvolvimento em sala.
    app.run(debug=True)
