"""
# Animations
This file contains beautiful animations that visualize the current COVID-19 situation
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pyarrow as pa
import redis
import main

r = redis.Redis()

confirmed_global, deaths_global, recovered_global, country_cases = (
    pa.deserialize(r.get("confirmed_global")),
    pa.deserialize(r.get("deaths_global")),
    pa.deserialize(r.get("recovered_global")),
    pa.deserialize(r.get("country_cases")),
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


def plot_fig(ff):
    fig = px.bar(
        ff,
        x="Country",
        y="Cases",
        color="Country",
        template="plotly_dark",
        animation_frame="Date",
        animation_group="Country",
        range_y=[0, ff["Cases"].max()],
    )
    fig.layout.update(showlegend=False)
    return fig


def animated_barchart(df):
    return plot_fig(create_data(take_top10(unpivot(df))))


def compare(df, *args):
    l = list(args)
    temp = unpivot(df)
    temp = temp[temp["country"].isin(l)]
    return temp


def plot_fig_compare(ff):
    fig = px.bar(
        ff,
        x="Country",
        y="Cases",
        color="Country",
        template="plotly_dark",
        animation_frame="Date",
        animation_group="Country",
        range_y=[0, ff["Cases"].max()],
    )
    fig.layout.update(hovermode="x")
    return fig


def create_comparison(df, *args):
    df = compare(df, *args)
    ff = create_data(df)
    return plot_fig_compare(ff)


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
        xaxis={"showgrid": False},
        yaxis={"showgrid": False},
        template="plotly_dark",
        title_text=f"Analysis of {country.title()}",
        hovermode="x",
    )

    return fig


"""
Example:

line_comparison("India")
static_line(recovered_global,"India","New Zealand","US")
create_comparison(confirmed_global,"India","US","Australia")
animated_barchart(confirmed_global)
"""
