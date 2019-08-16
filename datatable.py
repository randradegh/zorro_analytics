###
# Variable: Todas 
# Periodo: Datos en la DB
# Proyecto Zorro Abarrotero
# Graph: Varios
# Roberto Andrade Fonseca (c)
# Inicio: 13 de agosto de 2019
# Para: Avignon
###
import chart_studio.plotly
#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.offline as offline
import pandas as pd

import dash_table

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

#df[' index'] = range(1, len(df) + 1)

data_file = "/home/randrade/proyectos/zorro_abarrotero/dev/db/datasets/data_promedios_calificaciones.csv"
df = pd.read_csv(data_file,usecols=['cadena','nombre_tienda', 'dimension','mediciones', 'promedio'])
#df = pd.read_csv(data_file)

#df = df.loc[[:],['cadena','nombre_tienda', 'dimension','mediciones', 'promedio']]
# Generamos las lista de cadenas en el data set
cadenas = df.cadena.unique()
cadenas = (", ".join(map(str, cadenas)))

app = dash.Dash(__name__)
PAGE_SIZE = 20 

colors = {
    'background': 'white',
    'text': 'gray'
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2('Proyecto Zorro'),
    html.H3('Promedio de Calificaciones, 2019'),
    html.Div([
        html.H3('Instrucciones'),
        html.P('Las cadenas existentes son: ' + cadenas + '.'),
        html.P("Puede consultar las dimensiones: 'Surtido y existencia', 'Atención en cajas', 'Orden y limpieza', 'Rapidez', 'Ofertas y precios', 'Trato amable' y 'Seguridad industrial' y 'Calificación Total'."),
        html.P("Debe escribir la cadena o la dimensión de manera correcta y entre comillas simples en 'filter data...' de la columna correspondiente."),
    ]),
    html.Div([
        html.H4('Promedios de calificaciones para los meses de abril, junio y julio de 2019.'),
        html.P(' '),
	dash_table.DataTable(
	    id='table-filtering',
	    columns=[
	        {"name": i, "id": i} for i in df.columns
	    ],
	    page_current=0,
	    page_size=PAGE_SIZE,
	    page_action='custom',
	
	    filter_action='custom',
	    filter_query=''
            ),
    ]),
            ], style = {'width':'80%','textAlign':'center','backgroundColor': colors['background'], 'color': colors['text']}
    )

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-filtering', "data"),
    [Input('table-filtering', "page_current"),
     Input('table-filtering', "page_size"),
     Input('table-filtering', "filter_query")])
def update_table(page_current,page_size, filter):
    print(filter)
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
