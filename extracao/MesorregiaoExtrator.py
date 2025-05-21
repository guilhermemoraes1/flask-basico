import sqlite3
import requests

# 1 - Conectar ao banco
connection = sqlite3.connect('censoescolar.db')
cursor = connection.cursor()

# 2 - Criar a tabela (se necessário)
with open('schemas/mesorregioes.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

# 3 - Buscar os dados da API
url = "https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes"
response = requests.get(url)

if response.status_code == 200:
    mesorregioes = response.json()

    for meso in mesorregioes:
        try:
            co_mesorregiao = meso["id"]
            no_mesorregiao = meso["nome"]

            uf = meso["UF"]
            co_uf = uf["id"]
            sg_uf = uf["sigla"]
            no_uf = uf["nome"]

            regiao = uf["regiao"]
            co_regiao = regiao["id"]
            sg_regiao = regiao["sigla"]
            no_regiao = regiao["nome"]

            cursor.execute('''
                INSERT OR REPLACE INTO tb_mesorregiao (
                    co_mesorregiao, no_mesorregiao,
                    co_uf, sg_uf, no_uf,
                    co_regiao, sg_regiao, no_regiao
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                co_mesorregiao, no_mesorregiao,
                co_uf, sg_uf, no_uf,
                co_regiao, sg_regiao, no_regiao
            ))

        except Exception as e:
            print(f"Erro ao inserir mesorregião: {e}")
else:
    print(f"Erro ao acessar a API. Código HTTP: {response.status_code}")

# 4 - Finalizar
connection.commit()
connection.close()

print("Mesorregiões inseridas com sucesso.")
