###
# Variable: Todas 
# Periodo: Datos en la DB
# Proyecto Zorro Abarrotero
# Graph: Varios
# Roberto Andrade Fonseca (c)
# Inicio: lun ago 12 21:20:59 CDT 2019
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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#dimension='Atención en cajas'
dimension='Orden y limpieza'
# Read in data from csv file
# Usamos el CSV modificado para contar con registros únicos
data_file = "/home/randrade/proyectos/zorro_abarrotero/dev/db/datasets/data_promedios_calificaciones.csv"
#df = pd.read_csv(data_file,index_col=2)
df = pd.read_csv(data_file)

df = df.loc[df['cadena_id'] == 1, ['cadena','nombre_tienda', 'dimension','mediciones', 'promedio']]
df = df.loc[df['dimension'] == dimension]

app.layout = html.Div([

    html.H1('Proyecto Zorro Abarrotero'),
    html.H3('Análisis de Calificaciones por Dimensión'),
    
    html.H3('Seleccione una Cadena'),
    dcc.RadioItems(
        id='cadena',
        options=[{'label': i, 'value': i} for i in cadenas],
        value='Zorro Abarrotero'
    )
    html.Div(id='display-table'),

], style={'columnCount': 1})

@app.callback(
        Output(

def generate_table(dataframe, max_rows=15):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns]) ] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash(__name__, )

app.layout = html.Div(children=[
    html.H4(children='Proyecto Zorro'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)
