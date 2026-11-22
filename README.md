# 📊 Inteligência de Vendas para Pequenos Negócios

> **Projeto Integrador - 2º Período de ADS (Senac EAD)**  
> **Disciplina:** Desenvolvimento Low Code em Ciência de Dados  

---

## 👨‍💻 Integrantes do Grupo 33
* Lucas de Freitas Costa - *Desenvolvimento / Programação & Documentação*
* Gabriel Marques Higawa; Henrique Loiola Santos - *Ciência de Dados*
* Gabriel de Siqueira Souza - *Banco de Dados*
* Lara Rafaela Leme Marinho - *Interface / Visualização*
* Eduardo Pereira Guedes - *Scrum / Gestão do Projeto*

---

## 📌 Visão Geral do Projeto
Aplicação Low Code focada em analisar dados reais de vendas do varejo, convertendo registros brutos em indicadores estratégicos de desempenho (faturamento, produtos mais vendidos, evolução temporal e ticket médio) para apoiar a tomada de decisão em pequenos negócios.

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem / Tratamento:** Python e pandas
* **Dashboard e gráficos:** Streamlit e Plotly
* **Gestão Ágil:** GitHub Projects (Scrum)
* **Versionamento:** Git & GitHub

## ▶️ Como executar
Instale as dependências na pasta do projeto:

```bash
pip install -r requirements.txt
streamlit run app.py
```

O dashboard lê `Base_de_Vendas.csv` usando `;` como separador e `utf-8-sig` como
encoding. A base deve conter as colunas `Data do Pedido`, `Categoria`, `Produto`,
`Quantidade`, `Custo` e `Vendas`; valores monetários no padrão brasileiro
(por exemplo, `1.234,00`) são convertidos durante a leitura. O dashboard também
remove colunas extras `Unnamed` e cria filtros anuais e uma série mensal a partir
da data do pedido.

---

## 📂 Estrutura da 1ª Etapa
* Os slides oficiais da 1ª entrega estão disponíveis na pasta `/documentacao`.
