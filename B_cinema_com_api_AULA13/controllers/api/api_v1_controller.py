from flask import Blueprint, jsonify, request

from services import CinemaService

# Blueprint da API REST — prefixo /api/v1 em todas as rotas
api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")


# ==================== FILMES ====================

@api_v1_bp.route("/filmes", methods=["GET"])
def listar_filmes():
    # TODO ALUNO: usar o service para listar e devolver em JSON
    filmes = CinemaService.listar_filmes()
    return jsonify([CinemaService.filme_para_dict(f) for f in filmes]), 200


@api_v1_bp.route("/filmes/<int:filme_id>", methods=["GET"])
def buscar_filme(filme_id):
    # TODO ALUNO: buscar filme pelo id, 404 se não existir
    filme = CinemaService.buscar_filme(filme_id)
    if not filme:
        return jsonify({"erro": "Filme não encontrado"}), 404
    return jsonify(CinemaService.filme_para_dict(filme)), 200


# ==================== SALAS ====================

@api_v1_bp.route("/salas", methods=["GET"])
def listar_salas():
    # TODO ALUNO: usar o service para listar e devolver em JSON
    salas = CinemaService.listar_salas()
    return jsonify([CinemaService.sala_para_dict(s) for s in salas]), 200


@api_v1_bp.route("/salas/<int:sala_id>", methods=["GET"])
def buscar_sala(sala_id):
    # TODO ALUNO: buscar sala pelo id, 404 se não existir
    sala = CinemaService.buscar_sala(sala_id)
    if not sala:
        return jsonify({"erro": "Sala não encontrada"}), 404
    return jsonify(CinemaService.sala_para_dict(sala)), 200


# ==================== SESSOES ====================

@api_v1_bp.route("/sessoes", methods=["GET"])
def listar_sessoes():
    # TODO ALUNO: usar o service para listar e devolver em JSON
    sessoes = CinemaService.listar_sessoes()
    return jsonify([CinemaService.sessao_para_dict(s) for s in sessoes]), 200


@api_v1_bp.route("/sessoes/<int:sessao_id>", methods=["GET"])
def buscar_sessao(sessao_id):
    # TODO ALUNO: buscar sessão pelo id, 404 se não existir
    sessao = CinemaService.buscar_sessao(sessao_id)
    if not sessao:
        return jsonify({"erro": "Sessão não encontrada"}), 404
    return jsonify(CinemaService.sessao_para_dict(sessao)), 200


@api_v1_bp.route("/sessoes", methods=["POST"])
def criar_sessao():
    # TODO ALUNO: ler JSON do corpo da requisição e validar campos obrigatórios
    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = ["filme_id", "sala_id", "data_hora", "preco"]
    faltando = [c for c in campos_obrigatorios if c not in dados]
    if faltando:
        return jsonify(
            {"erro": f"Campos obrigatórios faltando: {', '.join(faltando)}"}
        ), 400

    try:
        sessao = CinemaService.criar_sessao(
            filme_id=dados["filme_id"],
            sala_id=dados["sala_id"],
            data_hora=dados["data_hora"],
            preco=dados["preco"],
        )
    except (ValueError, TypeError) as erro:
        return jsonify({"erro": f"Dados inválidos: {erro}"}), 400

    return jsonify(CinemaService.sessao_para_dict(sessao)), 201


@api_v1_bp.route("/sessoes/<int:sessao_id>", methods=["DELETE"])
def excluir_sessao(sessao_id):
    # TODO ALUNO: excluir sessão pelo id, 404 se não existir
    sessao = CinemaService.excluir_sessao(sessao_id)
    if not sessao:
        return jsonify({"erro": "Sessão não encontrada"}), 404
    return jsonify({"mensagem": "Sessão excluída com sucesso"}), 200


# ==================== INGRESSOS (opcional) ====================

@api_v1_bp.route("/sessoes/<int:sessao_id>/ingressos", methods=["GET"])
def listar_ingressos(sessao_id):
    ingressos = CinemaService.listar_ingressos_da_sessao(sessao_id)
    return jsonify([CinemaService.ingresso_para_dict(i) for i in ingressos]), 200


@api_v1_bp.route("/sessoes/<int:sessao_id>/ingressos", methods=["POST"])
def criar_ingresso(sessao_id):
    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = ["assento", "nome_comprador"]
    faltando = [c for c in campos_obrigatorios if c not in dados]
    if faltando:
        return jsonify(
            {"erro": f"Campos obrigatórios faltando: {', '.join(faltando)}"}
        ), 400

    ingresso = CinemaService.criar_ingresso(
        sessao_id=sessao_id,
        assento=dados["assento"],
        nome_comprador=dados["nome_comprador"],
    )
    return jsonify(CinemaService.ingresso_para_dict(ingresso)), 201


# ==================== STATUS ====================

@api_v1_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "API está funcionando"}), 200
