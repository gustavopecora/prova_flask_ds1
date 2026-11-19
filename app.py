import os

from flask import Flask

from models import db, Categoria

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

CATEGORIAS_INICIAIS = ["Eletrônicos", "Roupas", "Alimentos", "Livros"]


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "chave-dev-ds1")
    # O arquivo .db é criado automaticamente na pasta instance/
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///produtos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static", "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # limite de 5 MB por upload

    db.init_app(app)

    from routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()          # cria as tabelas se ainda não existirem
        seed_categorias()        # garante as categorias iniciais

    return app


def seed_categorias():
    """Cadastra as categorias iniciais apenas se a tabela estiver vazia."""
    if Categoria.query.count() == 0:
        db.session.add_all([Categoria(nome=n) for n in CATEGORIAS_INICIAIS])
        db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
