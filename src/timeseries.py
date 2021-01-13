# Imports
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from datetime import date
import app_vars as av

confirmed_global, deaths_global, recovered_global, country_cases_sorted = (
    av.confirmed_global,
    av.deaths_global,
    av.recovered_global,
    av.country_cases_sorted,
)


def get_new_cases(country):
    time_series = confirmed_global.melt(
        id_vars=["country"], var_name="date", value_name="cases"
    )
    time_series = time_series[time_series["country"] == country]
    time_series = time_series.drop(["country"], axis=1)
    time_series.index = [x for x in range(len(time_series))]
    return time_series


def get_new_deaths(country):
    time_series = deaths_global.melt(
        id_vars=["country"], var_name="date", value_name="cases"
    )
    time_series = time_series[time_series["country"] == country]
    time_series = time_series.drop(["country"], axis=1)
    time_series.index = [x for x in range(len(time_series))]
    return time_series


def get_new_recoveries(country):
    time_series = recovered_global.melt(
        id_vars=["country"], var_name="date", value_name="cases"
    )
    time_series = time_series[time_series["country"] == country]
    time_series = time_series.drop(["country"], axis=1)
    time_series.index = [x for x in range(len(time_series))]
    return time_series


def get_plot(time_series, name):
    color = (
        "#f54842" if "deaths" in name else "#45a2ff" if "cases" in name else "#42f587"
    )
    fig = px.bar(
        time_series,
        x="date",
        y="cases",
        color_discrete_sequence=[color] * len(time_series),
    )
    return fig


def plot_timeseries(country_name, func_name, title, n=-90, daily=False):
    if not daily:
        new_confirmed_cases = func_name(country_name)[n:]
    else:
        confirmed_cases = func_name(country_name)
        cases = confirmed_cases["cases"].diff()[1:]
        new_confirmed_cases = confirmed_cases[1:]
        new_confirmed_cases["cases"] = cases
        new_confirmed_cases = new_confirmed_cases[n:]
    fig = get_plot(new_confirmed_cases, str(func_name))
    fig.update_layout(
        template="plotly_dark",
        title=title,
        xaxis_title="Date",
        yaxis_title=f'Number of {"deaths" if "deaths" in title else "new cases"}',
    )
    return fig


def get_world_timeseries(df):
    data = df.sum()
    data = data[1:]
    data = pd.DataFrame(data={"Date": data.index, "Cases": data})
    return data


def plot_world_timeseries(df, name, n=-90, daily=False):
    data, new_data = None, None
    if not daily:
        new_data = get_world_timeseries(df)[n:]
        data = get_world_timeseries(df)
    else:
        data = get_world_timeseries(df)
        cases = data["Cases"].diff()[1:]
        new_data = data[1:]
        new_data["Cases"] = cases
        new_data = new_data[n:]
    color = (
        "#f54842"
        if "deaths" == name
        else "#45a2ff"
        if "confirmed" == name
        else "#42f587"
    )
    fig = px.bar(
        new_data,
        x="Date",
        y="Cases",
        template="plotly_dark",
        color_discrete_sequence=[color] * len(data),
    )
    return fig


"""
Examples:
fig = plot_timeseries("US", get_new_cases, "Confirmed Cases")
fig = plot_timeseries("India", get_new_recoveries, "Recoveries", n=-30, daily=True)
"""
