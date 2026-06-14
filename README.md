# Pipeline BigQuery + Python

## Descrição do Projeto

Este projeto foi desenvolvido como atividade prática da EBAC com o objetivo de aplicar consultas SQL no Google BigQuery utilizando Python, automatizar a extração de dados, realizar tratamentos e validações básicas de qualidade e exportar os resultados em formatos adequados para análise posterior.

O pipeline realiza consultas em uma base pública de COVID-19, processa os dados utilizando Pandas e gera arquivos finais em CSV e Parquet.

---

## Objetivos

* Conectar Python ao Google BigQuery.
* Executar consultas SQL de forma programática.
* Carregar resultados em DataFrames Pandas.
* Aplicar limpeza e padronização dos dados.
* Validar a qualidade das informações extraídas.
* Exportar resultados em CSV e Parquet.
* Organizar um pipeline reutilizável para futuras análises.

---

## Tecnologias Utilizadas

* Python 3.12
* Google BigQuery
* Pandas
* Google Cloud SDK
* PyArrow
* VS Code
* Git e GitHub

---

## Base de Dados Utilizada

Tabela:

```sql
covid_19_geographic_distribution_worldwide
```

Projeto utilizado:

```text
curso-ebac-498816
```

A base contém informações históricas relacionadas à pandemia de COVID-19, incluindo registros de casos confirmados e óbitos por país ao longo do tempo.

---

## Estrutura do Projeto

```text
atividade_bigquery_python/
│
├── pipeline_bigquery_python.py
│
├── output/
│   ├── csv/
│   │   ├── top20_paises_covid.csv
│   │   └── serie_temporal_covid_brasil.csv
│   │
│   └── parquet/
│       ├── top20_paises_covid.parquet
│       └── serie_temporal_covid_brasil.parquet
```

---

## Consultas Desenvolvidas

### Query 1 - Validação da Conexão

Consulta simples utilizada para validar a comunicação entre Python e BigQuery.

### Query 2 - Top 20 Países por Casos Confirmados

Objetivo:

Identificar os países com maior número acumulado de casos confirmados registrados na base de dados.

### Query 3 - Série Temporal do Brasil

Objetivo:

Extrair a evolução temporal dos casos confirmados de COVID-19 para o Brasil.

---

## Tratamentos Aplicados

Durante o processamento dos dados foram realizados:

* Padronização dos nomes das colunas.
* Conversão de tipos de dados.
* Conversão de datas.
* Tratamento de valores inválidos.
* Remoção de registros inconsistentes.
* Organização dos dados para análise.

---

## Validações Realizadas

Foram implementadas validações mínimas para garantir a qualidade dos dados:

* Verificação de schema.
* Verificação de tipos de dados.
* Identificação de valores nulos.
* Verificação de registros duplicados.
* Validação de consistência dos dados numéricos.

---

## Arquivos Gerados

### CSV

* top20_paises_covid.csv
* serie_temporal_covid_brasil.csv

### Parquet

* top20_paises_covid.parquet
* serie_temporal_covid_brasil.parquet

---

## Como Executar

Instalar dependências:

```bash
pip install pandas google-cloud-bigquery db-dtypes google-cloud-bigquery-storage pyarrow
```

Executar o pipeline:

```bash
python pipeline_bigquery_python.py
```

---

## Autor

João Euzébio

Projeto desenvolvido como atividade prática da EBAC para aplicação de BigQuery, SQL Analítico e Engenharia de Dados com Python.
