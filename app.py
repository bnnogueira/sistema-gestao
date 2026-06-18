from flask import Flask, render_template, request, redirect, url_for
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
    return render_template("produtos.html", produto=produto, produtos=banco.listar_produtos())

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

# ------------------
# VENDAS
# ------------------
@app.route("/vendas")
def vendas():
    # Exibe o formulário de venda e a lista de vendas realizadas.
    lista_vendas   = banco.listar_vendas()
    lista_produtos = banco.listar_produtos()
    return render_template("vendas.html", vendas=lista_vendas, produtos=lista_produtos)

@app.route("/vendas/registrar", methods=["POST"])
def registrar_venda():
    # Recebe os dados do formulário e registra a venda.
    produto_id = int(request.form["produto_id"])
    quantidade = int(request.form["quantidade"])

    # Busca o preço do produto para calcular o total
    produto = banco.buscar_produto_por_id(produto_id)
    total   = produto[2] * quantidade
    # produto[2] → preço (terceira coluna do SELECT)

    sucesso, mensagem = banco.registrar_venda(produto_id, quantidade, total)
    # A função retorna dois valores:
    # sucesso → True ou False
    # mensagem → texto explicando o resultado

    return redirect(url_for("vendas"))

@app.route("/vendas/cancelar/<int:venda_id>")
def cancelar_venda(venda_id):
    # Cancela uma venda e restaura o estoque.
    banco.cancelar_venda(venda_id)
    return redirect(url_for("vendas"))

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
    # debug=True -> mostra erros detalhados no navegador e reinicia o servidor automaticamente ao salvar o arquivo