import pandas as pd
import streamlit as st

# 1. Lê o arquivo CSV
dados = pd.read_csv("vendas.csv", sep=";", encoding="utf-8-sig")
dados.columns = dados.columns.str.strip()

# 2. Título da aplicação
st.title("Painel de Controle de Vendas")

# 3. Filtro interativo por Categoria
categorias = dados["Categoria"].unique()
categoria_selecionada = st.selectbox("Selecione a Categoria:", categorias)

# 4. Filtrando a base de dados
dados_filtrados = dados[dados["Categoria"] == categoria_selecionada]

# 5. Métrica principal (KPI)
total_vendas = dados_filtrados["Valor"].sum()
st.metric(label="Total de Vendas", value=f"R$ {total_vendas:,.2f}")

# 6. Gráfico de barras de Vendas por Produto
st.subheader("Vendas por Produto")
grafico_barra = dados_filtrados.groupby("Produto")["Valor"].sum()
st.bar_chart(grafico_barra)

# 7. Exibição da Tabela de Dados
st.write("Tabela de Dados Filtrados:")
st.dataframe(dados_filtrados)