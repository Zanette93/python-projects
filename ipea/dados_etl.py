# %% (Importa as bibliotecas necessárias)
import pandas as pd
import os
import sqlalchemy

# %% (Definir Dicionários de Regiões e Estados)
# Define dicionário com regiões e seus respectivos estados
regioes_brasil = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}

# Cria dicionário que mapeia cada estado para sua respectiva região
estado_para_regiao = {estado: regiao for regiao, estados in regioes_brasil.items() for estado in estados}

# %% (Importar e Tratar Dados)
# Define função para importar e tratar dados de homicídios
def import_etl_hom(hom: str):
    """Importa e trata dados de homicídios de um arquivo CSV."""
    name_hom = hom.split("/")[-1].split(".")[0]
    name_hom = name_hom.replace("-", "_")

    df = (pd.read_csv(hom, sep=';')
            .drop(columns=["cod"])
            .rename(columns={"nome": "UF",
                             "período": "Ano",
                             "valor": name_hom})
            .set_index(["UF", "Ano"]))
    
    return df

# Define função para importar e tratar dados de taxas
def import_etl_tax(tax: str):
    """Importa e trata dados de taxas de um arquivo CSV."""
    name_tax = tax.split("/")[-1].split(".")[0]
    name_tax = name_tax.replace("-", "_").replace("taxa_de_", "")

    df = (pd.read_csv(tax, sep=';')
            .drop(columns=["cod"])
            .rename(columns={"nome": "UF",
                             "período": "Ano",
                             "valor": name_tax})
            .set_index(["UF", "Ano"]))
    
    return df

# %% (Carregar Arquivos)
# Define os caminhos para as pastas de dados
path_hom = "../ipea/dados_homicidios/"
path_tax = "../ipea/dados_taxa_estados/"

# Lista os arquivos nas pastas
files_hom = os.listdir(path_hom)
files_tax = os.listdir(path_tax)

# %% (Compilar DataFrames)
# Cria listas para armazenar os DataFrames de homicídios e taxas
dfs_hom = []
dfs_tax = []

# Itera sobre os arquivos de homicídios e taxas, importando e adicionando à lista
for i in files_hom:
    dfs_hom.append(import_etl_hom(path_hom + i))
for i in files_tax:
    dfs_tax.append(import_etl_tax(path_tax + i))

# Concatena os DataFrames de homicídios e taxas
df_compilado_hom = pd.concat(dfs_hom, axis=1).reset_index()
df_compilado_hom = df_compilado_hom.set_index(["UF", "Ano"])

df_compilado_tax = pd.concat(dfs_tax, axis=1).reset_index()
df_compilado_tax = df_compilado_tax.set_index(["UF", "Ano"])

# %% (Ajustar Estrutura dos DataFrames)
# Ajusta a estrutura dos DataFrames para facilitar a análise
df_compilado_hom = (df_compilado_hom.stack().reset_index()
                 .rename(columns={"level_2": "Tipo_homicidio",
                                  0: "Qtd_homicidio"}))

df_compilado_tax = (df_compilado_tax.stack().reset_index()
                     .rename(columns={"level_2": "Tipo_homicidio",
                                      0: "Taxa_homicidio"}))

# %% (Combinar DataFrames)
# Combina os DataFrames de homicídios e taxas
df_final = pd.merge(df_compilado_hom, df_compilado_tax, on=["UF", "Ano", "Tipo_homicidio"], how="outer")

# Adiciona coluna 'Regiao' usando o dicionário 'estado_para_regiao'
df_final['Regiao'] = df_final['UF'].map(estado_para_regiao)

# Seleciona as colunas desejadas
df_final = df_final[['Regiao', 'UF', 'Ano', 'Tipo_homicidio', 'Qtd_homicidio', 'Taxa_homicidio']]

# %% (Salvar Dados)
# Salva o DataFrame em um arquivo CSV
df_final.to_csv("../ipea/homicidios.csv", sep=";", index=False)

# Cria conexão com banco de dados SQLite
engine = sqlalchemy.create_engine("sqlite:///../ipea/database.db")

# Salva o DataFrame em uma tabela no banco de dados
df_final.to_sql('homicidios', engine, if_exists='replace', index=False)

# %% (Analisar Dados)
# Exibe informações sobre os valores nulos
df_final.isnull().sum()

# %% (Estatísticas Descritivas)
# Calcula estatísticas descritivas do DataFrame
df_final.describe()

# %% (Informações do DataFrame)
# Exibe informações sobre o DataFrame
df_final.info()