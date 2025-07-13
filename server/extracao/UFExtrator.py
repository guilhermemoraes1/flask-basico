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
with open('schemas/estados.sql', encoding='utf-8') as f:
    cursor.execute(f.read())

# 4 - Requisição à API do IBGE
url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
response = requests.get(url)

if response.status_code == 200:
    estados = response.json()

    for estado in estados:
        try:
            co_uf = estado["id"]
            sg_uf = estado["sigla"]
            no_uf = estado["nome"]
            co_regiao = estado["regiao"]["id"]
            no_regiao = estado["regiao"]["nome"]

            cursor.execute('''
                INSERT INTO tb_estado (
                    co_uf, sg_uf, no_uf,
                    co_regiao, no_regiao
                ) VALUES (%s, %s, %s, %s, %s)
            ''', (co_uf, sg_uf, no_uf, co_regiao, no_regiao))

        except KeyError as e:
            print(f"Campo ausente: {e}")
        except Exception as e:
            print(f"Erro ao inserir estado: {e}")
else:
    print(f"Erro ao acessar a API do IBGE. Status code: {response.status_code}")

# 5 - Commit
connection.commit()

# 6 - Fechar a conexão
connection.close()
