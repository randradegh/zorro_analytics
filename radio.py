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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
cadenas=pd.Series(df['cadena']).sort_values().unique()
dimensiones=pd.Series(df['dimension']).sort_values().unique()
df = df.loc[df['cadena_id'] == 1, ['cadena','nombre_tienda', 'dimension','mediciones', 'promedio']]
app.layout = html.Div([

dcc.RadioItems(
    id='cadena',
    options=[{'label': i, 'value': i} for i in cadenas],
    value='Zorro Abarrotero'
),  

dcc.RadioItems(
    id='dimension',
    options=[{'label': i, 'value': i} for i in dimensiones],
    value='Atención en cajas'
),  

html.Div(id='display-cadena'),

#html.Button(id='submit-button', children='Aceptar'),
#    html.Div(id='output-state'),

], style={'columnCount': 1})

@app.callback(
        Output(component_id='display-cadena', component_property='children'),
        [Input(component_id='my-data', component_property='df')]
),
def update_output(df):
    return {
    html.H4(children='Calificaciones'),
    generate_table(df)
    }   

#def set_cadena_valor(value,value2):
#    return 'La cadena es {} y el dominio {}'.format(value, value2)
#@app.callback(Output('output-state', 'children'),
#    [Input('submit-button',)]
#    )

if __name__ == '__main__':
    app.run_server(debug=True)

