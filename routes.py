import math
import os
import uuid

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for
)
from werkzeug.utils import secure_filename

from models import db, Categoria, Produto

bp = Blueprint("main", __name__)

IMAGEM_PADRAO = "padrao.png"
EXTENSOES_PERMITIDAS = {"png", "jpg", "jpeg", "gif"}


# ----------------------------------------------------------------------
# Funções auxiliares
# ----------------------------------------------------------------------
def extensao_permitida(nome_arquivo):
    return (
        "." in nome_arquivo
        and nome_arquivo.rsplit(".", 1)[1].lower() in EXTENSOES_PERMITIDAS
    )


def converter_preco(texto):
    """Converte o texto do formulário em float. Retorna None se for inválido."""
    try:
        valor = float((texto or "").strip().replace(",", "."))
    except ValueError:
        return None
    if math.isnan(valor) or math.isinf(valor):
        return None
    return valor


def validar_dados(nome, preco_texto, categoria_id):
    """Valida os campos do formulário. Retorna (preco, categoria, erros)."""
    erros = []

    if len(nome) < 3:
        erros.append("O nome do produto deve ter pelo menos 3 caracteres.")

    preco = converter_preco(preco_texto)
    if preco is None:
        erros.append("Preço inválido: informe um número (ex.: 19.90).")
    elif preco <= 0:
        erros.append("O preço deve ser maior que zero.")

    categoria = db.session.get(Categoria, categoria_id) if categoria_id else None
    if categoria is None:
        erros.append("Selecione uma categoria válida.")

    return preco, categoria, erros


def salvar_imagem(arquivo):
    """Salva o arquivo em static/uploads/ com nome único e retorna o nome."""
    nome_seguro = secure_filename(arquivo.filename)
    nome_final = f"{uuid.uuid4().hex}_{nome_seguro}"
    arquivo.save(os.path.join(current_app.config["UPLOAD_FOLDER"], nome_final))
    return nome_final


def remover_imagem(nome_arquivo):
    """Apaga a imagem do disco, preservando sempre a padrao.png."""
    if not nome_arquivo or nome_arquivo == IMAGEM_PADRAO:
        return
    caminho = os.path.join(
        current_app.config["UPLOAD_FOLDER"], os.path.basename(nome_arquivo)
    )
    if os.path.isfile(caminho):
        os.remove(caminho)


def foto_enviada(arquivo):
    return arquivo is not None and arquivo.filename != ""


# ----------------------------------------------------------------------
# Rotas
# ----------------------------------------------------------------------
@bp.route("/")
def index():
    busca = request.args.get("busca", "").strip()

    query = Produto.query
    if busca:
        query = query.filter(Produto.nome.ilike(f"%{busca}%"))
    produtos = query.order_by(Produto.nome.asc()).all()

    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template(
        "index.html", produtos=produtos, categorias=categorias, busca=busca
    )


@bp.route("/salvar", methods=["POST"])
def salvar():
    nome = request.form.get("nome", "").strip()
    preco_texto = request.form.get("preco", "")
    categoria_id = request.form.get("categoria_id", type=int)
    foto = request.files.get("foto")

    preco, categoria, erros = validar_dados(nome, preco_texto, categoria_id)

    if foto_enviada(foto) and not extensao_permitida(foto.filename):
        erros.append(
            "Extensão de imagem não permitida. Use: "
            + ", ".join(sorted(EXTENSOES_PERMITIDAS)) + "."
        )

    if erros:
        for erro in erros:
            flash(erro, "erro")
        # Reexibe a tela mantendo o que o usuário digitou
        categorias = Categoria.query.order_by(Categoria.nome).all()
        produtos = Produto.query.order_by(Produto.nome.asc()).all()
        return render_template(
            "index.html", produtos=produtos, categorias=categorias, busca="",
            form={"nome": nome, "preco": preco_texto, "categoria_id": categoria_id},
        ), 400

    imagem = IMAGEM_PADRAO
    if foto_enviada(foto):
        imagem = salvar_imagem(foto)

    produto = Produto(
        nome=nome, preco=preco, imagem=imagem, categoria_id=categoria.id
    )
    db.session.add(produto)
    db.session.commit()

    flash("Produto cadastrado com sucesso!", "sucesso")
    return redirect(url_for("main.index"))


@bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    produto = db.get_or_404(Produto, id)
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "GET":
        return render_template("editar.html", produto=produto, categorias=categorias)

    nome = request.form.get("nome", "").strip()
    preco_texto = request.form.get("preco", "")
    categoria_id = request.form.get("categoria_id", type=int)
    foto = request.files.get("foto")

    preco, categoria, erros = validar_dados(nome, preco_texto, categoria_id)

    if foto_enviada(foto) and not extensao_permitida(foto.filename):
        erros.append(
            "Extensão de imagem não permitida. Use: "
            + ", ".join(sorted(EXTENSOES_PERMITIDAS)) + "."
        )

    if erros:
        for erro in erros:
            flash(erro, "erro")
        return render_template(
            "editar.html", produto=produto, categorias=categorias,
            form={"nome": nome, "preco": preco_texto, "categoria_id": categoria_id},
        ), 400

    imagem_antiga = produto.imagem
    produto.nome = nome
    produto.preco = preco
    produto.categoria_id = categoria.id

    if foto_enviada(foto):
        produto.imagem = salvar_imagem(foto)

    db.session.commit()

    # Só apaga a foto antiga depois que o banco foi atualizado com sucesso
    if foto_enviada(foto):
        remover_imagem(imagem_antiga)

    flash("Produto atualizado com sucesso!", "sucesso")
    return redirect(url_for("main.index"))


@bp.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    produto = db.get_or_404(Produto, id)
    imagem = produto.imagem

    db.session.delete(produto)
    db.session.commit()
    remover_imagem(imagem)

    flash("Produto excluído com sucesso!", "sucesso")
    return redirect(url_for("main.index"))
