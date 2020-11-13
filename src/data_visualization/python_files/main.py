# Imports
import os
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go


def collect_data():

    # Data from the John Hopkins University Dataset on GitHub
    # https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

    # Defining the variables requiredk
    filenames = [
        "time_series_covid19_confirmed_global.csv",
        "time_series_covid19_deaths_global.csv",
        "time_series_covid19_recovered_global.csv",
    ]

    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

    # Making the main dataframes required for the analysis
    confirmed_global = pd.read_csv(url + filenames[0])
    deaths_global = pd.read_csv(url + filenames[1])
    recovered_global = pd.read_csv(url + filenames[2])
    country_cases = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
    )

    # Simple Data Cleaning - Removing and renaming the Columns

    # Removing the Province/State column, as it is pretty much not of any use
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
    # Renaming the columns for easier access
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

    # Removing some duplicate values from the table
    confirmed_global = confirmed_global.groupby(["country"], as_index=False).sum()
    deaths_global = deaths_global.groupby(["country"], as_index=False).sum()
    recovered_global = recovered_global.groupby(["country"], as_index=False).sum()

    # This value is being changed as there was an error in the original dataset that had to be modified
    confirmed_global.at[178, "5/20/20"] = 251667

    return (confirmed_global, deaths_global, recovered_global, country_cases)


# Run the collect data function for use in the functions of this file
confirmed_global, deaths_global, recovered_global, country_cases = collect_data()


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


def get_plot(time_series):
    fig = px.bar(time_series, x="date", y="cases")
    return fig


def plot_timeseries(country_name, func_name, title):
    new_confirmed_cases = func_name(country_name)
    fig = get_plot(new_confirmed_cases)
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=f'Number of {"deaths" if "deaths" in title else "new cases"}',
    )
    fig.show()


chloropleths = {
    "confirmed": ["CONFIRMED CASES", "No. of confirmed cases", "blues_r"],
    "deaths": ["NUMBER OF DEATHS", "No. of deaths", "oranges_r"],
    "recovered": ["RECOVERED CASES", "No. of recovered cases", "teal"],
}


def curr_date():
    t = date.today()
    date1 = t.strftime("%d-%m-%Y")
    return date1


def chloropleth(based_on, title, bar_title, color_scale):
    date = curr_date()
    fig = go.Figure(
        data=go.Choropleth(
            locations=country_cases["ISO3"],
            z=country_cases[based_on],
            text=country_cases["country"],
            colorscale=color_scale,
            autocolorscale=False,
            reversescale=False,
            marker_line_color="darkgrey",
            marker_line_width=0.5,
            colorbar_tickprefix="#",
            colorbar_title=bar_title,
        )
    )

    fig.update_layout(
        title_text=f"COVID-19 - {title} AS OF {date}",
        geo=dict(
            showframe=True,
            showcoastlines=False,
            projection_type="orthographic",
            showocean=True,
            oceancolor="white",
            bgcolor="white",
        ),
        annotations=[
            dict(
                x=0.55,
                y=0.1,
                xref="paper",
                yref="paper",
                text="Source: John Hopkins University",
                showarrow=False,
            )
        ],
        paper_bgcolor="white",
    )
    # fig.show()
    return fig
