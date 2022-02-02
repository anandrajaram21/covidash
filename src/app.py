# Imports and data preprocessing
from dash import *
from dash_bootstrap_components._components.Col import Col
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
import pickle
import json
from fake_useragent import UserAgent

pio.templates.default = "plotly_dark"

external_stylesheets = [dbc.themes.CYBORG]

temp_user_agent = UserAgent()
header = {'User-Agent': temp_user_agent.random}
district_list=[]
dist_id=[]
for code in range(1,40):
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(code), headers=header)
    json_data = json.loads(response.text)
    for i in json_data["districts"]:
        district_list.append(i['district_name'])
        dist_id.append(i['district_id'])



app = Dash(
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
    filenames = [
        "time_series_covid19_confirmed_global.csv",
        "time_series_covid19_deaths_global.csv",
        "time_series_covid19_recovered_global.csv",
    ]
    url = av.main_url
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

    country_cases_sorted = country_cases.sort_values("confirmed", ascending=False)
    country_cases_sorted.index = [x for x in range(len(country_cases_sorted))]

    return (confirmed_global, deaths_global, recovered_global, country_cases_sorted)


@cache.memoize(timeout=TIMEOUT)
def get_today_data():
    today_data = requests.get("https://corona.lmao.ninja/v2/all?yesterday")
    today_country_data = requests.get("https://corona.lmao.ninja/v2/jhucsse")

    today_data = today_data.json()
    today_country_data = today_country_data.json()

    return today_data, today_country_data


def cases_object(array):
    obj1 = {
        study: sum([(i["stats"][study]) for i in array if i["stats"][study]])
        for study in ["confirmed", "deaths", "recovered"]
    }
    return {**obj1, "updatedAt": [i["updatedAt"] for i in array]}


def choose_country(array, country):
    return [i for i in array if (i["country"] == country)]


def get_final_object(country, array):
    return cases_object(choose_country(array, country))


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

av.country_cases_sorted = av.country_cases

(
    confirmed_global,
    deaths_global,
    recovered_global,
    country_cases,
    country_cases_sorted,
) = (
    av.confirmed_global,
    av.deaths_global,
    av.recovered_global,
    av.country_cases,
    av.country_cases_sorted,
)

# Importing these modules later as they rely on having data stored

import animations
import maps
import country_visuals as cv
import timeseries

import cnn

# Making the Graphs and Declaring the Variables Required for the Pages

animations_figure = animations.animated_barchart(confirmed_global, "confirmed")

confirmed = dict(study="confirmed", color="#45a2ff")
recovered = dict(study="recovered", color="#42f587")
deaths = dict(study="deaths", color="#f54842")

columns = ["country", ["deaths", "confirmed", "recovered"], "Lat", "Long_"]

world_map = maps.plot_study(country_cases_sorted, columns, confirmed)

confirmed_timeseries = timeseries.plot_world_timeseries(
    confirmed_global, "confirmed", n=-20, daily=True
)

country_list = confirmed_global["country"]

today = date.today()

world_timeseries_confirmed = timeseries.get_world_timeseries(confirmed_global)
world_timeseries_deaths = timeseries.get_world_timeseries(deaths_global)
world_timeseries_recovered = timeseries.get_world_timeseries(recovered_global)

confirmed_global_cases_today = format(today_data["cases"], ",d")
confirmed_recovered_cases_today = format(today_data["recovered"], ",d")
confirmed_deaths_cases_today = format(today_data["deaths"], ",d")

# Making the Individual Pages

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Global Situation", href="/global")),
        dbc.NavItem(dbc.NavLink("Country Analysis", href="/country")),
        dbc.NavItem(dbc.NavLink("Forecasts", href="/forecast")),
        dbc.NavItem(dbc.NavLink("Preventive Measures", href="/prevent")),
        dbc.NavItem(dbc.NavLink("Vaccination", href="/vaccine")),
    ],
    dark=True,
    color="dark",
    brand="Covidash",
    brand_href="/",
)

home_page = dbc.Container(
    children=[
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(
                                            src=av.img1,
                                            height="100%",
                                            width="100%",
                                            style={"border-radius": "2rem"},
                                        ),
                                        sm=12,
                                        md=8,
                                        lg=9,
                                    ),
                                    dbc.Col(
                                        [
                                            html.H4(
                                                "Save yourself",
                                                style={
                                                    "text-align": "left",
                                                    "padding-top": "5%",
                                                    "font-size": "1.4rem",
                                                },
                                            ),
                                            html.H4(
                                                "Save the world.",
                                                style={
                                                    "text-align": "left",
                                                    "font-size": "1.4rem",
                                                },
                                            ),
                                            html.Br(),
                                            html.P(
                                                av.covid_19,
                                                style={"text-align": "left"},
                                            ),
                                            html.Br(),
                                            dbc.Button(
                                                "Preventive Measures",
                                                color="danger",
                                                className="mr-1",
                                                style={"border-radius": "1rem"},
                                                id="prevent-button",
                                                href="/prevent",
                                            ),
                                        ],
                                        sm=12,
                                        md=4,
                                        lg=3,
                                    ),
                                ],
                            ),
                        ],
                        className="clearfix",
                    )
                ]
            ),
            style={
                "width": "100%",
                "display": "flex",
                "flex": "1 1 auto",
                "margin-top": "5%",
                "margin-bottom": "5%",
                "border-radius": "2rem",
                "background-color": "#060606",
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "Symptoms of COVID-19",
                                    className="card-title",
                                    style={
                                        "text-align": "center",
                                        "font-weight": "bold",
                                    },
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(
                                                    src=av.img2,
                                                    height="100%",
                                                    width="100%",
                                                    className="img-fluid",
                                                    style={
                                                        "padding-bottom": "10%",
                                                        "border-radius": "5rem",
                                                    },
                                                ),
                                                sm=8,
                                                lg=6,
                                                md=12,
                                                style={
                                                    "display": "flex",
                                                    "align-items": "center",
                                                },
                                            ),
                                            dbc.Col(
                                                html.P(
                                                    av.symptoms,
                                                    style={
                                                        "text-align": "left",
                                                        "font-size": "large",
                                                    },
                                                ),
                                                sm=12,
                                                md=12,
                                                lg=6,
                                                style={
                                                    "display": "flex",
                                                    "align-items": "center",
                                                },
                                            ),
                                        ]
                                    ),
                                    className="clearfix",
                                ),
                            ]
                        ),
                        style={
                            "width": "100%",
                            "display": "flex",
                            "flex": "1 1 auto",
                            "margin-top": "5%",
                            "margin-bottom": "5%",
                            "border-radius": "2rem",
                            "background-color": "#f5f5f5",
                            "color": "black",
                        },
                    ),
                    lg=8,
                    md=8,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "Treatment",
                                    className="card-title",
                                    style={
                                        "text-align": "center",
                                        "font-weight": "bold",
                                    },
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(
                                                    src=av.img3,
                                                    height="100%",
                                                    width="100%",
                                                    className="img-fluid",
                                                    style={
                                                        "padding-bottom": "10%",
                                                        "border-radius": "5rem",
                                                    },
                                                ),
                                                sm=8,
                                                lg=6,
                                                md=12,
                                            ),
                                            dbc.Col(
                                                html.P(
                                                    av.treatment,
                                                    style={
                                                        "text-align": "left",
                                                        "font-size": "large",
                                                    },
                                                ),
                                                sm=12,
                                                md=12,
                                                lg=6,
                                                style={
                                                    "display": "flex",
                                                    "align-items": "center",
                                                },
                                            ),
                                        ]
                                    ),
                                    className="clearfix",
                                ),
                            ]
                        ),
                        style={
                            "width": "100%",
                            "display": "flex",
                            "flex": "1 1 auto",
                            "margin-top": "5%",
                            "margin-bottom": "5%",
                            "border-radius": "2rem",
                            "background-color": "#f5f5f5",
                            "color": "black",
                        },
                    ),
                    lg=8,
                    md=8,
                    sm=12,
                ),
            ],
            style={"justify-content": "center"},
        ),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H5(
                                                "Global Situation",
                                                className="card-title",
                                                style={"text-align": "center"},
                                            ),
                                            html.P(
                                                "See the statistics for the global situation",
                                                className="card-text text-center",
                                            ),
                                            dbc.Button(
                                                "Global Situation",
                                                href="/global",
                                                style={
                                                    "text-align": "center",
                                                    "background-color": "#322daa",
                                                    "border-color": "transparent",
                                                    "border-radius": "1rem",
                                                },
                                                className="mr-1",
                                                # block=True,
                                            ),
                                        ]
                                    ),
                                ],
                                style={
                                    "border-radius": "2rem",
                                    "border-color": "#322daa",
                                    "background-color": "#000000",
                                    "border-style": "solid",
                                    "border-width": "medium",
                                },
                                inverse=True,
                                className="mb-4",
                            ),
                            sm=12,
                            md=12,
                            lg=4,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H5(
                                                "Country Analysis",
                                                className="card-title",
                                                style={"text-align": "center"},
                                            ),
                                            html.P(
                                                "See the statistics for your country",
                                                className="card-text text-center",
                                            ),
                                            dbc.Button(
                                                "Country Analysis",
                                                href="/country",
                                                style={
                                                    "text-align": "center",
                                                    "background-color": "#322daa",
                                                    "border-color": "transparent",
                                                    "border-radius": "1rem",
                                                },
                                                className="mr-1",
                                                # block=True,
                                            ),
                                        ]
                                    ),
                                ],
                                style={
                                    "border-radius": "2rem",
                                    "border-color": "#322daa",
                                    "background-color": "#000000",
                                    "border-style": "solid",
                                    "border-width": "medium",
                                },
                                inverse=True,
                            ),
                            sm=12,
                            md=12,
                            lg=4,
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H5(
                                                "Forecasts",
                                                className="card-title",
                                                style={"text-align": "center"},
                                            ),
                                            html.P(
                                                "Generate forecasts for your country",
                                                className="card-text text-center",
                                            ),
                                            dbc.Button(
                                                "Forecast",
                                                href="/forecast",
                                                style={
                                                    "text-align": "center",
                                                    "background-color": "#322daa",
                                                    "border-color": "transparent",
                                                    "border-radius": "1rem",
                                                },
                                                className="mr-1",
                                                #block=True,
                                            ),
                                        ]
                                    ),
                                ],
                                style={
                                    "border-radius": "2rem",
                                    "border-color": "#322daa",
                                    "background-color": "#000000",
                                    "border-style": "solid",
                                    "border-width": "medium",
                                },
                                inverse=True,
                            ),
                            sm=12,
                            md=12,
                            lg=4,
                        ),
                    ],
                    className="mb-4",
                ),
            ],
        ),
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
                        #block=True,
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
                        #block=True,
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
                        #block=True,
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
                                "backgroundColor": "#8634eb",
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
                                "backgroundColor": "#8634eb",
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
                        #block=True,
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
                        #block=True,
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
                        #block=True,
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
                                "backgroundColor": "#8634eb",
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
                                "backgroundColor": "#8634eb",
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
                        #block=True,
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
                        #block=True,
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
                        #block=True,
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


vaccine_page = html.Div(
    [
        dbc.Row(
            dbc.Col(
                 dcc.Input(
            id="dtrue", type="number",
            debounce=True, placeholder="Enter Your Age",min=15, max=110,
            style={"text-align":"center","width":"100%"}
        ),
            ),
            className="m-5",
        ),
            dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="vaccine-dropdown",
                    options=[
                        {"label": district_list[i], "value": dist_id[i]}
                        for i in range(1,len(district_list))
                    ],
                    value=265,
                    style={"color": "black","text-align":"center"},
                ),
            ),
            className="m-5",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Check Vaccination Slots",
                        size="lg",
                        id="check-vaccine",
                        color="primary",
                        #block=True,
                    ),
                    sm=12,
                    md=12,
                    lg=4,
                    xl=4,
                    className="mb-4 d-grid gap-2 col-6 mx-auto"
                ),
            ],
            className="mt-5 justify-content-center",
        ),
        dbc.Row(
            id="vacc",
            className="mt-5 justify-content-center",
        ),
    ],
    className="m-5",
)

preventive_page = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "Wash Your Hands",
                                    className="card-title",
                                    style={
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "color": "black",
                                    },
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(
                                                    src=av.pcloud1,
                                                    height="100%",
                                                    width="100%",
                                                    className="img-fluid",
                                                    style={
                                                        "padding-bottom": "10%",
                                                        "border-radius": "5rem",
                                                    },
                                                ),
                                                sm=8,
                                                lg=6,
                                                md=8,
                                                style={
                                                    "display": "flex",
                                                    "align-items": "center",
                                                },
                                            ),
                                            dbc.Col(
                                                html.P(
                                                    av.wash,
                                                    style={
                                                        "text-align": "left",
                                                        "font-size": "large",
                                                    },
                                                ),
                                                sm=12,
                                                md=12,
                                                lg=6,
                                                style={
                                                    "display": "flex",
                                                    "align-items": "center",
                                                },
                                            ),
                                        ]
                                    ),
                                    className="clearfix",
                                ),
                            ]
                        ),
                        style={
                            "width": "100%",
                            "display": "flex",
                            "flex": "1 1 auto",
                            "margin-top": "5%",
                            "margin-bottom": "5%",
                            "border-radius": "2rem",
                            "background-color": "#f5f5f5",
                            "color": "black",
                        },
                    ),
                    lg=8,
                    md=8,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "Clean Surfaces In Contact",
                                    className="card-title",
                                    style={
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "color": "black",
                                    },
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(
                                                    src=av.pcloud2,
                                                    height="100%",
                                                    width="100%",
                                                    className="img-fluid",
                                                    style={
                                                        "padding-bottom": "10%",
                                                        "border-radius": "5rem",
                                                    },
                                                ),
                                                sm=8,
                                                lg=6,
                                                md=8,
                                            ),
                                            dbc.Col(
                                                html.P(
                                                    av.clean,
                                                    style={
                                                        "text-align": "left",
                                                        "font-size": "large",
                                                    },
                                                ),
                                                sm=12,
                                                md=12,
                                                lg=6,
                                                style={
                                                    "display": "flex",
                                                    "align-items": "center",
                                                },
                                            ),
                                        ]
                                    ),
                                    className="clearfix",
                                ),
                            ]
                        ),
                        style={
                            "width": "100%",
                            "display": "flex",
                            "flex": "1 1 auto",
                            "margin-top": "5%",
                            "margin-bottom": "5%",
                            "border-radius": "2rem",
                            "background-color": "#f5f5f5",
                            "color": "black",
                        },
                    ),
                    lg=8,
                    md=8,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "Always Cover Your Mouth",
                                    className="card-title",
                                    style={
                                        "text-align": "center",
                                        "font-weight": "bold",
                                        "color": "black",
                                    },
                                ),
                                html.Div(
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Img(
                                                    src=av.pcloud3,
                                                    height="100%",
                                                    width="100%",
                                                    className="img-fluid",
                                                    style={
                                                        "padding-bottom": "10%",
                                                        "border-radius": "5rem",
                                                    },
                                                ),
                                                sm=8,
                                                lg=6,
                                                md=8,
                                            ),
                                            dbc.Col(
                                                html.P(
                                                    av.mask,
                                                    style={
                                                        "text-align": "left",
                                                        "font-size": "large",
                                                    },
                                                ),
                                                sm=12,
                                                md=12,
                                                lg=6,
                                                style={
                                                    "display": "flex",
                                                    "align-items": "center",
                                                },
                                            ),
                                        ]
                                    ),
                                    className="clearfix",
                                ),
                            ]
                        ),
                        style={
                            "width": "100%",
                            "display": "flex",
                            "flex": "1 1 auto",
                            "margin-top": "5%",
                            "margin-bottom": "5%",
                            "border-radius": "2rem",
                            "background-color": "#f5f5f5",
                            "color": "black",
                        },
                    ),
                    lg=8,
                    md=8,
                    sm=12,
                ),
            ],
            style={"justify-content": "center"},
        ),
        dbc.Row(
            [
                # dbc.Col(
                #     html.Img(
                #         src=av.pcloud4,
                #         height="60%",
                #         width="90%",
                #         style={"margin-top": "25%", "width": "125%"},
                #     ),
                #     align="start",
                #     width=3,
                # ),
                # dbc.Col(
                #     html.Img(
                #         src=av.pcloud5,
                #         width="100%",
                #     ),
                #     align="center",
                #     width=6,
                # ),
                # dbc.Col(
                #     html.Img(
                #         src=av.pcloud6,
                #         height="45%",
                #         width="100%",
                #         style={"float": "right"},
                #     ),
                #     align="end",
                #     width=3,
                # ),
            ]
        ),
    ],
)

   
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), navbar, html.Div(id="page-content")]
)

# Callbacks for the Global Situation Page

# Updates the message on top of the page
@app.callback(
    dependencies.Output("global-message", "children"),
    dependencies.Input("confirmed", "n_clicks"),
    dependencies.Input("recoveries", "n_clicks"),
    dependencies.Input("deaths", "n_clicks"),
)
def update_message(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
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


# Updates the huge world map, the animation, and the time series on the page
@app.callback(
    dependencies.Output("metric-output", "figure"),
    dependencies.Output("animation-output", "figure"),
    dependencies.Output("timeseries-output", "figure"),
    dependencies.Input("confirmed", "n_clicks"),
    dependencies.Input("recoveries", "n_clicks"),
    dependencies.Input("deaths", "n_clicks"),
)
@cache.memoize(timeout=TIMEOUT)
def update_graphs(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

    if "confirmed" in changed_id:
        return (
            maps.plot_study(country_cases_sorted, columns, confirmed),
            animations.animated_barchart(df=confirmed_global, name="confirmed"),
            timeseries.plot_world_timeseries(
                confirmed_global, "confirmed", n=-20, daily=True
            ),
        )
    elif "recoveries" in changed_id:
        return (
            maps.plot_study(country_cases_sorted, columns, recovered),
            animations.animated_barchart(df=recovered_global, name="recovered"),
            timeseries.plot_world_timeseries(
                recovered_global, "recovered", n=-20, daily=True
            ),
        )
    elif "deaths" in changed_id:
        return (
            maps.plot_study(country_cases_sorted, columns, deaths),
            animations.animated_barchart(df=deaths_global, name="deaths"),
            timeseries.plot_world_timeseries(
                deaths_global, "deaths", n=-20, daily=True
            ),
        )
    else:
        return (
            maps.plot_study(country_cases_sorted, columns, confirmed),
            animations.animated_barchart(df=confirmed_global, name="confirmed"),
            timeseries.plot_world_timeseries(
                confirmed_global, "confirmed", n=-20, daily=True
            ),
        )


# Updates the text and stats on the page
@app.callback(
    dependencies.Output("today", "children"),
    dependencies.Output("lastweek", "children"),
    dependencies.Output("lastweek-diff", "children"),
    dependencies.Output("lastmonth", "children"),
    dependencies.Output("lastmonth-diff", "children"),
    dependencies.Input("confirmed", "n_clicks"),
    dependencies.Input("recoveries", "n_clicks"),
    dependencies.Input("deaths", "n_clicks"),
)
@cache.memoize(timeout=TIMEOUT)
def update_cases(btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

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
            "+" + format(today_data["cases"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "+" + format(today_data["cases"] - lastmonth_cases, ",d"),
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
            "+" + format(today_data["recovered"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "+" + format(today_data["recovered"] - lastmonth_cases, ",d"),
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
            "+" + format(today_data["deaths"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "+" + format(today_data["deaths"] - lastmonth_cases, ",d"),
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
            "+" + format(today_data["cases"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "+" + format(today_data["cases"] - lastmonth_cases, ",d"),
        )


# Callbacks for the Country Analysis Page

# Updates the message on top of the page for the country selected in the dropdown
@app.callback(
    dependencies.Output("country-message", "children"),
    dependencies.Input("country-dropdown", "value"),
    dependencies.Input("confirmed-country", "n_clicks"),
    dependencies.Input("recoveries-country", "n_clicks"),
    dependencies.Input("deaths-country", "n_clicks"),
)
def update_country_message(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
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


# Updates the graphs shown on the page for the country chosen in the dropdown
@app.callback(
    dependencies.Output("metric-output-country", "figure"),
    dependencies.Output("timeseries-output-country", "figure"),
    dependencies.Input("country-dropdown", "value"),
    dependencies.Input("confirmed-country", "n_clicks"),
    dependencies.Input("recoveries-country", "n_clicks"),
    dependencies.Input("deaths-country", "n_clicks"),
)
def update_graphs_country(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

    if "confirmed-country" in changed_id:
        try:
            return (
                maps.plot_country(value, today_country_data, "Confirmed"),
                timeseries.plot_timeseries(
                    value,
                    timeseries.get_new_cases,
                    "Confirmed Cases",
                    n=-20,
                    daily=True,
                ),
            )
        except:
            return (
                maps.plot_study(country_cases_sorted, columns, confirmed, value),
                timeseries.plot_timeseries(
                    value,
                    timeseries.get_new_cases,
                    "Confirmed Cases",
                    n=-20,
                    daily=True,
                ),
            )
    elif "recoveries-country" in changed_id:
        try:
            return (
                maps.plot_country(value, today_country_data, "Recoveries"),
                timeseries.plot_timeseries(
                    value,
                    timeseries.get_new_recoveries,
                    "Recoveries",
                    n=-20,
                    daily=True,
                ),
            )
        except:
            return (
                maps.plot_study(country_cases_sorted, columns, recovered, value),
                timeseries.plot_timeseries(
                    value,
                    timeseries.get_new_recoveries,
                    "Recoveries",
                    n=-20,
                    daily=True,
                ),
            )
    elif "deaths-country" in changed_id:
        try:
            return (
                maps.plot_country(value, today_country_data, "Deaths"),
                timeseries.plot_timeseries(
                    value,
                    timeseries.get_new_deaths,
                    "Deaths",
                    n=-20,
                    daily=True,
                ),
            )
        except:
            return (
                maps.plot_study(country_cases_sorted, columns, deaths, value),
                timeseries.plot_timeseries(
                    value,
                    timeseries.get_new_deaths,
                    "Deaths",
                    n=-20,
                    daily=True,
                ),
            )
    else:
        try:
            return (
                maps.plot_country(value, today_country_data, "Confirmed"),
                timeseries.plot_timeseries(
                    value,
                    timeseries.get_new_cases,
                    "Confirmed Cases",
                    n=-20,
                    daily=True,
                ),
            )
        except:
            return (
                maps.plot_study(country_cases_sorted, columns, confirmed, value),
                timeseries.plot_timeseries(
                    value,
                    timeseries.get_new_cases,
                    "Confirmed Cases",
                    n=-20,
                    daily=False,
                ),
            )


# Update the stats shown on the page
@app.callback(
    dependencies.Output("today-country", "children"),
    dependencies.Output("lastweek-country", "children"),
    dependencies.Output("lastweek-country-diff", "children"),
    dependencies.Output("lastmonth-country", "children"),
    dependencies.Output("lastmonth-country-diff", "children"),
    dependencies.Input("country-dropdown", "value"),
    dependencies.Input("confirmed-country", "n_clicks"),
    dependencies.Input("recoveries-country", "n_clicks"),
    dependencies.Input("deaths-country", "n_clicks"),
)
def update_cases_country(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]

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
            "+" + format(country_stats["confirmed"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "+" + format(country_stats["confirmed"] - lastmonth_cases, ",d"),
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
            "+" + format(country_stats["recovered"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "+" + format(country_stats["recovered"] - lastmonth_cases, ",d"),
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
            "+" + format(country_stats["deaths"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "+" + format(country_stats["deaths"] - lastmonth_cases, ",d"),
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
            "+" + format(country_stats["confirmed"] - lastweek_cases, ",d"),
            format(lastmonth_cases, ",d"),
            "+" + format(country_stats["confirmed"] - lastmonth_cases, ",d"),
        )


@app.callback(
    dependencies.Output("stats-graph", "children"),
    dependencies.Output("stats-table", "children"),
    dependencies.Input("country-dropdown", "value"),
    dependencies.Input("confirmed-country", "n_clicks"),
    dependencies.Input("recoveries-country", "n_clicks"),
    dependencies.Input("deaths-country", "n_clicks"),
)
def update_stats(value, btn1, btn2, btn3):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    country_stats = maps.get_country_frame(
        maps.choose_country(today_country_data, value)
    )

    try:
        if "confirmed-country" in changed_id:
            return (
                dcc.Graph(
                    figure=cv.plot_province(
                        country_stats, "Confirmed", "Confirmed Cases"
                    )
                ),
                dbc.Table.from_dataframe(
                    cv.table_province_data(country_stats, "Confirmed"),
                    striped=True,
                    bordered=True,
                    hover=True,
                ),
            )
        elif "recoveries-country" in changed_id:
            return (
                dcc.Graph(
                    figure=cv.plot_province(country_stats, "Recoveries", "Recoveries")
                ),
                dbc.Table.from_dataframe(
                    cv.table_province_data(country_stats, "Recoveries"),
                    striped=True,
                    bordered=True,
                    hover=True,
                ),
            )
        elif "deaths-country" in changed_id:
            return (
                dcc.Graph(figure=cv.plot_province(country_stats, "Deaths", "Deaths")),
                dbc.Table.from_dataframe(
                    cv.table_province_data(country_stats, "Deaths"),
                    striped=True,
                    bordered=True,
                    hover=True,
                ),
            )
        else:
            return (
                dcc.Graph(
                    figure=cv.plot_province(
                        country_stats, "Confirmed", "Confirmed Cases"
                    )
                ),
                dbc.Table.from_dataframe(
                    cv.table_province_data(country_stats, "Confirmed"),
                    striped=True,
                    bordered=True,
                    hover=True,
                ),
            )
    except:
        return (
            html.H5(
                "Sorry! Unfortunately we do not have sufficient data at the moment."
            ),
            None,
        )


# Callbacks for the Forecasts Page


@app.callback(
    dependencies.Output("predictions-graph", "children"),
    dependencies.Output("predictions-table", "children"),
    dependencies.Input("forecast-confirmed", "n_clicks"),
    dependencies.Input("forecast-recoveries", "n_clicks"),
    dependencies.Input("forecast-deaths", "n_clicks"),
    dependencies.State("country-dropdown-prediction", "value"),
    prevent_initial_call=True,

)


@app.callback(
    dependencies.Output("vacc", "children"),
    dependencies.Input("check-vaccine", "n_clicks"),
    dependencies.Input("vaccine-dropdown", "value"),
    dependencies.Input("dtrue", "value"),
    prevent_initial_call=True,

)
def check_slot(value,children,age):
    print("AGE IS",age)
    # print('CHECK SLOT VALUE IS:',value)
    # print('CHECK SLOT CHILDREN IS:',children)
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    print(changed_id)
    if "check-vaccine" in changed_id:
        DIST_ID = children
        # Print available centre description (y/n)?
        print_flag = 'y'

        numdays = 20
        base = datetime.datetime.today()
        date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
        date_str = [x.strftime("%d-%m-%Y") for x in date_list]

        print('DIST_ID',DIST_ID)
        for INP_DATE in date_str:
            print(INP_DATE)
            URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={DIST_ID}&date={INP_DATE}"
            print("URL",URL)
            response = requests.get(URL, headers=header)
            print(response)
            if response.ok:
                resp_json = response.json()
                print('Here')
                L=[]
                D={}
                # print(json.dumps(resp_json, indent = 1))
                if resp_json["centers"]:
                    print("Available on: {}".format(INP_DATE))
                    if(print_flag=='y' or print_flag=='Y'):
                        for center in resp_json["centers"]:
                            for session in center["sessions"]:
                                # print('SESSION')
                                print(session)
                                if session["min_age_limit"] <= age:
                                    print("\t", center["name"])
                                    D['Name']= center["name"]
                                    print("\t", center["block_name"])
                                    D['Block_Name']= center["block_name"]
                                    print("\t Price: ", center["fee_type"])
                                    D['Price']=center['fee_type']
                                    print("\t Available Capacity: ", session["available_capacity"])
                                    if(session["vaccine"] != ''):
                                        print("\t Vaccine: ", session["vaccine"])
                                        D['Vaccine']=session["vaccine"]
                                        # D['Address']=session['address']
                                        Time=[]
                                        for i in session['slots']:
                                            Time.append(i+'\n')
                                        D['Time']=Time
                                        D['Date']=session['date']
                                        D['available']=session['available_capacity']
                                    L.append(dict(D))
                                    print("\n\n")
                      
                else:
                    print("No available slots on {}".format(INP_DATE))
                    L=None
                return [dbc.Col(dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.P(
                                                x['Name']),
                                            html.P(
                                                x['Block_Name']),
                                                html.P(x['Vaccine']),
                                                html.P(x['Date']),
                                                html.P(x['Price']),
                                                html.P(x['Time']),
                                                dbc.Col(

                                                html.Img(
                                                    src="https://api.pcloud.com/getpubthumb?code=XZyfAnXZjGYa5SIIYkFc5jBUTYY13j6c3VOV&linkpassword=undefined&size=524x476&crop=0&type=auto" if x['available'] else "https://img.pngio.com/wrong-multicolor-icon-with-png-and-vector-format-for-free-wrong-png-512_512.png",
                                                    height="20%",
                                                    width="20%",
                                                    className="img-fluid",
                                                    style={
                                                        "float":"right"
                                                    },
                                                ),
                                                sm=12,
                                                lg=12,
                                                md=12,
                                                style={
                                                    "text-align": "center",
                                                },
                                            ),
                                            html.Br(),
                                        ],
                                        sm=12,
                                        md=12,
                                        lg=12,
                                    ),
                                ],
                            ),
                        ],
                        className="clearfix",
                    )
                ]
            ),
            style={
                "width": "100%",
                "display": "flex",
                "flex": "1 1 auto",
                "align-items":'end',
                "margin-top": "5%",
                "margin-bottom": "5%",
                "border-radius": "2rem",
                "background-color": "white",
                'color':'black'
            },
        ), sm=12,
                            md=12,
                            lg=4, ) for x in L]
                




def forecast_cases(btn1, btn2, btn3, value):
    changed_id = [p["prop_id"] for p in callback_context.triggered][0]
    if "forecast-confirmed" in changed_id:
        try:
            response = requests.get(
                f"https://github.com/anandrajaram21/covidash/raw/main/output/{value}-confirmed.pkl"
            )
            with open("temp.pkl", "wb") as fh:
                fh.write(response.content)
            with open("temp.pkl", "rb") as fh:
                data = pickle.load(fh)
                return (
                    dcc.Graph(figure=data["fig"]),
                    dbc.Table.from_dataframe(
                        data["predictions"], striped=True, bordered=True, hover=True
                    ),
                )
            os.remove("temp.pkl")
        except:
            preds, _, fig = cnn.cnn_predict("confirmed", value)
            return (
                dcc.Graph(figure=fig),
                dbc.Table.from_dataframe(
                    preds, striped=True, bordered=True, hover=True
                ),
            )
    elif "forecast-recoveries" in changed_id:
        try:
            response = requests.get(
                f"https://github.com/anandrajaram21/covidash/raw/main/output/{value}-recovered.pkl"
            )
            with open("temp.pkl", "wb") as fh:
                fh.write(response.content)
            with open("temp.pkl", "rb") as fh:
                data = pickle.load(fh)
                return (
                    dcc.Graph(figure=data["fig"]),
                    dbc.Table.from_dataframe(
                        data["predictions"], striped=True, bordered=True, hover=True
                    ),
                )
            os.remove("temp.pkl")
        except:
            preds, _, fig = cnn.cnn_predict("recovered", value)
            return (
                dcc.Graph(figure=fig),
                dbc.Table.from_dataframe(
                    preds, striped=True, bordered=True, hover=True
                ),
            )
    elif "forecast-deaths" in changed_id:
        try:
            response = requests.get(
                f"https://github.com/anandrajaram21/covidash/raw/main/output/{value}-deaths.pkl"
            )
            with open("temp.pkl", "wb") as fh:
                fh.write(response.content)
            with open("temp.pkl", "rb") as fh:
                data = pickle.load(fh)
                return (
                    dcc.Graph(figure=data["fig"]),
                    dbc.Table.from_dataframe(
                        data["predictions"], striped=True, bordered=True, hover=True
                    ),
                )
            os.remove("temp.pkl")
        except:
            preds, _, fig = cnn.cnn_predict("deaths", value)
            return (
                dcc.Graph(figure=fig),
                dbc.Table.from_dataframe(
                    preds, striped=True, bordered=True, hover=True
                ),
            )


@app.callback(
    dependencies.Output("page-content", "children"),
    [dependencies.Input("url", "pathname")],
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
    elif pathname == "/vaccine":
        return vaccine_page


if __name__ == "__main__":
    app.run_server()