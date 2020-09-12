# Imports
import copy
import sys
import os
from datetime import datetime
from datetime import date
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

# Custom file imports
import vars_for_streamlit as vfs
import map 
import ARIMA
import animations
import main

# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------

# The Data Collection and Preprocessing
@st.cache
def collect_data():
    # Defining the variables required
    filenames = ['time_series_covid19_confirmed_global.csv',
                'time_series_covid19_deaths_global.csv',
                'time_series_covid19_recovered_global.csv']

    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

    # Making the main dataframes required for the analysis
    confirmed_global = pd.read_csv(url + filenames[0])
    deaths_global = pd.read_csv(url + filenames[1])
    recovered_global = pd.read_csv(url + filenames[2])
    country_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')

    # Simple Data Cleaning - Removing and renaming the Columns

    # Removing the Province/State column, as it is pretty much not of any use
    confirmed_global.drop(columns = ['Province/State', 'Lat', 'Long'], inplace = True)
    deaths_global.drop(columns = ['Province/State', 'Lat', 'Long'], inplace = True)
    recovered_global.drop(columns = ['Province/State', 'Lat', 'Long'], inplace = True)
    country_cases.drop(columns = ['Last_Update', 'Incident_Rate', 'People_Tested', 'People_Hospitalized', 'UID'], inplace = True)

    # Renaming the columns for easier access
    confirmed_global.rename(columns = {"Country/Region": "country"}, inplace = True)
    deaths_global.rename(columns = {"Country/Region": "country"}, inplace = True)
    recovered_global.rename(columns = {"Country/Region": "country"}, inplace = True)

    country_cases.rename(columns = {
        "Country_Region" : "country",
        "Confirmed": "confirmed",
        "Deaths": "deaths",
        "Recovered" : "recovered",
        "Active" : "active",
        "Mortality_Rate": "mortality"
    }, inplace = True)

    # Removing some duplicate values from the table
    confirmed_global = confirmed_global.groupby(['country'], as_index = False).sum()
    deaths_global = deaths_global.groupby(['country'], as_index = False).sum()
    recovered_global = recovered_global.groupby(['country'], as_index = False).sum()

    # This value is being changed as there was an error in the original dataset that had to be modified
    confirmed_global.at[178, '5/20/20'] = 251667

    return (confirmed_global, deaths_global, recovered_global, country_cases)

confirmed_global, deaths_global, recovered_global, country_cases = collect_data()

# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------

# The Landing Page
def option0():
    st.image('./images/virus1.jpeg', use_column_width = True)
    covid_19 = vfs.covid_19
    
    st.markdown(covid_19)

# The Global Pandemic Situation Page
@st.cache(show_spinner=False)
def option1(metric):
    metrics = ('Confirmed Cases', 'Recoveries', 'Deaths')

    confirmed = dict(study = "confirmed",color = "blue")
    recovered = dict(study = "recovered",color = "green")
    deaths = dict(study = "deaths",color = "red")
    columns = ["country",["deaths","confirmed","recovered"],"Lat","Long_"]

    if metric == metrics[0]:
        figure = map.plot_study(map.country_cases_sorted, columns, confirmed, "global")

    elif metric == metrics[1]:
        figure = map.plot_study(map.country_cases_sorted, columns, recovered, "global")
    
    elif metric == metrics[2]:
        figure = map.plot_study(map.country_cases_sorted, columns, deaths, "global")
    
    return figure

# The Individual Country Analysis Page
@st.cache(allow_output_mutation = True,show_spinner=False)
def option2(country_name, metric):
    metrics = ('Confirmed Cases', 'Recoveries', 'Deaths')

    confirmed = dict(study = "confirmed",color = "blue")
    recovered = dict(study = "recovered",color = "green")
    deaths = dict(study = "deaths",color = "red")
    columns = ["country",["deaths","confirmed","recovered"],"Lat","Long_"]
    
    forecast, graph, error = None, None, None

    if metric == metrics[0]:
        figure = map.plot_study(map.country_cases_sorted, columns, confirmed, country_name)
        forecast, graph, error = ARIMA.arima_predict('confirmed', country_name)

    elif metric == metrics[1]:
        figure = map.plot_study(map.country_cases_sorted, columns, recovered, country_name)
        forecast, graph, error = ARIMA.arima_predict('recovered', country_name)
    
    elif metric == metrics[2]:
        figure = map.plot_study(map.country_cases_sorted, columns, deaths, country_name)
        forecast, graph, error = ARIMA.arima_predict('deaths', country_name)

    return forecast, graph, error, figure
    

# The Safety Measures Page
def option3():
    safety = vfs.safety
    st.markdown(safety)

# The About Us Page
def option4():
    about = vfs.about
    st.markdown(about)

# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------

# The Main App Starts Here
def main_app_function():
    st.title('COVID-19 Pandemic Analysis')
    options = ('What is COVID-19', 'Global Pandemic Situation', 'Individual Country Analysis', 'Safety Measures', 'About Us')

    choice = st.sidebar.selectbox('Choose an Option', options)

    if choice == options[0]:
        option0()

    elif choice == options[1]:
        st.subheader('Global Pandemic Situation')

        metrics = ('Confirmed Cases', 'Recoveries', 'Deaths')
        metric = st.selectbox('Choose any one', metrics)

        figure = option1(metric)
        st.plotly_chart(figure)

        bar_df = confirmed_global.transpose()
        l = [datetime.strptime(date,"%m/%d/%y").strftime("20%y-%m-%d") for date in bar_df.index[1:]]
        l.insert(0,0)
        bar_df.set_index(pd.Index(l),inplace=True)
        L = pd.to_datetime(l,utc=False)

        bar_df.set_index(pd.Index(L),inplace=True)
        bar_df = bar_df.transpose()
        pio.templates.default = "plotly"

        st.plotly_chart(animations.animated_barchart(bar_df, '1970-01-01',bar_df.columns[1],bar_df.columns[-1],title = "VIZUALIZATION OF TOP 10 BY COMPARISON", frame_rate = 24))

    elif choice == options[2]:
        st.subheader('Individual Country Analysis')

        country_name = st.selectbox('Choose a country', list(map.country_cases_sorted['country'].unique()))
        metrics = ('Confirmed Cases', 'Recoveries', 'Deaths')
        metric = st.selectbox('Choose any one', metrics)
        
        forecast, graph, error, figure = option2(country_name, metric)
        forecast1, graph1, error1, figure1 = copy.deepcopy(forecast), copy.deepcopy(graph), copy.deepcopy(error), copy.deepcopy(figure)
        
        st.plotly_chart(figure1)
        st.plotly_chart(graph1)
        st.write(forecast1)
        st.write(f'Allow an error of upto: {round(error1,2)}%')

    elif choice == options[3]:
        option3()

    elif choice == options[4]:
        option4()

if __name__ == "__main__":
    main_app_function()