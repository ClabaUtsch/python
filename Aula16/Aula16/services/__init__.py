# Pacote services — funções que falam com o mundo externo (sites, APIs).
# O Controller importa daqui; os alunos costumam copiar este padrão da Aula 9/14.

from services.ge_globo import buscar_mencoes_selecao

__all__ = ["buscar_mencoes_selecao"]
