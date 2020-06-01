# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Analiza danych z Instagrama', style={
        'textAlign': 'center'}),

    dcc.Graph(
        id='like-komments-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [150, 80, 188], 'type': 'bar', 'name': 'komentarze'},
                {'x': [1, 2, 3], 'y': [200, 376, 140], 'type': 'bar', 'name': u'like'},
            ],
            'layout': {
                'title': 'Wyres przedstawiający ilość lików i komentarzy pod poszczególnymi zdjęciami.'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)