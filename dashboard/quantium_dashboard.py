#!/usr/bin/env python3
"""
Dashboard interactivo Plotly Dash para el análisis de chips Quantium.
Genera un dashboard con 4 páginas: Resumen, Segmentos, Marcas, y Trial.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pathlib import Path


# ============================================================
# CARGA Y PREPARACIÓN DE DATOS
# ============================================================

def load_data():
    """Carga y prepara los datos para el dashboard."""
    base_path = Path(__file__).parent.parent
    
    # Cargar datos principales
    df = pd.read_csv(base_path / 'QVI_data.csv')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['YEARMONTH'] = df['DATE'].dt.year * 100 + df['DATE'].dt.month
    df['Fecha'] = pd.to_datetime(df['YEARMONTH'].astype(str), format='%Y%m')
    
    # Cargar datos de trial
    df2 = pd.read_csv(base_path / 'QVI_data_2.csv')
    df2['DATE'] = pd.to_datetime(df2['DATE'])
    df2['YEARMONTH'] = df2['DATE'].dt.year * 100 + df2['DATE'].dt.month
    df2['Fecha'] = pd.to_datetime(df2['YEARMONTH'].astype(str), format='%Y%m')
    
    return df, df2


def calculate_metrics(df):
    """Calcula todas las métricas necesarias."""
    metrics = {}
    
    # KPIs globales
    metrics['total_ventas'] = df['TOT_SALES'].sum()
    metrics['total_unidades'] = df['PROD_QTY'].sum()
    metrics['total_clientes'] = df['LYLTY_CARD_NBR'].nunique()
    metrics['total_transacciones'] = df['TXN_ID'].nunique()
    metrics['ticket_promedio'] = metrics['total_ventas'] / metrics['total_transacciones']
    metrics['precio_prom_unidad'] = metrics['total_ventas'] / metrics['total_unidades']
    
    # Métricas mensuales
    metrics['tendencia'] = df.groupby('Fecha').agg(
        Ventas=('TOT_SALES', 'sum'),
        Unidades=('PROD_QTY', 'sum'),
        Clientes=('LYLTY_CARD_NBR', 'nunique')
    ).reset_index()
    
    # Segmentos
    segmentos = df.groupby(['LIFESTAGE', 'PREMIUM_CUSTOMER']).agg(
        Ventas=('TOT_SALES', 'sum'),
        Clientes=('LYLTY_CARD_NBR', 'nunique'),
        Transacciones=('TXN_ID', 'nunique')
    ).reset_index()
    segmentos['TicketPromedio'] = segmentos['Ventas'] / segmentos['Transacciones']
    segmentos['Participacion'] = segmentos['Ventas'] / segmentos['Ventas'].sum() * 100
    metrics['segmentos'] = segmentos.sort_values('Ventas', ascending=False)
    
    # Marcas
    metrics['marcas'] = df.groupby('BRAND').agg(
        Ventas=('TOT_SALES', 'sum'),
        Unidades=('PROD_QTY', 'sum')
    ).reset_index()
    metrics['marcas']['Participacion'] = metrics['marcas']['Ventas'] / metrics['marcas']['Ventas'].sum() * 100
    metrics['marcas'] = metrics['marcas'].sort_values('Ventas', ascending=False)
    
    # Afinidad de marcas (segmento Mainstream Young Singles/Couples)
    target_mask = (df['LIFESTAGE'] == 'YOUNG SINGLES/COUPLES') & (df['PREMIUM_CUSTOMER'] == 'Mainstream')
    target = df[target_mask]
    rest = df[~target_mask]
    
    target_brand = target['BRAND'].value_counts(normalize=True)
    rest_brand = rest['BRAND'].value_counts(normalize=True).replace(0, np.nan)
    metrics['afinidad_marcas'] = (target_brand / rest_brand).sort_values(ascending=False).reset_index()
    metrics['afinidad_marcas'].columns = ['BRAND', 'IndiceAfinidad']
    
    # Tamaños de paquete
    metrics['paquetes'] = df.groupby('PACK_SIZE')['TOT_SALES'].sum().reset_index()
    metrics['paquetes'].columns = ['PACK_SIZE', 'Ventas']
    metrics['paquetes'] = metrics['paquetes'].sort_values('Ventas', ascending=False)
    
    # Afinidad de paquetes
    target_pack = target['PACK_SIZE'].value_counts(normalize=True)
    rest_pack = rest['PACK_SIZE'].value_counts(normalize=True).replace(0, np.nan)
    metrics['afinidad_paquetes'] = (target_pack / rest_pack).sort_values(ascending=False).reset_index()
    metrics['afinidad_paquetes'].columns = ['PACK_SIZE', 'IndiceAfinidad']
    
    return metrics


# ============================================================
# CARGA DE DATOS
# ============================================================

print("Cargando datos...")
df, df2 = load_data()
metrics = calculate_metrics(df)
print("Datos cargados correctamente.")


# ============================================================
# DEFINICIÓN DEL DASHBOARD
# ============================================================

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
                title='Quantium Chips Dashboard')

# Layout principal
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1('Dashboard de Análisis - Chips Quantium',
                    className='text-primary mb-2'),
            html.P('Análisis exploratorio y evaluación de prueba de tiendas',
                   className='text-muted')
        ], width=12)
    ], className='my-3'),
    
    # Tabs de navegación
    dbc.Tabs([
        dbc.Tab(label='Resumen Ejecutivo', tab_id='resumen', children=[
            html.Div(id='tab-resumen', className='mt-3')
        ]),
        dbc.Tab(label='Análisis por Segmento', tab_id='segmentos', children=[
            html.Div(id='tab-segmentos', className='mt-3')
        ]),
        dbc.Tab(label='Análisis de Marcas', tab_id='marcas', children=[
            html.Div(id='tab-marcas', className='mt-3')
        ]),
        dbc.Tab(label='Evaluación de Trial', tab_id='trial', children=[
            html.Div(id='tab-trial', className='mt-3')
        ])
    ], id='tabs', active_tab='resumen', className='mb-4'),
    
    # Footer
    html.Hr(),
    html.P('Quantium Virtual Internship - Retail Strategy and Analytics',
           className='text-center text-muted')
], fluid=True)


# ============================================================
# CALLBACKS
# ============================================================

@app.callback(
    Output('tab-resumen', 'children'),
    Input('tabs', 'active_tab')
)
def render_resumen(active_tab):
    if active_tab != 'resumen':
        return None
    
    return dbc.Row([
        # KPIs Cards
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f'${metrics["total_ventas"]:,.0f}', className='text-primary'),
                    html.P('Ventas Totales', className='text-muted mb-0')
                ])
            ], className='mb-3')
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f'{metrics["total_unidades"]:,.0f}', className='text-success'),
                    html.P('Unidades Totales', className='text-muted mb-0')
                ])
            ], className='mb-3')
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f'{metrics["total_clientes"]:,}', className='text-info'),
                    html.P('Clientes Únicos', className='text-muted mb-0')
                ])
            ], className='mb-3')
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f'${metrics["ticket_promedio"]:.2f}', className='text-warning'),
                    html.P('Ticket Promedio', className='text-muted mb-0')
                ])
            ], className='mb-3')
        ], md=3),
        
        # Gráfico de tendencia
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Evolución Mensual de Ventas'),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.line(metrics['tendencia'], x='Fecha', y='Ventas',
                                      title='Tendencia de Ventas Mensuales',
                                      markers=True).update_layout(
                            xaxis_title='Fecha', yaxis_title='Ventas ($)',
                            template='plotly_white'
                        ),
                        style={'height': '300px'}
                    )
                ])
            ])
        ], md=8),
        
        # Top segmentos
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Top 5 Segmentos'),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.bar(metrics['segmentos'].head(5),
                                     x='Ventas', y='LIFESTAGE',
                                     color='PREMIUM_CUSTOMER',
                                     orientation='h',
                                     title='Segmentos por Ventas',
                                     labels={'Ventas': 'Ventas ($)', 'LIFESTAGE': 'Segmento'}
                                    ).update_layout(
                            yaxis={'categoryorder': 'total ascending'},
                            template='plotly_white', height=300
                        ),
                        style={'height': '300px'}
                    )
                ])
            ])
        ], md=4),
    ])


@app.callback(
    Output('tab-segmentos', 'children'),
    Input('tabs', 'active_tab')
)
def render_segmentos(active_tab):
    if active_tab != 'segmentos':
        return None
    
    # Crear heatmap
    pivot = metrics['segmentos'].pivot_table(
        values='Ventas', index='LIFESTAGE', columns='PREMIUM_CUSTOMER', aggfunc='sum'
    )
    
    heatmap_fig = px.imshow(pivot/1000,
                           labels=dict(x='Nivel de Gasto', y='Etapa de Vida', color='Ventas (miles $)'),
                           title='Mapa de Calor: Ventas por Segmento',
                           aspect='auto',
                           color_continuous_scale='YlOrRd')
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Filtros'),
                dbc.CardBody([
                    html.Label('Seleccionar Etapa de Vida:'),
                    dcc.Dropdown(
                        id='filter-lifestage',
                        options=[{'label': x, 'value': x} for x in df['LIFESTAGE'].unique()],
                        value=df['LIFESTAGE'].unique()[0],
                        className='mb-3'
                    ),
                    html.Label('Seleccionar Nivel de Gasto:'),
                    dcc.Dropdown(
                        id='filter-premium',
                        options=[{'label': x, 'value': x} for x in df['PREMIUM_CUSTOMER'].unique()],
                        value=df['PREMIUM_CUSTOMER'].unique()[0],
                        className='mb-3'
                    )
                ])
            ], className='mb-3'),
            
            dbc.Card([
                dbc.CardHeader('Detalle del Segmento'),
                dbc.CardBody(id='segment-detail')
            ])
        ], md=4),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Mapa de Calor - Ventas por Segmento'),
                dbc.CardBody([
                    dcc.Graph(figure=heatmap_fig, style={'height': '500px'})
                ])
            ])
        ], md=8)
    ])


@app.callback(
    Output('segment-detail', 'children'),
    [Input('filter-lifestage', 'value'),
     Input('filter-premium', 'value')]
)
def update_segment_detail(lifestage, premium):
    segment = metrics['segmentos'][
        (metrics['segmentos']['LIFESTAGE'] == lifestage) &
        (metrics['segmentos']['PREMIUM_CUSTOMER'] == premium)
    ]
    
    if len(segment) == 0:
        return html.P('No hay datos para este segmento')
    
    row = segment.iloc[0]
    return html.Div([
        html.H5(f'{lifestage} - {premium}', className='text-primary'),
        html.Hr(),
        html.P([html.Strong('Ventas: '), f'${row["Ventas"]:,.0f}']),
        html.P([html.Strong('Clientes: '), f'{row["Clientes"]:,}']),
        html.P([html.Strong('Transacciones: '), f'{row["Transacciones"]:,}']),
        html.P([html.Strong('Ticket Promedio: '), f'${row["TicketPromedio"]:.2f}']),
        html.P([html.Strong('Participación: '), f'{row["Participacion"]:.1f}%']),
    ])


@app.callback(
    Output('tab-marcas', 'children'),
    Input('tabs', 'active_tab')
)
def render_marcas(active_tab):
    if active_tab != 'marcas':
        return None
    
    # Gráfico de market share
    marcas_fig = px.bar(metrics['marcas'].head(10),
                       x='BRAND', y='Participacion',
                       title='Top 10 Marcas por Participación en Ventas',
                       labels={'BRAND': 'Marca', 'Participacion': 'Participación (%)'},
                       color='Ventas',
                       color_continuous_scale='Blues')
    
    # Gráfico de afinidad
    afinidad_fig = px.bar(metrics['afinidad_marcas'].head(10),
                         x='IndiceAfinidad', y='BRAND',
                         orientation='h',
                         title='Índice de Afinidad por Marca\n(Segmento: Mainstream Young Singles/Couples)',
                         labels={'BRAND': 'Marca', 'IndiceAfinidad': 'Índice de Afinidad'},
                         color='IndiceAfinidad',
                         color_continuous_scale='RdYlGn',
                         range_color=[0.8, 1.3])
    afinidad_fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Market Share por Marca'),
                dbc.CardBody([
                    dcc.Graph(figure=marcas_fig, style={'height': '400px'})
                ])
            ])
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Índice de Afinidad por Marca'),
                dbc.CardBody([
                    dcc.Graph(figure=afinidad_fig, style={'height': '400px'})
                ])
            ])
        ], md=6),
        
        # Tamaño de paquete
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Ventas por Tamaño de Paquete'),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.bar(metrics['paquetes'],
                                     x='PACK_SIZE', y='Ventas',
                                     title='Ventas por Tamaño de Paquete',
                                     labels={'PACK_SIZE': 'Tamaño (g)', 'Ventas': 'Ventas ($)'},
                                     color='Ventas',
                                     color_continuous_scale='Viridis')
                        .update_layout(xaxis_title='Tamaño (g)', template='plotly_white'),
                        style={'height': '300px'}
                    )
                ])
            ])
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Afinidad por Tamaño de Paquete'),
                dbc.CardBody([
                    dcc.Graph(
                        figure=px.bar(metrics['afinidad_paquetes'].head(10),
                                     x='IndiceAfinidad', y='PACK_SIZE',
                                     orientation='h',
                                     title='Índice de Afinidad por Tamaño',
                                     labels={'PACK_SIZE': 'Tamaño (g)', 'IndiceAfinidad': 'Índice'},
                                     color='IndiceAfinidad',
                                     color_continuous_scale='RdYlGn')
                        .update_layout(yaxis={'categoryorder': 'total ascending'}, template='plotly_white'),
                        style={'height': '300px'}
                    )
                ])
            ])
        ], md=6)
    ])


@app.callback(
    Output('tab-trial', 'children'),
    Input('tabs', 'active_tab')
)
def render_trial(active_tab):
    if active_tab != 'trial':
        return None
    
    # Definir tiendas
    tiendas = {77: 233, 86: 155, 88: 237}
    
    # Calcular métricas para cada tienda
    trial_data = []
    for trial_store, control_store in tiendas.items():
        trial = df2[df2['STORE_NBR'] == trial_store].groupby('YEARMONTH').agg(
            Ventas=('TOT_SALES', 'sum'), Clientes=('LYLTY_CARD_NBR', 'nunique')
        ).reset_index()
        
        control = df2[df2['STORE_NBR'] == control_store].groupby('YEARMONTH').agg(
            VentasControl=('TOT_SALES', 'sum'), ClientesControl=('LYLTY_CARD_NBR', 'nunique')
        ).reset_index()
        
        merged = trial.merge(control, on='YEARMONTH')
        merged['TiendaPrueba'] = trial_store
        merged['TiendaControl'] = control_store
        
        # Scaling pre-trial
        pre = merged[merged['YEARMONTH'] < 201902]
        scale_v = pre['Ventas'].sum() / pre['VentasControl'].sum() if len(pre) > 0 else 1
        scale_c = pre['Clientes'].sum() / pre['ClientesControl'].sum() if len(pre) > 0 else 1
        
        merged['VentasControlEsc'] = merged['VentasControl'] * scale_v
        merged['ClientesControlEsc'] = merged['ClientesControl'] * scale_c
        merged['Fecha'] = pd.to_datetime(merged['YEARMONTH'].astype(str), format='%Y%m')
        
        trial_data.append(merged)
    
    trial_df = pd.concat(trial_data)
    
    # Crear gráficos
    fig_ventas = go.Figure()
    fig_clientes = go.Figure()
    
    for trial_store, control_store in tiendas.items():
        data = trial_df[trial_df['TiendaPrueba'] == trial_store]
        
        fig_ventas.add_trace(go.Scatter(
            x=data['Fecha'], y=data['Ventas'],
            name=f'Tienda {trial_store}', mode='lines+markers'
        ))
        fig_ventas.add_trace(go.Scatter(
            x=data['Fecha'], y=data['VentasControlEsc'],
            name=f'Control {control_store}', mode='lines+markers',
            line=dict(dash='dash')
        ))
        
        fig_clientes.add_trace(go.Scatter(
            x=data['Fecha'], y=data['Clientes'],
            name=f'Tienda {trial_store}', mode='lines+markers'
        ))
        fig_clientes.add_trace(go.Scatter(
            x=data['Fecha'], y=data['ClientesControlEsc'],
            name=f'Control {control_store}', mode='lines+markers',
            line=dict(dash='dash')
        ))
    
    fig_ventas.update_layout(
        title='Comparativa de Ventas: Trial vs Control',
        xaxis_title='Fecha', yaxis_title='Ventas ($)',
        template='plotly_white',
        shapes=[dict(type='rect', x0='2019-02-01', x1='2019-04-30',
                    y0=0, y1=1, yref='paper', fillcolor='gray', opacity=0.2)]
    )
    
    fig_clientes.update_layout(
        title='Comparativa de Clientes: Trial vs Control',
        xaxis_title='Fecha', yaxis_title='Clientes Únicos',
        template='plotly_white',
        shapes=[dict(type='rect', x0='2019-02-01', x1='2019-04-30',
                    y0=0, y1=1, yref='paper', fillcolor='gray', opacity=0.2)]
    )
    
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Seleccionar Tienda de Prueba'),
                dbc.CardBody([
                    dcc.Dropdown(
                        id='filter-trial-store',
                        options=[{'label': f'Tienda {k} (Control: {v})', 'value': k}
                                for k, v in tiendas.items()],
                        value=77,
                        className='mb-3'
                    )
                ])
            ])
        ], md=12),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Evolución de Ventas'),
                dbc.CardBody([
                    dcc.Graph(figure=fig_ventas, style={'height': '400px'})
                ])
            ])
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Evolución de Clientes'),
                dbc.CardBody([
                    dcc.Graph(figure=fig_clientes, style={'height': '400px'})
                ])
            ])
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Resultados Estadísticos'),
                dbc.CardBody([
                    html.Table([
                        html.Thead(html.Tr([
                            html.Th('Tienda'), html.Th('Mes'), html.Th('Diff Ventas'),
                            html.Th('Significativo'), html.Th('Diff Clientes'), html.Th('Significativo')
                        ])),
                        html.Tbody([
                            html.Tr([
                                html.Td(f'Tienda {row["TiendaPrueba"]}'),
                                html.Td(f'{int(row["YEARMONTH"]//100)}-{int(row["YEARMONTH"]%100):02d}'),
                                html.Td(f'{(row["Ventas"]-row["VentasControlEsc"])/row["VentasControlEsc"]*100:+.1f}%'),
                                html.Td('✓' if abs((row["Ventas"]-row["VentasControlEsc"])/row["VentasControlEsc"]) > 0.1 else '✗',
                                       style={'color': 'green' if abs((row["Ventas"]-row["VentasControlEsc"])/row["VentasControlEsc"]) > 0.1 else 'red'}),
                                html.Td(f'{(row["Clientes"]-row["ClientesControlEsc"])/row["ClientesControlEsc"]*100:+.1f}%'),
                                html.Td('✓' if abs((row["Clientes"]-row["ClientesControlEsc"])/row["ClientesControlEsc"]) > 0.1 else '✗',
                                       style={'color': 'green' if abs((row["Clientes"]-row["ClientesControlEsc"])/row["ClientesControlEsc"]) > 0.1 else 'red'})
                            ])
                            for _, row in trial_df[
                                (trial_df['YEARMONTH'] >= 201902) &
                                (trial_df['YEARMONTH'] <= 201904)
                            ].iterrows()
                        ])
                    ], className='table table-striped')
                ])
            ])
        ], md=12)
    ])


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == '__main__':
    print("\nIniciando dashboard...")
    print("Accede a http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
