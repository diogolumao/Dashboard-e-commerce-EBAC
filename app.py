import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# --- 1. Dados e Configurações ---
try:
    df = pd.read_csv('ecommerce_estatistica.csv')
except FileNotFoundError:
    df = pd.DataFrame()

# Paleta de Cores
colors = {
    'bg': '#1E1E1E',
    'card': '#252525',
    'text': '#E0E0E0',
    'primary': '#00BFA5',   # Verde Teal
    'secondary': '#FF4081', # Rosa
    'accent': '#FFC107',    # Amarelo
    'blue': '#2979FF'       # Azul complementar
}

def format_br(val, prefix="", precision=2):
    """Formata número padrão BR."""
    if isinstance(val, (int, float)):
        fmt = "{:,." + str(precision) + "f}"
        val_str = fmt.format(val)
        return f"{prefix} {val_str}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return val

# --- 2. Funções de Gráficos ---

def common_layout(fig):
    """Aplica estilo padrão a todos os gráficos"""
    fig.update_layout(
        plot_bgcolor=colors['card'],
        paper_bgcolor=colors['card'],
        font_color=colors['text'],
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_showgrid=False,
        yaxis_showgrid=True,
        yaxis_gridcolor='#333'
    )
    return fig

def fig_scatter(df_in):
    if df_in.empty: return {}
    df_in = df_in.copy()
    df_in['Preço'] = pd.to_numeric(df_in['Preço'], errors='coerce')
    df_in['Nota'] = pd.to_numeric(df_in['Nota'], errors='coerce')
    
    fig = px.scatter(
        df_in, x='Preço', y='Nota', color='Gênero',
        trendline="ols",
        title='Dispersão: Preço vs. Avaliação',
        color_discrete_sequence=[colors['primary'], colors['secondary'], colors['accent']],
        opacity=0.7
    )
    return common_layout(fig)

def fig_density(df_in):
    if df_in.empty: return {}
    fig = px.density_contour(
        df_in, x='Preço', y='Nota',
        title='Densidade de Preço e Nota',
        color_discrete_sequence=[colors['primary']]
    )
    fig.update_traces(contours_coloring="fill")
    return common_layout(fig)

def fig_hist(df_in):
    if df_in.empty: return {}
    fig = px.histogram(
        df_in, x='Preço', nbins=30,
        title='Distribuição de Preços',
        color_discrete_sequence=[colors['secondary']]
    )
    fig.update_layout(bargap=0.1, yaxis_title="Frequência")
    return common_layout(fig)

def fig_heatmap(df_in):
    if df_in.empty: return {}
    cols = ['Preço', 'Nota', 'N_Avaliações', 'Desconto', 'Qtd_Vendidos_Cod']
    dff = df_in[cols].corr()
    fig = px.imshow(
        dff, text_auto='.2f', aspect="auto",
        title='Mapa de Calor: Correlações',
        color_continuous_scale='Viridis'
    )
    return common_layout(fig)

def fig_line_brands(df_in):
    if df_in.empty: return {}
    dff = df_in.groupby('Marca')['Preço'].mean().sort_values(ascending=False).head(10).reset_index()
    
    fig = px.line(
        dff, x='Marca', y='Preço', 
        title='Top 10 Marcas (Preço Médio)',
        markers=True, text='Preço',
        color_discrete_sequence=[colors['primary']]
    )
    fig.update_traces(texttemplate='R$ %{text:.0f}', textposition="top center")
    fig.update_layout(yaxis=dict(range=[0, dff['Preço'].max() * 1.2]))
    return common_layout(fig)

def fig_col_gender(df_in):
    if df_in.empty: return {}
    dff = df_in['Gênero'].value_counts().reset_index()
    dff.columns = ['Gênero', 'Qtd']
    
    fig = px.bar(
        dff, x='Gênero', y='Qtd', text='Qtd',
        title='Produtos por Gênero',
        color='Gênero',
        color_discrete_sequence=[colors['primary'], colors['secondary'], colors['accent']]
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(showlegend=False, yaxis=dict(range=[0, dff['Qtd'].max() * 1.2]))
    return common_layout(fig)

def fig_pie_season(df_in):
    if df_in.empty: return {}
    dff = df_in.groupby('Temporada')['Qtd_Vendidos_Cod'].sum().reset_index()
    fig = px.pie(
        dff, values='Qtd_Vendidos_Cod', names='Temporada',
        title='Vendas por Temporada',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return common_layout(fig)

# --- 3. App e Layout ---
app = dash.Dash(__name__)
server = app.server

opt_marca = [{'label': i, 'value': i} for i in sorted(df['Marca'].unique().astype(str))]
opt_material = [{'label': i, 'value': i} for i in sorted(df['Material'].unique().astype(str))]
opt_genero = [{'label': i, 'value': i} for i in sorted(df['Gênero'].unique().astype(str))]
opt_temporada = [{'label': i, 'value': i} for i in sorted(df['Temporada'].unique().astype(str))]

graph_style = {'height': '400px'}

app.layout = html.Div([
    
    html.Div([
        html.H1("DASHBOARD E-COMMERCE"),
        html.P("Análise Estratégica de Vendas e Performance de Produtos")
    ], className='header'),

    html.Div([
        # Filtros Globais
        html.Div([
            html.Div([
                html.Span("Marca (Global)", className='control-label'),
                dcc.Dropdown(id='global-marca', options=opt_marca, multi=True, placeholder="Filtrar Marcas...")
            ], className='control-item'),
            html.Div([
                html.Span("Material (Global)", className='control-label'),
                dcc.Dropdown(id='global-material', options=opt_material, multi=True, placeholder="Filtrar Materiais...")
            ], className='control-item'),
        ], className='global-controls'),

        # KPIs
        html.Div([
            html.Div([html.Div("Total Vendas", className='kpi-title'), html.Div(id='kpi-vendas', className='kpi-value')], className='kpi-card'),
            html.Div([html.Div("Preço Médio", className='kpi-title'), html.Div(id='kpi-preco', className='kpi-value')], className='kpi-card'),
            html.Div([html.Div("Avaliação Média", className='kpi-title'), html.Div(id='kpi-nota', className='kpi-value')], className='kpi-card'),
            html.Div([html.Div("Total Reviews", className='kpi-title'), html.Div(id='kpi-reviews', className='kpi-value')], className='kpi-card'),
        ], className='kpi-row'),

        # Linha 1: Scatter + Density
        html.Div([
            html.Div([
                html.Div([
                    html.Span("Filtro Local: Gênero", className='control-label', style={'fontSize': '0.8em', 'color': '#888'}),
                    dcc.Dropdown(id='filter-scatter-gender', options=opt_genero, multi=True, placeholder="Selecione Gênero...")
                ], className='local-filter'),
                dcc.Graph(id='g-scatter', style=graph_style)
            ], className='graph-container'),
            
            html.Div([
                dcc.Graph(id='g-density', style=graph_style)
            ], className='graph-container')
        ], className='chart-row'),

        # Linha 2: Hist + Heatmap
        html.Div([
            html.Div([dcc.Graph(id='g-hist', style=graph_style)], className='graph-container'),
            html.Div([dcc.Graph(id='g-heatmap', style=graph_style)], className='graph-container'),
        ], className='chart-row'),

        # Linha 3: Top 10 Marcas (CORRIGIDO: full-width aplicado no item interno)
        html.Div([
            html.Div([dcc.Graph(id='g-brands', style=graph_style)], className='graph-container full-width')
        ], className='chart-row'),

        # Linha 4: Gênero + Temporada
        html.Div([
            html.Div([
                html.Div([
                    html.Span("Filtro Local: Temporada", className='control-label', style={'fontSize': '0.8em', 'color': '#888'}),
                    dcc.Dropdown(id='filter-gender-season', options=opt_temporada, multi=True, placeholder="Filtrar Temporada...")
                ], className='local-filter'),
                dcc.Graph(id='g-gender-col', style=graph_style)
            ], className='graph-container'),

            html.Div([
                html.Div([
                    html.Span("Filtro Local: Gênero", className='control-label', style={'fontSize': '0.8em', 'color': '#888'}),
                    dcc.Dropdown(id='filter-season-gender', options=opt_genero, multi=True, placeholder="Filtrar Gênero...")
                ], className='local-filter'),
                dcc.Graph(id='g-pie', style=graph_style)
            ], className='graph-container'),
        ], className='chart-row'),

    ], className='main-container'),

# Rodapé
    html.Footer([
        html.Div([
            html.Div([
                html.H3("Sobre o Projeto"),
                html.P("Dashboard desenvolvido como parte do módulo de visualização de dados. Utiliza Python, Dash e Plotly.")
            ], className='footer-col'),
            
            html.Div([
                html.H3("Navegação"),
                html.Ul([
                    html.Li(html.A("Linkedin", href="https://www.linkedin.com/in/diogoalves-dados/", target="_blank")),
                    html.Li(html.A("Portfólio", href="https://diogolumao.com.br/", target="_blank")),
                    html.Li(html.A("Repositório GitHub", href="https://github.com/diogolumao", target="_blank")),
                ], className='footer-links')
            ], className='footer-col'),
            
            html.Div([
                html.H3("Contato"),
                html.P("Diogo Alves Azevedo"),
                html.P("Analista de Dados"),
                html.P("diogolumao@gmail.com")
            ], className='footer-col'),
        ], className='footer-content'),
        
        html.Div([
            html.P("© 2025 Diogo Alves. Todos os direitos reservados.")
        ], className='footer-bottom')
    ], className='footer-professional')
])

# --- 4. Callbacks ---
@app.callback(
    [Output('kpi-vendas', 'children'), Output('kpi-preco', 'children'),
     Output('kpi-nota', 'children'), Output('kpi-reviews', 'children'),
     Output('g-scatter', 'figure'), Output('g-density', 'figure'),
     Output('g-hist', 'figure'), Output('g-heatmap', 'figure'),
     Output('g-brands', 'figure'), 
     Output('g-gender-col', 'figure'),
     Output('g-pie', 'figure')],
    [Input('global-marca', 'value'),
     Input('global-material', 'value'),
     Input('filter-scatter-gender', 'value'),
     Input('filter-gender-season', 'value'),
     Input('filter-season-gender', 'value')]
)
def update_all(marcas, materiais, f_scatter_gen, f_gender_season, f_season_gen):
    # Global
    dff = df.copy()
    if marcas: dff = dff[dff['Marca'].isin(marcas)]
    if materiais: dff = dff[dff['Material'].isin(materiais)]
    
    # KPIs
    if not dff.empty:
        k_vendas = format_br(dff['Qtd_Vendidos_Cod'].sum(), precision=0)
        k_preco = format_br(dff['Preço'].mean(), "R$", precision=2)
        k_nota = f"{dff['Nota'].mean():.1f}/5.0"
        k_rev = format_br(dff['N_Avaliações'].sum(), precision=0)
    else:
        k_vendas, k_preco, k_nota, k_rev = "0", "R$ 0,00", "0.0", "0"

    # Filtros Locais
    dff_scatter = dff.copy()
    if f_scatter_gen:
        dff_scatter = dff_scatter[dff_scatter['Gênero'].isin(f_scatter_gen)]

    dff_gender = dff.copy()
    if f_gender_season:
        dff_gender = dff_gender[dff_gender['Temporada'].isin(f_gender_season)]

    dff_season = dff.copy()
    if f_season_gen:
        dff_season = dff_season[dff_season['Gênero'].isin(f_season_gen)]

    return (
        k_vendas, k_preco, k_nota, k_rev,
        fig_scatter(dff_scatter), 
        fig_density(dff_scatter),
        fig_hist(dff), 
        fig_heatmap(dff),
        fig_line_brands(dff),
        fig_col_gender(dff_gender),
        fig_pie_season(dff_season)
    )

if __name__ == '__main__':
    app.run(debug=True)