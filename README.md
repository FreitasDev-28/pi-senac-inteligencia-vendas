# 📊 Dashboard de Inteligência de Vendas

> **Projeto Integrador - Grupo 15**
> **Curso:** Análise e Desenvolvimento de Sistemas — Senac EAD
> **Disciplina:** Desenvolvimento Low Code em Ciência de Dados

## Sobre o projeto

O **Inteligência de Vendas** é um dashboard interativo para análise de dados comerciais de uma base de vendas do varejo. A aplicação transforma registros brutos em indicadores visuais e apoiadores da tomada de decisão, permitindo identificar faturamento, volume vendido, ticket médio, produtos relevantes, categorias mais representativas e evolução mensal das vendas.

O sistema foi desenvolvido em Python com a biblioteca Streamlit e apresenta os dados em uma interface ampla, responsiva e organizada em abas de navegação. Sua principal finalidade é tornar a leitura dos resultados mais rápida e acessível para gestores ou pequenos negócios.

## Objetivos

- Consolidar o faturamento e a quantidade de itens vendidos.
- Analisar o desempenho dos produtos e das categorias.
- Identificar o período com maior faturamento.
- Acompanhar a evolução mensal das vendas.
- Permitir consultas por categoria, ano e produto.
- Evidenciar os principais resultados por meio de indicadores e gráficos.

## Funcionalidades

### Navegação

A barra lateral oferece duas páginas:

- **Dashboard:** apresenta os indicadores gerais, os gráficos e o histórico de faturamento.
- **Destaques da Análise:** concentra a tabela consolidada por produto e os principais destaques do recorte selecionado.

### Filtros interativos

Os dados podem ser filtrados por:

- Categoria;
- Ano do pedido;
- Produto.

Os valores disponíveis no filtro de produtos consideram o resultado dos filtros de categoria e ano já escolhidos. A interface informa a quantidade de registros e o número de categorias presentes no recorte atual.

### Indicadores principais

Na visão de Dashboard são exibidos:

- **Faturamento Total:** soma da coluna `Vendas` no recorte selecionado.
- **Total de Vendas:** quantidade de unidades vendidas e número de pedidos registrados.
- **Ticket Médio:** faturamento dividido pelo número de registros presentes no recorte.
- **Categoria Líder:** categoria com maior faturamento e sua participação no total filtrado.

### Visualizações

A aplicação oferece:

- gráfico de barras com os dez produtos de maior faturamento;
- gráfico de rosca com a participação das categorias;
- gráfico de área com o histórico mensal de faturamento;
- tabela com produto, categoria, quantidade vendida e faturamento;
- cartões de destaque do produto líder, mês líder e categoria líder.

Na página de destaques, a tabela é ordenada pelo faturamento, do maior valor para o menor.

## Base de dados

A aplicação utiliza o arquivo [`Base_de_Vendas.csv`](./Base_de_Vendas.csv), localizado na raiz do projeto.

Antes de usar os dados, o dashboard valida a presença das seguintes colunas obrigatórias:

| Coluna | Uso na aplicação |
|---|---|
| `Data do Pedido` | Conversão em data, extração do ano e agrupamento mensal |
| `Categoria` | Filtros, agrupamentos e participação no faturamento |
| `Produto` | Filtros, ranking e tabela consolidada |
| `Quantidade` | Total de unidades vendidas |
| `Custo` | Coluna validada e convertida durante a leitura |
| `Vendas` | Faturamento, tickets e gráficos |

A base precisa usar `;` como separador e `UTF-8` com BOM compatível (`utf-8-sig`). As colunas `Vendas` e `Custo` são convertidas do padrão monetário brasileiro, como `1.234,00`, para valores numéricos. As datas seguem o formato `dd/mm/aa`.

O sistema também:

- remove automaticamente colunas cujo nome começa com `Unnamed`;
- transforma `Quantidade`, `Vendas` e `Custo` em valores numéricos;
- cria as colunas derivadas `Ano` e `Mes_Ano`;
- interrompe a inicialização com uma mensagem clara quando a base ou uma coluna obrigatória não está disponível.

## Tecnologias utilizadas

- **Python:** linguagem principal da aplicação.
- **pandas:** leitura, limpeza, conversão e agrupamento dos dados.
- **Streamlit:** interface do dashboard e navegação.
- **Plotly Express e Plotly Graph Objects:** construção dos gráficos interativos.
- **HTML e CSS:** personalização visual da interface.
- **Git e GitHub:** versionamento e colaboração.

## Como executar

### Pré-requisitos

- Python 3 instalado;
- gerenciador de pacotes `pip`;
- arquivo `Base_de_Vendas.csv` na raiz do projeto.

### Instalação e execução

Na pasta do projeto, execute:

```bash
pip install -r requirements.txt
streamlit run app.py
```

O Streamlit abrirá o dashboard no navegador, normalmente no endereço `http://localhost:8501`.

## Estrutura do projeto

```text
pi-senac-inteligencia-vendas/
├── app.py                 # Interface, tratamento e visualizações
├── Base_de_Vendas.csv     # Base utilizada pela aplicação
├── requirements.txt       # Dependências Python
└── README.md              # Documentação do projeto
```

## Formato dos valores

A interface foi configurada para o contexto brasileiro:

- moeda em reais (BRL), por exemplo `R$ 1.234,56`;
- separador decimal representado por vírgula;
- valores inteiros formatados com ponto como separador de milhares;
- percentuais com duas casas decimais.

## Tratamento dos casos vazios

Quando o conjunto filtrado não possui registros, a aplicação:

- informa que não há vendas no período;
- mantém os indicadores com valor zero ou conteúdo neutro;
- evita a criação de gráficos sem dados;
- exibe mensagens apropriadas em gráficos, tabelas e destaques.

## Equipe

Projeto Integrador — **Grupo 15**

* Lucas de Freitas Costa
* Gabriel Marques Higawa
* Henrique Loiola Santos
* Gabriel de Siqueira Souza
* Lara Rafaela Leme Marinho
* Eduardo Pereira Guedes
