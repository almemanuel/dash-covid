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

df = pd.read_csv('src/db/base.csv', sep=';')
df_states = df[(~df['estado'].isna()) & (~df['codmun'].isna())]
df_brasil = df[df.regiao == 'Brasil']
df_states.to_csv('src/db/states.csv')
df_brasil.to_csv('src/db/brasil.csv')
