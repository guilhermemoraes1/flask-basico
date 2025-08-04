from flask import request
from helpers.application import app
from helpers.logging import logger
from helpers.CORS import cors
from helpers.database import db
from models.InstituicaoEnsino import InstituicaoEnsino
from flask import jsonify

from resources.sqlQuery import consulta_por_estado, consulta_por_municipio

cors.init_app(app)

@app.get("/dados/escolas")
def dados_escolas():
    try:
        pagina = request.args.get("page", default=1, type=int)
        por_pagina = request.args.get("per_page", default=20, type=int)

        # Obtem o valor real do ano mais recente
        ano_mais_recente = db.session.query(
            db.func.max(InstituicaoEnsino.ano)
        ).scalar()

        query = db.session.query(
            InstituicaoEnsino.no_entidade.label("escola"),
            InstituicaoEnsino.no_municipio.label("municipio"),
            InstituicaoEnsino.no_microrregiao.label("microrregiao"),
            InstituicaoEnsino.no_mesorregiao.label("mesorregiao"),
            InstituicaoEnsino.sg_uf.label("uf")
        ).filter(InstituicaoEnsino.ano == ano_mais_recente)

        total = query.count()
        result = query.offset((pagina - 1) * por_pagina).limit(por_pagina).all()

        return jsonify({
            "pagina": pagina,
            "escolas_Por_Pagina": por_pagina,
            "total_de_Paginas": (total + por_pagina - 1) // por_pagina,
            "total_de_Escolas": total,
            "data": [
                {
                    "Escola": row.escola,
                    "Municipio": row.municipio,
                    "Microrregiao": row.microrregiao,
                    "Mesorregiao": row.mesorregiao,
                    "Estado": row.uf
                }
                for row in result
            ]
        })

    except Exception as e:
        logger.error(f"Erro ao buscar dados das escolas: {e}")
        return jsonify({"mensagem": f"Erro ao acessar os dados: {str(e)}"}), 500



@app.get("/dados/estados2023")
def dados_por_estado_2023():
    return consulta_por_estado(2023)

@app.get("/dados/estados2024")
def dados_por_estado_2024():
    return consulta_por_estado(2024)

@app.get("/dados/municipios2023")
def dados_por_municipio_2023():
    uf = request.args.get("uf")
    return consulta_por_municipio(2023, uf)

@app.get("/dados/municipios2024")
def dados_por_municipio_2024():
    uf = request.args.get("uf")
    return consulta_por_municipio(2024, uf)
