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
from dash.dependencies import Output, Input
import plotly.graph_objects as go


csv_dir = 'sample_route_step4.csv'
widget = go.FigureWidget()

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph',
                  animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 1000,
            n_intervals = 0
        ),
    ]
)

@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)

def update_graph_scatter(csv):
    df = pd.read_csv(csv_dir)

    data = plotly.graph_objs.Scatter(
        x=df["polyline_point_index"],
        y=df["elevation(m)"],
        name='Scatter',
        mode='lines+markers'
    )

    print("hello")

    return {'data': [data],
            'layout': go.Layout(xaxis=dict(range=[min(df["polyline_point_index"]),
                                                  max(df["polyline_point_index"])]), yaxis=dict(range=[min(df["elevation(m)"]), max(df["elevation(m)"])]), )}


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
