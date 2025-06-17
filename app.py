import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from datetime import datetime
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe # bibliotecas para manipular o Google Sheets
from google.oauth2.service_account import Credentials
import pytz

# layout da página
st.set_page_config(
    page_title="Estatísticas do Buraco",
    page_icon="🃏",
    layout="wide", 
    initial_sidebar_state="expanded",
    menu_items={  # tres pontinhos
        'Get Help': 'mailto:henriquetarginoalbuquerque@gmail.com',
        'Report a bug': 'mailto:henriquetarginoalbuquerque@gmail.com',
        'About': """# Estatísticas Buraco\n\n https://www.linkedin.com/in/henriquetargino/\n\n 
        Esta aplicação foi desenvolvida por Henrique Targino, estudante de Ciência de Dados. \n\n 
        A ideia é acompanhar as estatísticas do jogo de Buraco entre Henrique e Silvana, mantendo um registro das vitórias, derrotas e outras métricas relevantes."""
    }
)

# --- sidebar ---
with st.sidebar:
    pagina = option_menu(
        menu_title="Navegação",
        options=["Estatísticas Gerais", "Dashboard Gráfico", "Adicionar Partida"],
        icons=["bar-chart", "graph-up", "plus-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "10px", "background-color": "#0e1117"},
            "icon": {"color": "#A37500", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "--hover-color": "#e0a000"
            },
            "nav-link-selected": {"background-color": "#FFB700", "color": "white"},
        },
    )


# --- preparação dos dados ---

# dados com cache para evitar múltiplas requisicoes
@st.cache_data(ttl=600) # 10 minutos de cache
def load_data():
    service_account_info = st.secrets["GOOGLE_SERVICE_ACCOUNT"]
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
    gc = gspread.authorize(creds)
    sheet = gc.open("buraco-dados").sheet1
    df = get_as_dataframe(sheet).dropna(how="all")
    return df

df = load_data()

df['pontos'] = pd.to_numeric(df['pontos'], errors='coerce')
df['data'] = pd.to_datetime(df['data'], dayfirst=True)
df = df.sort_values(by='rodada')
rodadas = df.groupby(['rodada'])

vencedores = []
diferencas = []
datas_rodadas = []
for rodada, grupo in rodadas:
    if len(grupo) != 2:
        continue
    jogador_1, jogador_2 = grupo.iloc[0], grupo.iloc[1]
    if jogador_1['pontos'] > jogador_2['pontos']:
        vencedor = jogador_1['jogador']
        diferenca = jogador_1['pontos'] - jogador_2['pontos']
    else:
        vencedor = jogador_2['jogador']
        diferenca = jogador_2['pontos'] - jogador_1['pontos']
    vencedores.append(vencedor)
    diferencas.append(diferenca)
    datas_rodadas.append(grupo['data'].iloc[0])

df_vitorias = pd.DataFrame({
    'rodada': list(rodadas.groups.keys()),
    'vencedor': vencedores,
    'diferenca': diferencas,
    'data': datas_rodadas
})
# pra nao ficar bugado com o horario pq n tem
df_vitorias['data'] = df_vitorias['data'].dt.normalize()

vitorias = df_vitorias['vencedor'].value_counts().reset_index()
vitorias.columns = ['jogador', 'vitórias']
pontos_totais = df.groupby('jogador')['pontos'].sum().reset_index()
maior_dif = df_vitorias.loc[df_vitorias['diferenca'].idxmax()]
menor_dif = df_vitorias.loc[df_vitorias['diferenca'].idxmin()]

def calcular_maior_sequencia(nome):
    seq_max = atual = 0
    for vencedor in df_vitorias['vencedor']:
        if vencedor == nome:
            atual += 1
            seq_max = max(seq_max, atual)
        else:
            atual = 0
    return seq_max

# ---- estatísticas gerais ----
if pagina == "Estatísticas Gerais":
    st.header("📊 Estatísticas Gerais")

    # vitórias e total de rodadas
    col1, col2, col3 = st.columns(3)
    col1.metric("🏆 Vitórias de Henrique", vitorias.set_index('jogador').get('vitórias', pd.Series()).get('henrique', 0))
    col2.metric("🏆 Vitórias de Silvana", vitorias.set_index('jogador').get('vitórias', pd.Series()).get('silvana', 0))
    col3.metric("🎯 Total de Rodadas", len(df_vitorias))

    # diferença de pontos
    col4, col5 = st.columns(2)
    col4.metric("🔥 Vitória com maior diferença", f"{int(maior_dif['diferenca'])} pontos ({maior_dif['vencedor'].capitalize()})")
    col5.metric("❗ Vitória com menor diferença", f"{int(menor_dif['diferenca'])} pontos ({menor_dif['vencedor'].capitalize()})")

    # sequência invicta
    col6, col7 = st.columns(2)
    col6.metric("📈 Maior sequência invicta - Henrique", calcular_maior_sequencia("henrique"))
    col7.metric("📈 Maior sequência invicta - Silvana", calcular_maior_sequencia("silvana"))

    # ultimas vitórias
    col8, col9 = st.columns(2)
    col8.metric("🕒 Última vitória - Henrique", df_vitorias[df_vitorias['vencedor'] == 'henrique']['data'].max().strftime('%d/%m/%Y'))
    col9.metric("🕒 Última vitória - Silvana", df_vitorias[df_vitorias['vencedor'] == 'silvana']['data'].max().strftime('%d/%m/%Y'))

    # médias de pontos
    col10, col11 = st.columns(2)
    col10.metric("📊 Média de pontos por partida - Henrique", round(df[df['jogador'] == 'henrique']['pontos'].mean(), 1))
    col11.metric("📊 Média de pontos por partida - Silvana", round(df[df['jogador'] == 'silvana']['pontos'].mean(), 1))

    # pontuação máxima
    col12, col13 = st.columns(2)
    col12.metric("📈 Maior pontuação em uma rodada - Henrique", int(df[df['jogador'] == 'henrique']['pontos'].max()))
    col13.metric("📈 Maior pontuação em uma rodada - Silvana", int(df[df['jogador'] == 'silvana']['pontos'].max()))

    # pontuação mínima
    col14, col15 = st.columns(2)
    col14.metric("📉 Menor pontuação em uma rodada - Henrique", int(df[df['jogador'] == 'henrique']['pontos'].min()))
    col15.metric("📉 Menor pontuação em uma rodada - Silvana", int(df[df['jogador'] == 'silvana']['pontos'].min()))

    st.markdown("---")
    st.markdown("### 📈 Estatísticas Avançadas")

    # aproveitamento
    total_rodadas = len(df_vitorias)
    aproveitamento_henrique = round((vitorias[vitorias['jogador'] == 'henrique']['vitórias'].values[0] / total_rodadas) * 100, 1)
    aproveitamento_silvana = round((vitorias[vitorias['jogador'] == 'silvana']['vitórias'].values[0] / total_rodadas) * 100, 1)

    col16, col17 = st.columns(2)
    col16.metric("🎯 Aproveitamento", f"{aproveitamento_henrique}%", "Henrique")
    col17.metric("🎯 Aproveitamento", f"{aproveitamento_silvana}%", "Silvana")

    # dia com mais rodadas
    rodadas_por_data = df_vitorias['data'].value_counts().reset_index()
    rodadas_por_data.columns = ['data', 'quantidade']
    dia_top = rodadas_por_data.iloc[0]
    st.metric("🗓️ Dia com mais rodadas jogadas", f"{dia_top['data'].strftime('%d/%m')} – {dia_top['quantidade']} rodadas")

    # maior pontuação em dia
    df_pontos_dia = df.groupby(['data', 'jogador'])['pontos'].sum().reset_index()
    melhor_dia = df_pontos_dia.sort_values(by='pontos', ascending=False).iloc[0]
    st.markdown(f"💥 **{melhor_dia['jogador'].capitalize()} fez {int(melhor_dia['pontos'])} pontos em {melhor_dia['data'].strftime('%d/%m')}**")

    # rodadas disputadas
    disputadas = df_vitorias[df_vitorias['diferenca'] < 200]
    st.markdown(f"⚖️ **Rodadas disputadas:** {len(disputadas)} com menos de 200 pontos de diferença")
    
    # uultimo vencedor
    ultima_rodada = df_vitorias.sort_values(by='rodada', ascending=False).iloc[0]
    st.markdown(f"🏁 **Último vencedor: {ultima_rodada['vencedor'].capitalize()}** (diferença: {int(ultima_rodada['diferenca'])} pts)")

# --- dashboard gráfico ---
if pagina == "Dashboard Gráfico":
    st.header("📈 Dashboard Interativo")

    st.subheader("Pontos Totais por Jogador")
    fig1 = px.bar(pontos_totais, x='jogador', y='pontos', color='jogador',
                  color_discrete_map={'henrique': '#FFB700', 'silvana': '#083D77'},
                  text='pontos')
    fig1.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Vitórias por Jogador")
    fig2 = px.bar(vitorias, x='jogador', y='vitórias', color='jogador',
                  color_discrete_map={'henrique': '#FFB700', 'silvana': '#083D77'},
                  text='vitórias')
    fig2.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Diferença de Pontos por Rodada")
    fig3 = px.bar(df_vitorias, x='rodada', y='diferenca', color='vencedor',
                  color_discrete_map={'henrique': '#FFB700', 'silvana': '#083D77'},
                  text='diferenca')
    fig3.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
    st.plotly_chart(fig3, use_container_width=True)

    # agrupar vitórias por dia e jogador
    vitorias_por_dia = df_vitorias.groupby(['data', 'vencedor']).size().reset_index(name='vitorias')

    # criar estrutura com todos os dias e jogadores
    dias_unicos = pd.date_range(start=df_vitorias['data'].min(), end=df_vitorias['data'].max())
    todos_os_dias = pd.DataFrame([(dia, jogador) for dia in dias_unicos for jogador in df['jogador'].unique()],
                                columns=['data', 'jogador'])

    # unir com as vitórias
    df_evolucao = todos_os_dias.merge(vitorias_por_dia, how='left', left_on=['data', 'jogador'], right_on=['data', 'vencedor'])
    df_evolucao['vitorias'] = df_evolucao['vitorias'].fillna(0)
    df_evolucao = df_evolucao.drop(columns=['vencedor'])

    # acumular vitórias
    df_evolucao['vitorias_acumuladas'] = df_evolucao.groupby('jogador')['vitorias'].cumsum()

    st.subheader("Evolução das Vitórias ao Longo do Tempo")
    fig4 = px.line(df_evolucao, x='data', y='vitorias_acumuladas', color='jogador',
                labels={'data': 'Data', 'vitorias_acumuladas': 'Vitórias Acumuladas', 'jogador': 'Jogador'},
                color_discrete_map={'henrique': '#FFB700', 'silvana': '#083D77'},
                markers=True)

    fig4.update_layout(
        xaxis=dict(
            tickformat="%d/%m"
        ),
        xaxis_tickangle=-45,
        plot_bgcolor='#0e1117',
        paper_bgcolor='#0e1117',
        font_color='white'
    )

    st.plotly_chart(fig4, use_container_width=True)

    # histórico completo por rodada
    historico = []
    for rodada, grupo in df.groupby('rodada'):
        if len(grupo) != 2:
            continue

        silvana_pontos = grupo[grupo['jogador'] == 'silvana']['pontos'].values[0]
        henrique_pontos = grupo[grupo['jogador'] == 'henrique']['pontos'].values[0]
        data = grupo['data'].iloc[0].date()  # só a data sem hora

        vencedor = 'henrique' if henrique_pontos > silvana_pontos else 'silvana'
        diferenca = abs(henrique_pontos - silvana_pontos)

        historico.append({
            'Data': data.strftime('%d/%m'),
            'Silvana': int(silvana_pontos),
            'Henrique': int(henrique_pontos),
            'Vencedor': vencedor.capitalize(),
            'Diferença': int(diferenca)
        })

    df_historico = pd.DataFrame(historico)

    st.subheader("Histórico de Vitórias")
    st.dataframe(df_historico, use_container_width=True)

# --- adicionar partida ---
if pagina == "Adicionar Partida":
    st.header("➕ Adicionar Nova Partida")

    df_cached = df.copy()
    df_cached['rodada'] = pd.to_numeric(df_cached['rodada'], errors='coerce')
    ultima_rodada = int(df_cached['rodada'].max()) if not df_cached['rodada'].isna().all() else 0
    proxima_rodada = ultima_rodada + 1

    with st.form("form_partida", clear_on_submit=True):
        st.markdown(f"#### Rodada Atual: {proxima_rodada}")
        
        col1, col2 = st.columns(2)
        with col1:
            data = st.date_input(
                "Data da Partida", 
                value=datetime.now(pytz.timezone("America/Sao_Paulo")).date()
            )
            pontos_henrique = st.number_input("Pontos Henrique", step=5)
        
        with col2:
            data_silvana = st.date_input(
                "Data da Partida (Silvana)", 
                value=datetime.now(pytz.timezone("America/Sao_Paulo")).date(),
                label_visibility="hidden"
            )
            pontos_silvana = st.number_input("Pontos Silvana", step=5)

        st.markdown("---")
        password = st.text_input("Digite a senha para confirmar", type="password")
        submitted = st.form_submit_button("Salvar Partida")

    # if senha = st.secrets["APP_SECRETS"]["password"]:
    if submitted:
        if password == st.secrets["APP_SECRETS"]["password"]:
            try:
                st.info("Conectando e salvando a partida...")

                service_account_info = st.secrets["GOOGLE_SERVICE_ACCOUNT"]
                scopes = [
                    "https://www.googleapis.com/auth/spreadsheets",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
                gc = gspread.authorize(creds)
                worksheet_para_escrever = gc.open("buraco-dados").sheet1

                sheet_data = get_as_dataframe(worksheet_para_escrever).dropna(how="all")

                nova_linha_henrique = {
                    'data': data.strftime('%d/%m/%Y'),
                    'jogador': 'henrique',
                    'pontos': pontos_henrique,
                    'rodada': proxima_rodada
                }
                nova_linha_silvana = {
                    'data': data.strftime('%d/%m/%Y'),
                    'jogador': 'silvana',
                    'pontos': pontos_silvana,
                    'rodada': proxima_rodada   
                }

                df_novos = pd.DataFrame([nova_linha_henrique, nova_linha_silvana])
                df_final = pd.concat([sheet_data, df_novos], ignore_index=True)
                set_with_dataframe(worksheet_para_escrever, df_final)

                st.cache_data.clear()
                
                st.success(f"✅ Partida da rodada {proxima_rodada} adicionada com sucesso!")
                st.balloons()

            except Exception as e:
                st.error(f"Ocorreu um erro ao salvar: {e}")
        # if senha != st.secrets["APP_SECRETS"]["password"]:
        else:
            st.error("Senha incorreta. A partida não foi salva.")
