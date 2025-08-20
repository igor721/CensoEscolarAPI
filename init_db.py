import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "censo.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def init_db():
    """
    Inicializa o banco de dados e cria a tabela 'instituicoes'
    lendo o esquema do arquivo schema.sql.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        print("Conectado ao banco de dados para inicialização.")
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            conn.executescript(sql_script)
            print("Esquema do banco de dados criado com sucesso a partir de schema.sql.")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados SQLite durante a inicialização: {e}")
    except FileNotFoundError as e:
        print(f"Erro: Arquivo '{SCHEMA_PATH}' não encontrado. {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a inicialização do banco: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == '__main__':
    init_db()
