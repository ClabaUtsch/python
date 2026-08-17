from datetime import datetime

from models import Filme, Ingresso, Sala, Sessao, db


class CinemaService:
    """
    Camada de serviço: concentra as regras de negócio e o acesso ao banco.
    Tanto as rotas web (render_template) quanto a API REST (jsonify)
    chamam esses mesmos métodos, evitando duplicar lógica.
    """

    # ---------------- FILMES ----------------

    @staticmethod
    def listar_filmes():
        return Filme.listar()

    @staticmethod
    def buscar_filme(filme_id):
        return db.session.get(Filme, filme_id)

    @staticmethod
    def filme_para_dict(filme):
        return {
            "id": filme.id,
            "titulo": filme.titulo,
            "duracao_min": filme.duracao_min,
            "classificacao": filme.classificacao,
        }

    # ---------------- SALAS ----------------

    @staticmethod
    def listar_salas():
        return Sala.listar()

    @staticmethod
    def buscar_sala(sala_id):
        return db.session.get(Sala, sala_id)

    @staticmethod
    def sala_para_dict(sala):
        return {
            "id": sala.id,
            "numero": sala.numero,
            "capacidade": sala.capacidade,
        }

    # ---------------- SESSOES ----------------

    @staticmethod
    def listar_sessoes():
        return Sessao.listar_com_detalhes()

    @staticmethod
    def buscar_sessao(sessao_id):
        return db.session.get(Sessao, sessao_id)

    @staticmethod
    def criar_sessao(filme_id, sala_id, data_hora, preco):
        sessao = Sessao(
            filme_id=filme_id,
            sala_id=sala_id,
            data_hora=datetime.fromisoformat(data_hora),
            preco=preco,
        )
        db.session.add(sessao)
        db.session.commit()
        return sessao

    @staticmethod
    def excluir_sessao(sessao_id):
        sessao = db.session.get(Sessao, sessao_id)
        if sessao:
            db.session.delete(sessao)
            db.session.commit()
        return sessao

    @staticmethod
    def sessao_para_dict(sessao):
        return {
            "id": sessao.id,
            "filme_id": sessao.filme_id,
            "sala_id": sessao.sala_id,
            "filme": sessao.filme.titulo if sessao.filme else None,
            "sala": sessao.sala.numero if sessao.sala else None,
            "data_hora": sessao.data_hora.isoformat() if sessao.data_hora else None,
            "preco": sessao.preco,
        }

    # ---------------- INGRESSOS (opcional) ----------------

    @staticmethod
    def listar_ingressos_da_sessao(sessao_id):
        return Ingresso.query.filter_by(sessao_id=sessao_id).all()

    @staticmethod
    def criar_ingresso(sessao_id, assento, nome_comprador):
        ingresso = Ingresso(
            sessao_id=sessao_id,
            assento=assento,
            nome_comprador=nome_comprador,
        )
        db.session.add(ingresso)
        db.session.commit()
        return ingresso

    @staticmethod
    def ingresso_para_dict(ingresso):
        return {
            "id": ingresso.id,
            "sessao_id": ingresso.sessao_id,
            "assento": ingresso.assento,
            "nome_comprador": ingresso.nome_comprador,
        }
