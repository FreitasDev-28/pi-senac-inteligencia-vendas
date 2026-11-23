from html import escape
from pathlib import Path
#
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout="wide", page_title="Inteligência de Vendas")

PALETA_CATEGORIAS = {
    "Material de Escritório": "#5B21B6",
    "Móveis": "#2563EB",
    "Tecnologia": "#10B981",
}

st.markdown(
    """
    <style>
    :root {
        --ink: #0F172A;
        --muted: #64748B;
        --purple: #5B21B6;
        --line: #E2E8F0;
    }
    [data-testid="stAppViewContainer"] {
        background: #F8FAFC;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        border-radius: 16px;
    }
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    [data-testid="stSidebar"] h2 {
        color: #172033;
        line-height: 1.15;
        margin-bottom: 0.2rem;
    }
    #MainMenu, footer {
        visibility: hidden;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        display: none;
    }
    .brand {
        align-items: center;
        display: flex;
        gap: 0.75rem;
        margin: 0.4rem 0 0.25rem;
    }
    .brand-mark {
        align-items: center;
        background: #F5F3FF;
        border: 1px solid #EDE9FE;
        border-radius: 12px;
        display: flex;
        height: 42px;
        justify-content: center;
        min-width: 42px;
    }
    .brand-bars {
        align-items: end;
        display: flex;
        gap: 3px;
        height: 20px;
    }
    .brand-bars span {
        background: #5B21B6;
        border-radius: 2px 2px 0 0;
        display: block;
        width: 4px;
    }
    .brand-bars span:nth-child(1) { height: 9px; }
    .brand-bars span:nth-child(2) { height: 15px; }
    .brand-bars span:nth-child(3) { height: 20px; }
    .brand-title {
        color: #0F172A;
        font-size: 1.06rem;
        font-weight: 750;
        line-height: 1.2;
    }
    .sidebar-subtitle {
        color: #64748B;
        font-size: 0.88rem;
        margin: 0.15rem 0 2rem 3.2rem;
    }
    .sidebar-section {
        color: #94A3B8;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        margin: 1rem 0 0.5rem;
    }
    .sidebar-footer {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        color: #64748B;
        font-size: 0.76rem;
        line-height: 1.6;
        padding: 0.9rem;
        position: fixed;
        bottom: 1rem;
        left: 1.25rem;
        width: 250px;
        z-index: 5;
    }
    .sidebar-footer strong {
        color: #334155;
    }
    .eyebrow {
        color: #64748B;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        margin: 0 0 0.45rem;
    }
    .page-title {
        color: #172033;
        font-size: clamp(1.8rem, 3vw, 2.35rem);
        font-weight: 700;
        letter-spacing: -0.035em;
        line-height: 1.15;
        margin: 0;
    }
    .page-subtitle {
        color: #64748B;
        font-size: 0.96rem;
        margin: 0.55rem 0 0;
    }
    .currency-badge {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 999px;
        color: #475569;
        display: inline-block;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        padding: 0.5rem 0.75rem;
        text-align: center;
        white-space: normal;
    }
    .header-badges {
        align-items: flex-end;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .updated-badge {
        align-items: center;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 999px;
        color: #475569;
        display: inline-flex;
        font-size: 0.72rem;
        font-weight: 600;
        gap: 0.45rem;
        padding: 0.4rem 0.7rem;
        white-space: nowrap;
    }
    .updated-dot {
        background: #10B981;
        border-radius: 50%;
        height: 7px;
        width: 7px;
    }
    .filter-summary {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 999px;
        color: #64748B;
        display: inline-block;
        font-size: 0.82rem;
        margin: 0.55rem 0 0;
        padding: 0.35rem 0.75rem;
    }
    .chart-heading {
        color: #172033;
        font-size: 1.08rem;
        font-weight: 650;
        margin: 0;
    }
    .chart-caption {
        color: #64748B;
        font-size: 0.82rem;
        margin: 0.25rem 0 0.55rem;
    }
    .chart-badge {
        background: #F5F3FF;
        border-radius: 999px;
        color: #5B21B6;
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.4rem 0.65rem;
        text-align: right;
    }
    .kpi-header {
        align-items: center;
        color: #64748B;
        display: flex;
        font-size: 0.78rem;
        font-weight: 600;
        justify-content: space-between;
        gap: 0.5rem;
    }
    .kpi-icon {
        align-items: center;
        background: #F5F3FF;
        border-radius: 9px;
        color: #5B21B6;
        display: inline-flex;
        font-size: 0.8rem;
        height: 30px;
        justify-content: center;
        min-width: 30px;
    }
    .kpi-value {
        color: #0F172A;
        font-size: clamp(1.15rem, 1.7vw, 1.65rem);
        font-weight: 750;
        letter-spacing: -0.035em;
        line-height: 1.2;
        margin-top: 0.7rem;
        overflow-wrap: anywhere;
    }
    .kpi-detail {
        color: #64748B;
        font-size: 0.74rem;
        line-height: 1.45;
        margin-top: 0.4rem;
    }
    .kpi-emphasis {
        color: #5B21B6;
        font-weight: 650;
    }
    .category-row {
        border-bottom: 1px solid #F1F5F9;
        padding: 0.62rem 0;
    }
    .category-row:last-child {
        border-bottom: 0;
    }
    .category-name {
        align-items: center;
        color: #334155;
        display: flex;
        font-size: 0.8rem;
        font-weight: 600;
        gap: 0.42rem;
    }
    .category-dot {
        border-radius: 50%;
        display: inline-block;
        height: 8px;
        min-width: 8px;
    }
    .category-value {
        color: #172033;
        font-size: 0.83rem;
        font-weight: 650;
    }
    .category-share {
        color: #5B21B6;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.16rem;
    }
    .highlight-label {
        color: #64748B;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
    }
    .highlight-title {
        color: #172033;
        font-size: 1rem;
        font-weight: 650;
        line-height: 1.35;
        margin: 0;
        overflow-wrap: anywhere;
    }
    .highlight-detail {
        color: #64748B;
        font-size: 0.8rem;
        margin: 0.3rem 0 0;
    }
    .highlight-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        margin-top: 0.65rem;
        padding: 0.8rem 0.9rem;
    }
    .highlight-card .highlight-title {
        color: #5B21B6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

arquivo_vendas = Path(__file__).parent / "Base_de_Vendas.csv"
if not arquivo_vendas.exists():
    st.error("Não foi possível encontrar o arquivo Base_de_Vendas.csv.")
    st.stop()

dados = pd.read_csv(arquivo_vendas, sep=";", encoding="utf-8-sig")
dados.columns = dados.columns.str.strip()
dados = dados.loc[
    :, ~dados.columns.str.match(r"^Unnamed", case=False, na=False)
]

colunas_obrigatorias = {
    "Data do Pedido",
    "Categoria",
    "Produto",
    "Quantidade",
    "Custo",
    "Vendas",
}
colunas_ausentes = colunas_obrigatorias.difference(dados.columns)
if colunas_ausentes:
    raise ValueError(
        "A base de vendas não contém as colunas obrigatórias: "
        + ", ".join(sorted(colunas_ausentes))
    )

for coluna in ("Vendas", "Custo"):
    dados[coluna] = pd.to_numeric(
        dados[coluna]
        .astype(str)
        .str.strip()
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False),
        errors="raise",
    )

dados["Quantidade"] = pd.to_numeric(dados["Quantidade"], errors="raise")
dados["Data do Pedido"] = pd.to_datetime(
    dados["Data do Pedido"], format="%d/%m/%y", errors="raise"
)
dados["Ano"] = dados["Data do Pedido"].dt.year
dados["Mes_Ano"] = dados["Data do Pedido"].dt.strftime("%Y-%m")


def formatar_moeda(valor):
    valor_formatado = f"R$ {valor:,.2f}"
    return valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_percentual(valor):
    return f"{valor:.2f}".replace(".", ",") + "%"


def formatar_inteiro(valor):
    return f"{valor:,.0f}".replace(",", ".")


def renderizar_kpi(coluna, titulo, valor, detalhe, icone):
    with coluna:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="kpi-header">
                    <span>{escape(titulo)}</span>
                    <span class="kpi-icon">{escape(icone)}</span>
                </div>
                <div class="kpi-value">{escape(valor)}</div>
                <div class="kpi-detail">{escape(detalhe)}</div>
                """,
                unsafe_allow_html=True,
            )


def tabela_produtos(dados_filtrados):
    tabela = (
        dados_filtrados.groupby(["Produto", "Categoria"], as_index=False, sort=False)
        .agg(Quantidade=("Quantidade", "sum"), Vendas=("Vendas", "sum"))
        .sort_values("Vendas", ascending=False, kind="stable")
    )
    tabela["Quantidade"] = tabela["Quantidade"].map(formatar_inteiro)
    tabela["Vendas (R$)"] = tabela.pop("Vendas").map(formatar_moeda)
    return tabela[["Produto", "Categoria", "Quantidade", "Vendas (R$)"]]


def resumo_destaques(dados_filtrados):
    if dados_filtrados.empty:
        return None, None, None

    por_produto = (
        dados_filtrados.groupby("Produto", as_index=False, sort=False)
        .agg(Vendas=("Vendas", "sum"), Quantidade=("Quantidade", "sum"))
        .sort_values("Vendas", ascending=False, kind="stable")
    )
    produto_lider = por_produto.iloc[0]

    por_mes = dados_filtrados.groupby("Mes_Ano", as_index=False)["Vendas"].sum()
    mes_lider = por_mes.loc[por_mes["Vendas"].idxmax()]

    por_categoria = (
        dados_filtrados.groupby("Categoria", as_index=False, sort=False)
        .agg(Vendas=("Vendas", "sum"), Registros=("Produto", "size"))
        .sort_values("Vendas", ascending=False, kind="stable")
    )
    categoria_lider = por_categoria.iloc[0]
    categoria_lider["Participacao"] = (
        categoria_lider["Vendas"] / dados_filtrados["Vendas"].sum()
        if dados_filtrados["Vendas"].sum()
        else 0
    )
    return produto_lider, mes_lider, categoria_lider


def renderizar_destaques(dados_filtrados):
    produto_lider, mes_lider, categoria_lider = resumo_destaques(dados_filtrados)
    destaques = [
        (
            "Produto de maior faturamento",
            str(produto_lider["Produto"]),
            (
                f"{formatar_moeda(produto_lider['Vendas'])} · "
                f"{formatar_inteiro(produto_lider['Quantidade'])} unidades vendidas"
                if produto_lider is not None
                else "Sem vendas no período selecionado"
            ),
        ),
        (
            "Período de maior venda",
            str(mes_lider["Mes_Ano"]) if mes_lider is not None else "—",
            (
                formatar_moeda(mes_lider["Vendas"])
                if mes_lider is not None
                else "Sem vendas no período selecionado"
            ),
        ),
        (
            "Categoria com maior participação",
            str(categoria_lider["Categoria"]) if categoria_lider is not None else "—",
            (
                f"{formatar_inteiro(categoria_lider['Registros'])} registros · "
                f"{formatar_percentual(categoria_lider['Participacao'] * 100)} "
                "do faturamento"
                if categoria_lider is not None
                else "Sem categorias no período selecionado"
            ),
        ),
    ]

    for titulo, valor, detalhe in destaques:
        st.markdown(
            f"""
            <div class="highlight-card">
                <div class="highlight-label">{escape(titulo)}</div>
                <div class="highlight-title">{escape(valor)}</div>
                <div class="highlight-detail">{escape(detalhe)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.sidebar.markdown(
    """
    <div class="brand">
        <div class="brand-mark">
            <div class="brand-bars"><span></span><span></span><span></span></div>
        </div>
        <div class="brand-title">Inteligência de Vendas</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    "<div class='sidebar-subtitle'>Business Intelligence</div>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("<div class='sidebar-section'>PRINCIPAL</div>", unsafe_allow_html=True)
pagina = st.sidebar.radio(
    "Navegação",
    ["Dashboard", "Destaques da Análise"],
    label_visibility="collapsed",
)
st.sidebar.markdown(
    """
    <div class="sidebar-footer">
        <div class="sidebar-section">PROJETO ACADÊMICO</div>
        <strong>Projeto Integrador - Grupo 15</strong><br>
        Análise e Desenvolvimento de Sistemas
    </div>
    """,
    unsafe_allow_html=True,
)

cabecalho, badge = st.columns([3, 1], vertical_alignment="center")
with cabecalho:
    st.markdown(
        "<div class='eyebrow'>WORKSPACE / VISÃO GERAL</div>",
        unsafe_allow_html=True,
    )
    titulo_pagina = (
        "Visão Geral de Vendas"
        if pagina == "Dashboard"
        else "Destaques da Análise"
    )
    subtitulo_pagina = (
        "Acompanhe os indicadores e a distribuição dos valores por produto e categoria."
        if pagina == "Dashboard"
        else "Explore os principais produtos, períodos e categorias do recorte selecionado."
    )
    st.markdown(f"<h1 class='page-title'>{titulo_pagina}</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='page-subtitle'>{subtitulo_pagina}</p>",
        unsafe_allow_html=True,
    )
with badge:
    st.markdown(
        """
        <div class="header-badges">
            <div class="updated-badge">
                <span class="updated-dot"></span>Dados atualizados
            </div>
            <div class="currency-badge">VALORES EM REAIS - BRL</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
with st.container(border=True):
    filtro_categoria, filtro_ano, filtro_produto = st.columns(3)

    with filtro_categoria:
        categorias = [
            "Todas as categorias",
            *sorted(dados["Categoria"].dropna().astype(str).unique().tolist()),
        ]
        categoria_selecionada = st.selectbox(
            "Filtrar por categoria",
            categorias,
        )
    with filtro_ano:
        anos = ["Todos os anos"] + sorted(dados["Ano"].dropna().unique().tolist())
        ano_selecionado = st.selectbox(
            "Filtrar por ano", anos
        )

    dados_produtos = dados.copy()
    if categoria_selecionada != "Todas as categorias":
        dados_produtos = dados_produtos[
            dados_produtos["Categoria"] == categoria_selecionada
        ]
    if ano_selecionado != "Todos os anos":
        dados_produtos = dados_produtos[dados_produtos["Ano"] == ano_selecionado]
    with filtro_produto:
        produtos = ["Todos os produtos"] + sorted(
            dados_produtos["Produto"].dropna().astype(str).unique().tolist()
        )
        produto_selecionado = st.selectbox("Filtrar por produto", produtos)

    dados_filtrados = dados.copy()
    if categoria_selecionada != "Todas as categorias":
        dados_filtrados = dados_filtrados[
            dados_filtrados["Categoria"] == categoria_selecionada
        ]
    if ano_selecionado != "Todos os anos":
        dados_filtrados = dados_filtrados[dados_filtrados["Ano"] == ano_selecionado]
    if produto_selecionado != "Todos os produtos":
        dados_filtrados = dados_filtrados[
            dados_filtrados["Produto"] == produto_selecionado
        ]

    total_registros = formatar_inteiro(len(dados_filtrados))
    st.markdown(
        f"<p class='filter-summary'>{total_registros} registros • "
        f"{dados_filtrados['Categoria'].nunique()} categorias</p>",
        unsafe_allow_html=True,
    )

if pagina == "Destaques da Análise":
    col_tabela, col_destaques = st.columns([1.3, 1])
    with col_tabela:
        with st.container(border=True):
            st.markdown(
                "<div class='chart-heading'>Resumo de Vendas por Produto</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='chart-caption'>Produtos ordenados pelo faturamento no período.</div>",
                unsafe_allow_html=True,
            )
            st.dataframe(
                tabela_produtos(dados_filtrados),
                use_container_width=True,
                hide_index=True,
            )
    with col_destaques:
        st.markdown(
            "<div class='chart-heading'>Destaques da Análise</div>",
            unsafe_allow_html=True,
        )
        st.write("")
        renderizar_destaques(dados_filtrados)
    st.stop()

total_faturamento = dados_filtrados["Vendas"].sum()
total_unidades = dados_filtrados["Quantidade"].sum()
numero_pedidos = len(dados_filtrados)
ticket_medio = total_faturamento / numero_pedidos if numero_pedidos else 0

vendas_categoria = (
    dados_filtrados.groupby("Categoria", sort=False)["Vendas"]
    .sum()
    .sort_values(ascending=False, kind="stable")
)
if not vendas_categoria.empty:
    categoria_destaque = vendas_categoria.index[0]
    valor_categoria_destaque = vendas_categoria.iloc[0]
    percentual_categoria_destaque = (
        valor_categoria_destaque / total_faturamento * 100
        if total_faturamento
        else 0
    )
else:
    categoria_destaque = "—"
    valor_categoria_destaque = 0
    percentual_categoria_destaque = 0

col_faturamento, col_unidades, col_ticket, col_categoria = st.columns(4)
renderizar_kpi(
    col_faturamento,
    "Faturamento Total",
    formatar_moeda(total_faturamento),
    "Soma total das vendas cadastradas.",
    "R$",
)
renderizar_kpi(
    col_unidades,
    "Total de Vendas (Unidades)",
    formatar_inteiro(total_unidades),
    f"Itens vendidos em {formatar_inteiro(numero_pedidos)} pedidos.",
    "▦",
)
renderizar_kpi(
    col_ticket,
    "Ticket Médio",
    formatar_moeda(ticket_medio),
    "Valor médio por pedido registrado.",
    "↗",
)
renderizar_kpi(
    col_categoria,
    "Categoria Líder",
    f"{categoria_destaque} · {formatar_moeda(valor_categoria_destaque)}",
    f"{formatar_percentual(percentual_categoria_destaque)} do valor filtrado.",
    "★",
)

st.write("")
col_produtos, col_categorias = st.columns([1.35, 1])

with col_produtos:
    with st.container(border=True):
        if numero_pedidos:
            ranking_produtos = (
                dados_filtrados.groupby("Produto", as_index=False, sort=False)["Vendas"]
                .sum()
                .sort_values("Vendas", ascending=False, kind="stable")
                .head(10)
            )
        else:
            ranking_produtos = pd.DataFrame(columns=["Produto", "Vendas"])

        titulo_grafico, badge_produto = st.columns([1, 1.2], vertical_alignment="center")
        with titulo_grafico:
            st.markdown(
                "<div class='chart-heading'>Valores por Produto (Top 10)</div>",
                unsafe_allow_html=True,
            )
        with badge_produto:
            if not ranking_produtos.empty:
                st.markdown(
                    "<div class='chart-badge'>• Maior valor: "
                    f"{escape(str(ranking_produtos.iloc[0]['Produto']))}</div>",
                    unsafe_allow_html=True,
                )
        st.markdown(
            "<div class='chart-caption'>Comparação dos 10 produtos com maior faturamento.</div>",
            unsafe_allow_html=True,
        )

        if ranking_produtos.empty:
            st.info("Não há vendas para exibir no período selecionado.")
        else:
            ranking_produtos["Rótulo"] = ranking_produtos["Vendas"].map(formatar_moeda)
            cores_produtos = [
                "#5B21B6" if indice == 0 else "#C4B5FD"
                for indice in range(len(ranking_produtos))
            ]
            grafico_produtos = go.Figure(
                data=[
                    go.Bar(
                        x=ranking_produtos["Produto"],
                        y=ranking_produtos["Vendas"],
                        marker_color=cores_produtos,
                        text=ranking_produtos["Rótulo"],
                        textposition="outside",
                        cliponaxis=False,
                        hovertemplate="%{x}<br>Faturamento: %{text}<extra></extra>",
                    )
                ]
            )
            grafico_produtos.update_layout(
                showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=12, r=12, t=18, b=92),
                xaxis_title=None,
                yaxis_title=None,
                uniformtext_minsize=9,
                uniformtext_mode="hide",
            )
            grafico_produtos.update_xaxes(showgrid=False, tickangle=-35)
            grafico_produtos.update_yaxes(
                showgrid=True,
                gridcolor="#F1F5F9",
                tickprefix="R$ ",
                tickformat=",.0f",
                zeroline=False,
            )
            st.plotly_chart(
                grafico_produtos,
                width="stretch",
                config={"displayModeBar": False},
            )

with col_categorias:
    with st.container(border=True):
        st.markdown(
            "<div class='chart-heading'>Distribuição por Categoria</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='chart-caption'>Participação de cada categoria no faturamento.</div>",
            unsafe_allow_html=True,
        )

        valores_por_categoria = (
            dados_filtrados.groupby("Categoria")["Vendas"].sum().to_dict()
        )
        resumo_categoria = pd.DataFrame(
            {
                "Categoria": list(PALETA_CATEGORIAS),
                "Vendas": [
                    valores_por_categoria.get(categoria, 0)
                    for categoria in PALETA_CATEGORIAS
                ],
            }
        )
        col_donut, col_legenda = st.columns([1.15, 1], vertical_alignment="center")
        with col_donut:
            if total_faturamento:
                grafico_categorias = go.Figure(
                    data=[
                        go.Pie(
                            labels=resumo_categoria["Categoria"],
                            values=resumo_categoria["Vendas"],
                            hole=0.72,
                            sort=False,
                            textinfo="none",
                            marker=dict(
                                colors=[
                                    PALETA_CATEGORIAS[categoria]
                                    for categoria in resumo_categoria["Categoria"]
                                ]
                            ),
                            hovertemplate=(
                                "%{label}<br>Faturamento: R$ %{value:,.2f}<extra></extra>"
                            ),
                        )
                    ]
                )
                grafico_categorias.update_layout(
                    showlegend=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=0, t=8, b=8),
                    height=280,
                    annotations=[
                        dict(
                            text="<span style='font-size:10px;color:#64748B'>TOTAL</span>"
                            f"<br><b>{formatar_moeda(total_faturamento)}</b>",
                            x=0.5,
                            y=0.5,
                            showarrow=False,
                            font=dict(size=13, color="#0F172A"),
                        )
                    ],
                )
                st.plotly_chart(
                    grafico_categorias,
                    width="stretch",
                    config={"displayModeBar": False},
                )
            else:
                st.info("Sem faturamento para distribuir.")

        with col_legenda:
            for _, linha in resumo_categoria.iterrows():
                participacao = (
                    linha["Vendas"] / total_faturamento * 100
                    if total_faturamento
                    else 0
                )
                cor = PALETA_CATEGORIAS[linha["Categoria"]]
                st.markdown(
                    f"""
                    <div class="category-row">
                        <div class="category-name" style="color:{cor}">
                            <span class="category-dot" style="background:{cor}"></span>
                            {escape(str(linha['Categoria']))}
                        </div>
                        <div class="category-value">{formatar_moeda(linha['Vendas'])}</div>
                        <div class="category-share">{formatar_percentual(participacao)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

with st.container(border=True):
    st.markdown(
        "<div class='chart-heading'>Histórico de Faturamento por Período</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='chart-caption'>Evolução mensal do faturamento no período selecionado.</div>",
        unsafe_allow_html=True,
    )
    if numero_pedidos:
        historico = (
            dados_filtrados.groupby("Mes_Ano", as_index=False)["Vendas"]
            .sum()
            .sort_values("Mes_Ano")
        )
        grafico_historico = px.area(
            historico,
            x="Mes_Ano",
            y="Vendas",
            line_shape="spline",
            category_orders={"Mes_Ano": historico["Mes_Ano"].tolist()},
        )
        grafico_historico.update_traces(
            line_color="#5B21B6",
            fillcolor="rgba(91, 33, 182, 0.12)",
            hovertemplate="%{x}<br>Faturamento: R$ %{y:,.2f}<extra></extra>",
        )
        grafico_historico.update_layout(
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=12, r=12, t=12, b=12),
            xaxis_title=None,
            yaxis_title=None,
        )
        grafico_historico.update_xaxes(showgrid=False)
        grafico_historico.update_yaxes(
            showgrid=True,
            gridcolor="#F1F5F9",
            tickprefix="R$ ",
            tickformat=",.0f",
            zeroline=False,
        )
        st.plotly_chart(
            grafico_historico,
            width="stretch",
            config={"displayModeBar": False},
        )
    else:
        st.info("Não há registros para exibir o histórico.")

st.write("")
col_tabela, col_destaques = st.columns([1.35, 1])
with col_tabela:
    with st.container(border=True):
        st.markdown(
            "<div class='chart-heading'>Resumo de Vendas por Produto</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='chart-caption'>Visualização detalhada dos dados consolidados na análise.</div>",
            unsafe_allow_html=True,
        )
        st.dataframe(
            tabela_produtos(dados_filtrados),
            use_container_width=True,
            hide_index=True,
        )
with col_destaques:
    with st.container(border=True):
        st.markdown(
            "<div class='chart-heading'>Destaques da Análise</div>",
            unsafe_allow_html=True,
        )
        renderizar_destaques(dados_filtrados)
