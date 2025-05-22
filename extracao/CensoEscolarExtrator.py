import sqlite3
import csv

# 1 - Abrir a conexão
connection = sqlite3.connect('censoescolar.db')

# 2 - Criar o cursor
cursor = connection.cursor()

# 3 - Executar o schema
with open('schemas/institutos.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

# 4 - Abrir o arquivo CSV e ler os dados
with open('pb_pe_rn.csv', newline='', encoding='ISO-8859-1') as csvfile:
    reader = csv.DictReader(csvfile)

    # Campos esperados pela tabela, na ordem correta
    campos_esperados = [
        'CO_REGIAO', 'SG_UF', 'CO_UF',
        'CO_MUNICIPIO', 'CO_MESORREGIAO',
        'CO_MICRORREGIAO', 'NO_ENTIDADE', 'CO_ENTIDADE',
        'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND', 'QT_MAT_MED',
        'QT_MAT_EJA', 'QT_MAT_ESP'
    ]


    # 5 - Inserir dados no banco de dados
    for row in reader:
        try:
            valores = tuple(row[campo] for campo in campos_esperados)
            cursor.execute('''
                INSERT INTO tb_instituicao (
                    co_regiao, sg_uf, co_uf,
                    co_municipio, co_mesorregiao,
                    co_microrregiao, no_entidade, co_entidade,
                    qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                    qt_mat_eja, qt_mat_esp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', valores)
        except KeyError as e:
            print(f"Coluna ausente no CSV: {e}")
        except Exception as e:
            print(f"Erro ao inserir linha: {e}")

# 6 - Commit
connection.commit()

# 7 - Fechar a conexão
connection.close()
