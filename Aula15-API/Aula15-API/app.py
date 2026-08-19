import os

from flask import Flask, jsonify

from controllers import livros_api_bp
from models import Livro, db

DADOS_INICIAIS = [
    ("Dom Casmurro", "Machado de Assis", 1899),
    ("O Cortiço", "Aluísio Azevedo", 1890),
    ("1984", "George Orwell", 1949),
]
ENDPOINTS = [
    {"metodo": "GET", "rota": "/api/livros", "descricao": "Listar todos os livros"},
    {"metodo": "GET", "rota": "/api/livros/<id>", "descricao": "Detalhe de um livro"},
    {"metodo": "POST", "rota": "/api/livros", "descricao": "Criar livro (JSON no body)"},
    {"metodo": "PUT", "rota": "/api/livros/<id>", "descricao": "Atualizar livro"},
    {"metodo": "DELETE", "rota": "/api/livros/<id>", "descricao": "Excluir livro"},
]


def criar_app():
    app = Flask(__name__)

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "biblioteca.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "aula15-api-rest-dev"

    db.init_app(app)
    app.register_blueprint(livros_api_bp)

    with app.app_context():
        db.create_all()
        if Livro.query.count() == 0:
            for titulo, autor, ano in DADOS_INICIAIS:
                db.session.add(Livro(titulo=titulo, autor=autor, ano=ano))
            db.session.commit()

    @app.route("/")
    def index():
        return jsonify(
            {
                "aula": "15 — API REST (somente JSON)",
                "mensagem": "Use Postman, Insomnia ou curl. Não há páginas HTML neste projeto.",
                "endpoints": ENDPOINTS,
            }
        )

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
