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


csv_dir = 'sample_route_step4.csv'
widget = go.FigureWidget()


def init_dash_app(server):
    app = dash.Dash(
            server=server,
            routes_pathname_prefix="/dashapp/",
            external_stylesheets=[
                "/static/dist/css/styles.css",
                "https://fonts.googleapis.com/css?family=Lato",
            ],
        )
    app.layout = html.Div(
        [
            dcc.Graph(id = 'live-graph',
                      animate = True),
            dcc.Input(id='my-id', value=0, type="number"),
            html.Button('Submit', id='submit-val' )
        ]
    )

    @app.callback(
        Output('live-graph', 'figure'),
        [Input('submit-val', 'n_clicks') ],
        State(component_id='my-id', component_property='value')
    )
    def update_graph_scatter(n_clicks, value):
        df = pd.read_csv(csv_dir)

        data = plotly.graph_objs.Scatter(
            x=df["trip(m)"].iloc[0:value],
            y=df["elevation(m)"].iloc[0:value],
            name='Scatter',
            mode='lines+markers'
        )

        return {'data': [data],
                'layout': go.Layout(xaxis=dict(range=[min(df["trip(m)"]),
                                                      max(df["trip(m)"])]), yaxis=dict(range=[min(df["elevation(m)"]), max(df["elevation(m)"])]), )}
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
