import streamlit as st
import pandas as pd

# --- Configuração da página ---
st.set_page_config(page_title="Painel de Comissões", layout="wide")

st.title("📊 Sistema de Comissões - Piloto")
st.markdown("Selecione uma tabela e visualize a comissão associada")

# --- Carregar dados ---
@st.cache_data
def carregar_dados():
    try:
        df_tabelas = pd.read_excel("Tabelas.xlsx")
        df_regras = pd.read_excel("RegraComissao.xlsx")
        return df_tabelas, df_regras
    except Exception as e:
        st.error(f"Erro ao carregar planilhas: {e}")
        return None, None

df_tabelas, df_regras = carregar_dados()

if df_tabelas is not None:
    tabela_selecionada = st.selectbox("Selecione o nome da tabela:", df_tabelas["NOME DA TABELA"].unique())

    if tabela_selecionada:
        st.subheader(f"Comissão para: **{tabela_selecionada}**")
        regra = df_regras[df_regras["ID"] == df_tabelas.loc[df_tabelas["NOME DA TABELA"] == tabela_selecionada, "ID"].values[0]]
        st.dataframe(regra, use_container_width=True)
