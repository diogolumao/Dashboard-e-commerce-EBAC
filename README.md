# 📊 Dashboard de Análise de E-commerce

> Projeto desenvolvido como parte do curso da EBAC, focado em Visualização de Dados Interativa com Python e Dash.

![Status do Projeto](https://img.shields.io/badge/Status-Finalizado-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Dash](https://img.shields.io/badge/Library-Dash-orange)

## 📝 Descrição

Este projeto consiste em uma aplicação web interativa para análise de dados de um E-commerce fictício de vestuário. O objetivo é fornecer insights estratégicos sobre vendas, precificação, avaliações de clientes e tendências sazonais através de uma interface moderna e responsiva (Dark Mode).

A aplicação processa um conjunto de dados (`ecommerce_estatistica.csv`) e gera visualizações dinâmicas que permitem a filtragem cruzada e análise exploratória.

## 🚀 Funcionalidades

* **KPIs em Tempo Real:** Visualização rápida de Total de Vendas Estimadas, Preço Médio, Nota Média e Total de Avaliações.
* **Filtros Globais:** Controle de dados por **Marca** e **Material** que afetam todo o dashboard.
* **Análise de Correlação:** Gráficos de dispersão com **Regressão Linear** e mapas de calor (Heatmaps) para identificar padrões entre preço e nota.
* **Análise Sazonal e Demográfica:** Gráficos interativos cruzando dados de **Temporada** e **Gênero** com filtros locais dedicados.
* **Top 10 Marcas:** Ranking visual das marcas com maior ticket médio.
* **Design Responsivo:** Layout construído com CSS Grid e Flexbox, adaptável a diferentes tamanhos de tela com tema escuro profissional.

## 🛠️ Tecnologias Utilizadas

* **[Python](https://www.python.org/):** Linguagem base.
* **[Dash](https://dash.plotly.com/):** Framework para criação da aplicação web.
* **[Plotly Express](https://plotly.com/python/plotly-express/):** Criação dos gráficos interativos.
* **[Pandas](https://pandas.pydata.org/):** Manipulação e limpeza dos dados.
* **Statsmodels:** Cálculos estatísticos para a linha de tendência (regressão).
* **CSS3:** Estilização personalizada da interface.

## 📂 Estrutura do Projeto

```text
ecommerce-dash/
│
├── assets/
│   └── style.css            # Folha de estilos personalizada (Dark Theme)
├── app.py                   # Código principal da aplicação
├── ecommerce_estatistica.csv # Dataset utilizado
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação
```

## 🔧 Como Executar o Projeto
Siga os passos abaixo para rodar a aplicação em sua máquina local:

1. Clone o repositório

```Bash

git clone [https://github.com/seu-usuario/ecommerce-dash.git](https://github.com/seu-usuario/ecommerce-dash.git)
cd ecommerce-dash
```

2. Crie um ambiente virtual (Opcional, mas recomendado)

```Bash

# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências
```Bash

pip install -r requirements.txt
```

4. Execute a aplicação

```Bash

python app.py
```
5. Acesse no navegador
O terminal exibirá um endereço local. Geralmente, acesse: http://127.0.0.1:8050/

📊 Prévia da Aplicação
(Dica: Tire um print da sua tela finalizada e coloque o link da imagem aqui depois que subir no GitHub, ex: ![Dashboard Screenshot](assets/print.png))

✒️ Autor
Diogo Alves Azevedo Analista de Dados em Formação | Desenvolvedor Python

💼 LinkedIn

🌐 Portfólio

Desenvolvido com 💙 e Python.