from flask import request
from helpers.application import app
from helpers.logging import logger
from helpers.CORS import cors

from resources.sqlQuery import consulta_por_estado, consulta_por_municipio

cors.init_app(app)

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
