from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

ARQUIVO_JSON = 'pb_pe_rn.json'

# Carregando os dados do JSON para memória
if os.path.exists(ARQUIVO_JSON):
    with open(ARQUIVO_JSON, 'r', encoding='utf-8') as file:
        instituicoes = json.load(file)

def salvar_json():
    with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
        json.dump(instituicoes, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    versao = {"path": "/instituicoes"}
    return jsonify(versao), 200

@app.route('/instituicoesensino', methods=['GET'])
def instituicoesResource():
    return jsonify(instituicoes), 200

@app.route('/instituicoesensino/<int:co_instituicao>', methods=['GET'])
def recuperar_instituicao(co_instituicao):
    for instituicao in instituicoes:
        if int(instituicao['CO_ENTIDADE']) == co_instituicao:
            return jsonify(instituicao), 200
    return jsonify({'erro': 'Instituição não encontrada'}), 404

@app.route('/instituicoesensino', methods=['POST'])
def instituicaoInsercaoResource():
    nova_instituicao = request.get_json()
    for instituicao in instituicoes:
        if instituicao['CO_ENTIDADE'] == nova_instituicao.get('co_instituicao'):
            return jsonify({'erro': 'Instituição já existe'}), 406
    instituicoes.append(nova_instituicao)
    salvar_json()
    return jsonify({'mensagem': 'Instituição adicionada com sucesso'}), 201

@app.route('/instituicoesensino', methods=['PUT'])
def atualizar_instituicao():
    dados_atualizados = request.get_json()
    for indice, instituicao in enumerate(instituicoes):
        if instituicao['CO_ENTIDADE'] == dados_atualizados.get('CO_ENTIDADE'):
            instituicoes[indice] = dados_atualizados
            salvar_json()
            return jsonify({'mensagem': 'Instituição atualizada com sucesso'}), 200
    return jsonify({'erro': 'Instituição não encontrada'}), 404

@app.route('/instituicoesensino/<int:co_instituicao>', methods=['DELETE'])
def deletar_instituicao(co_instituicao):
    for instituicao in instituicoes:
        if int(instituicao['CO_ENTIDADE']) == co_instituicao:
            instituicoes.remove(instituicao)
            salvar_json()
            return jsonify({'mensagem': 'Instituição removida com sucesso'}), 200
    return jsonify({'erro': 'Instituição não encontrada'}), 404


if __name__ == '__main__':
    app.run()
