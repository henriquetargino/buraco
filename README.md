# 🃏 Dashboard Buraco - Aplicativo com Streamlit

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29%2B-ff69b4.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**Acesse a aplicação ao vivo:** [**https://buraco.streamlit.app**](https://buraco.streamlit.app)

Este aplicativo representa o encontro entre um hobby pessoal e a paixão por dados. Buraco, um jogo de baralho que é um passatempo entre eu e minha mãe, sempre teve seus resultados anotados em papel. Vendo isso como uma oportunidade de automação para nosso dia a dia, desenvolvi esta plataforma do zero. O projeto evoluiu de uma simples folha A4 para uma aplicação de análise de dados completa, com persistência em nuvem via Google Sheets, dashboards em Plotly e uma interface interativa em Streamlit que tornou nosso hobby muito mais competitivo.

![Demo](https://github.com/user-attachments/assets/307496a2-b404-466c-a288-10251d35951f)

## 🎯 Principais Funcionalidades

O aplicativo foi desenvolvido com foco em usabilidade e análise de dados, dividido em três seções principais:

* **📊 Dashboard de Estatísticas Gerais:**
    * Cálculo automático de vitórias, derrotas e percentual de aproveitamento de cada jogador.
    * Métricas detalhadas como maior e menor diferença de pontos em uma vitória.
    * Acompanhamento da maior sequência invicta.
    * Cálculo de médias de pontos, além das pontuações máxima e mínima por partida.
    * Estatísticas avançadas como o dia com mais partidas jogadas e o jogador com mais pontos em um único dia.

* **📈 Visualizações Interativas:**
    * Gráficos de barra comparando o total de pontos e o número de vitórias.
    * Visualização da evolução das vitórias ao longo do tempo, mostrando o desempenho de cada jogador.
    * Gráfico de barras com a diferença de pontos a cada rodada, destacando o vencedor.
    * Tabela com o histórico completo de todas as partidas jogadas.

* **🔐 Adição Segura de Partidas:**
    * Formulário intuitivo para adicionar os resultados de novas partidas.
    * Funcionalidade protegida por senha para garantir a integridade dos dados e que apenas os jogadores possam registrar os pontos.
    * Feedback visual com uma barra de progresso durante o salvamento dos dados.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando um conjunto de bibliotecas modernas de Python para análise e visualização de dados:

* **Frontend:** [Streamlit](https://streamlit.io/) - Para a criação da interface web interativa.
* **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/) - Para toda a estruturação e cálculo das estatísticas.
* **Visualização de Dados:** [Plotly](https://plotly.com/python/) - Para a criação dos gráficos interativos.
* **Banco de Dados:** [Google Sheets](https://www.google.com/sheets/about/) - Utilizado como um banco de dados simples e eficaz para persistir os dados das partidas.
* **API do Google:** [gspread](https://docs.gspread.org/en/latest/) e [gspread-dataframe](https://github.com/robin900/gspread-dataframe) - Para a integração entre a aplicação Python e a planilha do Google.
* **Utilitários:** [pytz](https://pypi.org/project/pytz/) (para fuso horário) e [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu) (para o menu de navegação).

## 🚀 Desafios e Aprendizados

* **Integração com API Externa:** Um dos principais desafios foi configurar a autenticação segura com a API do Google Sheets usando as credenciais de uma conta de serviço, garantindo que as chaves de acesso não ficassem expostas no código (`st.secrets`).
* **Otimização de Performance:** Para garantir uma experiência de usuário fluida, foi implementado o sistema de cache do Streamlit (`@st.cache_data`) para evitar múltiplas requisições à API do Google, o que reduziu drasticamente o tempo de carregamento das páginas.
* **Robustez da Aplicação:** Foi necessário refatorar a lógica de escrita de dados para evitar erros de "conexão expirada" (stale connection), estabelecendo uma nova conexão a cada escrita e limpando o cache para exibir os dados novos instantaneamente.


## 📬 Contato

**Henrique Targino**

* [Linkedin](https://www.linkedin.com/in/henriquetargino/)
* Email: henriquetarginoalbuquerque@gmail.com
