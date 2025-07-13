import psycopg2
import requests

# 1 - Abrir a conexão
connection = psycopg2.connect(
        host="localhost",
        port=5432,
        database="censoescolar",
        user="postgres",
        password="1234")

# 2 - Criar o cursor
cursor = connection.cursor()

# 3 - Executar o schema
with open('schemas/municipios.sql', encoding='utf-8') as f:
    cursor.execute(f.read())

# 3 - Obter os dados da API de municípios
url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
response = requests.get(url)

if response.status_code == 200:
    municipios = response.json()

    for municipio in municipios:
        try:
            co_municipio = municipio["id"]
            no_municipio = municipio["nome"]

            microrregiao = municipio["microrregiao"]
            co_microrregiao = microrregiao["id"]
            no_microrregiao = microrregiao["nome"]

            mesorregiao = microrregiao["mesorregiao"]
            co_mesorregiao = mesorregiao["id"]
            no_mesorregiao = mesorregiao["nome"]

            uf = mesorregiao["UF"]
            co_uf = uf["id"]
            sg_uf = uf["sigla"]
            no_uf = uf["nome"]

            regiao = uf["regiao"]
            co_regiao = regiao["id"]
            sg_regiao = regiao["sigla"]
            no_regiao = regiao["nome"]

            # Inserir no banco
            cursor.execute('''
                INSERT INTO tb_municipio (
                    co_municipio, no_municipio,
                    co_microrregiao, no_microrregiao,
                    co_mesorregiao, no_mesorregiao,
                    co_uf, sg_uf, no_uf,
                    co_regiao, sg_regiao, no_regiao
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                co_municipio, no_municipio,
                co_microrregiao, no_microrregiao,
                co_mesorregiao, no_mesorregiao,
                co_uf, sg_uf, no_uf,
                co_regiao, sg_regiao, no_regiao
            ))

        except Exception as e:
            print(f"Erro ao inserir município: {e}")
else:
    print(f"Erro na requisição da API. Status code: {response.status_code}")

# 4 - Commit e fechar
connection.commit()
connection.close()

print("Municípios inseridos com sucesso.")
