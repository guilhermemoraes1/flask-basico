import sqlite3
import csv

# 1 - Abrir a conexão
connection = sqlite3.connect('censoescolar.db')

# 2 - Criar o cursor
cursor = connection.cursor()

# 3 - Executar o schema
with open('schemas.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

# 4 - Abrir o arquivo CSV e ler os dados
with open('microdados_filtrados.csv', newline='', encoding='ISO-8859-1') as csvfile:
    reader = csv.reader(csvfile)
    
    # Ignorar o cabeçalho do CSV (se houver)
    next(reader)

    # 5 - Inserir dados no banco de dados
    for row in reader:
        cursor.execute('''
        INSERT INTO tb_instituicao (
            no_regiao, co_regiao, no_uf, sg_uf, co_uf,
            no_municipio, co_municipio, no_mesorregiao, co_mesorregiao,
            no_microrregiao, co_microrregiao, no_entidade, co_entidade,
            qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
            qt_mat_eja, qt_mat_esp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', row)

# 6 - Commit
connection.commit()

# 7 - Fechar a conexão
connection.close()

print("Dados inseridos com sucesso.")
