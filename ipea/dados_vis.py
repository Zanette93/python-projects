# %% (Importa as bibliotecas necessárias)
import pandas as pd
import plotly.graph_objects as go

# %% (Carregar Dados)
# Carrega os dados do arquivo CSV 'homicidios.csv'
df = pd.read_csv('homicidios.csv', sep=';')

df_hom = df[df["Tipo_homicidio"] == 'homicidios']
# %%
def plot_taxa_homicidios_com_menu(df_homicidios, tipo_homicidio, y_label):
    """Plota gráfico interativo da taxa de homicídios por estado ao longo dos anos, com controle por região via menu suspenso."""
    fig = go.Figure()

    # Lista de regiões para o loop
    regioes = df_homicidios['Regiao'].unique()
    
    # Dicionário para armazenar traços por região
    regioes_estados_map = {regiao: [] for regiao in regioes}

    # Adiciona traços individuais para cada estado
    for estado in df_homicidios['UF'].unique():
        df_estado = df_homicidios[df_homicidios['UF'] == estado]
        regiao = df_estado['Regiao'].iloc[0]
        trace = go.Scatter(
            x=df_estado['Ano'], 
            y=df_estado['Taxa_homicidio'],
            mode='lines',
            name=estado,
            showlegend=True,
            visible=True,
            customdata=df_estado['UF']  # Adiciona o estado como dado personalizado para o hover (nested list)
        )
        fig.add_trace(trace)
        regioes_estados_map[regiao].append(trace)

    # Customiza o layout
    fig.update_layout(
        title=f'Taxa de {tipo_homicidio} nos Estados Brasileiros (Controle por Região)',
        xaxis_title='Ano',
        yaxis_title=y_label,
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        legend_title_text='Estados',
        template="plotly_white",
        yaxis_range=[0, df_homicidios['Taxa_homicidio'].max() * 1.1]  # Adiciona 10% de margem no eixo y
    )

    # Adiciona menu suspenso para controle das regiões
    updatemenus = [
        {
            'buttons': [
                {'label': 'Mostrar Todas as Regiões', 'method': 'update', 'args': [{'visible': [True] * len(fig.data)}]},
                {'label': 'Ocultar Todas as Regiões', 'method': 'update', 'args': [{'visible': [False] * len(fig.data)}]},
            ] + [
                {'label': regiao, 'method': 'update', 'args': [
                    {'visible': [trace in regioes_estados_map[regiao] for trace in fig.data]},
                    {'yaxis': {'range': [0, df_homicidios['Taxa_homicidio'].max() * 1.1]}}
                ]} 
                for regiao in regioes
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.17,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top'
        }
    ]
    
    fig.update_layout(updatemenus=updatemenus)

    # Corrige o hovertemplate
    fig.update_traces(
        selector={'type': 'scatter'},
        hovertemplate='UF: %{customdata}<br>Ano: %{x}<br>Taxa de Homicídios: %{y:.2f}'
    )

    # Remove o agrupamento por região para que o clique afete apenas a UF individual
    fig.update_layout(legend=dict(itemclick='toggleothers'))  # Define que o clique na legenda deve esconder as outras UFs
    fig.write_html("taxa_homicidios_interativo.html")
    fig.show()

plot_taxa_homicidios_com_menu(df_hom, 'Homicídios', 'Homicídios por 100 mil habitantes')

# %% (Análise de Estatísticas)
# Define função para analisar estatísticas de homicídios por tipo
def analisar_estatisticas_homicidios(df_homicidios, tipo_homicidio):
    """Calcula e exibe estatísticas de homicídios para um determinado tipo."""
    df_homicidios_tipo = df_homicidios[df_homicidios["Tipo_homicidio"] == tipo_homicidio]
    
    # Quantidade total de homicídios
    df_ano = df_homicidios_tipo.groupby('Ano').sum().reset_index()
    hom_2022 = df_ano["Qtd_homicidio"].iloc[-1]
    
    # Análise para o ano de 2022
    df_homicidios_2022 = df_homicidios_tipo[df_homicidios_tipo["Ano"] == 2022]
    
    # Homicídios por região
    homicidios_regiao_2022 = df_homicidios_2022.groupby('Regiao')['Taxa_homicidio'].mean().reset_index()
    regiao_mais_homicidios = homicidios_regiao_2022.sort_values(by='Taxa_homicidio', ascending=False).iloc[0]
    regiao_menos_homicidios = homicidios_regiao_2022.sort_values(by='Taxa_homicidio').iloc[0]
    
    # Homicídios por estado
    homicidios_estado_2022 = df_homicidios_2022[['UF', 'Taxa_homicidio']].reset_index(drop=True)
    estados_mais_homicidios_2022 = homicidios_estado_2022.sort_values(by='Taxa_homicidio', ascending=False).head(3)
    estados_menos_homicidios_2022 = homicidios_estado_2022.sort_values(by='Taxa_homicidio').head(3)

    return {
        'hom_2022': hom_2022,
        'regiao_mais_homicidios': regiao_mais_homicidios,
        'regiao_menos_homicidios': regiao_menos_homicidios,
        'estados_mais_homicidios_2022': estados_mais_homicidios_2022,
        'estados_menos_homicidios_2022': estados_menos_homicidios_2022
    }

# Define função para analisar homicídios por tipo
def analisar_homicidios_por_tipo(df_homicidios, tipo_homicidio):
    """Exibe estatísticas de homicídios por tipo, como quantidade total, região e estado."""
    estatisticas = analisar_estatisticas_homicidios(df_homicidios, tipo_homicidio)
    
    print(f'Quantidade de {tipo_homicidio} em 2022: {round(estatisticas["hom_2022"])}\n')
    
    hom_hora = estatisticas["hom_2022"] / (365 * 24)
    print(f'{tipo_homicidio.capitalize()} por hora no Brasil em 2022: {round(hom_hora, 1)}\n')
    
    print(f"Região com maior taxa de {tipo_homicidio} em 2022: {estatisticas['regiao_mais_homicidios']['Regiao']}, Média da taxa de {tipo_homicidio} a cada 100 mil habitantes em 2022: {estatisticas['regiao_mais_homicidios']['Taxa_homicidio']:.2f}")
    print(f"Região com menor taxa de {tipo_homicidio} em 2022: {estatisticas['regiao_menos_homicidios']['Regiao']}, Média da taxa de {tipo_homicidio} a cada 100 mil habitantes em 2022: {estatisticas['regiao_menos_homicidios']['Taxa_homicidio']:.2f}")

    print(f"\nTop 3 estados com maior taxa de {tipo_homicidio} em 2022:")
    for index, row in estatisticas['estados_mais_homicidios_2022'].iterrows():
        print(f"Estado: {row['UF']}, {tipo_homicidio} por 100 mil habitantes: {row['Taxa_homicidio']:.2f}")

    print(f"\nTop 3 estados com menor taxa de {tipo_homicidio} em 2022:")
    for index, row in estatisticas['estados_menos_homicidios_2022'].iterrows():
        print(f"Estado: {row['UF']}, {tipo_homicidio.capitalize()} por 100 mil habitantes: {row['Taxa_homicidio']:.2f}")
    print('\n')

# Analisa estatísticas de "Homicídios"
analisar_homicidios_por_tipo(df, 'homicidios')

# Analisa estatísticas de "Homicídios por Armas de Fogo"
analisar_homicidios_por_tipo(df, 'homicidios_por_armas_de_fogo')

# %% (Análise da Evolução)
# Define função para analisar a evolução da taxa de homicídios
def analisar_evolucao_homicidios_2004_2022(df_homicidios, tipo_homicidio):
    """Analisa a evolução da taxa de homicídios entre 2004 e 2022."""
    # Filtrar os dados para o tipo de homicídio desejado
    df_hom_tipo = df_homicidios[df_homicidios["Tipo_homicidio"] == tipo_homicidio]
    
    # Filtrar os dados para os anos de 2004 e 2022
    df_hom_2004 = df_hom_tipo[df_hom_tipo["Ano"] == 2004].copy()
    df_hom_2022 = df_hom_tipo[df_hom_tipo["Ano"] == 2022].copy()

    # Obter as taxas de homicídio por UF para 2004 e 2022
    taxas_2004 = df_hom_2004[['Regiao', 'UF', 'Taxa_homicidio']].set_index('UF')
    taxas_2022 = df_hom_2022[['Regiao', 'UF', 'Taxa_homicidio']].set_index('UF')

    # Alinhar os índices e calcular a diferença
    df_dif_taxas = (taxas_2022['Taxa_homicidio'] - taxas_2004['Taxa_homicidio']).reset_index().rename(columns={"Taxa_homicidio": f"Evolução da taxa de {tipo_homicidio} entre 2004 e 2022"})

    # Exibir a evolução das taxas
    print(df_dif_taxas)

    # Contar valores negativos e positivos
    negativos = (df_dif_taxas[f'Evolução da taxa de {tipo_homicidio} entre 2004 e 2022'] < 0).sum()
    positivos = (df_dif_taxas[f'Evolução da taxa de {tipo_homicidio} entre 2004 e 2022'] > 0).sum()

    print('\n')
    print(f"Quantidade de Estados onde a taxa de {tipo_homicidio} reduziu após o Estatuto do Desarmamento: {negativos}")
    print(f"Quantidade de Estados onde a taxa de {tipo_homicidio} aumentou após o Estatuto do Desarmamento: {positivos}")
    print('\n')

# Analisa a evolução da taxa de homicídios
analisar_evolucao_homicidios_2004_2022(df, 'homicidios')

# Analisa a evolução da taxa de homicídios por armas de fogo
analisar_evolucao_homicidios_2004_2022(df, 'homicidios_por_armas_de_fogo')

# %% (Aumentos Significativos)
# Define função para analisar aumentos significativos nas taxas de homicídios
def analisar_aumentos_significativos(df_homicidios, tipo_homicidio):
    """Identifica os aumentos mais significativos nas taxas de homicídios desde 2004."""
    df_hom_estatuto = df_homicidios[df_homicidios["Ano"] >= 2004].copy()
    df_hom_estatuto['Diferença'] = df_hom_estatuto.groupby('UF')['Taxa_homicidio'].diff()
    maiores_diferencas = df_hom_estatuto.dropna(subset=['Diferença']).sort_values(by='Diferença', ascending=False)
    top10_aumentos = maiores_diferencas.head(10).reset_index(drop=True)

    return top10_aumentos[['UF', 'Ano', 'Diferença']]

# Analisa aumentos significativos em "Homicídios"
df_hom = df[df["Tipo_homicidio"] == 'homicidios']
aumentos_significativos = analisar_aumentos_significativos(df_hom, 'homicidios')

print(f"Aumentos mais significativos nos números de homicídios desde 2004: \n\n{aumentos_significativos}")
# %% (Conclusões)

print("Leia o arquivo README.md para acessar os objetivos, explicações e conclusões do estudo")
