
from flask import Blueprint, jsonify, request

from models import Livro, db

livros_api_bp = Blueprint("livros_api", __name__, url_prefix="/api")


@livros_api_bp.route("/livros", methods=["GET"])
def listar():
    return jsonify([livro.para_dict() for livro in Livro.listar()])


@livros_api_bp.route("/livros/<int:livro_id>", methods=["GET"])
def detalhe(livro_id):
    livro = db.session.get(Livro, livro_id)

    if not livro:
        return jsonify({"erro": "Livro não encontrado"}), 404

    return jsonify(livro.para_dict())


@livros_api_bp.route("/livros", methods=["POST"])
def criar():
    dados = request.get_json()

    if not dados:
        return jsonify(
            {"erro": "Envie JSON no body (Content-Type: application/json)"}
        ), 400

    try:
        livro = Livro.a_partir_de_dict(dados)
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    if not livro.titulo or not livro.autor:
        return jsonify({"erro": "Título e autor não podem ser vazios"}), 400
    db.session.add(livro)
    db.session.commit()

    return jsonify(livro.para_dict()), 201


@livros_api_bp.route("/livros/<int:livro_id>", methods=["PUT"])
def atualizar(livro_id):
    livro = db.session.get(Livro, livro_id)
    if not livro:
        return jsonify({"erro": "Livro não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body"}), 400

    try:
        livro.atualizar_de_dict(dados)
    except (ValueError, TypeError):
        return jsonify({"erro": "Campo ano deve ser um número inteiro"}), 400

    db.session.commit()
    return jsonify(livro.para_dict())


@livros_api_bp.route("/livros/<int:livro_id>", methods=["DELETE"])
def excluir(livro_id):
    # DELETE = remover.
    livro = db.session.get(Livro, livro_id)
    if not livro:
        return jsonify({"erro": "Livro não encontrado"}), 404

    db.session.delete(livro)
    db.session.commit()

    return "", 204
