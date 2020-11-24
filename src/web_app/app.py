"""
# App
This file contains the source code for the web app made with plotly dash
"""

# Imports and data preprocessing

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pyarrow as pa
import redis
from datetime import datetime
import plotly.io as pio

pio.templates.default = "plotly_dark"

external_stylesheets = [dbc.themes.CYBORG]

r = redis.Redis()


def collect_data():
    if (
        r.exists("confirmed_global")
        and r.exists("recovered_global")
        and r.exists("deaths_global")
    ):
        return (
            pa.deserialize(r.get("confirmed_global")),
            pa.deserialize(r.get("deaths_global")),
            pa.deserialize(r.get("recovered_global")),
            pa.deserialize(r.get("country_cases")),
        )

    else:
        filenames = [
            "time_series_covid19_confirmed_global.csv",
            "time_series_covid19_deaths_global.csv",
            "time_series_covid19_recovered_global.csv",
        ]

        url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

        confirmed_global = pd.read_csv(url + filenames[0])
        deaths_global = pd.read_csv(url + filenames[1])
        recovered_global = pd.read_csv(url + filenames[2])
        country_cases = pd.read_csv(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
        )

        confirmed_global.drop(columns=["Province/State", "Lat", "Long"], inplace=True)
        deaths_global.drop(columns=["Province/State", "Lat", "Long"], inplace=True)
        recovered_global.drop(columns=["Province/State", "Lat", "Long"], inplace=True)
        country_cases.drop(
            columns=[
                "Last_Update",
                "Incident_Rate",
                "People_Tested",
                "People_Hospitalized",
                "UID",
            ],
            inplace=True,
        )

        confirmed_global.rename(columns={"Country/Region": "country"}, inplace=True)
        deaths_global.rename(columns={"Country/Region": "country"}, inplace=True)
        recovered_global.rename(columns={"Country/Region": "country"}, inplace=True)

        country_cases.rename(
            columns={
                "Country_Region": "country",
                "Confirmed": "confirmed",
                "Deaths": "deaths",
                "Recovered": "recovered",
                "Active": "active",
                "Mortality_Rate": "mortality",
            },
            inplace=True,
        )

        confirmed_global = confirmed_global.groupby(["country"], as_index=False).sum()
        deaths_global = deaths_global.groupby(["country"], as_index=False).sum()
        recovered_global = recovered_global.groupby(["country"], as_index=False).sum()

        confirmed_global.at[178, "5/20/20"] = 251667

        r.set(
            "confirmed_global", pa.serialize(confirmed_global).to_buffer().to_pybytes()
        )
        r.expire("confirmed_global", 43200)
        r.set("deaths_global", pa.serialize(deaths_global).to_buffer().to_pybytes())
        r.expire("deaths_global", 43200)
        r.set(
            "recovered_global", pa.serialize(recovered_global).to_buffer().to_pybytes()
        )
        r.expire("recovered_global", 43200)
        r.set("country_cases", pa.serialize(country_cases).to_buffer().to_pybytes())
        r.expire("country_cases", 43200)

        return (confirmed_global, deaths_global, recovered_global, country_cases)


confirmed_global, deaths_global, recovered_global, country_cases = collect_data()
country_cases_sorted = country_cases.sort_values("confirmed", ascending=False)

# Importing these modules later as they rely on having data stored in redis

import map
import animations
import prophet
import app_vars as av

# Main app starts here

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Making the Graphs Required for the Pages

animations_figure = animations.animated_barchart(df=confirmed_global)

confirmed = dict(study="confirmed", color="blue")
recovered = dict(study="recovered", color="pink")
deaths = dict(study="deaths", color="red")

columns = ["country", ["deaths", "confirmed", "recovered"], "Lat", "Long_"]

world_map = map.plot_study(country_cases_sorted, columns, confirmed)
confirmed_timeseries = animations.plot_world_timeseries(confirmed_global)
deaths_timeseries = animations.plot_world_timeseries(deaths_global)
recovered_timeseries = animations.plot_world_timeseries(recovered_global)

# Making the Individual Pages

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Global Situation", href="/global")),
        dbc.NavItem(dbc.NavLink("Country Analysis", href="/country")),
        dbc.NavItem(dbc.NavLink("Preventive Measures", href="/prevent")),
    ],
    dark=True,
    color="dark",
    brand="Covidash",
    brand_href="/",
)

home_page = dbc.Container(
    children=[
        html.Img(
            src="https://www.fda.gov/files/covid19-1600x900.jpg",
            height="35%",
            width="80%",
        ),
        dcc.Markdown(av.covid_19, className="mt-5"),
    ],
    className="mt-5",
)

global_page = html.Div(
    children=[
        dcc.Dropdown(
            id="metric",
            options=[
                {"label": "Confirmed Cases", "value": "Confirmed"},
                {"label": "Recoveries", "value": "Recoveries"},
                {"label": "Deaths", "value": "Deaths"},
            ],
            value="Confirmed",
            style={"fontSize": 22, "margin": "10px"},
        ),
        dbc.Row(dcc.Graph(id="metric-output"), className="mt-5 justify-content-center"),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=confirmed_timeseries), className="m-3"),
                dbc.Col(dcc.Graph(figure=deaths_timeseries), className="m-3"),
                dbc.Col(dcc.Graph(figure=recovered_timeseries), className="m-3"),
            ]
        ),
    ],
    className="mt-5 justify-content-center text-center",
)

country_page = dbc.Container(
    children=[html.H1("This is the individual country analysis page")]
)

preventive_page = dbc.Container(
    children=[
        html.Img(
            src="https://images.pexels.com/photos/3735769/pexels-photo-3735769.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260",
            height="35%",
            width="80%",
        ),
        dcc.Markdown(av.safety, className="mt-5"),
    ],
)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), navbar, html.Div(id="page-content")]
)

# Defining the Callbacks


# @app.callback(
#     dash.dependencies.Output("metric-output", "figure"),
#     [
#         dash.dependencies.Input("confirmed", "n_clicks"),
#         dash.dependencies.Input("recoveries", "n_clicks"),
#         dash.dependencies.Input("deaths", "n_clicks"),
#     ],
# )
# def update_graph(btn1, btn2, btn3):
#     changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
#     if "confirmed" in changed_id:
#         return map.plot_study(country_cases_sorted, columns, confirmed)
#     elif "recoveries" in changed_id:
#         return map.plot_study(country_cases_sorted, columns, recovered)
#     elif "deaths" in changed_id:
#         return map.plot_study(country_cases_sorted, columns, deaths)
#     else:
#         return map.plot_study(country_cases_sorted, columns, confirmed)


@app.callback(
    dash.dependencies.Output("metric-output", "figure"),
    [dash.dependencies.Input("metric", "value")],
)
def update_graph(value):
    if value == "Confirmed":
        return map.plot_study(country_cases_sorted, columns, confirmed)
    elif value == "Recoveries":
        return map.plot_study(country_cases_sorted, columns, recovered)
    elif value == "Deaths":
        return map.plot_study(country_cases_sorted, columns, deaths)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname):
    if pathname == "/":
        return home_page
    elif pathname == "/global":
        return global_page
    elif pathname == "/country":
        return country_page
    elif pathname == "/prevent":
        return preventive_page


if __name__ == "__main__":
    app.run_server()
