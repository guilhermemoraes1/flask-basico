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
with open('schemas/microrregioes.sql', encoding='utf-8') as f:
    cursor.execute(f.read())

# 3 - Obter os dados da API
url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"
response = requests.get(url)

if response.status_code == 200:
    microrregioes = response.json()

    for micro in microrregioes:
        try:
            co_microrregiao = micro["id"]
            no_microrregiao = micro["nome"]

            meso = micro.get("mesorregiao", {})
            co_mesorregiao = meso.get("id")
            no_mesorregiao = meso.get("nome")

            uf = meso.get("UF", {})
            co_uf = uf.get("id")
            sg_uf = uf.get("sigla")
            no_uf = uf.get("nome")

            regiao = uf.get("regiao", {})
            co_regiao = regiao.get("id")
            sg_regiao = regiao.get("sigla")
            no_regiao = regiao.get("nome")

            cursor.execute('''
                INSERT INTO tb_microrregiao (
                    co_microrregiao, no_microrregiao,
                    co_mesorregiao, no_mesorregiao,
                    co_uf, sg_uf, no_uf,
                    co_regiao, sg_regiao, no_regiao
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                co_microrregiao, no_microrregiao,
                co_mesorregiao, no_mesorregiao,
                co_uf, sg_uf, no_uf,
                co_regiao, sg_regiao, no_regiao
            ))

        except Exception as e:
            print(f"Erro ao inserir microrregião: {e}")
else:
    print(f"Erro ao acessar a API. Código HTTP: {response.status_code}")

# 4 - Finalizar
connection.commit()
connection.close()