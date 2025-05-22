from flask import Flask, request, jsonify, g
import sqlite3
from marshmallow import Schema, fields, ValidationError

from models.InstituicaoEnsino import InstituicaoEnsino

app = Flask(__name__)

DATABASE = 'censoescolar.db'

@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()

def getConnection():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = sqlite3.connect(DATABASE)
        conn.execute("PRAGMA foreign_keys = ON")
    return conn

class InstituicaoSchema(Schema):
    no_regiao = fields.Str(required=True, error_messages={"required": "Informe o nome da região."})
    co_regiao = fields.Int(required=True, error_messages={"required": "Informe o código da região."})
    sg_uf = fields.Str(required=True, error_messages={"required": "Informe a sigla da UF."})
    co_uf = fields.Int(required=True, error_messages={"required": "Informe o código da UF."})
    no_entidade = fields.Str(required=True, error_messages={"required": "Informe o nome da entidade."})
    co_entidade = fields.Int(required=True, error_messages={"required": "Informe o código da entidade."})
    co_municipio = fields.Int(required=True, error_messages={"required": "Informe o código do município."})
    co_mesorregiao = fields.Int(required=True, error_messages={"required": "Informe o código da mesorregião."})
    co_microrregiao = fields.Int(required=True, error_messages={"required": "Informe o código da microrregião."})
    qt_mat_bas = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para educação básica."})
    qt_mat_inf = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para educação infantil."})
    qt_mat_fund = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para ensino fundamental."})
    qt_mat_med = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para ensino médio."})
    qt_mat_eja = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para EJA."})
    qt_mat_esp = fields.Int(allow_none=True, error_messages={"invalid": "Quantidade inválida para educação especial."})



@app.route("/")
def index():
    versao = {"path": "/instituicoes"}
    return jsonify(versao), 200


@app.get("/instituicoes")
def instituicoesResource():
    print("Get - Instituições")

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
    instituicaoData = request.get_json()
    schema = InstituicaoSchema()

    try:
        instituicaoJson = schema.load(instituicaoData) 
    except ValidationError as err:
        return jsonify({"mensagem": "Erro de validação", "erros": err.messages}), 400
    
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
