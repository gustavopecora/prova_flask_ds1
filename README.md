# Cadastro de Produtos — Avaliação Final DS1

## 1. Descrição do sistema e tecnologias

Sistema web para cadastro de produtos com categorias, desenvolvido como avaliação final de DS1 (Etec de Itaquera). Os dados agora são **persistidos em banco de dados SQLite** (antes ficavam apenas na memória RAM).

**Funcionalidades**
- Cadastro de produtos (nome, preço, categoria e foto opcional)
- Edição de produtos, com troca de foto (a foto antiga é removida do disco)
- Exclusão de produtos (a foto também é removida do disco, preservando `padrao.png`)
- Busca por nome, com resultados em ordem alfabética
- Relacionamento 1:N: uma **Categoria** possui vários **Produtos**
- Validações: nome com no mínimo 3 caracteres, preço numérico maior que zero, categoria válida e extensão de imagem permitida (`png`, `jpg`, `jpeg`, `gif`)

**Tecnologias**
- Python 3
- Flask
- Flask-SQLAlchemy (ORM) + SQLite
- HTML5, Jinja2 e CSS

**Estrutura de pastas**
```
prova_flask_ds1/
├── app.py              # criação do app, configuração e criação do banco
├── models.py           # tabelas Categoria e Produto (1:N)
├── routes.py           # rotas e validações
├── requirements.txt
├── .gitignore
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   └── editar.html
├── static/
│   ├── css/style.css
│   └── uploads/padrao.png
└── instance/           # (gerada automaticamente) contém o produtos.db
```

## 2. Como rodar o projeto localmente

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/prova_flask_ds1.git
cd prova_flask_ds1

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / macOS

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
python app.py
```

Abra no navegador: <http://127.0.0.1:5000>

O banco de dados (`instance/produtos.db`) e as categorias iniciais (Eletrônicos, Roupas, Alimentos e Livros) são criados **automaticamente** na primeira execução.

## 3. Comandos Git utilizados

```bash
git init
# Inicializa um repositório Git local na pasta do projeto

git add .
# Adiciona todos os arquivos ao stage (o .gitignore evita subir arquivos desnecessários)

git status
# Confere quais arquivos serão incluídos no commit

git commit -m "Entrega final DS1: Flask + SQLAlchemy, CRUD completo e validações"
# Registra o commit com uma mensagem descritiva

git branch -M main
# Renomeia a branch principal para "main"

git remote add origin https://github.com/gustavopecora/prova_flask_ds1.git
# Conecta o repositório local ao repositório remoto criado no GitHub

git push -u origin main
# Envia o commit para o GitHub e define "origin main" como destino padrão
```
