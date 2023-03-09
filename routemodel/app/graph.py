import pandas as pd
import plotly
import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import requests

csv_dir = 'sample_route_step4.csv'
widget = go.FigureWidget()
Distance = 0


def init_dash_app(server):

    app = dash.Dash(
            server=server,
            routes_pathname_prefix="/dashapp/",
            external_stylesheets=[dbc.themes.LUX]
        )

    app.layout = html.Div(
        [
            dcc.Graph(id='live-graph',
                      animate=True),
            dcc.Input(id='my-id', value=0, type="number"),
            html.Button('Submit', id='submit-val' ),
            dcc.Interval(
                id='graph-update',
                # number of milliseconds before the interval fires again
                interval=5000,
                n_intervals=0
            ),

        ]
    )

    @app.callback(
        Output('live-graph', 'figure'),
        [Input('graph-update', 'n_intervals')]
    )
    def listening_for_update(n_interval):
        global Distance
        latest_distance = Distance

        try:
            Distance += 100
            fetch_csv()
            df = pd.read_csv('file.csv')
            data = plotly.graph_objs.Scatter(
                x=df["trip(m)"].iloc[0:Distance],
                y=df["elevation(m)"].iloc[0:Distance],
                name='Scatter',
                mode='lines+markers'
            )
            data = update_graph_scatter(1, Distance)
        except:
            data = update_graph_scatter(1, latest_distance)

        return data

    def update_graph_scatter(n_clicks, value):
        fetch_csv()
        df = pd.read_csv('file.csv')

        data = plotly.graph_objs.Scatter(
            x=df["trip(m)"].iloc[0:value],
            y=df["elevation(m)"].iloc[0:value],
            name='Scatter',
            mode='lines+markers'
        )
        return {'data': [data],
                'layout': go.Layout(xaxis=dict(range=[min(df["trip(m)"]),
                                                      max(df["trip(m)"])], title="Trip (m)"), yaxis=dict(range=[min(df["elevation(m)"]),
                                                                                              max(df["elevation(m)"])], title="Elevation (m)"),
                                    title="MSXV Data")}

    def fetch_csv():
        data = requests.get('http://127.0.0.1:8000/csv').text
        with open('file.csv', 'w') as f:
            f.write(data)

    return app.server


