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

if __name__ == "__main__":
    criar_tabelas()