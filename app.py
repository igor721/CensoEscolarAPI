from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

CENSO_ESCOLAR = "censo_escolar.json"

def carregar_censo():
    if os.path.exists(CENSO_ESCOLAR):
        with open(CENSO_ESCOLAR, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def salvar_censo(dados):
    with open(CENSO_ESCOLAR, "w", encoding="utf-8") as file:
        json.dump(dados, file, ensure_ascii=False, indent=2)

@app.get("/")
def index():
    versao = {"versao": "0.0.1"}
    return jsonify(versao), 200

@app.get("/instituicoesensino")
def instituicoesResource():
    instituicoes = carregar_censo()
    return jsonify(instituicoes), 200

@app.get("/instituicoesensino/<codEntidade>")
def instituicoesByResource(codEntidade):
    instituicoes = carregar_censo()
    for inst in instituicoes:
        if str(inst["codEntidade"]) == codEntidade:
            return jsonify(inst), 200
    # Corrigido: retorna erro só depois de percorrer todos
    return jsonify({"erro": "Instituição não encontrada"}), 404

@app.delete("/instituicoesensino/<codEntidade>")
def instituicoesDeleteByResource(codEntidade):
    instituicoes = carregar_censo()
    novo_censo = [inst for inst in instituicoes if str(inst["codEntidade"]) != codEntidade]

    if len(novo_censo) == len(instituicoes):
        return jsonify({"erro": "Instituição não encontrada"}), 404

    salvar_censo(novo_censo)
    return jsonify({"mensagem": f"Instituição com o cod {codEntidade} foi removida"}), 200

if __name__ == "__main__":
    app.run(debug=True)
