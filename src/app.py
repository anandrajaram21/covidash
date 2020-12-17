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
import plotly.graph_objects as go
import pandas as pd
from datetime import date
import requests
from datetime import timedelta
import plotly.io as pio
import os
from flask_caching import Cache
import app_vars as av
import time
import datetime

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
        "CACHE_TYPE": "simple",
    },
)


TIMEOUT = 3600

@cache.memoize(timeout=TIMEOUT)
def collect_data():
    # try:
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

    # confirmed_global.to_csv("confirmed_global.csv",index = False)
    # deaths_global.to_csv("deaths_global.csv",index = False)
    # recovered_global.to_csv("recovered_global.csv",index = False)
    # country_cases.to_csv("country_cases.csv",index = False)

    return (confirmed_global, deaths_global, recovered_global, country_cases)

    # except:
        # #pass
        # return (
                # pd.read_csv("confirmed_global.csv"),
                # pd.read_csv("deaths_global.csv"),
                # pd.read_csv("recovered_global.csv"),
                # pd.read_csv("country_cases.csv")
            # )

@cache.memoize(timeout=TIMEOUT)           
def get_today_data():
    today_data = requests.get("https://corona.lmao.ninja/v2/all?yesterday")
    today_country_data = requests.get("https://corona.lmao.ninja/v2/jhucsse")

    today_data = today_data.json()
    today_country_data = today_country_data.json()

    return today_data, today_country_data


def cases_object(array):
    obj1 = {
        study: sum([(i["stats"][study]) for i in array])
        for study in ["confirmed", "deaths", "recovered"]
    }
    return {**obj1, "updatedAt": [i["updatedAt"] for i in array]}


def choose_country(array, country):
    return [i for i in array if (i["country"] == country)]


def get_final_object(country, array):
    return cases_object(choose_country(array, country))


def plot_province(data, metric, metric_name):
    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=data["Provinces"], y=data[metric])
    )

    fig.update_layout(
        title={
            "text": "Province Details",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        template="plotly_dark",
        xaxis_title="Province",
        yaxis_title="Cases",
    )

    return fig


def table_province_data(data, metric):
    df = pd.DataFrame(data={"Provinces": data["Provinces"], metric: data[metric]})
    df[metric] = df[metric].map(lambda x: format(x, ",d"))
    if len(df) <= 1:
        return
    else:
        return df


(
    today_data,
    today_country_data,
) = get_today_data()

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
import new_map_functions as nmf
import cnn

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
confirmed_recovered_cases_today = format(today_data["recovered"], ",d")
confirmed_deaths_cases_today = format(today_data["deaths"], ",d")

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
        dbc.NavItem(dbc.NavLink("Forecasts", href="/forecast")),
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
        dcc.Markdown(av.covid_19, className="m-5"),
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
        dbc.Row(html.H3(id="global-message"), className="mt-5 justify-content-center"),
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
                                "backgroundColor": "#5a1791",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Week"), className="ml-3 mt-2"),
                                dbc.Row(
                                    [
                                        html.H5(id="lastweek"),
                                        html.H5(
                                            id="lastweek-diff",
                                            style={"color": "red"},
                                            className="ml-3",
                                        ),
                                    ],
                                    className="ml-3 mb-2",
                                ),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#732abd",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Month"), className="ml-3 mt-2"),
                                dbc.Row(
                                    [
                                        html.H5(id="lastmonth"),
                                        html.H5(
                                            id="lastmonth-diff",
                                            style={"color": "red"},
                                            className="ml-3",
                                        ),
                                    ],
                                    className="ml-3 mb-2",
                                ),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#8634eb",
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
        dbc.Row(html.H3(id="country-message"), className="mt-5 justify-content-center"),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(id="metric-output-country"), id="map-loading-country"
                ),
                width=12,
            ),
            className="mt-5 justify-content-center",
        ),
        dbc.Row(html.H3("Statistics"), className="mt-5 justify-content-center"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(id="stats-graph", className="justify-content-center"),
                    sm=12,
                    md=12,
                    lg=12,
                    xl=12,
                    className="justify-content-center align-items-center",
                ),
            ],
            className="mt-5 justify-content-center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            id="stats-table", className="justify-content-center"
                        ),
                    ],
                    id="stats-table-container",
                    sm=12,
                    md=12,
                    lg=12,
                    xl=12,
                    className="justify-content-center align-items-center",
                ),
            ],
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
                                "backgroundColor": "#5a1791",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Week"), className="ml-3 mt-2"),
                                dbc.Row(
                                    [
                                        html.H5(id="lastweek-country"),
                                        html.H5(
                                            id="lastweek-country-diff",
                                            style={"color": "red"},
                                            className="ml-3",
                                        ),
                                    ],
                                    className="ml-3 mb-2",
                                ),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#732abd",
                            },
                            className="mt-3 p-3",
                        ),
                        html.Div(
                            [
                                dbc.Row(html.H4("Last Month"), className="ml-3 mt-2"),
                                dbc.Row(
                                    [
                                        html.H5(id="lastmonth-country"),
                                        html.H5(
                                            id="lastmonth-country-diff",
                                            style={"color": "red"},
                                            className="ml-3",
                                        ),
                                    ],
                                    className="ml-3 mb-2",
                                ),
                            ],
                            style={
                                "borderRadius": "30px",
                                "backgroundColor": "#8634eb",
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

forecast_page = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="country-dropdown-prediction",
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
            [
                html.H3("Predictions for the Following Week"),
            ],
            className="mt-5 justify-content-center",
        ),
        dbc.Row(
            [
                html.H5(
                    "It can take upto 2 minutes for our bots to generate the predictions.",
                ),
            ],
            className="mt-5 justify-content-center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Forecast confirmed cases",
                        size="lg",
                        id="forecast-confirmed",
                        color="primary",
                        block=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Button(
                        "Forecast recoveries",
                        size="lg",
                        id="forecast-recoveries",
                        color="success",
                        block=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Button(
                        "Forecast Deaths",
                        size="lg",
                        id="forecast-deaths",
                        color="danger",
                        block=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4",
                ),
            ],
            className="mt-5 justify-content-center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(id="predictions-table"),
                    ],
                    id="predictions-table-container",
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="align-items-center",
                ),
                dbc.Col(
                    dcc.Loading(
                        id="predictions-graph",
                    ),
                    id="predictions-graph-container",
                    sm=12,
                    md=12,
                    lg=8,
                    xl=8,
                ),
            ],
            className="mt-5 justify-content-center",
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
            src="https://images.pexels.com/photos/3735769/pexels-photo-3735769.jpeg?auto=comfpress&cs=tinysrgb&dpr=2&h=750&w=1260",
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
    dash.dependencies.Output("global-message", "children"),
    dash.dependencies.Input("confirmed", "n_clicks"),
    dash.dependencies.Input("recoveries", "n_clicks"),
    dash.dependencies.Input("deaths", "n_clicks"),
)
def update_message(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    time_updated = datetime.datetime.fromtimestamp(
        today_data["updated"] / 1000
    ).strftime("%H:%M")
    date_updated = datetime.datetime.fromtimestamp(
        today_data["updated"] / 1000
    ).strftime("%d %B %Y")
    output_str = "Globally, as of {time}, {date}, there have been {cases} {res_str}"

    if "confirmed" in changed_id:
        return output_str.format(
            time=time_updated,
            date=date_updated,
            cases=format(today_data["cases"], ",d"),
            res_str="confirmed cases",
        )
    elif "recoveries" in changed_id:
        return output_str.format(
            time=time_updated,
            date=date_updated,
            cases=format(today_data["recovered"], ",d"),
            res_str="recoveries",
        )
    elif "deaths" in changed_id:
        return output_str.format(
            time=time_updated,
            date=date_updated,
            cases=format(today_data["deaths"], ",d"),
            res_str="deaths",
        )
    else:
        return output_str.format(
            time=time_updated,
            date=date_updated,
            cases=format(today_data["cases"], ",d"),
            res_str="confirmed cases",
        )


@app.callback(
    dash.dependencies.Output("metric-output", "figure"),
    dash.dependencies.Output("animation-output", "figure"),
    dash.dependencies.Output("timeseries-output", "figure"),
    dash.dependencies.Input("confirmed", "n_clicks"),
    dash.dependencies.Input("recoveries", "n_clicks"),
    dash.dependencies.Input("deaths", "n_clicks"),
)
@cache.memoize(timeout=TIMEOUT)
def update_graphs(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    if "confirmed" in changed_id:
        return (
            map.plot_study(country_cases_sorted, columns, confirmed),
            animations.animated_barchart(df=confirmed_global),
            animations.plot_world_timeseries(confirmed_global, "confirmed"),
        )
    elif "recoveries" in changed_id:
        return (
            map.plot_study(country_cases_sorted, columns, recovered),
            animations.animated_barchart(df=recovered_global),
            animations.plot_world_timeseries(recovered_global, "recovered"),
        )
    elif "deaths" in changed_id:
        return (
            map.plot_study(country_cases_sorted, columns, deaths),
            animations.animated_barchart(df=deaths_global),
            animations.plot_world_timeseries(deaths_global, "deaths"),
        )
    else:
        return (
            map.plot_study(country_cases_sorted, columns, confirmed),
            animations.animated_barchart(df=confirmed_global),
            animations.plot_world_timeseries(confirmed_global, "confirmed"),
        )


@app.callback(
    dash.dependencies.Output("today", "children"),
    dash.dependencies.Output("lastweek", "children"),
    dash.dependencies.Output("lastweek-diff", "children"),
    dash.dependencies.Output("lastmonth", "children"),
    dash.dependencies.Output("lastmonth-diff", "children"),
    dash.dependencies.Input("confirmed", "n_clicks"),
    dash.dependencies.Input("recoveries", "n_clicks"),
    dash.dependencies.Input("deaths", "n_clicks"),
)
@cache.memoize(timeout=TIMEOUT)
def update_cases(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    lastweek = today - timedelta(weeks=1)
    lastmonth = today - timedelta(days=30)

    if "confirmed" in changed_id:
        lastweek_cases = world_timeseries_confirmed.at[
            lastweek.strftime("%-m/%-d/%y"), "Cases"
        ]
        lastmonth_cases = world_timeseries_confirmed.at[
            lastmonth.strftime("%-m/%-d/%y"), "Cases"
        ]
        return (
            confirmed_global_cases_today,
            format(lastweek_cases, ",d"),
            "-" + format(today_data["cases"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "-" + format(today_data["cases"] - lastmonth_cases, ",d"),
        )
    elif "recoveries" in changed_id:
        lastweek_cases = world_timeseries_recovered.at[
            lastweek.strftime("%-m/%-d/%y"), "Cases"
        ]
        lastmonth_cases = world_timeseries_recovered.at[
            lastmonth.strftime("%-m/%-d/%y"), "Cases"
        ]
        return (
            confirmed_recovered_cases_today,
            format(lastweek_cases, ",d"),
            "-" + format(today_data["recovered"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "-" + format(today_data["recovered"] - lastmonth_cases, ",d"),
        )
    elif "deaths" in changed_id:
        lastweek_cases = world_timeseries_deaths.at[
            lastweek.strftime("%-m/%-d/%y"), "Cases"
        ]
        lastmonth_cases = world_timeseries_deaths.at[
            lastmonth.strftime("%-m/%-d/%y"), "Cases"
        ]
        return (
            confirmed_deaths_cases_today,
            format(lastweek_cases, ",d"),
            "-" + format(today_data["deaths"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "-" + format(today_data["deaths"] - lastmonth_cases, ",d"),
        )
    else:
        lastweek_cases = world_timeseries_confirmed.at[
            lastweek.strftime("%-m/%-d/%y"), "Cases"
        ]
        lastmonth_cases = world_timeseries_confirmed.at[
            lastmonth.strftime("%-m/%-d/%y"), "Cases"
        ]
        return (
            confirmed_global_cases_today,
            format(lastweek_cases, ",d"),
            "-" + format(today_data["cases"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "-" + format(today_data["cases"] - lastmonth_cases, ",d"),
        )


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# Callbacks for the Country Analysis Page


@app.callback(
    dash.dependencies.Output("country-message", "children"),
    dash.dependencies.Input("country-dropdown", "value"),
    dash.dependencies.Input("confirmed-country", "n_clicks"),
    dash.dependencies.Input("recoveries-country", "n_clicks"),
    dash.dependencies.Input("deaths-country", "n_clicks"),
)
def update_country_message(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    country_stats = get_final_object(value, today_country_data)
    date_obj = datetime.datetime.strptime(
        country_stats["updatedAt"][0], "%Y-%m-%d %H:%M:%S"
    )
    time_updated = date_obj.strftime("%H:%M")
    date_updated = date_obj.strftime("%d %B %Y")
    output_str = (
        "In {country_name}, as of {time}, {date}, there have been {cases} {res_str}"
    )

    if "confirmed-country" in changed_id:
        return output_str.format(
            country_name=value,
            time=time_updated,
            date=date_updated,
            cases=format(country_stats["confirmed"], ",d"),
            res_str="confirmed cases",
        )
    elif "recoveries-country" in changed_id:
        return output_str.format(
            country_name=value,
            time=time_updated,
            date=date_updated,
            cases=format(country_stats["recovered"], ",d"),
            res_str="recoveries",
        )
    elif "deaths-country" in changed_id:
        return output_str.format(
            country_name=value,
            time=time_updated,
            date=date_updated,
            cases=format(country_stats["deaths"], ",d"),
            res_str="deaths",
        )
    else:
        return output_str.format(
            country_name=value,
            time=time_updated,
            date=date_updated,
            cases=format(country_stats["confirmed"], ",d"),
            res_str="confirmed cases",
        )


@app.callback(
    dash.dependencies.Output("metric-output-country", "figure"),
    dash.dependencies.Output("timeseries-output-country", "figure"),
    dash.dependencies.Input("country-dropdown", "value"),
    dash.dependencies.Input("confirmed-country", "n_clicks"),
    dash.dependencies.Input("recoveries-country", "n_clicks"),
    dash.dependencies.Input("deaths-country", "n_clicks"),
)
def update_graphs_country(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    if "confirmed-country" in changed_id:
        try:
            return (
                nmf.plot_country(value, today_country_data, "confirmed"),
                animations.static_line(confirmed_global, "confirmed", value),
            )
        except:
            return (
                map.plot_study(country_cases_sorted, columns, confirmed, value),
                animations.static_line(confirmed_global, "confirmed", value),
            )
    elif "recoveries-country" in changed_id:
        try:
            return (
                nmf.plot_country(value, today_country_data, "recoveries"),
                animations.static_line(confirmed_global, "recovered", value),
            )
        except:
            return (
                map.plot_study(country_cases_sorted, columns, recovered, value),
                animations.static_line(confirmed_global, "recovered", value),
            )
    elif "deaths-country" in changed_id:
        try:
            return (
                nmf.plot_country(value, today_country_data, "deaths"),
                animations.static_line(confirmed_global, "deaths", value),
            )
        except:
            return (
                map.plot_study(country_cases_sorted, columns, deaths, value),
                animations.static_line(confirmed_global, "deaths", value),
            )
    else:
        try:
            return (
                nmf.plot_country(value, today_country_data, "confirmed"),
                animations.static_line(confirmed_global, "confirmed", value),
            )
        except:
            return (
                map.plot_study(country_cases_sorted, columns, confirmed, value),
                animations.static_line(confirmed_global, "confirmed", value),
            )


@app.callback(
    dash.dependencies.Output("today-country", "children"),
    dash.dependencies.Output("lastweek-country", "children"),
    dash.dependencies.Output("lastweek-country-diff", "children"),
    dash.dependencies.Output("lastmonth-country", "children"),
    dash.dependencies.Output("lastmonth-country-diff", "children"),
    dash.dependencies.Input("country-dropdown", "value"),
    dash.dependencies.Input("confirmed-country", "n_clicks"),
    dash.dependencies.Input("recoveries-country", "n_clicks"),
    dash.dependencies.Input("deaths-country", "n_clicks"),
)
def update_cases_country(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

    country_stats = get_final_object(value, today_country_data)
    cases = format(country_stats["confirmed"], ",d")
    recovered = format(country_stats["recovered"], ",d")
    deaths = format(country_stats["deaths"], ",d")

    country_time_series = animations.line_comparison_data(value)
    country_time_series.index = country_time_series["dates"]

    lastweek = today - timedelta(weeks=1)
    lastmonth = today - timedelta(days=30)

    if "confirmed-country" in changed_id:
        lastweek_cases = country_time_series.at[
            lastweek.strftime("%-m/%-d/%y"), "confirmed"
        ]
        lastmonth_cases = country_time_series.at[
            lastmonth.strftime("%-m/%-d/%y"), "confirmed"
        ]
        return (
            cases,
            format(lastweek_cases, ",d"),
            "-" + format(country_stats["confirmed"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "-" + format(country_stats["confirmed"] - lastmonth_cases, ",d"),
        )
    elif "recoveries-country" in changed_id:
        lastweek_cases = country_time_series.at[
            lastweek.strftime("%-m/%-d/%y"), "recovered"
        ]
        lastmonth_cases = country_time_series.at[
            lastmonth.strftime("%-m/%-d/%y"), "recovered"
        ]
        return (
            recovered,
            format(lastweek_cases, ",d"),
            "-" + format(country_stats["recovered"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "-" + format(country_stats["recovered"] - lastmonth_cases, ",d"),
        )
    elif "deaths-country" in changed_id:
        lastweek_cases = country_time_series.at[
            lastweek.strftime("%-m/%-d/%y"), "deaths"
        ]
        lastmonth_cases = country_time_series.at[
            lastmonth.strftime("%-m/%-d/%y"), "deaths"
        ]
        return (
            deaths,
            format(lastweek_cases, ",d"),
            "-" + format(country_stats["deaths"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "-" + format(country_stats["deaths"] - lastmonth_cases, ",d"),
        )
    else:
        lastweek_cases = country_time_series.at[
            lastweek.strftime("%-m/%-d/%y"), "confirmed"
        ]
        lastmonth_cases = country_time_series.at[
            lastmonth.strftime("%-m/%-d/%y"), "confirmed"
        ]
        return (
            cases,
            format(lastweek_cases, ",d"),
            "-" + format(country_stats["confirmed"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "-" + format(country_stats["confirmed"] - lastmonth_cases, ",d"),
        )


@app.callback(
    dash.dependencies.Output("stats-graph", "children"),
    dash.dependencies.Output("stats-table", "children"),
    dash.dependencies.Input("country-dropdown", "value"),
    dash.dependencies.Input("confirmed-country", "n_clicks"),
    dash.dependencies.Input("recoveries-country", "n_clicks"),
    dash.dependencies.Input("deaths-country", "n_clicks"),
)
def update_stats(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    country_stats = nmf.get_country_frame(nmf.choose_country(today_country_data, value))

    try:
        if "confirmed-country" in changed_id:
            return (
                dcc.Graph(
                    figure=plot_province(country_stats, "Confirmed", "Confirmed Cases")
                ),
                dbc.Table.from_dataframe(
                    table_province_data(country_stats, "Confirmed"),
                    striped=True,
                    bordered=True,
                    hover=True,
                ),
            )
        elif "recoveries-country" in changed_id:
            return (
                dcc.Graph(
                    figure=plot_province(country_stats, "Recoveries", "Recoveries")
                ),
                dbc.Table.from_dataframe(
                    table_province_data(country_stats, "Recoveries"),
                    striped=True,
                    bordered=True,
                    hover=True,
                ),
            )
        elif "deaths-country" in changed_id:
            return (
                dcc.Graph(figure=plot_province(country_stats, "Deaths", "Deaths")),
                dbc.Table.from_dataframe(
                    table_province_data(country_stats, "Deaths"),
                    striped=True,
                    bordered=True,
                    hover=True,
                ),
            )
        else:
            return (
                dcc.Graph(
                    figure=plot_province(country_stats, "Confirmed", "Confirmed Cases")
                ),
                dbc.Table.from_dataframe(
                    table_province_data(country_stats, "Confirmed"),
                    striped=True,
                    bordered=True,
                    hover=True,
                ),
            )
    except:
        return (
            html.H5(
                "Sorry! Unfortunately we do no have sufficient data at the moment."
            ),
            None
            # html.H4(
            #     "Sorry! Unfortunately we do no have sufficient data at the moment."
            # ),
        )


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# Callbacks for the Forecasts Page


@app.callback(
    dash.dependencies.Output("predictions-graph", "children"),
    dash.dependencies.Output("predictions-table", "children"),
    dash.dependencies.Input("forecast-confirmed", "n_clicks"),
    dash.dependencies.Input("forecast-recoveries", "n_clicks"),
    dash.dependencies.Input("forecast-deaths", "n_clicks"),
    dash.dependencies.State("country-dropdown-prediction", "value"),
    prevent_initial_call=True,
)
def forecast_cases(btn1, btn2, btn3, value):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "forecast-confirmed" in changed_id:
        fig, err, preds = cnn.cnn_predict("confirmed", value)
        return (
            dcc.Graph(figure=fig),
            dbc.Table.from_dataframe(preds, striped=True, bordered=True, hover=True),
        )
    elif "forecast-recoveries" in changed_id:
        fig, err, preds = cnn.cnn_predict("recovered", value)
        return (
            dcc.Graph(figure=fig),
            dbc.Table.from_dataframe(preds, striped=True, bordered=True, hover=True),
        )
    elif "forecast-deaths" in changed_id:
        fig, err, preds = cnn.cnn_predict("deaths", value)
        return (
            dcc.Graph(figure=fig),
            dbc.Table.from_dataframe(preds, striped=True, bordered=True, hover=True),
        )


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
    elif pathname == "/forecast":
        return forecast_page


if __name__ == "__main__":
    app.run_server()
