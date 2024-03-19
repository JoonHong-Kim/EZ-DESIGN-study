import asyncio
import threading
from datetime import datetime, timedelta

import dash
import plotly.graph_objs as go
import psutil
from dash import dcc, html
from dash.dependencies import Input, Output

from handlers import log_to_file, log_to_stdout, save_data
from metrics import Metrics

time_range_map = {"15min": 900, "1h": 3600, "3h": 10800, "1d": 86400}


# 로거 설정

# Dash 앱 초기화
app = dash.Dash(__name__)

# 그래프 레이아웃 정의
app.layout = html.Div(
    [
        [html.H1("cpu usage"), dcc.Graph(id="cpu-graph")],
        dcc.Graph(id="memory-graph"),
        dcc.Graph(id="disk-graph"),
        dcc.Interval(id="interval-component", interval=5 * 1000, n_intervals=0),
    ]
)

app.layout = html.Div(
    [
        html.Div(  # make title and middle order
            [
                html.H1("Local Computer Dashboard", style={"textAlign": "center"}),
            ]
        ),
        html.Hr(),
        html.Div(
            [
                dcc.Dropdown(
                    [
                        {"label": "15min", "value": 900},
                        {"label": "1h", "value": 3600},
                        {"label": "3h", "value": 10800},
                        {"label": "1d", "value": 86400},
                    ],
                    900,
                    id="time-range",
                )
            ],
        ),
        html.Div(
            [
                html.H3("cpu usage"),
                dcc.Graph(id="cpu-graph"),
            ]
        ),
        html.Div(
            [
                html.H3("memory usage"),
                dcc.Graph(id="memory-graph"),
            ]
        ),
        html.Div(
            [
                html.H3("disk usage"),
                dcc.Graph(id="disk-graph"),
            ]
        ),
        dcc.Interval(
            id="interval-component",
            interval=5 * 1000,
            n_intervals=0,
        ),
    ]
)


# 그래프 업데이트 함수
@app.callback(
    [
        Output("cpu-graph", "figure"),
        Output("memory-graph", "figure"),
        Output("disk-graph", "figure"),
    ],
    [
        Input(
            "interval-component",
            "n_intervals",
        ),
        Input("time-range", "value"),
    ],
)
def update_graphs(n, v):
    metrics = Metrics()
    db = metrics.metrics
    cpu_data = go.Scatter(
        x=list(db.keys()), y=[v["cpu"] for v in db.values()], mode="lines"
    )
    mem_data = go.Scatter(
        x=list(db.keys()), y=[v["memory"] for v in db.values()], mode="lines"
    )
    disk_data = go.Scatter(
        x=list(db.keys()), y=[v["disk"] for v in db.values()], mode="lines"
    )
    cpu_fig = {
        "data": [cpu_data],
        "layout": go.Layout(
            xaxis=dict(
                dtick=v * 1000 // 8,
                range=[datetime.now() - timedelta(seconds=v), datetime.now()],
            ),
            yaxis=dict(range=[0, 100]),
        ),
    }
    mem_fig = {
        "data": [mem_data],
        "layout": go.Layout(
            xaxis=dict(
                dtick=v * 1000 // 8,
                range=[datetime.now() - timedelta(seconds=v), datetime.now()],
            ),
            yaxis=dict(range=[0, 100]),
        ),
    }
    disk_fig = {
        "data": [disk_data],
        "layout": go.Layout(
            xaxis=dict(
                dtick=v * 1000 // 8,
                range=[datetime.now() - timedelta(seconds=v), datetime.now()],
            ),
            yaxis=dict(range=[0, 100]),
        ),
    }

    return cpu_fig, mem_fig, disk_fig


async def collect_metrics():
    while True:
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage("/").percent
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await asyncio.gather(
            save_data(timestamp, cpu_usage, memory_usage, disk_usage),
            log_to_stdout(timestamp, cpu_usage, memory_usage, disk_usage),
            log_to_file(timestamp, cpu_usage, memory_usage, disk_usage),
        )
        await asyncio.sleep(10)


def run_collect_metrics():
    asyncio.run(collect_metrics())


if __name__ == "__main__":
    threading.Thread(target=run_collect_metrics, daemon=True).start()
    app.run_server(debug=True, use_reloader=False)
