# =============================================================================
# Controller da API — camada que o cliente (Postman) enxerga
# =============================================================================
# Responsabilidade:
#   • Ler parâmetros da URL (request.args)
#   • Chamar o Service (buscar_mencoes_selecao)
#   • Devolver JSON com jsonify e códigos HTTP corretos (200, 400, 502)
# O Controller NÃO faz requests nem parse de HTML — isso é do Service.
#
# TYPE HINT nesta camada:
#   O Flask aceita retorno "só o JSON" ou "(jsonify(...), 400)".
#   Por isso muitas rotas não anotam o retorno — variam entre 200 e erro.
#   O Service sim usa tipos fixos (-> dict / TypedDict) porque sempre devolve dict.

from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from services import buscar_mencoes_selecao

# Blueprint com prefixo /api → rota "/selecao" vira GET /api/selecao
selecao_api_bp = Blueprint("selecao_api", __name__, url_prefix="/api")


@selecao_api_bp.route("/selecao", methods=["GET"])
def listar_mencoes_selecao() -> Any:
    # Any = "pode ser Response do Flask ou tupla (response, status)".
    # Usamos Any aqui só para documentar que o retorno é flexível por causa do HTTP.

    # GET = apenas leitura; não há POST nesta aula (dados vêm do site, não do body).

    # request.args.get devolve str | None; damos default "substring" e garantimos str.
    modo: str = request.args.get("modo", "substring").strip().lower()

    if modo not in ("substring", "palavra"):
        # 400 Bad Request — o cliente mandou um parâmetro inválido.
        return jsonify(
            {"erro": "Parâmetro modo deve ser 'substring' ou 'palavra'"}
        ), 400

    try:
        # dados é dict conforme ResultadoBusca no Service (type hint lá).
        dados = buscar_mencoes_selecao(modo=modo)
    except ConnectionError as erro:
        # 502 Bad Gateway — nossa API está no ar, mas a fonte externa falhou.
        return jsonify({"erro": str(erro)}), 502

    # 200 OK — lista de menções em JSON (dict já montado pelo Service).
    return jsonify(dados)
