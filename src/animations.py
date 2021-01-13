# Imports
import app_vars as av
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

confirmed_global, deaths_global, recovered_global, country_cases_sorted = (
    av.confirmed_global,
    av.deaths_global,
    av.recovered_global,
    av.country_cases_sorted,
)


def unpivot(df):
    return df.melt(id_vars=["country"], value_vars=df.columns[1:])


def take_top10(df):
    top = list(
        df[df["variable"] == df["variable"][df.index[-1]]]
        .sort_values(by=["value"], ascending=False)
        .head(10)["country"]
    )
    df = df[df["country"].isin(top)]
    return df

def line_comparison_data(country):
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
    return whole_df

def compare(df, *args):
    l = list(args)
    temp = unpivot(df)
    temp = temp[temp["country"].isin(l)]
    return temp

def create_data(df):
    new = take_top10(df)
    l = list(set(new["variable"]))
    l.sort()
    l.reverse()
    ff = new[new["variable"].isin(l[::5])]
    ff.rename(
        columns={"country": "Country", "variable": "Date", "value": "Cases"},
        inplace=True,
    )
    return ff


def plot_fig(ff, Color):
    fig = px.bar(
        ff,
        x="Country",
        y="Cases",
        color_discrete_sequence=[Color] * len(ff),
        template="plotly_dark",
        animation_frame="Date",
        animation_group="Country",
        range_y=[0, ff["Cases"].max()],
    )
    fig.layout.update(showlegend=False)
    return fig


def animated_barchart(df, name):
    color = (
        "#f54842"
        if name == "deaths"
        else "#45a2ff"
        if name == "confirmed"
        else "#42f587"
    )
    return plot_fig(create_data(take_top10(unpivot(df))), color)

def static_line(df, df_name, *args):
    df = compare(df, *args)
    ff = create_data(df)
    if df_name == "confirmed":
        fig = px.line(
            ff,
            x="Date",
            y="Cases",
            template="plotly_dark",
            color_discrete_sequence=["blue"] * len(ff),
            range_y=[0, ff["Cases"].max()],
        )
        fig.layout.update(hovermode="x")
        return fig
    elif df_name == "recovered":
        fig = px.line(
            ff,
            x="Date",
            y="Cases",
            template="plotly_dark",
            color_discrete_sequence=["green"] * len(ff),
            range_y=[0, ff["Cases"].max()],
        )
        fig.layout.update(hovermode="x")
        return fig
    elif df_name == "deaths":
        fig = px.line(
            ff,
            x="Date",
            y="Cases",
            template="plotly_dark",
            color_discrete_sequence=["red"] * len(ff),
            range_y=[0, ff["Cases"].max()],
        )
        fig.layout.update(hovermode="x")
        return fig

"""
Examples:
fig = animated_barchart(confirmed_global, "confirmed")
fig = animated_barchart(deaths_global, "deaths")
fig = animated_barchart(recovered_global, "recovered")
"""
