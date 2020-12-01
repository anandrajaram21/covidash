"""
# Map
This file contains the functions required beautiful, interactive maps using Plotly Chart Studio and Mapbox
"""

# Imports
import copy
import sys
import os
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import chart_studio.plotly as py
import chart_studio
from math import log
from math import e
from itertools import chain
import app_vars as av
import requests

pio.templates.default = "plotly_dark"

# Setting up credentials for the map
chart_studio.tools.set_credentials_file(
    username="chartstudiouser", api_key="m9KxT5JPEEukONNW8E50"
)
mapbox_access_token = "pk.eyJ1IjoiY2hhcnRzdHVkaW91c2VyIiwiYSI6ImNrZXd3bTBoNTA4bnYyemw4N3l5aDN5azIifQ.7e-KoC1KMXr_EKbkahgAQQ"

# Getting sorted country cases
confirmed_global, deaths_global, recovered_global, country_cases = (
    av.confirmed_global,
    av.deaths_global,
    av.recovered_global,
    av.country_cases,
)

country_cases_sorted = country_cases.sort_values("confirmed", ascending=False)
country_cases_sorted.index = [x for x in range(len(country_cases_sorted))]


def chainer(s):
    return list(chain.from_iterable(s.str.split(",")))


# Data Preprocessing
def convert_df(df, cols):
    df.dropna(inplace=True)
    df.set_index(df[cols[0]].values)
    df.dropna(inplace=True)

    L = []
    for i in range(len(df)):
        string = ""
        for j in range(len(cols[1])):
            if j != (len(cols[1]) - 1):
                string = string + str(df[cols[1][j]].values[i]) + ","
            else:
                string = string + str(df[cols[1][j]].values[i])

        L.append(string)

    df["New"] = L
    lens = df["New"].str.split(",").map(len)

    df = pd.DataFrame(
        {
            "Country": np.repeat(df[cols[0]], lens),
            "Lat": np.repeat(df[cols[-2]], lens),
            "Long_": np.repeat(df[cols[-1]], lens),
            "Count": chainer(df["New"]),
        }
    )
    df["Study"] = [cols[1][i] for i in range(len(cols[1]))] * (
        len(df.index) // len(cols[1])
    )

    return df


def create_hovertemplate(df, study, country):
    emoji = "💀" if study == "deaths" else "😷" if study == "recovered" else "🏥"
    return f"{emoji}: {format(int(float(df.loc[(df['Study'] == study) & (df['Country'] == country), 'Count'])),',d')}"


def create_data(df, study, color):
    countries = list(df["Country"].value_counts().index)
    data = []
    df.dropna(inplace=True)

    for country in countries:
        try:
            event_data = dict(
                lat=df.loc[(df["Study"] == study) & (df["Country"] == country), "Lat"],
                lon=df.loc[
                    (df["Study"] == study) & (df["Country"] == country), "Long_"
                ],
                name=f"{country}",
                marker={
                    "size": log(
                        float(
                            df.loc[
                                (df["Study"] == study) & (df["Country"] == country),
                                "Count",
                            ]
                        ),
                        1.5,
                    ),
                    "opacity": 0.5,
                    "color": color,
                },
                type="scattermapbox",
                hovertemplate=create_hovertemplate(df, study, country),
            )
            data.append(event_data)
        except:
            continue

    return data


# Graphing
def create_basic_layout(latitude, longitude, zoom):
    layout = {
        "height": 700,
        "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
        "font": {"color": "#FFFFFF", "size": 15},
        "paper_bgcolor": "#000000",
        "showlegend": False,
        "mapbox": {
            "accesstoken": mapbox_access_token,
            "bearing": 0,
            "center": {"lat": latitude, "lon": longitude},
            "pitch": 0,
            "zoom": zoom,
            "style": "satellite-streets",
        },
    }
    return layout


def update_layout(study, layout):
    annotations = [
        {
            "text": f"{study.capitalize()} Cases",
            "font": {"color": "#FFFFFF", "size": 14},
            "borderpad": 10,
            "x": 0.05,
            "y": 0.05,
            "xref": "paper",
            "yref": "paper",
            "align": "left",
            "showarrow": False,
            "bgcolor": "black",
        }
    ]

    layout["title"] = f"{study.capitalize()}"
    layout["annotations"] = annotations
    layout["hoverlabel"] = dict(font_size=16, font_family="Rockwell")

    return layout


def interactive_map(data, layout):
    figure = {"data": data, "layout": layout}

    return figure


def get_lat_long(country, coord_df=country_cases_sorted):
    lat = float(coord_df.loc[(coord_df["country"] == country), "Lat"])
    long = float(coord_df.loc[(coord_df["country"] == country), "Long_"])
    return lat, long


def plot_study(
    starting_df,
    cols,
    study_dict,
    location="global",
    zoom=2,
    latitude=20.59,
    longitude=78.96,
):
    color = study_dict["color"]
    study = study_dict["study"]
    df = convert_df(starting_df, cols)
    data = create_data(df, study, color)
    layout = create_basic_layout(latitude, longitude, zoom)
    updated_layout = update_layout(study, layout)
    figure = interactive_map(data, updated_layout)
    return figure


def get_country_wise_data():
    response = requests.get("https://corona.lmao.ninja/v2/jhucsse")
    data = response.json()
    return data


def choose_country(array, country):
    return [i for i in array if (i["country"] == country)]


def plot_country(Country, data, study):
    country = choose_country(data, Country)

    def get(string, country):
        return [i[string] for i in country]

    coords = get("coordinates", country)
    stats = get("stats", country)
    names = get("province", country)

    def make_column(string, main):
        return [i[string] for i in main]

    df = pd.DataFrame()
    df["Provinces"] = names
    df["lat"] = make_column("latitude", coords)
    df["lon"] = make_column("longitude", coords)
    df["Confirmed"] = make_column("confirmed", stats)
    df["Recoveries"] = make_column("recovered", stats)
    df["Deaths"] = make_column("deaths", stats)
    df = df[df["Provinces"] != "Unknown"]
    columns = ["Provinces", ["Confirmed", "Recoveries", "Deaths"], "lat", "lon"]
    color = "blue" if study == "confirmed" else "red" if study == "deaths" else "green"
    d = dict(study=study.title(), color=color)
    figure = plot_study(
        df,
        columns,
        d,
        country,
        zoom=4.5,
        latitude=get_lat_long(Country)[0],
        longitude=get_lat_long(Country)[1],
    )
    return figure


"""
Example:

confirmed = dict(study="confirmed",color="blue
recovered = dict(study="recovered",color="pink")
deaths = dict(study="deaths",color="red")

columns = ["country", ["deaths", "confirmed", "recovered"], "Lat", "Long_"]

figure = plot_study(country_cases_sorted, columns, confirmed, "Japan")
py.iplot(figure)





example for country wise 

figure= plot_country("US",get_country_wise_data(),"deaths")
py.iplot(figure)
"""
