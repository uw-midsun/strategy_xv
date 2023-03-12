import pandas as pd
import plotly
import dash
from dash import html, dcc
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import requests
from constants import *

csv_dir = 'sample_route_step4.csv'
widget = go.FigureWidget()


def init_dash_app(server):
    app = dash.Dash(server=server, routes_pathname_prefix="/dashapp/",
                    external_stylesheets=[dbc.themes.LUX, "https://codepen.io/chriddyp/pen/bWLwgP.css"])

    app.layout = html.Div([html.Div(children=[html.Div(
        [dcc.Graph(id=TRIP_ELEVATION_ID, animate=True, style={'display':'inline-block'}),
         dcc.Interval(id=UPDATE_TRIP_ELEVATION,  # number of milliseconds before the interval fires again
                      interval=5000, n_intervals=0),
         dcc.Graph(id=TRIP_DISTANCE_ID, animate=True, style={'display':'inline-block'}),
         dcc.Interval(id=UPDATE_TRIP_DISTANCE,
                      interval=5000, n_intervals=0),
         dcc.Graph(id=TRIP_LATITUDE_ID, animate=True, style={'display':'inline-block'}),
         dcc.Interval(id=UPDATE_TRIP_LATITUDE,
                      interval=5000, n_intervals=0),
         dcc.Graph(id=TRIP_LONGITUDE_ID, animate=True, style={'display':'inline-block'}),
         dcc.Interval(id=UPDATE_TRIP_LONGITUDE,
                      interval=5000, n_intervals=0), ]),
        ], className='row')], )

    @app.callback(Output(TRIP_ELEVATION_ID, 'figure'), [Input(UPDATE_TRIP_ELEVATION, 'n_intervals')])
    def listening_for_update_elevation(n_interval):
        data = listening_for_update(n_interval, "trip_elevation.csv", "trip(m)", "elevation(m)")
        return data

    @app.callback(Output(TRIP_DISTANCE_ID, 'figure'), [Input(UPDATE_TRIP_DISTANCE, 'n_intervals')])
    def listening_for_update_distance(n_interval):
        data = listening_for_update(n_interval, "trip_distance.csv", "trip(m)", "dist_to_next_coordinate(m)")
        return data

    @app.callback(Output(TRIP_LATITUDE_ID, 'figure'), [Input(UPDATE_TRIP_LATITUDE, 'n_intervals')])
    def listening_for_update_distance(n_interval):
        data = listening_for_update(n_interval, "trip_latitude.csv", "trip(m)", "latitude")
        return data

    @app.callback(Output(TRIP_LONGITUDE_ID, 'figure'), [Input(UPDATE_TRIP_LONGITUDE, 'n_intervals')])
    def listening_for_update_distance(n_interval):
        data = listening_for_update(n_interval, "trip_longitude.csv", "trip(m)", "longitude")
        return data

    def listening_for_update(n_interval, name, x_axis, y_axis):
        n_interval *= 100
        latest_distance = n_interval - 100
        distance = n_interval
        try:
            distance += 100
            fetch_csv(name)
            df = pd.read_csv(name)
            data = plotly.graph_objs.Scatter(x=df[x_axis].iloc[0:distance], y=df[y_axis].iloc[0:distance],
                                             name='Scatter', mode='lines+markers')
            data = update_graph_scatter(distance, name, x_axis, y_axis)
        except:
            data = update_graph_scatter(latest_distance, name)

        return data

    def update_graph_scatter(value, name, x_axis, y_axis):
        fetch_csv(name)
        df = pd.read_csv(name)

        data = plotly.graph_objs.Scatter(x=df[x_axis].iloc[0:value], y=df[y_axis].iloc[0:value],
                                         name='Scatter', mode='lines+markers')
        return {'data': [data],
                'layout': go.Layout(xaxis=dict(range=[min(df[x_axis]), max(df[x_axis])], title=x_axis),
                                   yaxis=dict(range=[min(df[y_axis]), max(df[y_axis])],
                                              title=y_axis), title="MSXV Data: " + str(x_axis) + "-" + str(y_axis))
                }

    def fetch_csv(name):
        data = requests.get('http://127.0.0.1:8000/csv').text
        with open(name, 'w') as f:
            f.write(data)

    return app.server
