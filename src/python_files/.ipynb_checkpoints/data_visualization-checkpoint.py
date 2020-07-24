# Imports
import sys
import os
from datetime import datetime
from datetime import date
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

# Analysis of Worst Hit Countries

# Making a dataframe with the country data in sorted order
country_cases_sorted = country_cases.sort_values('confirmed', ascending = False)
country_cases_sorted.index = [x for x in range(len(country_cases_sorted))]

# Plotting the worst affected countries side by side for a direct comparison
fig = px.bar(country_cases_sorted.head(), x = 'country', y = 'confirmed', color = 'confirmed', \
            labels = {'country': 'Country', 'confirmed': 'Confirmed Cases'}, template = 'plotly_dark')
fig.show()

# Chloropleth Setup
chloropleths = main.chloropleths

# Plotting the confirmed cases chloropleth
graph = 'confirmed'
main.chloropleth(graph,chloropleths[graph][0],chloropleths[graph][1],chloropleths[graph][2])

# Plotting the deaths chloropleth
graph = 'deaths'
main.chloropleth(graph,chloropleths[graph][0],chloropleths[graph][1],chloropleths[graph][2])

# Plotting the recovered cases chloropleth
graph = 'recovered'
main.chloropleth(graph,chloropleths[graph][0],chloropleths[graph][1],chloropleths[graph][2])
