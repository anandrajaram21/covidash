# Imports
import app_vars as av
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio
import requests
from itertools import chain
from math import log
from math import e

chart_studio.tools.set_credentials_file(
    username="anirudhlakhotia", api_key="tcCFHV4CoCJaqmLfANU6"
)

mapbox_access_token = "pk.eyJ1IjoiYW5pcnVkaGxha2hvdGlhIiwiYSI6ImNreThyeDl6NDEyeHUyd3BmaWo3Ynp6MTcifQ.o7XgaewOUt_7BPH6F41R0w"

confirmed_global, deaths_global, recovered_global, country_cases_sorted = (
    av.confirmed_global,
    av.deaths_global,
    av.recovered_global,
    av.country_cases_sorted,
)


def chainer(s):
    return list(chain.from_iterable(s.astype(str).str.split(",")))


def convert_df(df, cols):
    df.dropna(inplace=True)
    df.set_index(df[cols[0]].values)

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
    lens = df["New"].astype(str).str.split(",").map(len)

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
    emoji = (
        "💀"
        if study.lower() == "deaths"
        else "😷"
        if study.lower() == "recovered"
        else "🏥"
    )
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
            "style": "dark",
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
    layout["hoverlabel"] = dict(
        font_size=16, font_family="Rockwell", font_color="black"
    )

    return layout


def get_lat_long(country, coord_df=country_cases_sorted):
    lat = float(coord_df.loc[(coord_df["country"] == country), "Lat"])
    long = float(coord_df.loc[(coord_df["country"] == country), "Long_"])
    return lat, long


def get_country_wise_data():
    response = requests.get("https://corona.lmao.ninja/v2/jhucsse")
    data = response.json()
    return data


def choose_country(array, country):
    return [i for i in array if (i["country"] == country)]


def get_country_frame(country):
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
    return df


def interactive_map(data, layout):
    figure = {"data": data, "layout": layout}

    return figure


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


def plot_country(Country, data, study):
    country = choose_country(data, Country)
    df = get_country_frame(country)
    columns = ["Provinces", ["Confirmed", "Recoveries", "Deaths"], "lat", "lon"]
    color = (
        "#45a2ff"
        if study == "Confirmed"
        else "#f54842"
        if study == "Deaths"
        else "#42f587"
    )
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
Examples:
confirmed = dict(study="confirmed", color="#45a2ff")
recovered = dict(study="recovered", color="#42f587")
deaths = dict(study="deaths", color="#f54842")

columns = ["country", ["deaths", "confirmed", "recovered"], "Lat", "Long_"]

figure = plot_study(country_cases_sorted, columns, confirmed)
py.iplot(figure)

figure= plot_country("Japan", get_country_wise_data(), "Recoveries")
py.iplot(figure)
"""