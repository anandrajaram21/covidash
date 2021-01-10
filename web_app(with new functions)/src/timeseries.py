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


def plot_world_timeseries(df, df_name):
    data = get_world_timeseries(df)
    if df_name == "confirmed":
        fig = px.bar(
            data,
            x="Date",
            y="Cases",
            template="plotly_dark",
            color_discrete_sequence=["blue"] * len(data),
        )
    elif df_name == "recovered":
        fig = px.bar(
            data,
            x="Date",
            y="Cases",
            template="plotly_dark",
            color_discrete_sequence=["green"] * len(data),
        )
    elif df_name == "deaths":
        fig = px.bar(
            data,
            x="Date",
            y="Cases",
            template="plotly_dark",
            color_discrete_sequence=["red"] * len(data),
        )
    fig.layout.update(hovermode="x")
    return fig


# Inter-Country plot
def unpivot(df):
    return df.melt(id_vars=["country"], value_vars=df.columns[1:])


def compare(df, *args):
    l = list(args)
    temp = unpivot(df)
    return temp[temp["country"].isin(l)]


def create_data(df):
    new = df
    l = list(set(new["variable"]))
    l.sort()
    l.reverse()
    ff = new[new["variable"].isin(l[::5])]
    ff.rename(
        columns={"country": "Country", "variable": "Date", "value": "Cases"},
        inplace=True,
    )
    return ff


def static_line(df, *args):
    df = compare(df, *args)
    ff = create_data(df)
    fig = px.line(
        ff,
        x="Date",
        y="Cases",
        color="Country",
        template="plotly_dark",
        range_y=[0, ff["Cases"].max()],
    )
    fig.layout.update(hovermode="x")
    return fig


# Intra-Country plot
def line_comparison(country):
    whole_df = pd.DataFrame()
    whole_df["dates"] = list(confirmed_global.columns[1:])
    whole_df["confirmed"] = list(
        confirmed_global.loc[confirmed_global["country"] == country].values.flatten()[
            1:
        ]
    )
    whole_df["deaths"] = list(
        deaths_global.loc[deaths_global["country"] == country].values.flatten()[1:]
    )
    whole_df["recovered"] = list(
        recovered_global.loc[recovered_global["country"] == country].values.flatten()[
            1:
        ]
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=whole_df["dates"], y=whole_df["confirmed"], mode="lines", name="confirmed"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["dates"], y=whole_df["deaths"], mode="lines", name="deaths"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=whole_df["dates"], y=whole_df["recovered"], mode="lines", name="recovered"
        )
    )

    fig.update_layout(
        height=500,
        showlegend=True,
        template="plotly_dark",
        title_text=f"Analysis of {country.title()}",
        hovermode="x",
    )

    return fig


"""
Examples:
fig = plot_timeseries("US", get_new_cases, "Confirmed Cases")
fig = plot_timeseries("India", get_new_recoveries, "Recoveries", n=-30, daily=True)

fig = static_line(recovered_global, "India", "New Zealand", "US", "Brazil")

fig = line_comparison("India")
"""
