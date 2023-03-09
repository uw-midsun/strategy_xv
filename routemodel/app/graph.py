import pandas as pd
import asyncio
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import plotly.express as px
import time
import atexit
import plotly
import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from flask import Flask, request, render_template
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
            dcc.Graph(id = 'live-graph',
                      animate = True),
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
        print("hello")

        try:
            Distance += 100
            df = pd.read_csv(file)
            data = plotly.graph_objs.Scatter(
                x=df["trip(m)"].iloc[0:distance],
                y=df["elevation(m)"].iloc[0:distance],
                name='Scatter',
                mode='lines+markers'
            )
            data = update_graph_scatter(1, Distance)

        except:
            data = update_graph_scatter(1, latest_distance)

        return data

    # @app.callback(
    #     Output('live-graph', 'figure'),
    #     [Input('submit-val', 'n_clicks') ],
    #     State(component_id='my-id', component_property='value')
    # )
    def update_graph_scatter(n_clicks, value):
        # file = requests.get('http://127.0.0.1:8000/')
        # decoded_content = file.content.decode('utf-8')
        # df = pd.read_csv(file)
        df = pd.read_csv(csv_dir)

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
    return app.server


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_graph_scatter, "interval", [csv_dir], seconds=5)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.run_server()

# NOTE: will probably delete later, kept it just in case this is useful
# async def display_graph(csv):
#     df = pd.read_csv(csv)
#     widget.add_scatter(x=df["polyline_point_index"], y=df["elevation(m)"])
#     # widget.add_scatter(y=[2, 1, 4, 3])
#
#
#
# async def graph_process():
#     # Init message
#     print('\nPress Ctrl-C to quit at anytime!\n')
#
