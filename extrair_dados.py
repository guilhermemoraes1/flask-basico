import pandas as pd
import json

df = pd.read_csv("microdados_ed_basica_2023.csv", sep=';', encoding="latin1")

df_filtrado = df[df['SG_UF'].isin(['PB', 'PE', 'RN'])]

df_filtrado = df_filtrado.fillna("")

dados_json = df_filtrado.to_dict(orient="records")

with open("dados_PB_PE_RN.json", "w", encoding="utf-8") as f:
    json.dump(dados_json, f, ensure_ascii=False, indent=4)

print("Arquivo JSON criado com sucesso!")
