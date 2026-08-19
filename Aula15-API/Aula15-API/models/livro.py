from . import db
from .base import ModeloBase


class Livro(ModeloBase):
    __tablename__ = "livros"

    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(120), nullable=False)
    ano = db.Column(db.Integer, nullable=False)

    @classmethod
    def listar(cls):
        """Lista todos os livros ordenados por título."""
        return cls.query.order_by(cls.titulo).all()

    @classmethod
    def a_partir_de_dict(cls, dados):
        """Monta um Livro a partir do JSON do POST (request.get_json())."""
        try:
            return cls(
                titulo=str(dados["titulo"]).strip(),
                autor=str(dados["autor"]).strip(),
                ano=int(dados["ano"]),
            )
        except (KeyError, ValueError, TypeError) as erro:
            raise ValueError("Campos obrigatórios: titulo, autor, ano (inteiro)") from erro

    def atualizar_de_dict(self, dados):
        """Atualiza só os campos que vierem no JSON do PUT."""
        if "titulo" in dados:
            self.titulo = str(dados["titulo"]).strip()
        if "autor" in dados:
            self.autor = str(dados["autor"]).strip()
        if "ano" in dados:
            self.ano = int(dados["ano"])

    def para_dict(self):
        """
        Converte o objeto em dict serializável.
        jsonify() só aceita tipos JSON (str, int, list, dict...).
        Por isso data_criacao vira string com str(...).
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "autor": self.autor,
            "ano": self.ano,
            "data_criacao": str(self.data_criacao),
        }
