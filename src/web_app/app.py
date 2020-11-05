import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import redis

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dbc.Container(
    dbc.Alert("Hello Bootstrap!", color="success"),
    className="p-5",
)

if __name__ == "__main__":
    app.run_server()
