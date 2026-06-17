import sqlite3

# Este é o nome do arquivo que vai guardar todos os dados do sistema
NOME_BANCO = "loja.db"

def conectar():
    """
    Abre uma conexão com o banco de dados.
    É como abrir o arquivo loja.db para poder ler ou escrever nele.
    """
    return sqlite3.connect(NOME_BANCO)

def criar_tabelas():
    """
    Cria as tabelas do banco de dados, caso ainda não existam.
    """
    conn = conectar()       # Abre a conexão
    cursor = conn.cursor()  # Cursor é o 'lápis' que escreve no banco

    # Tabela de produtos
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS produtos ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "nome_produto TEXT NOT NULL,"
        "preco REAL NOT NULL,"
        "estoque INTEGER NOT NULL DEFAULT 0"
        ")"
    )
    
    # INTEGER PRIMARY KEY AUTOINCREMENT -> número único gerado automaticamente para cada produto
    # TEXT NOT NULL -> texto obrigatório
    # REAL -> número com casas decimais (para preço)
    # DEFAULT 0 -> se não informar estoque, começa em 0

    # Tabela de vendas
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS vendas ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "produto_id INTEGER NOT NULL,"
        "quantidade INTEGER NOT NULL,"
        "total REAL NOT NULL,"
        "data_venda TEXT NOT NULL,"
        "FOREIGN KEY (produto_id) REFERENCES produtos(id)"
        ")"
    )

    # FOREIGN KEY -> liga cada venda a um produto cadastrado
    # data_venda -> vamos guardar a data como texto no formato AAAA-MM-DD HH:MM:SS

    conn.commit()   # salva as alterações no arquivo
    conn.close()    # fecha a conexão (importante sempre fechar!)
    print("Banco de dados pronto!")

def cadastrar_produto(nome, preco, estoque):
    """
    Insere um novo produto no banco de dados.
    Recebe o nome, preço e estoque como parâmetros.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO produtos(nome_produto, preco, estoque) VALUES (?, ?, ?)",
        (nome, preco, estoque)
    )

    # INSERT INTO -> comando para inserir uma nova linha na tabela
    # VALUES (?, ?, ?) -> os ? são substituídos pelos valores de forma segura
    # Nunca coloque os valores direto na string! Os ? protegem contra ataques

    conn.commit()
    conn.close()

def listar_produtos():
    """
    Retorna todos os produtos cadastrados no banco.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nome_produto, preco, estoque FROM produtos"
    )

    # SELECT -> busca dados do banco
    # Estamos pedindo todas as colunas da tabela produtos

    produtos = cursor.fetchall()
    # fetchall() -> traz todos os resultados de uma vez
    # Cada produto vira uma tupla: (id, nome, preco, estoque)

    conn.close()
    return produtos

def buscar_produto_por_id(id):
    """
    Retorna um único produto pelo seu id.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, nome_produto, preco, estoque FROM produtos WHERE id = ?",
        (id,)
    )
    # WHERE id = ? -> filtra apenas o produto com aquele id

    produto = cursor.fetchone()
    # fetchone() -> traz apenas um resultado

    conn.close()
    return produto

def atualizar_produto(id, nome, preco, estoque):
    """
    Atualiza os dados de um produto existente.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE produtos SET nome_produto = ?, preco = ?, estoque = ? WHERE id = ?",
        (nome, preco, estoque, id)
    )
    # UPDATE -> atualiza uma linha existente
    # SET -> define os novos lugares
    # WHERE id = ? -> garante que só esse produto seja alterado

    conn.commit()
    conn.close()

def deletar_produto(id):
    """
    Remove um produto do banco pelo id.
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM produtos WHERE id = ?",
        (id,)
    )
    # DELETE FROM -> remove a linha da tabela
    # WHERE id = ? -> garante que só esse produto seja removido

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()