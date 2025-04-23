import pandas as pd
import json

def ler_csv_especifico_pandas(caminho_arquivo, filtro_coluna, valor_filtro, colunas_selecionadas):
    df = pd.read_csv(caminho_arquivo, delimiter=';', encoding='ISO-8859-1')
    if filtro_coluna not in df.columns:
        raise KeyError(f"Coluna de filtro '{filtro_coluna}' não encontrada no arquivo CSV.")
    for coluna in colunas_selecionadas:
        if coluna not in df.columns:
            raise KeyError(f"Coluna '{coluna}' não encontrada no arquivo CSV.")
    df_filtrado = df[df[filtro_coluna] == valor_filtro]    
    df_selecionado = df_filtrado[colunas_selecionadas]
    lista_dicionarios_resultado = df_selecionado.to_dict(orient='records')
    return lista_dicionarios_resultado

def salvar_json(lista_dicionarios, caminho_saida):
    with open(caminho_saida, 'w', encoding='utf-8') as json_file:
        json.dump(lista_dicionarios, json_file, ensure_ascii=False, indent=4)
    print(f'Arquivo JSON gerado: {caminho_saida}')

caminho = 'microdados_ed_basica_2024.csv'  
coluna_filtro = 'SG_UF'
valor_filtro = 'PB'

colunas_selecionadas = ['NO_ENTIDADE', 'CO_ENTIDADE','NO_REGIAO', 'CO_UF', 'NO_MUNICIPIO', 'NO_MESORREGIAO', 'NO_MICRORREGIAO', 'QT_MAT_BAS','QT_MAT_INF','QT_MAT_FUND','QT_MAT_FUND_AF','QT_MAT_MED','QT_MAT_PROF','QT_MAT_EJA','QT_MAT_ESP']
dados_encontrados = ler_csv_especifico_pandas(caminho, coluna_filtro, valor_filtro, colunas_selecionadas)

if dados_encontrados:
    salvar_json(dados_encontrados, 'resultado.json')
else:
    print(f'Nenhum dado encontrado para {coluna_filtro} = {valor_filtro}')
