import pandas as pd
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import plotly.express as px


csv_dir = 'sample_route_step4.csv'


async def display_graph(csv):
    df = pd.read_csv(csv)
    fig = px.scatter(df, x="polyline_point_index", y="elevation(m)")
    fig.show()


async def graph_thread():
    # Init message
    print('\nPress Ctrl-C to quit at anytime!\n')

    scheduler = AsyncIOScheduler()
    scheduler.add_job(display_graph, "interval", [csv_dir], seconds=5)
    scheduler.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(graph_thread())
    loop.run_forever()