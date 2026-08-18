# Pacote controllers — agrupa os Blueprints da API REST.
# Nesta aula há um único Blueprint: selecao_api (rotas /api/selecao).

from controllers.selecao_api import selecao_api_bp

__all__ = ["selecao_api_bp"]
