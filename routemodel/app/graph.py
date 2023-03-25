import pandas as pd
import plotly
import dash
# import async_dash
import asyncio
import random
from dash import html, dcc
from dash.dependencies import Output, Input
from dash_extensions import WebSocket
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import requests
from constants import *
import json
import ast

csv_dir = 'sample_route_step4.csv'
widget = go.FigureWidget()


def init_dash_app(server):
    app = dash.Dash(server=server, routes_pathname_prefix="/dashapp/",
                    external_stylesheets=[dbc.themes.LUX, "https://codepen.io/chriddyp/pen/bWLwgP.css"],
                    prevent_initial_callbacks=True)

    def update_graph(message):
        if not message:
            return {}
        else:
            json_data = message['data']
            json_data = json.loads(json_data)
            data = plotly.graph_objs.Scatter(x=json_data['datas']['x'], y=json_data['datas']['y'], name='Scatter',
                                             mode='lines+markers')
            return {'data':[data], 'layout':go.Layout(
                xaxis=dict(range=[min(json_data['layout']['x_axis_range']), max(json_data['layout']['x_axis_range'])],
                           title=json_data['layout']['x_axis_title']),
                yaxis=dict(range=[min(json_data['layout']['y_axis_range']), max(json_data['layout']['y_axis_range'])],
                           title=json_data['layout']['y_axis_title']), title="MSXV Data")
                    }

    app.layout = html.Div([html.Div(children=[html.Div(
        [
          dcc.Graph(id=TRIP_ELEVATION_ID, animate=True, style={'display':'inline-block'}),
         WebSocket(id=UPDATE_TRIP_ELEVATION, url="ws://127.0.0.1:5000/trip_elevation"),
         dcc.Graph(id=TRIP_DISTANCE_ID, animate=True, style={'display':'inline-block'}),
         WebSocket(id=UPDATE_TRIP_DISTANCE, url="ws://127.0.0.1:5000/trip_distance"),
         dcc.Graph(id=TRIP_LATITUDE_ID, animate=True, style={'display':'inline-block'}),
         WebSocket(id=UPDATE_TRIP_LATITUDE, url="ws://127.0.0.1:5000/trip_latitude"),
         dcc.Graph(id=TRIP_LONGITUDE_ID, animate=True, style={'display':'inline-block'}),
         WebSocket(id=UPDATE_TRIP_LONGITUDE, url="ws://127.0.0.1:5000/trip_longitude"), ]),
        ], className='row')], )

    @app.callback(Output(TRIP_ELEVATION_ID, 'figure'), [Input(UPDATE_TRIP_ELEVATION, 'message')])
    def listening_for_update_elevation(message):
        data = update_graph(message)
        return data

    @app.callback(Output(TRIP_DISTANCE_ID, 'figure'), [Input(UPDATE_TRIP_DISTANCE, 'message')])
    def listening_for_update_distance(message):
        data = update_graph(message)
        return data

    @app.callback(Output(TRIP_LATITUDE_ID, 'figure'), [Input(UPDATE_TRIP_LATITUDE, 'message')])
    def listening_for_update_latitude(message):
        data = update_graph(message)
        return data

    @app.callback(Output(TRIP_LONGITUDE_ID, 'figure'), [Input(UPDATE_TRIP_LONGITUDE, 'message')])
    def listening_for_update_longitude(message):
        data = update_graph(message)
        return data


    return app.server
