import psycopg2
import csv

def converter_inteiro(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None  

# 1 - Abrir a conexão
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="censoescolar",
    user="postgres",
    password="1234"
)
cursor = connection.cursor()

# 3 - Executar o schema
with open('schemas/institutos.sql', encoding='utf-8') as f:
    cursor.execute(f.read())
connection.commit()

# 4 - Abrir o arquivo CSV e ler os dados
with open('microdados_filtrados.csv', newline='', encoding='ISO-8859-1') as csvfile:
    reader = csv.DictReader(csvfile)

    campos_esperados = [
        'NO_REGIAO', 'CO_REGIAO',
        'NO_UF', 'SG_UF', 'CO_UF',
        'NO_MUNICIPIO', 'CO_MUNICIPIO',
        'NO_MESORREGIAO', 'CO_MESORREGIAO',
        'NO_MICRORREGIAO', 'CO_MICRORREGIAO',
        'NO_ENTIDADE', 'CO_ENTIDADE',
        'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND',
        'QT_MAT_MED', 'QT_MAT_EJA', 'QT_MAT_ESP'
    ]

    for row in reader:
        try:
            valores = (
                row['NO_REGIAO'],
                converter_inteiro(row['CO_REGIAO']),
                row['NO_UF'],
                row['SG_UF'],
                converter_inteiro(row['CO_UF']),
                row['NO_MUNICIPIO'],
                converter_inteiro(row['CO_MUNICIPIO']),
                row['NO_MESORREGIAO'],
                converter_inteiro(row['CO_MESORREGIAO']),
                row['NO_MICRORREGIAO'],
                converter_inteiro(row['CO_MICRORREGIAO']),
                row['NO_ENTIDADE'],
                converter_inteiro(row['CO_ENTIDADE']),  # <- corrigido aqui
                converter_inteiro(row['QT_MAT_BAS']),
                converter_inteiro(row['QT_MAT_INF']),
                converter_inteiro(row['QT_MAT_FUND']),
                converter_inteiro(row['QT_MAT_MED']),
                converter_inteiro(row['QT_MAT_EJA']),
                converter_inteiro(row['QT_MAT_ESP']),
            )


            cursor.execute('''
                INSERT INTO tb_instituicao (
                    no_regiao, co_regiao,
                    no_uf, sg_uf, co_uf,
                    no_municipio, co_municipio,
                    no_mesorregiao, co_mesorregiao,
                    no_microrregiao, co_microrregiao,
                    no_entidade, co_entidade,
                    qt_mat_bas, qt_mat_inf, qt_mat_fund,
                    qt_mat_med, qt_mat_eja, qt_mat_esp
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', valores)

        except KeyError as e:
            print(f"Coluna ausente no CSV: {e}")
            connection.rollback()
        except Exception as e:
            print(f"Erro ao inserir linha: {e}")
            connection.rollback()

connection.commit()
connection.close()