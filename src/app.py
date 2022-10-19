import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

df_states:pd.DataFrame = pd.read_csv('src/db/states.csv')
df_brasil:pd.DataFrame = pd.read_csv('src/db/brasil.csv')

brazil_states:dict = json.load(open('src/geojson/brazil_geo.json', 'r'))

# obtendo dados da data inicial
df_states_:pd.DataFrame = df_states[df_states['data'] == df_states['data'].loc[0]]
df_data = df_states[df_states['estado'] == 'RJ']
select_columns = {
    'casosAcumulado': 'Total de Casos',
    'casosNovos': 'Novos Casos',
    'obitosAcumulado': 'Total de Óbitos',
    'obitosNovos': 'Novos Óbitos'
}

app:dash.Dash = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

fig:px.choropleth_mapbox = px.choropleth_mapbox(df_states, locations='estado', color='casosNovos',
    center={'lat': -16.95, 'lon': -47.48}, zoom=4,
    geojson=brazil_states, color_continuous_scale='Redor', opacity=0.4, hover_data={
        'casosAcumulado': True,'casosNovos':True, 'obitosNovos': True, 'estado': True
    }
)
fig.update_layout(
    paper_bgcolor='#242424',
    autosize=True,
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style='carto-darkmatter'
)

fig2:go.Figure = go.Figure(layout={'template': 'plotly_dark'})
fig2.add_trace(go.Scatter(x=df_data['data'], y=df_data['casosAcumulado']))
fig2.update_layout(
    paper_bgcolor='#242424',
    plot_bgcolor='#242424',
    autosize=True,
    margin=dict(l=10, r=10, t=10, b=10)
)


app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id='logo', src=app.get_asset_url('logo_dark.png'), height=50),
                html.H5('Covid-19 Evolution'),
                dbc.Button('BRAZIL', color='primary', id='location-button', size='lg')
            ], style={}),
            html.P('Select the date you want to get information:', style={'margin-top': '40px'}),
            html.Div(id='div-test', children=[
                dcc.DatePickerSingle(
                    id='date-picker',
                    min_date_allowed=df_brasil['data'].min(),
                    max_date_allowed=df_brasil['data'].max(),
                    initial_visible_month=df_brasil['data'].min(),
                    date=df_brasil['data'].max(),
                    display_format='MMMM D, YYYY',
                    style={'border': '0px solid black'}
                )
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Casos recuperados'),
                            html.H3(style={'color': '#adfc92'}, id='casos-recuperados-text'),
                            html.Span('Em acompanhamento'),
                            html.H5(id='em-acompanhamento-text'),
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px',
                        'box-shadow': '0 4px 0 rgba(0, 0, 0, 0.15)',
                        'color': '#FFFFFF'})
                ], md=4),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Casos confirmados'),
                            html.H3(style={'color': '#389fd6'}, id='casos-confirmados-text'),
                            html.Span('Casos confirmados'),
                            html.H5(id='novos-casos-text'),
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px',
                        'box-shadow': '0 4px 0 rgba(0, 0, 0, 0.15)',
                        'color': '#FFFFFF'})
                ], md=4),

                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Span('Óbitos'),
                            html.H3(style={'color': '#df2935'}, id='obitos-text'),
                            html.Span('Obitos'),
                            html.H5(id='obitos-na-data-text'),
                        ])
                    ], color='light', outline=True, style={'margin-top': '10px',
                        'box-shadow': '0 4px 0 rgba(0, 0, 0, 0.15)',
                        'color': '#FFFFFF'})
                ], md=4),
            ]),

            html.Div([
                html.P('Select the date you want to view:', style={'margin-top': '25px'}),
                dcc.Dropdown(id='location-dropdown',
                    options=[{'label': j, 'value': i} for i, j in select_columns.items()],
                    value='casosNovos',
                    style={'margin-top': '10px'}
                ),
                dcc.Graph(id='line-graph', figure=fig2)
            ]),
        ], md=5, style={'padding': '25px', 'background-color': '#242424'}),


         dbc.Col([
            dcc.Loading(id='loading-1', type='default',
                children=[dcc.Graph(id='choroplet-map', figure=fig, style={
                    'height': '100vh',
                    'margin-right': '10px'}
                )]
            ),
        ], md=7),
    ], className="g-0"),
    fluid=True
)

@app.callback(
    [
        Output('casos-recuperados-text', 'children'),
        Output('casos-confirmados-text', 'children'),
        Output('obitos-text', 'children'),
        Output('em-acompanhamento-text', 'children'),
        Output('novos-casos-text', 'children'),
        Output('obitos-na-data-text', 'children'),
    ],[
        Input('date-picker', 'date'),
        Input('location-button', 'children')
    ]
)
def display_status(date, location):
    if location == 'BRASIL':
        df_data_on_date = df_brasil[df_brasil['data'] == date]
    else:
        df_data_on_date = df_states[(df_states['estados'] == location) & (df_states['data'] == date)]
    return (1, 2, 3, 4, 5, 6)


if __name__ == '__main__':
    app.run_server(debug=True)

