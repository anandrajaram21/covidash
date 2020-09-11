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

st.title('COVID-19 Pandemic Analysis')

options = ('What is COVID-19', 'Global Pandemic Situation', 'Individual Country Analysis', 'Safety Measures', 'About Us')

choice = st.sidebar.selectbox('Choose an Option', options)

if choice == options[0]:
    
    st.image('./images/virus1.jpeg', use_column_width = True)
    covid_19 = vfs.covid_19
    
    st.markdown(covid_19)

elif choice == options[1]:
    
    st.subheader('Global Pandemic Situation')

    country_name = st.selectbox('Choose a Country/Region', map.country_cases_sorted['country'].unique())

    metrics = ('Confirmed Cases', 'Recoveries', 'Deaths')
    metric = st.selectbox('Choose any one', metrics)

    confirmed = dict(study = "confirmed",color = "blue")
    recovered = dict(study = "recovered",color = "pink")
    deaths = dict(study = "deaths",color = "red")
    columns = ["country",["deaths","confirmed","recovered"],"Lat","Long_"]

    if metric == metrics[0]:
        figure = map.plot_study(map.country_cases_sorted, columns, confirmed, country_name)

    elif metric == metrics[1]:
        figure = map.plot_study(map.country_cases_sorted, columns, recovered, country_name)
    
    elif metric == metrics[2]:
        figure = map.plot_study(map.country_cases_sorted, columns, deaths, country_name)
    
    st.plotly_chart(figure)
