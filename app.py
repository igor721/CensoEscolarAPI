from flask import Flask, jsonify, request, abort
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "censo.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

_db_initialized = False

@app.before_request
def setup_db():
    """Inicializa o banco apenas uma vez, na primeira requisição."""
    global _db_initialized
    if not _db_initialized:

        _db_initialized = True

@app.route("/instituicoes", methods=["GET"])
def listar():
    uf = request.args.get("uf")
    municipio = request.args.get("municipio")
    q = request.args.get("q")
    limit = min(request.args.get("limit", 50, type=int), 200)
    offset = request.args.get("offset", 0, type=int)

    query = "SELECT * FROM instituicoes WHERE 1=1"
    params = []
    if uf:
        query += " AND uf = ?"
        params.append(uf.upper())

    conn = get_conn()
    cur = conn.execute(query, params)
    items = [dict(row) for row in cur.fetchall()]
    total = conn.execute("SELECT COUNT(*) FROM instituicoes").fetchone()[0]

    return jsonify({"total": total, "items": items})

@app.route("/instituicoes/<int:codEntidade>", methods=["GET"])
def detalhe(codEntidade):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM instituicoes WHERE codEntidade = ?", (codEntidade,)
    ).fetchone()
    conn.close()
    if not row:
        abort(404)

    res = dict(row)
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)