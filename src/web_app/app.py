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
from datetime import date
import requests
from datetime import timedelta
import plotly.io as pio
import os
from flask_caching import Cache
import app_vars as av

pio.templates.default = "plotly_dark"

external_stylesheets = [dbc.themes.CYBORG]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

server = app.server

cache = Cache(
    server,
    config={
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_URL": os.environ.get("REDIS_URL", "redis://localhost:6379"),
    },
)


TIMEOUT = 3600


@cache.memoize(timeout=TIMEOUT)
def collect_data():
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

    return (confirmed_global, deaths_global, recovered_global, country_cases)


@cache.memoize(timeout=TIMEOUT)
def get_today_and_yesterday_data():
    today_data = requests.get("https://corona.lmao.ninja/v2/all?yesterday")
    today_country_data = requests.get(
        "https://corona.lmao.ninja/v2/countries?yesterday&sort"
    )

    today_data = today_data.json()
    today_country_data = today_country_data.json()

    return today_data, today_country_data


(
    today_data,
    today_country_data,
) = get_today_and_yesterday_data()

(
    av.confirmed_global,
    av.deaths_global,
    av.recovered_global,
    av.country_cases,
) = collect_data()

confirmed_global, deaths_global, recovered_global, country_cases = (
    av.confirmed_global,
    av.deaths_global,
    av.recovered_global,
    av.country_cases,
)

country_cases_sorted = country_cases.sort_values("confirmed", ascending=False)

# Importing these modules later as they rely on having data stored

import animations
import map
import prophet

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

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

world_timeseries_confirmed = animations.get_world_timeseries(confirmed_global)
world_timeseries_deaths = animations.get_world_timeseries(deaths_global)
world_timeseries_recovered = animations.get_world_timeseries(recovered_global)

confirmed_global_cases_today = format(today_data["cases"], ",d")
confirmed_recovered_cases_today = format(today_data["deaths"], ",d")
confirmed_deaths_cases_today = format(today_data["recovered"], ",d")

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

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
                                dbc.Row(html.H4("Today"), className="ml-3 mt-2"),
                                dbc.Row(html.H5(id="today"), className="ml-3 mb-2"),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#2f09ed",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Week"), className="ml-3 mt-2"),
                                dbc.Row(
                                    [
                                        html.H5(id="lastweek"),
                                        html.Span(
                                            id="lastweek-diff", style={"color": "red"}
                                        ),
                                    ],
                                    className="ml-3 mb-2",
                                ),
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
                                dbc.Row(
                                    [
                                        html.H5(id="lastmonth"),
                                        html.Span(
                                            id="lastmonth-diff", style={"color": "red"}
                                        ),
                                    ],
                                    className="ml-3 mb-2",
                                ),
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

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

country_page = html.Div(
    children=[
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[
                        {"label": country_name, "value": country_name}
                        for country_name in country_list
                    ],
                    value="India",
                    style={"color": "black"},
                ),
            ),
            className="m-5",
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
                dcc.Loading(
                    dcc.Graph(id="metric-output-country"), id="map-loading-country"
                ),
                width=12,
            ),
            className="mt-5 justify-content-center",
        ),
        dbc.Row(html.H3("Time Series"), className="mt-5 justify-content-center"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="timeseries-output-country"),
                        id="ts-loading-country",
                    ),
                    sm=12,
                    md=12,
                    lg=8,
                    xl=8,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Row(html.H4("Today"), className="ml-3 mt-2"),
                                dbc.Row(
                                    html.H5(id="today-country"), className="ml-3 mb-2"
                                ),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#2f09ed",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Week"), className="ml-3 mt-2"),
                                dbc.Row(
                                    [
                                        html.H5(id="lastweek-country"),
                                        html.Span(
                                            id="lastweek-country-diff",
                                            style={"color": "red"},
                                        ),
                                    ],
                                    className="ml-3 mb-2",
                                ),
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
                                dbc.Row(
                                    [
                                        html.H5(id="lastmonth-country"),
                                        html.Span(
                                            id="lastmonth-country-diff",
                                            style={"color": "red"},
                                        ),
                                    ],
                                    className="ml-3 mb-2",
                                ),
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
    className="m-5",
)

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

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

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

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


@app.callback(
    dash.dependencies.Output("today", "children"),
    [
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    ],
)
def update_today(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "confirmed" in changed_id:
        return confirmed_global_cases_today
    elif "recoveries" in changed_id:
        return confirmed_recovered_cases_today
    elif "deaths" in changed_id:
        return confirmed_deaths_cases_today
    else:
        return confirmed_global_cases_today


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
        return format(lastweek_cases, ",d")
    elif "recoveries" in changed_id:
        ts = animations.get_world_timeseries(recovered_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return format(lastweek_cases, ",d")
    elif "deaths" in changed_id:
        ts = animations.get_world_timeseries(deaths_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return format(lastweek_cases, ",d")
    else:
        ts = animations.get_world_timeseries(confirmed_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return format(lastweek_cases, ",d")


@app.callback(
    dash.dependencies.Output("lastweek-diff", "children"),
    [
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    ],
)
def update_lastweek_diff(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    lastweek = today - timedelta(weeks=1)
    if "confirmed" in changed_id:
        ts = animations.get_world_timeseries(confirmed_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return format(today_data["cases"] - lastweek_cases, ",d")
    elif "recoveries" in changed_id:
        ts = animations.get_world_timeseries(recovered_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return format(today_data["recovered"] - lastweek_cases, ",d")
    elif "deaths" in changed_id:
        ts = animations.get_world_timeseries(deaths_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return format(today_data["deaths"] - lastweek_cases, ",d")
    else:
        ts = animations.get_world_timeseries(confirmed_global)
        lastweek_cases = ts.at[lastweek.strftime("%m/%d/%y"), "Cases"]
        return format(today_data["cases"] - lastweek_cases, ",d")


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
        return format(lastmonth_cases, ",d")
    elif "recoveries" in changed_id:
        ts = animations.get_world_timeseries(recovered_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return format(lastmonth_cases, ",d")
    elif "deaths" in changed_id:
        ts = animations.get_world_timeseries(deaths_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return format(lastmonth_cases, ",d")
    else:
        ts = animations.get_world_timeseries(confirmed_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return format(lastmonth_cases, ",d")


@app.callback(
    dash.dependencies.Output("lastmonth-diff", "children"),
    [
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    ],
)
def update_lastmonth_diff(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    lastmonth = today - timedelta(days=30)
    if "confirmed" in changed_id:
        ts = animations.get_world_timeseries(confirmed_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return format(today_data["cases"] - lastmonth_cases, ",d")
    elif "recoveries" in changed_id:
        ts = animations.get_world_timeseries(recovered_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return format(today_data["recovered"] - lastmonth_cases, ",d")
    elif "deaths" in changed_id:
        ts = animations.get_world_timeseries(deaths_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return format(today_data["deaths"] - lastmonth_cases, ",d")
    else:
        ts = animations.get_world_timeseries(confirmed_global)
        lastmonth_cases = ts.at[lastmonth.strftime("%m/%d/%y"), "Cases"]
        return format(today_data["cases"] - lastmonth_cases, ",d")


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

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
        dash.dependencies.Input("country-dropdown", "value"),
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    ],
)
def update_timeseries_country(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "confirmed" in changed_id:
        return animations.static_line(confirmed_global, "confirmed", value)
    elif "recoveries" in changed_id:
        return animations.static_line(recovered_global, "recovered", value)
    elif "deaths" in changed_id:
        return animations.static_line(deaths_global, "deaths", value)
    else:
        return animations.static_line(confirmed_global, "confirmed", value)


@app.callback(
    dash.dependencies.Output("today-country", "children"),
    [
        dash.dependencies.Input("country-dropdown", "value"),
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    ],
)
def update_today_country(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    cases = 0
    recovered = 0
    deaths = 0
    for country in today_country_data:
        if country["country"] == value:
            cases = country["cases"]
            recovered = country["recovered"]
            deaths = country["deaths"]
    cases = format(cases, ",d")
    recovered = format(recovered, ",d")
    deaths = format(deaths, ",d")
    if "confirmed" in changed_id:
        return cases
    elif "recoveries" in changed_id:
        return recovered
    elif "deaths" in changed_id:
        return deaths
    else:
        return cases


@app.callback(
    dash.dependencies.Output("lastweek-country", "children"),
    [
        dash.dependencies.Input("country-dropdown", "value"),
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    ],
)
def update_lastweek_country(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    lastweek = today - timedelta(weeks=1)
    country_time_series = animations.line_comparison_data(value)
    country_time_series.index = country_time_series["dates"]
    if "confirmed" in changed_id:
        lastweek_cases = country_time_series.at[
            lastweek.strftime("%m/%d/%y"), "confirmed"
        ]
        return format(lastweek_cases, ",d")
    elif "recoveries" in changed_id:
        lastweek_cases = country_time_series.at[
            lastweek.strftime("%m/%d/%y"), "recovered"
        ]
        return format(lastweek_cases, ",d")
    elif "deaths" in changed_id:
        lastweek_cases = country_time_series.at[lastweek.strftime("%m/%d/%y"), "deaths"]
        return format(lastweek_cases, ",d")
    else:
        lastweek_cases = country_time_series.at[
            lastweek.strftime("%m/%d/%y"), "confirmed"
        ]
        return format(lastweek_cases, ",d")


@app.callback(
    dash.dependencies.Output("lastmonth-country", "children"),
    [
        dash.dependencies.Input("country-dropdown", "value"),
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    ],
)
def update_lastmonth_country(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    lastmonth = today - timedelta(days=30)
    country_time_series = animations.line_comparison_data(value)
    country_time_series.index = country_time_series["dates"]
    if "confirmed" in changed_id:
        lastmonth_cases = country_time_series.at[
            lastmonth.strftime("%m/%d/%y"), "confirmed"
        ]
        return format(lastmonth_cases, ",d")
    elif "recoveries" in changed_id:
        lastmonth_cases = country_time_series.at[
            lastmonth.strftime("%m/%d/%y"), "recovered"
        ]
        return format(lastmonth_cases, ",d")
    elif "deaths" in changed_id:
        lastmonth_cases = country_time_series.at[
            lastmonth.strftime("%m/%d/%y"), "deaths"
        ]
        return format(lastmonth_cases, ",d")
    else:
        lastmonth_cases = country_time_series.at[
            lastmonth.strftime("%m/%d/%y"), "confirmed"
        ]
        return format(lastmonth_cases, ",d")


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
