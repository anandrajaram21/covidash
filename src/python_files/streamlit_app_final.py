# Imports
import sys
import os
from datetime import datetime
from datetime import date
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

# Custom file imports
import vars_for_streamlit as vfs
import map 
import ARIMA
import animations
import main

# The Landing Page
def option0():
    st.image('./images/virus1.jpeg', use_column_width = True)
    covid_19 = vfs.covid_19
    
    st.markdown(covid_19)

# The Global Pandemic Situation Page
@st.cache
def option1(metric):
    metrics = ('Confirmed Cases', 'Recoveries', 'Deaths')

    confirmed = dict(study = "confirmed",color = "blue")
    recovered = dict(study = "recovered",color = "pink")
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
@st.cache
def option2(country_name, metric):
    metrics = ('Confirmed Cases', 'Recoveries', 'Deaths')

    confirmed = dict(study = "confirmed",color = "blue")
    recovered = dict(study = "recovered",color = "pink")
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

# The Main App Starts Here
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

elif choice == options[2]:
    st.subheader('Individual Country Analysis')

    country_name = st.selectbox('Choose a country', list(map.country_cases_sorted['country'].unique()))
    metrics = ('Confirmed Cases', 'Recoveries', 'Deaths')
    metric = st.selectbox('Choose any one', metrics)
    
    forecast, graph, error, figure = option2(country_name, metric)
    
    st.plotly_chart(figure)
    st.plotly_chart(graph)
    st.write(forecast)
    st.write(f'Error is {error}')

elif choice == options[3]:
    option3()

elif choice == options[4]:
    option4()
