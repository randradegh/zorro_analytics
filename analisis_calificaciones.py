#!/usr/bin/env python
# coding: utf-8

# In[19]:


###
# Variable: Todas 
# Periodo: Datos en la DB
# Proyecto Zorro Abarrotero
# Graph: Varios
# Roberto Andrade Fonseca (c)
# Inicio: 7 de agosto de 2019
# Para: Avignon
###
import chart_studio.plotly
#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.offline as offline
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Read in data from csv file
# Usamos el CSV modificado para contar con registros únicos
data_file = "/home/randrade/proyectos/zorro_abarrotero/dev/db/datasets/data_promedios_calificaciones.csv"
#df = pd.read_csv(data_file,index_col=2)
df = pd.read_csv(data_file)
#df = df.sort_values(by=['Tienda'])
#dimension='Atención en cajas'
#dimension='Orden y limpieza'
#df = df.loc[df['cadena_id'] == 1, ['cadena','nombre_tienda', 'dimension','mediciones', 'promedio']]
#Using external css from chriddyp from plotly for ease
app = dash.Dash(__name__)
server = app.server
#app.css.append_css({
#    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#})

left_margin = 200
right_margin = 100

colors = {
    'background': 'white',
    'text': 'gray'
}

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

#df = df.loc[df['dimension'] == dimension]

#print(df)
cadenas=pd.Series(df['cadena']).sort_values().unique()
dimensiones=pd.Series(df['dimension']).sort_values().unique()
#print(cadenas)
#df = df.loc[df['Cadena'] == 'Zorro Abarrotero']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1('Proyecto Zorro Abarrotero'),
    html.H3('Análisis de Calificaciones por Dimensión'),
    
    html.H3('Seleccione una Cadena'),
    dcc.RadioItems(
        id='cadena',
        options=[{'label': i, 'value': i} for i in cadenas],
        value='Zorro Abarrotero'
#        labelStyle={'display': 'inline-block'}
     ),
#    html.Div(id='display-cadena'),
#    dcc.Graph(id='heatmap_output')
#    ], style = {'textAlign':'center','backgroundColor': colors['background'], 'color': colors['text']}
#    ),

#app.layout = html.Div([
    html.H3('Seleccione una Dimensión'),
    dcc.RadioItems(
        id='dimension',
        options=[{'label': j, 'value': j} for j in dimensiones],
        value='Atención en cajas'
    ),

    html.Button(id='submit-button', children='Submit'),
         html.Div(id='output-state'),

    dcc.Slider(
        min=0,
        max=9,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
        value=5,
    ),
], style={'columnCount': 1})

#@app.callback(Output('output-state', 'children'),
#    [Input('submit-button', id, id)]
#    )

#def update_output(id, id):
#    df = df 
#    return {
#    html.H4(children='Calificaciones'),
#    generate_table(df)
#    }   


if __name__ == '__main__':
    app.run_server(debug=True)
