from flask import Flask, render_template
import banco

# Cria a aplicação Flask
# __name__ diz ao Flask qual é o arquivo principal
app = Flask(__name__)

# Garante que as tabelas existam ao iniciar sistema
banco.criar_tabelas()

"""
ROTAS (páginas do sistema)
"""

@app.route("/")
def index():
    """
    Rota principal - página inicial do sistema.
    @app.route("/") significa: Quando o usuário acessar http://localhost:5000/, execute esta função
    """
    return render_template("index.html")

# Inicia o servidor Flask
if __name__ == "__main__":
    app.run(debug=True)
    # debug=True -> mostra erros detalhados no navegador e reinicia o servidor automaticamente ao salvar o arquivo