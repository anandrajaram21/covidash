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
from datetime import date
from datetime import timedelta
import re
import plotly.io as pio

pio.templates.default = "plotly_dark"

external_stylesheets = [dbc.themes.DARKLY]

r = redis.Redis()


def prettify(amount, separator=","):
    """Separate with predefined separator."""
    orig = str(amount)
    new = re.sub("^(-?\d+)(\d{3})", "\g<1>{0}\g<2>".format(separator), str(amount))
    if orig == new:
        return new
    else:
        return prettify(new)


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
        r.expire("confirmed_global", 3600)
        r.set("deaths_global", pa.serialize(deaths_global).to_buffer().to_pybytes())
        r.expire("deaths_global", 3600)
        r.set(
            "recovered_global", pa.serialize(recovered_global).to_buffer().to_pybytes()
        )
        r.expire("recovered_global", 3600)
        r.set("country_cases", pa.serialize(country_cases).to_buffer().to_pybytes())
        r.expire("country_cases", 3600)

        return (confirmed_global, deaths_global, recovered_global, country_cases)


confirmed_global, deaths_global, recovered_global, country_cases = collect_data()
country_cases_sorted = country_cases.sort_values("confirmed", ascending=False)

# Importing these modules later as they rely on having data stored in redis

import app_vars as av
import animations
import map
import prophet

# Main app starts here

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server

# Making the Graphs and Declaring the Variables Required for the Pages

animations_figure = animations.animated_barchart(confirmed_global)

confirmed = dict(study="confirmed", color="blue")
recovered = dict(study="recovered", color="green")
deaths = dict(study="deaths", color="red")

columns = ["country", ["deaths", "confirmed", "recovered"], "Lat", "Long_"]

world_map = map.plot_study(country_cases_sorted, columns, confirmed)

confirmed_timeseries = animations.plot_world_timeseries(confirmed_global, "confirmed")

country_list = confirmed_global["country"]

today = date.today()

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
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Button(
                        "Confirmed Cases",
                        size="lg",
                        id="confirmed",
                        color="primary",
                        block=True,
                        outline=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Button(
                        "Recoveries",
                        size="lg",
                        id="recoveries",
                        color="success",
                        block=True,
                        outline=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Button(
                        "Deaths",
                        size="lg",
                        id="deaths",
                        color="danger",
                        block=True,
                        outline=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4",
                ),
            ]
        ),
        dbc.Row(html.H3("Global Situation"), className="mt-5 justify-content-center"),
        dbc.Row(
            dbc.Col(
                dcc.Loading(dcc.Graph(id="metric-output"), id="map-loading"), width=12
            ),
            className="mt-5 justify-content-center",
        ),
        dbc.Row(html.H3("Time Series"), className="mt-5 justify-content-center"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(dcc.Graph(id="timeseries-output"), id="ts-loading"),
                    sm=12,
                    md=12,
                    lg=8,
                    xl=8,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Row(html.H4("Yesterday"), className="ml-3 mt-2"),
                                dbc.Row(html.H5(id="yesterday"), className="ml-3 mb-2"),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#4d37ba",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Week"), className="ml-3 mt-2"),
                                dbc.Row(html.H5(id="lastweek"), className="ml-3 mb-2"),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#7156d6",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Month"), className="ml-3 mt-2"),
                                dbc.Row(html.H5(id="lastmonth"), className="ml-3 mb-2"),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#8e6ee6",
                            },
                            className="mt-3 p-3",
                        ),
                    ],
                    className="align-items-center",
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                ),
            ],
            className="mt-5 align-items-center",
        ),
        dbc.Row(html.H3("Animation"), className="mt-5 justify-content-center"),
        dbc.Row(
            dbc.Col(
                dcc.Loading(dcc.Graph(id="animation-output"), id="animation-loading"),
                sm=12,
                md=12,
                lg=12,
                xl=12,
            ),
            className="m-5 justify-content-center align-items-center",
        ),
    ],
    className="m-5",
)

country_page = html.Div(
    children=[
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[
                        {"label": country_name, "value": country_name} for country_name in country_list
                    ],
                    value="India",
                    style={"backgroundColor": "gray", "color": "black"},
                ),
            ),
            className="m-5"
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Button(
                        "Confirmed Cases",
                        size="lg",
                        id="confirmed-country",
                        color="primary",
                        block=True,
                        outline=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Button(
                        "Recoveries",
                        size="lg",
                        id="recoveries-country",
                        color="success",
                        block=True,
                        outline=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Button(
                        "Deaths",
                        size="lg",
                        id="deaths-country",
                        color="danger",
                        block=True,
                        outline=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4",
                ),
            ]
        ),
        dbc.Row(html.H3("Map"), className="mt-5 justify-content-center"),
        dbc.Row(
            dbc.Col(
                dcc.Loading(dcc.Graph(id="metric-output-country"), id="map-loading-country"), width=12
            ),
            className="mt-5 justify-content-center",
        ),
        dbc.Row(html.H3("Time Series"), className="mt-5 justify-content-center"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(dcc.Graph(id="timeseries-output-country"), id="ts-loading-country"),
                    sm=12,
                    md=12,
                    lg=8,
                    xl=8,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Row(html.H4("Yesterday"), className="ml-3 mt-2"),
                                dbc.Row(html.H5(id="yesterday-country"), className="ml-3 mb-2"),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#4d37ba",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Week"), className="ml-3 mt-2"),
                                dbc.Row(html.H5(id="lastweek-country"), className="ml-3 mb-2"),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#7156d6",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Month"), className="ml-3 mt-2"),
                                dbc.Row(html.H5(id="lastmonth-country"), className="ml-3 mb-2"),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#8e6ee6",
                            },
                            className="mt-3 p-3",
                        ),
                    ],
                    className="align-items-center",
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                ),
            ],
            className="mt-5 align-items-center",
        ),
    ],
    className="m-5"
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

# Callbacks for the Global Situation Page

@app.callback(
    dash.dependencies.Output("metric-output", "figure"),
    [
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    ],
)
def update_graph(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "confirmed" in changed_id:
        return map.plot_study(country_cases_sorted, columns, confirmed)
    elif "recoveries" in changed_id:
        return map.plot_study(country_cases_sorted, columns, recovered)
    elif "deaths" in changed_id:
        return map.plot_study(country_cases_sorted, columns, deaths)
    else:
        return map.plot_study(country_cases_sorted, columns, confirmed)


@app.callback(
    dash.dependencies.Output("animation-output", "figure"),
    [
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    ],
)
def update_animation(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "confirmed" in changed_id:
        return animations.animated_barchart(df=confirmed_global)
    elif "recoveries" in changed_id:
        return animations.animated_barchart(df=recovered_global)
    elif "deaths" in changed_id:
        return animations.animated_barchart(df=deaths_global)
    else:
        return animations.animated_barchart(df=confirmed_global)


@app.callback(
    dash.dependencies.Output("timeseries-output", "figure"),
    [
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    ],
)
def update_timeseries(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "confirmed" in changed_id:
        return animations.plot_world_timeseries(confirmed_global, "confirmed")
    elif "recoveries" in changed_id:
        return animations.plot_world_timeseries(recovered_global, "recovered")
    elif "deaths" in changed_id:
        return animations.plot_world_timeseries(deaths_global, "deaths")
    else:
        return animations.plot_world_timeseries(confirmed_global, "confirmed")

# Callbacks for the Country Analysis Page

@app.callback(
    dash.dependencies.Output("metric-output-country", "figure"),
    [
        dash.dependencies.Input("country-dropdown", "value"),
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    ],
)
def update_graph_country(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "confirmed" in changed_id:
        return map.plot_study(country_cases_sorted, columns, confirmed, value)
    elif "recoveries" in changed_id:
        return map.plot_study(country_cases_sorted, columns, recovered, value)
    elif "deaths" in changed_id:
        return map.plot_study(country_cases_sorted, columns, deaths, value)
    else:
        return map.plot_study(country_cases_sorted, columns, confirmed, value)

@app.callback(
    dash.dependencies.Output("timeseries-output-country", "figure"),
    [
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    ],
)
def update_timeseries_country(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "confirmed" in changed_id:
        return animations.plot_world_timeseries(confirmed_global, "confirmed")
    elif "recoveries" in changed_id:
        return animations.plot_world_timeseries(recovered_global, "recovered")
    elif "deaths" in changed_id:
        return animations.plot_world_timeseries(deaths_global, "deaths")
    else:
        return animations.plot_world_timeseries(confirmed_global, "confirmed")

@app.callback(
    dash.dependencies.Output("yesterday", "children"),
    [
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    ],
)
def update_yesterday(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    yesterday = today - timedelta(days=1)
    if "confirmed" in changed_id:
        ts = animations.get_world_timeseries(confirmed_global)
        yest_cases = ts.at[yesterday.strftime("%m/%d/%y"), "Cases"]
        return prettify(yest_cases)
    elif "recoveries" in changed_id:
        ts = animations.get_world_timeseries(recovered_global)
        yest_cases = ts.at[yesterday.strftime("%m/%d/%y"), "Cases"]
        return prettify(yest_cases)
    elif "deaths" in changed_id:
        ts = animations.get_world_timeseries(deaths_global)
        yest_cases = ts.at[yesterday.strftime("%m/%d/%y"), "Cases"]
        return prettify(yest_cases)
    else:
        ts = animations.get_world_timeseries(confirmed_global)
        yest_cases = ts.at[yesterday.strftime("%m/%d/%y"), "Cases"]
        return prettify(yest_cases)


@app.callback(
    dash.dependencies.Output("lastweek", "children"),
    [
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    ],
)
def update_lastweek(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    lastweek = today - timedelta(weeks=1)
    if "confirmed" in changed_id:
        ts = animations.get_world_timeseries(confirmed_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return prettify(lastweek_cases)
    elif "recoveries" in changed_id:
        ts = animations.get_world_timeseries(recovered_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return prettify(lastweek_cases)
    elif "deaths" in changed_id:
        ts = animations.get_world_timeseries(deaths_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return prettify(lastweek_cases)
    else:
        ts = animations.get_world_timeseries(confirmed_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return prettify(lastweek_cases)


@app.callback(
    dash.dependencies.Output("lastmonth", "children"),
    [
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    ],
)
def update_lastmonth(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    lastmonth = today - timedelta(days=30)
    if "confirmed" in changed_id:
        ts = animations.get_world_timeseries(confirmed_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return prettify(lastmonth_cases)
    elif "recoveries" in changed_id:
        ts = animations.get_world_timeseries(recovered_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return prettify(lastmonth_cases)
    elif "deaths" in changed_id:
        ts = animations.get_world_timeseries(deaths_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return prettify(lastmonth_cases)
    else:
        ts = animations.get_world_timeseries(confirmed_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return prettify(lastmonth_cases)


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
