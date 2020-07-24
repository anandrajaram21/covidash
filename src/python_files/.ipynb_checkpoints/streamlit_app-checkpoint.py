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

# To import the main.py file
sys.path.append('../')
from python_files import main

# Getting all the data
confirmed_global, deaths_global, recovered_global, country_cases = main.collect_data()

# Streamlit trials
st.title("COVID-19 Pandemic Analysis")

country_name = st.text_input('Enter Country Name', 'India')

st.write('Country name chosen is', country_name)

country_confirmed = main.get_new_cases(country_name)
country_deaths = main.get_new_deaths(country_name)
country_recoveries = main.get_new_recoveries(country_name)

st.write(main.get_plot(country_confirmed))
st.write(main.get_plot(country_deaths))
st.write(main.get_plot(country_recoveries))