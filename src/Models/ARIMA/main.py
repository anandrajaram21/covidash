"""
This file contains the outermost code that will be required by almost all other files in this repository
What this file will contain:
1. The data collection and preprocessing
2. The different functions to get the time series data for confirmed cases, recoveries, or deaths
This file should be imported into every other file, and the functions inside this must be reused as much as possible
"""

# COVID-19 Outbreak Analysis

# Imports
import os
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go

"""
This function scrapes COVID-19 data, cleans it, and returns all the dataframes required for the analysis
Values returned:
confirmed_global: A list of confirmed cases by date, of each country in the world (cumulative)
deaths_global: A list of deaths by date, of each conutry in the world (cumulative)
recovered_global: A list of recoveries by date, of each country in the world (cumulative)
country_cases: A list of confirmed cases, deaths, and recoveries at the time of scraping, of each country in the world
"""


def collect_data():

    # Data from the John Hopkins University Dataset on GitHub
    # https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

    # Defining the variables required
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

"""
This function takes a country as a parameter and returns a dataframe that contains the number of confirmed cases each day up to the current date
The resultant data frame contains 2 columns:
1. date: Has the dates
2. cases: Has the number of confirmed cases on that particular date
"""


def get_new_cases(country):
    time_series = confirmed_global.melt(
        id_vars=["country"], var_name="date", value_name="cases"
    )
    time_series = time_series[time_series["country"] == country]
    time_series = time_series.drop(["country"], axis=1)
    time_series.index = [x for x in range(len(time_series))]
    return time_series


"""
This function takes a country as a parameter and returns a dataframe that contains the number of deaths each day up to the current date
The resultant data frame contains 2 columns:
1. date: Has the dates
2. cases: Has the number of deaths on that particular date
"""


def get_new_deaths(country):
    time_series = deaths_global.melt(
        id_vars=["country"], var_name="date", value_name="cases"
    )
    time_series = time_series[time_series["country"] == country]
    time_series = time_series.drop(["country"], axis=1)
    time_series.index = [x for x in range(len(time_series))]
    return time_series


"""
This function takes a country as a parameter and returns a dataframe that contains the number of recoveries each day up to the current date
The resultant data frame contains 2 columns:
1. date: Has the dates
2. cases: Has the number of recoveries on that particular date
"""


def get_new_recoveries(country):
    time_series = recovered_global.melt(
        id_vars=["country"], var_name="date", value_name="cases"
    )
    time_series = time_series[time_series["country"] == country]
    time_series = time_series.drop(["country"], axis=1)
    time_series.index = [x for x in range(len(time_series))]
    return time_series


"""
This function takes a time series object as a parameter and plots it on a bar graph
The time series object MUST be formatted in the right manner for this function to work
The get_new_cases function can be used to obtain a time series of the right format
Function can be used universally to plot any time series object
Returns a plotly express object which you can then display with the show method of the object
"""


def get_plot(time_series):
    fig = px.bar(time_series, x="date", y="cases")
    return fig


"""
This function takes the name of a country, the function to use to get the time series(must be either get_new_cases, or get_new_deaths), and the graph title and plots either one of the following:
1. If the function is get_new_cases, then a plot of the new confirmed cases per day v/s the date is plotted for the country specified
2. If the function is get_new_deaths, then a plot of the new deaths per day v/s the date is plotted for the country specified
"""


def plot_timeseries(country_name, func_name, title):
    new_confirmed_cases = func_name(country_name)
    fig = get_plot(new_confirmed_cases)
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=f'Number of {"deaths" if "deaths" in title else "new cases"}',
    )
    fig.show()


"""
Creating a dictionary with keys as based_on parameter with its value being a list of other required parameters for the chloropleth function
The following dictionary can be used in other files as well
"""
chloropleths = {
    "confirmed": ["CONFIRMED CASES", "No. of confirmed cases", "blues_r"],
    "deaths": ["NUMBER OF DEATHS", "No. of deaths", "oranges_r"],
    "recovered": ["RECOVERED CASES", "No. of recovered cases", "teal"],
}

"""
Defining a function to find current date as to use in graph
takes in no parameters 
returns current date in the fomrat dd-mm-yyyy
"""


def curr_date():
    t = date.today()
    date1 = t.strftime("%d-%m-%Y")
    return date1


"""
Defining a function to plot a global chloropleth
Takes in the following parameters:
1.based_on: Graph is plotted and scaled on this parameter
2.title: Provides graph title
3.bar_title: Provides the colorbar title
4.color_scale: Gives the color on which the map is being plotted
"""


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
