from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .livro import Livro

__all__ = ["db", "ModeloBase", "Livro"]
