from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide", page_title="Inteligência de Vendas")

# Carregando a base de dados
arquivo_vendas = Path(__file__).parent / "vendas.csv"
dados = pd.read_csv(arquivo_vendas, sep=";", encoding="utf-8-sig")
dados.columns = dados.columns.str.strip()
dados["Valor"] = pd.to_numeric(dados["Valor"], errors="raise")


def formatar_moeda(valor):
    valor_formatado = f"R$ {valor:,.2f}"
    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    return valor_formatado.replace("X", ".")


# Procurando as colunas de data e quantidade, se existirem
coluna_data = None
coluna_quantidade = None

for coluna in dados.columns:
    nome_coluna = coluna.lower()

    if coluna_data is None:
        if "data" in nome_coluna or "date" in nome_coluna:
            coluna_data = coluna
        elif "mes" in nome_coluna or "mês" in nome_coluna or "month" in nome_coluna:
            coluna_data = coluna

    if coluna_quantidade is None:
        if (
            "quantidade" in nome_coluna
            or "quantity" in nome_coluna
            or "qtd" in nome_coluna
            or "units" in nome_coluna
        ):
            coluna_quantidade = coluna

# Criando os filtros na barra lateral
st.sidebar.title("Inteligência de Vendas")
st.sidebar.subheader("Filtros de Análise")
st.sidebar.divider()

if coluna_data:
    periodos = dados[coluna_data].dropna().astype(str).unique().tolist()
    periodos.sort()
    periodos.insert(0, "Todos")
    periodo_selecionado = st.sidebar.selectbox("Período/Data", periodos)
else:
    st.sidebar.selectbox(
        "Período/Data",
        ["Todos"],
        disabled=True,
        help="O arquivo vendas.csv não possui uma coluna de data.",
    )
    periodo_selecionado = "Todos"

categorias = dados["Categoria"].dropna().astype(str).unique().tolist()
categorias.sort()
categorias.insert(0, "Todos")
categoria_selecionada = st.sidebar.selectbox("Categoria", categorias)

dados_para_produtos = dados
if categoria_selecionada != "Todos":
    dados_para_produtos = dados[
        dados["Categoria"].astype(str) == categoria_selecionada
    ]

produtos = dados_para_produtos["Produto"].dropna().astype(str).unique().tolist()
produtos.sort()
produtos.insert(0, "Todos")
produto_selecionado = st.sidebar.selectbox("Produto", produtos)

# Aplicando os filtros selecionados
dados_filtrados = dados.copy()

if coluna_data and periodo_selecionado != "Todos":
    dados_filtrados = dados_filtrados[
        dados_filtrados[coluna_data].astype(str) == periodo_selecionado
    ]

if categoria_selecionada != "Todos":
    dados_filtrados = dados_filtrados[
        dados_filtrados["Categoria"].astype(str) == categoria_selecionada
    ]

if produto_selecionado != "Todos":
    dados_filtrados = dados_filtrados[
        dados_filtrados["Produto"].astype(str) == produto_selecionado
    ]

# Calculando os indicadores
if coluna_quantidade:
    volume_vendas = pd.to_numeric(
        dados_filtrados[coluna_quantidade], errors="raise"
    )
else:
    volume_vendas = pd.Series(1, index=dados_filtrados.index)

total_faturamento = dados_filtrados["Valor"].sum()
total_vendas = volume_vendas.sum()

if total_vendas > 0:
    ticket_medio = total_faturamento / total_vendas
else:
    ticket_medio = 0

vendas_por_produto = volume_vendas.groupby(
    dados_filtrados["Produto"], sort=False
).sum()

if len(vendas_por_produto) > 0:
    produto_mais_vendido = vendas_por_produto.idxmax()
else:
    produto_mais_vendido = "Sem vendas"

# Exibindo os cartões de KPI
st.title("Resumo Comercial")
col_faturamento, col_vendas, col_ticket, col_produto = st.columns(4)

with col_faturamento:
    with st.container(border=True):
        st.metric("Faturamento", formatar_moeda(total_faturamento))

with col_vendas:
    with st.container(border=True):
        st.metric("Total de vendas", f"{total_vendas:,.0f}".replace(",", "."))

with col_ticket:
    with st.container(border=True):
        st.metric("Ticket médio", formatar_moeda(ticket_medio))

with col_produto:
    with st.container(border=True):
        st.metric("Produto mais vendido", produto_mais_vendido)

# Criando as abas do dashboard
st.divider()
aba_graficos, aba_dados = st.tabs(["📊 Análise Gráfica", "📋 Dados Filtrados"])

# Exibindo os gráficos
with aba_graficos:
    col_historico, col_ranking = st.columns([1.3, 1])

    with col_historico:
        with st.container(border=True):
            st.subheader("Histórico de Faturamento")

            if coluna_data:
                historico = dados_filtrados.copy()
                historico["Data"] = pd.to_datetime(
                    historico[coluna_data], errors="coerce", dayfirst=True
                )
                historico = historico.dropna(subset=["Data"])

                if len(historico) > 0:
                    historico = historico.groupby("Data", as_index=False)["Valor"].sum()
                    historico = historico.sort_values("Data")

                    grafico_historico = px.area(
                        historico, x="Data", y="Valor", title=None
                    )
                    grafico_historico.update_traces(
                        line_color="#5B21B6",
                        fillcolor="rgba(91, 33, 182, 0.18)",
                    )
                    grafico_historico.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                    )
                    grafico_historico.update_xaxes(showgrid=False)
                    st.plotly_chart(grafico_historico, width="stretch")
                else:
                    st.info("Não há datas válidas para exibir o histórico.")
            else:
                st.info(
                    "O arquivo vendas.csv não possui uma coluna de data ou mês "
                    "para exibir o histórico."
                )

    with col_ranking:
        with st.container(border=True):
            st.subheader("Produtos mais vendidos")
            ranking_produtos = vendas_por_produto.sort_values(
                ascending=False, kind="stable"
            ).head(5)

            if len(ranking_produtos) > 0:
                dados_ranking = pd.DataFrame(
                    {
                        "Produto": ranking_produtos.index.astype(str),
                        "Vendas": ranking_produtos.values,
                    }
                )
                nomes_produtos = dados_ranking["Produto"].tolist()
                nomes_produtos.reverse()

                grafico_produtos = px.bar(
                    dados_ranking,
                    x="Vendas",
                    y="Produto",
                    orientation="h",
                    category_orders={"Produto": nomes_produtos},
                )
                grafico_produtos.update_traces(marker_color="#5B21B6")
                st.plotly_chart(grafico_produtos, width="stretch")
            else:
                st.info("Não há vendas para exibir no ranking.")

    with st.container(border=True):
        st.subheader("Vendas por categoria")

        if coluna_quantidade:
            vendas_por_categoria = volume_vendas.groupby(
                dados_filtrados["Categoria"], sort=False
            ).sum()
        else:
            vendas_por_categoria = dados_filtrados["Categoria"].value_counts(
                sort=False
            )

        if len(vendas_por_categoria) > 0:
            grafico_categorias = px.pie(
                names=vendas_por_categoria.index.astype(str),
                values=vendas_por_categoria.values,
                hole=0.6,
                color_discrete_sequence=[
                    "#5B21B6",
                    "#2563EB",
                    "#16A34A",
                    "#F97316",
                ],
            )
            st.plotly_chart(grafico_categorias, width="stretch")
        else:
            st.info("Não há vendas para exibir por categoria.")

# Exibindo os dados filtrados
with aba_dados:
    tabela_filtrada = dados_filtrados.copy()
    tabela_filtrada["Valor"] = tabela_filtrada["Valor"].apply(formatar_moeda)
    st.dataframe(
        tabela_filtrada,
        use_container_width=True,
        hide_index=True,
    )
