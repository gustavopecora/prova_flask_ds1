from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Categoria(db.Model):
    """Lado '1' da relação 1:N: uma categoria possui vários produtos."""
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)

    # Acesso aos produtos da categoria: categoria.produtos
    # Acesso à categoria do produto:    produto.categoria
    produtos = db.relationship("Produto", backref="categoria", lazy=True)

    def __repr__(self):
        return f"<Categoria {self.nome}>"


class Produto(db.Model):
    """Lado 'N' da relação 1:N: cada produto pertence a uma categoria."""
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(255), nullable=False, default="padrao.png")

    # Chave estrangeira que liga o produto à sua categoria
    categoria_id = db.Column(
        db.Integer, db.ForeignKey("categoria.id"), nullable=False
    )

    def __repr__(self):
        return f"<Produto {self.nome}>"
