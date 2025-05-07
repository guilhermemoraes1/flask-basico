from flask import Flask, request, jsonify
import sqlite3

from models.InstituicaoEnsino import InstituicaoEnsino

app = Flask(__name__)

@app.route("/")
def index():
    versao = {"path": "/instituicoes"}
    return jsonify(versao), 200


@app.get("/instituicoes")
def instituicoesResource():
    print("Get - Instituições")

    try:
        instituicoesEnsino = []

        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tb_instituicao')
        resultSet = cursor.fetchall()

        for row in resultSet:

            instituicaoEnsino = InstituicaoEnsino(
                *row 
            )
            instituicoesEnsino.append(instituicaoEnsino.toDict())


    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

    return jsonify(instituicoesEnsino), 200


def validarInstituicao(content):
    isValido = True
    
    if (len(content['no_regiao']) < 3 or content['no_regiao'].isdigit()):
        isValido = False

    if (not (content['co_regiao'].isdigit())):
        isValido = False

    if (len(content['no_uf']) < 3 or content['no_uf'].isdigit()):
        isValido = False

    if (len(content['sg_uf']) < 2 or content['sg_uf'].isdigit()):
        isValido = False

    if (not (content['co_uf'].isdigit() )):
        isValido = False

    if (len(content['no_municipio']) < 3 or content['no_municipio'].isdigit()):
        isValido = False

    if (not (content['co_municipio'].isdigit())):
        isValido = False

    if (len(content['no_mesorregiao']) < 3 or content['no_mesorregiao'].isdigit()):
        isValido = False

    if (not (content['co_mesorregiao'].isdigit())):
        isValido = False

    if (len(content['no_microrregiao']) < 3 or content['no_microrregiao'].isdigit()):
        isValido = False

    if (not (content['co_microrregiao'].isdigit())):
        isValido = False

    if (not (content['qt_mat_bas'].isdigit())):
        isValido = False
    
    if (not (content['qt_mat_inf'].isdigit())):
        isValido = False

    if (not (content['qt_mat_fund'].isdigit())):
        isValido = False

    if (not (content['qt_mat_med'].isdigit())):
        isValido = False

    if (not (content['qt_mat_eja'].isdigit())):
        isValido = False

    if (not (content['qt_mat_esp'].isdigit())):
        isValido = False

    return isValido

@app.post("/instituicoes")
def instituicaoInsercaoResource():
    print("Post - Instituição")
    jsonCliente = request.get_json()

    # colocar em lowercase
    instituicaoJson = {}
    for chave, valor in jsonCliente.items():
        instituicaoJson[chave.lower()] = valor

    print(instituicaoJson)

    isValido = validarInstituicao(instituicaoJson)
    if (isValido):

        no_regiao = instituicaoJson["no_regiao"]
        co_regiao = int(instituicaoJson["co_regiao"])
        no_uf = instituicaoJson["no_uf"]
        sg_uf = instituicaoJson["sg_uf"]
        co_uf = int(instituicaoJson["co_uf"])
        no_municipio = instituicaoJson["no_municipio"]
        co_municipio = int(instituicaoJson["co_municipio"])
        no_mesorregiao = instituicaoJson["no_mesorregiao"]
        co_mesorregiao = int(instituicaoJson["co_mesorregiao"])
        no_microrregiao = instituicaoJson["no_microrregiao"]
        co_microrregiao = int(instituicaoJson["co_microrregiao"])
        no_entidade = instituicaoJson["no_entidade"]
        co_entidade = int(instituicaoJson["co_entidade"])
        qt_mat_bas = int(instituicaoJson["qt_mat_bas"])
        qt_mat_inf = int(instituicaoJson["qt_mat_inf"])
        qt_mat_fund = int(instituicaoJson["qt_mat_fund"])
        qt_mat_med = int(instituicaoJson["qt_mat_med"])
        qt_mat_eja = int(instituicaoJson["qt_mat_eja"])
        qt_mat_esp = int(instituicaoJson["qt_mat_esp"])


        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO tb_instituicao (
            no_regiao, co_regiao, no_uf, sg_uf, co_uf,
            no_municipio, co_municipio, no_mesorregiao, co_mesorregiao,
            no_microrregiao, co_microrregiao, no_entidade, co_entidade,
            qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
            qt_mat_eja, qt_mat_esp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        instituicaoJson["no_regiao"], int(instituicaoJson["co_regiao"]),
        instituicaoJson["no_uf"], instituicaoJson["sg_uf"], int(instituicaoJson["co_uf"]),
        instituicaoJson["no_municipio"], int(instituicaoJson["co_municipio"]),
        instituicaoJson["no_mesorregiao"], int(instituicaoJson["co_mesorregiao"]),
        instituicaoJson["no_microrregiao"], int(instituicaoJson["co_microrregiao"]),
        instituicaoJson["no_entidade"], int(instituicaoJson["co_entidade"]),
        int(instituicaoJson["qt_mat_bas"]), int(instituicaoJson["qt_mat_inf"]),
        int(instituicaoJson["qt_mat_fund"]), int(instituicaoJson["qt_mat_med"]),
        int(instituicaoJson["qt_mat_eja"]), int(instituicaoJson["qt_mat_esp"])
        ))

        conn.commit()

        id = cursor.lastrowid

        instituicaoEnsino = InstituicaoEnsino(
            id,
            no_regiao, co_regiao, no_uf, sg_uf, co_uf,
            no_municipio, co_municipio, no_mesorregiao, co_mesorregiao,
            no_microrregiao, co_microrregiao, no_entidade, co_entidade,
            qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
            qt_mat_eja, qt_mat_esp
        )


        conn.close()

        return jsonify(instituicaoEnsino.toDict()), 200

    return jsonify({"mensagem": "Não cadastrado"}), 406




@app.route("/instituicoes/<int:id>", methods=["PUT"])
def instituicaoAtualizacaoResource(id):
    print("Put - Instituição")
    jsonCliente = request.get_json()

    # colocar em lowercase
    instituicaoJson = {}
    for chave, valor in jsonCliente.items():
        instituicaoJson[chave.lower()] = valor

    print(instituicaoJson)
    isValido = validarInstituicao(instituicaoJson)
    
    if not isValido:
        return jsonify({"mensagem": "Dados inválidos"}), 406

    try:
        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE tb_instituicao SET
            no_regiao = ?, co_regiao = ?, no_uf = ?, sg_uf = ?, co_uf = ?,
            no_municipio = ?, co_municipio = ?, no_mesorregiao = ?, co_mesorregiao = ?,
            no_microrregiao = ?, co_microrregiao = ?, no_entidade = ?, co_entidade = ?,
            qt_mat_bas = ?, qt_mat_inf = ?, qt_mat_fund = ?, qt_mat_med = ?,
            qt_mat_eja = ?, qt_mat_esp = ?
        WHERE id = ?
        ''', (
            instituicaoJson["no_regiao"], int(instituicaoJson["co_regiao"]),
            instituicaoJson["no_uf"], instituicaoJson["sg_uf"], int(instituicaoJson["co_uf"]),
            instituicaoJson["no_municipio"], int(instituicaoJson["co_municipio"]),
            instituicaoJson["no_mesorregiao"], int(instituicaoJson["co_mesorregiao"]),
            instituicaoJson["no_microrregiao"], int(instituicaoJson["co_microrregiao"]),
            instituicaoJson["no_entidade"], int(instituicaoJson["co_entidade"]),
            int(instituicaoJson["qt_mat_bas"]), int(instituicaoJson["qt_mat_inf"]),
            int(instituicaoJson["qt_mat_fund"]), int(instituicaoJson["qt_mat_med"]),
            int(instituicaoJson["qt_mat_eja"]), int(instituicaoJson["qt_mat_esp"]),
            id
        ))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada"}), 404

        instituicaoAtualizada = InstituicaoEnsino(
            id,
            instituicaoJson["no_regiao"], int(instituicaoJson["co_regiao"]),
            instituicaoJson["no_uf"], instituicaoJson["sg_uf"], int(instituicaoJson["co_uf"]),
            instituicaoJson["no_municipio"], int(instituicaoJson["co_municipio"]),
            instituicaoJson["no_mesorregiao"], int(instituicaoJson["co_mesorregiao"]),
            instituicaoJson["no_microrregiao"], int(instituicaoJson["co_microrregiao"]),
            instituicaoJson["no_entidade"], int(instituicaoJson["co_entidade"]),
            int(instituicaoJson["qt_mat_bas"]), int(instituicaoJson["qt_mat_inf"]),
            int(instituicaoJson["qt_mat_fund"]), int(instituicaoJson["qt_mat_med"]),
            int(instituicaoJson["qt_mat_eja"]), int(instituicaoJson["qt_mat_esp"])
        )

        return jsonify(instituicaoAtualizada.toDict()), 200

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Erro no banco de dados"}), 500
    finally:
        conn.close()


@app.route("/instituicoes/<int:id>", methods=["DELETE"])
def instituicaoRemocaoResource(id):
    try:
        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM tb_instituicao WHERE id = ?', (id,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({"mensagem": "Instituição não encontrada."}), 404

        cursor.execute('DELETE FROM tb_instituicao WHERE id = ?', (id,))
        conn.commit()

        conn.close()

        return jsonify({"mensagem": "Instituição removida com sucesso."}), 200

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Erro ao acessar o banco de dados."}), 500


@app.route("/instituicoes/<int:id>", methods=["GET"])
def instituicoesByIdResource(id):
    try:
        conn = sqlite3.connect('censoescolar.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM tb_instituicao WHERE id = ?', (id, ))
        row = cursor.fetchone()
        
        instituicaoEnsino = InstituicaoEnsino(*row)

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500
    finally:
        conn.close()

    return jsonify(instituicaoEnsino.toDict()), 200
