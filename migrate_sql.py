import sqlite3
import json
import os
import math

def migrate_data():

    db_name = 'censo.db'
    json_file_name = 'censo_escolar.json'

    # Conectar ao banco de dados SQLite
    conn = None
    try:
        if not os.path.exists(db_name):
            raise FileNotFoundError(f"Arquivo de banco de dados '{db_name}' não encontrado. Execute init_db.py primeiro.")

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        print(f"Conectado com sucesso ao banco de dados '{db_name}'.")

        # Leitura do JSON
        if not os.path.exists(json_file_name):
            raise FileNotFoundError(f"Arquivo '{json_file_name}' não encontrado no diretório.")

        with open(json_file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Arquivo '{json_file_name}' lido com sucesso. Total de {len(data)} registros encontrados.")

        # SQL para INSERT
        insert_sql = """
        INSERT INTO instituicoes (
            codEntidade, entidade, regiao, uf, municipio,
            mesoregiao, microregiao, matriculas_base
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        
        records_processed = 0
        records_skipped = 0

        for i, record in enumerate(data):
            try:
                # Limpeza de Dados: Tratar 'NaN' para 'NULL'
                matriculas_base = record.get('matriculas_base')
                if isinstance(matriculas_base, (int, float)) and math.isnan(matriculas_base):
                    matriculas_base = None

                # Verifica se as chaves obrigatórias existem
                if 'codEntidade' not in record or 'entidade' not in record:
                    raise KeyError("Registro não possui as chaves obrigatórias 'codEntidade' ou 'entidade'.")

                # Constrói a tupla de dados
                record_tuple = (
                    record.get('codEntidade'),
                    record.get('entidade'),
                    record.get('regiao'),
                    record.get('uf'),
                    record.get('municipio'),
                    record.get('mesoregiao'),
                    record.get('microregiao'),
                    matriculas_base
                )

                # Executa o INSERT
                cursor.execute(insert_sql, record_tuple)
                
                records_processed += 1

            except (KeyError, ValueError, sqlite3.IntegrityError) as e:
                # A exceção sqlite3.IntegrityError será lançada se houver uma violação de unicidade
                print(f"Erro ao processar o registro {i+1} (codEntidade: {record.get('codEntidade')}): {e}. Pulando registro.")
                records_skipped += 1
                continue

        # Confirmar as alterações no banco de dados
        conn.commit()

        # Confirmação
        print("\n" + "-"*50)
        print("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"Dados do '{json_file_name}' foram migrados para '{db_name}'.")
        print(f"Total de registros processados: {records_processed}")
        print(f"Total de registros pulados: {records_skipped}")
        print("-" * 50)

    except FileNotFoundError as e:
        print(f"Erro de arquivo: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro de decodificação JSON: O arquivo '{json_file_name}' não é um JSON válido. Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if conn:
            conn.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == '__main__':
    migrate_data()
