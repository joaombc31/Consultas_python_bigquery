"""
PROJETO: Pipeline BigQuery + Python

OBJETIVO:
Executar consultas SQL no BigQuery via Python, carregar os resultados em
DataFrames, aplicar limpeza e padronização, validar a qualidade dos dados
e salvar as bases finais em CSV e Parquet.

DEPENDÊNCIAS UTILIZADAS:
- pandas
- google-cloud-bigquery
- db-dtypes
- google-cloud-bigquery-storage
- pyarrow
- pathlib

BASE UTILIZADA : 
"bigquery-public-data.covid19_ecdc_eu.covid_19_geographic_distribution_worldwide"
copiei essa base para o meu projeto para evitar problemas de acesso e performance, então a tabela utilizada é:
curso-ebac-498816.db_covid19.covid_19_geographic_distribution_worldwide
"""

import pandas as pd
from google.cloud import bigquery
from pathlib import Path

# Projeto Google Cloud
PROJECT_ID = "curso-ebac-498816"

# Tabela utilizada
TABLE = "curso-ebac-498816.db_covid19.covid_19_geographic_distribution_worldwide"

# Pastas de saída
OUTPUT_CSV = Path("output/csv")
OUTPUT_PARQUET = Path("output/parquet")

OUTPUT_CSV.mkdir(parents=True, exist_ok=True)
OUTPUT_PARQUET.mkdir(parents=True, exist_ok=True)

# Conexão com BigQuery
client = bigquery.Client(
    project=PROJECT_ID
)

# Teste de conexão
query_teste = """
SELECT CURRENT_DATE() AS data_hoje
"""

df_teste = client.query(query_teste).to_dataframe()

print("Conexão realizada com sucesso!")
print(df_teste)


# ETAPA 2 - FUNÇÃO PARA EXECUTAR QUERIES NO BIGQUERY
def executar_query(sql):
    """
    Executa uma query SQL no BigQuery e retorna o resultado em um DataFrame.

    Parâmetros:
    sql (str): consulta SQL que será executada no BigQuery.

    Retorno:
    pandas.DataFrame: tabela com o resultado da consulta.
    """

    query_job = client.query(sql)

    df = query_job.to_dataframe()

    return df

"""
Bibliotecas necessárias para executar este pipeline:

- pandas:
  utilizada para manipulação dos dados em formato de DataFrame.

- google-cloud-bigquery:
  utilizada para conectar o Python ao BigQuery e executar queries SQL.

- pathlib:
  utilizada para criar e organizar as pastas de saída dos arquivos CSV e Parquet.

Parâmetros principais:

PROJECT_ID:
  projeto Google Cloud utilizado na execução.

TABLE:
  tabela consultada no BigQuery.

OUTPUT_CSV:
  pasta onde serão salvos os arquivos CSV.

OUTPUT_PARQUET:
  pasta onde serão salvos os arquivos Parquet.
"""

# ETAPA 3 - QUERY TOP 20 PAÍSES POR CASOS CONFIRMADOS
query_top20_paises = f"""
SELECT
    countries_and_territories AS country_region,
    SUM(CAST(daily_confirmed_cases AS INT64)) AS total_confirmed,
    SUM(CAST(daily_deaths AS INT64)) AS total_deaths,
    SUM(CAST(daily_confirmed_cases AS INT64))
        - SUM(CAST(daily_deaths AS INT64)) AS total_recovered_estimate
FROM `{TABLE}`
WHERE countries_and_territories IS NOT NULL
GROUP BY country_region
ORDER BY total_confirmed DESC
LIMIT 20
"""

df_top20_paises = executar_query(query_top20_paises)

print("\nETAPA 3 - TOP 20 PAÍSES POR CASOS CONFIRMADOS")
print(df_top20_paises.head(20))



# ETAPA 4 - QUERY 3 FILTRADA PARA BRAZIL
query_brazil = f"""
SELECT
    date,
    countries_and_territories AS country_region,
    SUM(CAST(daily_confirmed_cases AS INT64)) AS confirmed
FROM `{TABLE}`
WHERE countries_and_territories = 'Brazil'
GROUP BY date, country_region
ORDER BY date
"""

df_brazil = executar_query(query_brazil)

print("\nETAPA 4 - DADOS DO BRASIL(OS 10 PRIMEIROS E ÚLTIMOS REGISTROS)")
print(df_brazil.head(10))
print(df_brazil.tail(10))




# ETAPA 5 - LIMPEZA E PADRONIZAÇÃO DOS DATAFRAMES
# Tratamento do DataFrame Top 20 Países
df_top20_paises.columns = (
    df_top20_paises.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

df_top20_paises["country_region"] = (
    df_top20_paises["country_region"]
    .astype("string")
    .str.strip()
)

df_top20_paises["total_confirmed"] = pd.to_numeric(
    df_top20_paises["total_confirmed"],
    errors="coerce"
).fillna(0).astype("int64")

df_top20_paises["total_deaths"] = pd.to_numeric(
    df_top20_paises["total_deaths"],
    errors="coerce"
).fillna(0).astype("int64")

df_top20_paises["total_recovered_estimate"] = pd.to_numeric(
    df_top20_paises["total_recovered_estimate"],
    errors="coerce"
).fillna(0).astype("int64")

df_top20_paises = df_top20_paises.dropna(
    subset=["country_region"]
)

df_top20_paises = df_top20_paises.sort_values(
    by="total_confirmed",
    ascending=False
).reset_index(drop=True)


# Tratamento do DataFrame Brazil
df_brazil.columns = (
    df_brazil.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

df_brazil["date"] = pd.to_datetime(
    df_brazil["date"],
    errors="coerce"
)

df_brazil["country_region"] = (
    df_brazil["country_region"]
    .astype("string")
    .str.strip()
)

df_brazil["confirmed"] = pd.to_numeric(
    df_brazil["confirmed"],
    errors="coerce"
).fillna(0).astype("int64")

df_brazil = df_brazil.dropna(
    subset=["date", "country_region"]
)

df_brazil = df_brazil.sort_values(
    by="date"
).reset_index(drop=True)


# Visualização após tratamento
print("\nETAPA 5 - DATAFRAME TOP 20 PAÍSES PADRONIZADO")
print(df_top20_paises.head())

print("\nTipos de dados - Top 20 Países")
print(df_top20_paises.dtypes)

print("\nETAPA 5 - DATAFRAME BRAZIL PADRONIZADO")
print(df_brazil.head())

print("\nTipos de dados - Brazil")
print(df_brazil.dtypes)



# ETAPA 6 - VALIDAÇÕES MÍNIMAS DAS BASES EXTRAÍDAS
def validar_base(df, nome_base):
    """
    Executa validações mínimas de qualidade dos dados.

    Validações realizadas:
    - Schema e tipos de dados
    - Quantidade de linhas e colunas
    - Valores nulos por coluna
    - Registros duplicados
    - Consistência de valores numéricos
    """

    print(f"\nETAPA 6 - VALIDAÇÕES MÍNIMAS DA BASE: {nome_base}")

    # Schema / tipos
    print("\nSchema e tipos de dados:")
    print(df.dtypes)

    # Quantidade de registros
    print("\nQuantidade de linhas e colunas:")
    print(df.shape)

    # Valores nulos
    print("\nValores nulos por coluna:")
    print(df.isna().sum())

    # Duplicidades
    print("\nQuantidade de registros duplicados:")
    print(df.duplicated().sum())

    # Consistência dos dados
    print("\nConsistência dos dados (valores negativos):")

    colunas_numericas = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    if len(colunas_numericas) == 0:
        print("Nenhuma coluna numérica encontrada.")

    else:
        for coluna in colunas_numericas:
            qtd_negativos = (df[coluna] < 0).sum()
            print(f"{coluna}: {qtd_negativos}")

    # Amostra
    print("\nAmostra da base:")
    print(df.head())

validar_base(
    df_top20_paises,
    "Top 20 países por casos confirmados"
)

validar_base(
    df_brazil,
    "Query 3 filtrada para Brazil"
)


# ETAPA 7 - SALVAR BASES EM CSV E PARQUET
# Arquivos da base Top 20 Países
top20_csv = OUTPUT_CSV / "top20_paises_covid.csv"
top20_parquet = OUTPUT_PARQUET / "top20_paises_covid.parquet"

df_top20_paises.to_csv(
    top20_csv,
    index=False,
    encoding="utf-8"
)

df_top20_paises.to_parquet(
    top20_parquet,
    index=False
)


# Arquivos da base Brazil
brazil_csv = OUTPUT_CSV / "serie_temporal_covid_brasil.csv"
brazil_parquet = OUTPUT_PARQUET / "serie_temporal_covid_brasil.parquet"

df_brazil.to_csv(
    brazil_csv,
    index=False,
    encoding="utf-8"
)

df_brazil.to_parquet(
    brazil_parquet,
    index=False
)


# Confirmação dos arquivos salvos
print("\nETAPA 7 - ARQUIVOS SALVOS COM SUCESSO")

print(f"CSV Top 20 Países: {top20_csv}")
print(f"Parquet Top 20 Países: {top20_parquet}")

print(f"CSV Brazil: {brazil_csv}")
print(f"Parquet Brazil: {brazil_parquet}")

