from flask import request, jsonify, g
import sqlite3
from marshmallow import ValidationError

from helpers.application import app
from helpers.database import getConnection
from helpers.logging import logger
from helpers.CORS import cors

from models.InstituicaoEnsino import InstituicaoEnsino

cors.init_app(app)

@app.route("/")
def index():
    versao = {"path": "/instituicoes"}
    return jsonify(versao), 200

@app.get("/instituicoes")
def instituicoesResource():
    logger.info("Get - Instituições")

    try:
        instituicoesEnsino = []

        cursor = getConnection().cursor()
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

    return jsonify(instituicoesEnsino), 200


@app.post("/instituicoes")
def instituicaoInsercaoResource():
    logger.info("Post - Instituições")
    instituicaoJson = request.get_json()

    co_regiao = int(instituicaoJson["co_regiao"])
    sg_uf = instituicaoJson["sg_uf"]
    co_uf = int(instituicaoJson["co_uf"])
    co_municipio = int(instituicaoJson["co_municipio"])
    co_mesorregiao = int(instituicaoJson["co_mesorregiao"])
    co_microrregiao = int(instituicaoJson["co_microrregiao"])
    no_entidade = instituicaoJson["no_entidade"]
    co_entidade = int(instituicaoJson["co_entidade"])
    qt_mat_bas = int(instituicaoJson["qt_mat_bas"])
    qt_mat_inf = int(instituicaoJson["qt_mat_inf"])
    qt_mat_fund = int(instituicaoJson["qt_mat_fund"])
    qt_mat_med = int(instituicaoJson["qt_mat_med"])
    qt_mat_eja = int(instituicaoJson["qt_mat_eja"])
    qt_mat_esp = int(instituicaoJson["qt_mat_esp"])


    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tb_instituicao (
        co_regiao, no_uf, sg_uf, co_uf,
        co_municipio, co_mesorregiao,
        co_microrregiao, no_entidade, co_entidade,
        qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
        qt_mat_eja, qt_mat_esp
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
    int(instituicaoJson["co_regiao"]),
    int(instituicaoJson["co_uf"]),
    int(instituicaoJson["co_municipio"]),
    int(instituicaoJson["co_mesorregiao"]),
    int(instituicaoJson["co_microrregiao"]),
    instituicaoJson["no_entidade"], int(instituicaoJson["co_entidade"]),
    int(instituicaoJson["qt_mat_bas"]), int(instituicaoJson["qt_mat_inf"]),
    int(instituicaoJson["qt_mat_fund"]), int(instituicaoJson["qt_mat_med"]),
    int(instituicaoJson["qt_mat_eja"]), int(instituicaoJson["qt_mat_esp"])
    ))

    conn.commit()

    id = cursor.lastrowid

    instituicaoEnsino = InstituicaoEnsino(
        id,
        co_regiao, sg_uf, co_uf,
        co_municipio, co_mesorregiao,
        co_microrregiao, no_entidade, co_entidade,
        qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
        qt_mat_eja, qt_mat_esp
    )

    return jsonify(instituicaoEnsino.toDict()), 200

@app.route("/instituicoes/<int:id>", methods=["DELETE"])
def instituicaoRemocaoResource(id):
    try:
        conn = getConnection()
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


@app.route("/instituicoes/<int:id>", methods=["PUT"])
def instituicaoAtualizacaoResource(id):
    logger.info("Put - Instituições")
    jsonCliente = request.get_json()

    # colocar em lowercase
    instituicaoJson = {}
    for chave, valor in jsonCliente.items():
        instituicaoJson[chave.lower()] = valor
        
    try:
        conn = getConnection()
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE tb_instituicao SET
            co_regiao = ?, sg_uf = ?, co_uf = ?,
            co_municipio = ?, co_mesorregiao = ?,
            co_microrregiao = ?, no_entidade = ?, co_entidade = ?,
            qt_mat_bas = ?, qt_mat_inf = ?, qt_mat_fund = ?, qt_mat_med = ?,
            qt_mat_eja = ?, qt_mat_esp = ?
        WHERE id = ?
        ''', (
            id,
            int(instituicaoJson["co_regiao"]),
            int(instituicaoJson["co_uf"]),
            int(instituicaoJson["co_municipio"]),
            int(instituicaoJson["co_mesorregiao"]),
            int(instituicaoJson["co_microrregiao"]),
            instituicaoJson["no_entidade"], int(instituicaoJson["co_entidade"]),
            int(instituicaoJson["qt_mat_bas"]), int(instituicaoJson["qt_mat_inf"]),
            int(instituicaoJson["qt_mat_fund"]), int(instituicaoJson["qt_mat_med"]),
            int(instituicaoJson["qt_mat_eja"]), int(instituicaoJson["qt_mat_esp"])
            
        ))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"mensagem": "Instituição não encontrada"}), 404

        instituicaoAtualizada = InstituicaoEnsino(
            id,
            int(instituicaoJson["co_regiao"]),
            int(instituicaoJson["co_uf"]),
            int(instituicaoJson["co_municipio"]),
            int(instituicaoJson["co_mesorregiao"]),
            int(instituicaoJson["co_microrregiao"]),
            instituicaoJson["no_entidade"], int(instituicaoJson["co_entidade"]),
            int(instituicaoJson["qt_mat_bas"]), int(instituicaoJson["qt_mat_inf"]),
            int(instituicaoJson["qt_mat_fund"]), int(instituicaoJson["qt_mat_med"]),
            int(instituicaoJson["qt_mat_eja"]), int(instituicaoJson["qt_mat_esp"])
        )

        return jsonify(instituicaoAtualizada.toDict()), 200

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Erro no banco de dados"}), 500


@app.route("/instituicoes/<int:id>", methods=["GET"])
def instituicoesByIdResource(id):
    try:
        cursor = getConnection().cursor()
        cursor.execute(
            'SELECT * FROM tb_instituicao WHERE id = ?', (id, ))
        row = cursor.fetchone()
        
        instituicaoEnsino = InstituicaoEnsino(*row)

    except sqlite3.Error as e:
        return jsonify({"mensagem": "Problema com o banco de dados."}), 500

    return jsonify(instituicaoEnsino.toDict()), 200
