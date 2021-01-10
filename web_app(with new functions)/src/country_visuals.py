# Imports
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import plotly.graph_objects as go


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


def plot_province(data, metric, metric_name):
    fig = go.Figure()

    fig.add_trace(go.Bar(x=data["Provinces"], y=data[metric]))

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


"""
Examples:
today_data, today_country_data = get_today_data()
country_stats = get_country_frame(choose_country(today_country_data, "India"))

bar_chart = plot_province(country_stats, "Confirmed", "Confirmed Cases")
table = table_province_data(country_stats, "Confirmed")
"""
