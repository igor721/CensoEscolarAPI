from flask import Flask, jsonify, request
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


@app.route("/")
def index():
    versao = {"versao": "0.0.1"}
    return jsonify(versao), 200 


@app.route("/instituicoesensino", methods=["GET"])
def instituicoesResource():
    instituicoes = carregar_censo()
    return jsonify(instituicoes), 200


@app.route("/instituicoesensino/<codEntidade>", methods=["GET"])
def instituicoesByResource(codEntidade):
    instituicoes = carregar_censo()
    for inst in instituicoes:
        if str(inst["codEntidade"]) == codEntidade:
            return jsonify(inst), 200
    return jsonify({"erro": "Instituição não encontrada"}), 404


@app.route("/instituicoesensino/<codEntidade>", methods=["DELETE"])
def instituicoesDeleteByResource(codEntidade):
    instituicoes = carregar_censo()
    novo_censo = [inst for inst in instituicoes if str(inst["codEntidade"]) != codEntidade]

    if len(novo_censo) == len(instituicoes):
        return jsonify({"erro": "Instituição não encontrada"}), 404
    
    salvar_censo(novo_censo)
    return jsonify({"mensagem": f"Instituição com o cod {codEntidade} foi removida"}), 200


# ----------- NOVOS ENDPOINTS -----------

# Inserir instituição
@app.route("/instituicoesensino", methods=["POST"])
def instituicoesCreateResource():
    instituicoes = carregar_censo()
    nova_instituicao = request.get_json()

    # validar se já existe
    for inst in instituicoes:
        if str(inst["codEntidade"]) == str(nova_instituicao.get("codEntidade")):
            return jsonify({"erro": "Instituição já existe"}), 400

    instituicoes.append(nova_instituicao)
    salvar_censo(instituicoes)
    return jsonify({"mensagem": "Instituição adicionada com sucesso"}), 201


# Atualizar instituição
@app.route("/instituicoesensino", methods=["PUT"])
def instituicoesUpdateResource():
    instituicoes = carregar_censo()
    dados_atualizados = request.get_json()

    codEntidade = str(dados_atualizados.get("codEntidade"))
    if not codEntidade:
        return jsonify({"erro": "É necessário informar o codEntidade"}), 400

    for i, inst in enumerate(instituicoes):
        if str(inst["codEntidade"]) == codEntidade:
            instituicoes[i] = dados_atualizados
            salvar_censo(instituicoes)
            return jsonify({"mensagem": "Instituição atualizada com sucesso"}), 200

    return jsonify({"erro": "Instituição não encontrada"}), 404
