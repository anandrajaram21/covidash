# Imports
import sys
import os
from datetime import datetime
from datetime import date
import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import vars_for_streamlit as vfs

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
    country_name = st.selectbox('Choose a Country/Region', list(country_cases['country'].sort_values().unique()))
    st.write(f'Country chosen is {country_name}')
#     # Chloropleth Setup
#     chloropleths = main.chloropleths

#     # Plotting the confirmed cases chloropleth
#     graph = 'confirmed'
#     graph1 = main.chloropleth(graph,chloropleths[graph][0],chloropleths[graph][1],chloropleths[graph][2])

#     # Plotting the deaths chloropleth
#     graph = 'deaths'
#     graph2 = main.chloropleth(graph,chloropleths[graph][0],chloropleths[graph][1],chloropleths[graph][2])

#     # Plotting the recovered cases chloropleth
#     graph = 'recovered'
#     graph3 = main.chloropleth(graph,chloropleths[graph][0],chloropleths[graph][1],chloropleths[graph][2])

#     st.write(graph1)
#     st.write(graph2)
#     st.write(graph3)

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