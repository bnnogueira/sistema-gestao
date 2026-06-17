from flask import Flask, render_template
import banco

# Cria a aplicação Flask
# __name__ diz ao Flask qual é o arquivo principal
app = Flask(__name__)

# Garante que as tabelas existam ao iniciar sistema
banco.criar_tabelas()

# --------------
# PÁGINA INICIAL
# --------------

@app.route("/")
def index():
    """
    Rota principal - página inicial do sistema.
    @app.route("/") significa: Quando o usuário acessar http://localhost:5000/, execute esta função
    """
    return render_template("index.html")

# --------------------
# CADASTRO DE PRODUTOS
# --------------------
@app.route("/produtos")
def produtos():
    # Exibe a lista de produtos cadastrados
    lista = banco.listar_produtos()
    return render_template("produtos.html", produtos = lista)
    # produtos = lista -> envia a lista para o html usar

@app.route("/produtos/cadastrar", methods=["POST"])
def cadastrar_produto():
    # Recebe os dados do formulário e salva no banco.
    # methods=["POST"] -> essa rota só aceita envio de formulário
    nome = request.form["nome"]
    preco = float(request.form["preco"])
    estoque = int(request.form["estoque"])
    # request.form -> acessa os dados enviados pelo formulário html

    banco.cadastrar_produto(nome, preco, estoque)
    return redirect(url_for("produtos"))
    # redirect -> redirecione para outra página após salvar
    # url_for("produtos") -> gera o endereço da função produtos()

@app.route("/produtos/editar/<int:id>")
def editar_produto(id):
    # Exibe o formulário preenchido com os dados do produto para edição.
    # <int:id> -> captura o id da URL, ex: /produtos/editar/3
    produto = banco.buscar_produto_por_id(id)
    return render_template("produtos.html", produto=produto, produto=banco.listar_produtos())

@app.route("/produtos/atualizar", methods=["POST"])
def atualizar_produto():
    # Recebe os dados editados e salva no banco.
    id = int(request.form["id"])
    nome = request.form["nome"]
    preco = float(request.form["preco"])
    estoque = int(request.form["estoque"])

    banco.atualizar_produto(id, nome, preco, estoque)
    return redirect(url_for("produtos"))
   
@app.route("/produtos/deletar/<int:id>")
def deletar_produto(id):
    # Remove um produto pelo id.
    banco.deletar_produto(id)
    return redirect(url_for("produtos"))

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
    # debug=True -> mostra erros detalhados no navegador e reinicia o servidor automaticamente ao salvar o arquivo