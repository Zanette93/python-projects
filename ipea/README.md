## Análise de Homicídios no Brasil: ETL e Visualização de Dados

Este repositório contém dois scripts Python que juntos realizam a extração, transformação, carregamento (ETL) e a visualização de dados sobre homicídios no Brasil. O objetivo é analisar a evolução das taxas de homicídios por diferentes tipos, bem como identificar tendências e padrões ao longo dos anos.

### Estrutura do Repositório

* **dados_homicidios e dados_taxa_estados**: Pastas contendo os arquivos csv utilizados no tratamento dos dados.
* **dados_etl.py**: Script responsável pelo processo ETL dos dados.
* **dados_vis.py**: Script responsável pela visualização e análise dos dados tratados.
* **dados_etl.ipynb e * **dados_vis.ipynb****: Script para serem usados em notebooks.
* **README.md**: Este arquivo, que descreve o projeto e as funcionalidades dos scripts.
* **database.db**: Base de dados criada ao rodar o programa, pode ser utilzada para diferentes pesquisas.

### dados_etl.py

Este script extrai dados de arquivos CSV sobre homicídios e taxas de homicídios, realiza o tratamento dos dados, combinando-os em um único DataFrame e, finalmente, salva os dados tratados em um arquivo CSV e em um banco de dados SQLite.

#### Funcionalidades:

1. **Importação de Bibliotecas**: Importa as bibliotecas necessárias para a manipulação de dados e a conexão com o banco de dados.
2. **Definição de Dicionários**: Define dicionários para mapear regiões e estados do Brasil.
3. **Importação e Tratamento de Dados**: Define funções para importar dados de homicídios e taxas de homicídios a partir de arquivos CSV.
4. **Carregamento de Arquivos**: Lista os arquivos CSV que contém os dados nas pastas definidas.
5. **Compilação de DataFrames**: Importa e concatena os DataFrames de homicídios e taxas.
6. **Ajustar Estrutura dos DataFrames**: Ajusta a estrutura dos DataFrames para facilitar a análise, criando colunas para o tipo de homicídio e seus valores.
7. **Combinar DataFrames**: Combina os DataFrames de homicídios e taxas em um único DataFrame.
8. **Adicionar Coluna de Região**: Adiciona uma coluna "Região" ao DataFrame, utilizando o dicionário definido para mapear os estados para suas respectivas regiões.
9. **Salvar Dados**: Salva o DataFrame em um arquivo CSV e em uma tabela no banco de dados SQLite.
10. **Análise de Dados**: Realiza uma análise básica dos dados, incluindo verificação de valores nulos, estatísticas descritivas e informações sobre o DataFrame.

### dados_vis.py

Este script realiza a visualização e análise dos dados tratados. Ele plota gráficos para comparar a evolução da taxa de homicídios por região e estado ao longo dos anos, identifica as regiões e estados com as maiores e menores taxas de homicídios e calcula a taxa de homicídios por hora no Brasil.

#### Funcionalidades:

1. **Importação de Bibliotecas**: Importa as bibliotecas necessárias para a visualização de dados.
2. **Carregar Dados**: Carrega os dados do arquivo CSV tratado.
3. **Plotar Gráficos**: Define funções para plotar gráficos que mostram a taxa de homicídios por estado e região ao longo dos anos, com destaque para o ano de 2022. Para plotar gráficos com diferentes tipos de homicídios deve-se atentar ao offset que definem os parâmetros usados nos rótulos de dados dos gráficos, cuidando para eles não se sobreporem.
4. **Análise de Estatísticas**: Realiza cálculos e exibe estatísticas sobre os tipos de homicídios, incluindo as regiões e estados com as maiores e menores taxas.
5. **Análise da Evolução**: Analisa a evolução das taxas de homicídios entre os anos de 2004 e 2022, destacando o impacto do Estatuto do Desarmamento.
6. **Aumentos Significativos**: Identifica os aumentos mais significativos nas taxas de homicídios desde 2004.

### Utilização

1. **Clonar o Repositório**: Clone este repositório para seu ambiente de trabalho.
2. **Instalar as Dependências**: Execute o comando `pip install -r requirements.txt` para instalar as bibliotecas necessárias.
3. **Executar os Scripts**: Execute os scripts `dados_etl.py` e `dados_vis.py` na ordem para realizar a análise dos dados.

### Resultados 

Após a execução dos scripts, você terá:

* Um arquivo CSV chamado `homicidios.csv` com os dados tratados.
* Um banco de dados SQLite chamado `database.db` contendo a tabela `homicidios`.
* Diversos gráficos com a visualização da taxa de homicídios por estado e região:
O primeiro objetivo deste trabalho foi avaliar as taxas de homicídios e homicídios por armas de fogo e tentar entender se o estatuto do desarmamento (Lei nº 10.826, de 22 de dezembro de 2003) foi eficaz na sua redução.
Após avaliar minuciosamente os gráficos e os resultados nota-se que a taxa aumentou em aproximadamente metade dos estados (especialmente Norte e Nordeste) e reduziu na outra metade (Sul e Sudeste). A única comprovação que esses dados fornecem é que as armas de fogo ainda são o método mais utilizado para se cometer homicídios no Brasil. Então quais as causas dos homicídios no Brasil? Porque a diferença tão grande entre as diferentes regiões?

* Resultados da análise estatística e da evolução das taxas de homicídios:
Segundo a ONU (Organização das Nações Unidas) a taxa aceitável para uma Segurança Pública eficaz é de 10 homicídios a cada 100 mil habitantes, sendo assim somente São Paulo e Santa Catarina atenderam esse indicador em 2022.
Foi então que surgiu a ideia de avaliar os maiores aumentos das taxas entre os anos e buscar matérias que os explicassem pois sabendo os motivos ficaria mais fácil a compreensão do problema e encontrar soluções, pois em muitos estados a taxa aceitável de 10 homicidios por 100 mil habitantes foi um aumento que ocorreu em um intervalo de 1 ano!

Separando as 5 maiores (optei por esse intervalo para não sobrecarregar o trabalho com informações e também pois as 5 maiores diferenças ocorreram após 2016, facilitando a pesquisa) observa-se que todos estados se encontram nas regiões Norte e Nordeste e que 4 desses aumentos está ligado ao tráfico e disputa de facções por territórios conforme disponível abaixo:

1: Roraima 2018: Guerra entre facções Primeiro Comando Capital (PCC) e Comando Vermelho(CV) criminosas rivais que disputam o controle do tráfico de drogas no estado
[Link para matéria](https://g1.globo.com/rr/roraima/noticia/2019/02/27/roraima-e-o-estado-com-maior-numero-de-mortes-violentas-no-brasil-em-2018.ghtml)

2: Ceara 2017: Guerra entre facções Comando Vermelho e Guardiões do Estado [Link para matéria](https://diariodonordeste.verdesmares.com.br/seguranca/guerra-entre-faccao-local-e-comando-vermelho-e-motivada-pelo-trafico-1.1886687)

3/4: Acre 2016/2017: Brigas entre facções Comando Vermelho e PCC e por territórios [Link para matéria](https://www.bbc.com/portuguese/brasil-42783116#:~:text=Guerra%20de%20fac%C3%A7%C3%B5es%20torna%20Rio%20Branco%2C%20no%20Acre%2C,dos%20Estados%20que%20mais%20aprisionam%20no%20pa%C3%ADs%20)

5: Ceara 2020: motim dos policiais militares. Durante os 13 dias da greve policial, houve 312 homicídios, uma média de 26 por dia. [Link para matéria](https://g1.globo.com/ce/ceara/noticia/2021/02/12/ceara-e-o-estado-com-maior-aumento-dos-homicidios-em-2020.ghtml)

Isso se relaciona diretamente com outro trabalho disponível em meu portfólio que foi feito em EXCEL onde o foco é avaliar a desigualdade socioeconômica entre as diferentes regiões no Brasil. 

Os dados sobre homicídios no Brasil demonstram uma situação grave, com disparidades regionais e diversos desafios a serem enfrentados. As ações para combater a violência devem ser multidimensionais, incluindo o combate ao crime organizado, ao tráfico de drogas, investimentos em segurança pública, a promoção de políticas sociais que combatam as raízes da criminalidade e principalmente que minimizem a desigualdade social no país.


### Considerações

* O código assume que os arquivos CSV com os dados de homicídios e taxas estão localizados nas pastas definidas nos scripts.
* As pastas e nomes de arquivo podem ser modificados de acordo com a organização dos seus dados.
* O código pode ser expandido para incluir mais tipos de homicídios e realizar análises mais complexas.

### Próximos Passos

* Explorar diferentes métodos de visualização de dados para apresentar os resultados de forma mais eficiente.
* Realizar análises mais aprofundadas, incluindo correlações com outros fatores socioeconômicos.
* Criar um dashboard interativo para facilitar a exploração dos dados. 