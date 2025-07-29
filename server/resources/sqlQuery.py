from helpers.database import db
from models.InstituicaoEnsino import InstituicaoEnsino
from flask import jsonify


def consulta_por_estado(ano):
    try:
        result = db.session.query(
            InstituicaoEnsino.sg_uf,
            db.func.sum(InstituicaoEnsino.qt_mat_bas).label("mat_bas")
        ).filter(InstituicaoEnsino.ano == ano).group_by(InstituicaoEnsino.sg_uf).all()

        return jsonify([
            {"sg_uf": row.sg_uf, "mat_bas": row.mat_bas}
            for row in result
        ]), 200

    except Exception as e:
        return jsonify({"mensagem": f"Erro ao acessar os dados: {str(e)}"}), 500


def consulta_por_municipio(ano, uf=None):
    try:
        query = db.session.query(
            InstituicaoEnsino.co_municipio,
            InstituicaoEnsino.no_municipio,
            InstituicaoEnsino.sg_uf,
            db.func.sum(InstituicaoEnsino.qt_mat_bas).label("mat_bas")
        ).filter(InstituicaoEnsino.ano == ano)

        if uf:
            query = query.filter(InstituicaoEnsino.sg_uf == uf)

        result = query.group_by(
            InstituicaoEnsino.co_municipio,
            InstituicaoEnsino.no_municipio,
            InstituicaoEnsino.sg_uf
        ).all()

        return jsonify([
            {
                "co_municipio": row.co_municipio,
                "no_municipio": row.no_municipio,
                "sg_uf": row.sg_uf,
                "mat_bas": row.mat_bas
            } for row in result
        ]), 200

    except Exception as e:
        return jsonify({"mensagem": f"Erro ao acessar os dados: {str(e)}"}), 500
