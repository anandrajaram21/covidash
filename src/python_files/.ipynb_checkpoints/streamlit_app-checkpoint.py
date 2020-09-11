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
import vars_for_streamlit as vfs
import map 

# To import the main.py file
sys.path.append('../')
from python_files import main

# Getting all the data
@st.cache
def collect_data():
    confirmed_global, deaths_global, recovered_global, country_cases = main.collect_data()
    return confirmed_global, deaths_global, recovered_global, country_cases

confirmed_global, deaths_global, recovered_global, country_cases = collect_data()

# Streamlit trials
st.title("COVID-19 Pandemic Analysis")

option = st.sidebar.selectbox('Choose your option', ('What is COVID-19', 'Global Pandemic Situation', 'Individual Country Analysis', 'Safety Measures', 'About Us'))

if option == 'What is COVID-19':

    st.image('./images/virus1.jpeg', use_column_width = True)
    covid_19 = vfs.covid_19
    
    st.markdown(covid_19)
    

elif option == 'Global Pandemic Situation':
    st.write("Global Pandemic Situation")
    
    metrics = ('Confirmed Cases', 'Recoveries', 'Deaths')
    metric = st.selectbox('Choose any one', ('Confirmed Cases', 'Recoveries', 'Deaths'))
    country_name = st.selectbox('Choose a Country/Region', list(country_cases['country'].sort_values().unique()))
    
    country_cases_sorted = country_cases.sort_values('confirmed', ascending = False)
    country_cases_sorted.index = [x for x in range(len(country_cases_sorted))]
    
    confirmed = dict(study = "confirmed",color = "blue")
    recovered = dict(study = "recovered",color = "pink")
    deaths = dict(study = "deaths",color = "red")
    columns = ["country",["deaths","confirmed","recovered"],"Lat","Long_"]
    
    if metric == metrics[0]:
        figure = map.plot_study(country_cases_sorted, columns, confirmed, country_name)
    
    elif metric == metrics[1]:
        figure = map.plot_study(country_cases_sorted, columns, recovered, country_name)
    
    elif metric == metrics[2]:
        figure = map.plot_study(country_cases_sorted, columns, deaths, country_name)
        
    st.plotly_chart(figure)

elif option == 'Individual Country Analysis':
    st.write('Individual Country Analysis')
#     country_name = st.text_input('Enter Country Name', 'India')

#     st.write('Country name chosen is', country_name)

#     country_confirmed = main.get_new_cases(country_name)
#     country_deaths = main.get_new_deaths(country_name)
#     country_recoveries = main.get_new_recoveries(country_name)

#     st.write(main.get_plot(country_confirmed))
#     st.write(main.get_plot(country_deaths))
#     st.write(main.get_plot(country_recoveries))

elif option == 'Safety Measures':

    safety = vfs.safety
    
    st.markdown(safety)

elif option == 'About Us':
    
    about = vfs.about
    
    st.markdown(about)
    
# elif option == 'Test':
#     components.html("""
#     <img src="https://raw.githubusercontent.com/anandrajaram21/covid-19/master/src/python_files/images/sanitizer.jpeg" alt="virus" style="width: 50%;">
#     <img src="https://raw.githubusercontent.com/anandrajaram21/covid-19/master/src/python_files/images/virus1.jpeg" alt="sanitizer" style="width: 50%;">
#     """, height = 1920)