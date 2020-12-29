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
