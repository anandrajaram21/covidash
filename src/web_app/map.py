'''
This file contains the functions required beautiful, interactive maps using Plotly Chart Studio and Mapbox
'''

# Imports
import copy
import sys
import os
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import chart_studio.plotly as py
import chart_studio
from math import log
from math import e
from itertools import chain

# Setting up credentials for the map 
chart_studio.tools.set_credentials_file(username='chartstudiouser', api_key='m9KxT5JPEEukONNW8E50')
mapbox_access_token = 'pk.eyJ1IjoiY2hhcnRzdHVkaW91c2VyIiwiYSI6ImNrZXd3bTBoNTA4bnYyemw4N3l5aDN5azIifQ.7e-KoC1KMXr_EKbkahgAQQ'

# Getting sorted country cases
confirmed_global, deaths_global, recovered_global, country_cases = (context.deserialize(r.get("confirmed_global")), context.deserialize(r.get("deaths_global")), context.deserialize(r.get("recovered_global")), context.deserialize(r.get("country_cases")))

country_cases_sorted = country_cases.sort_values('confirmed', ascending = False)
country_cases_sorted.index = [x for x in range(len(country_cases_sorted))]

def chainer(s):
    return list(chain.from_iterable(s.str.split(',')))

# Data Preprocessing
def convert_df(df, cols):
    df.dropna(inplace=True)
    df.set_index(df[cols[0]].values)
    df.dropna(inplace=True)

    L=[]
    for i in range(len(df)):
        string = ''
        for j in range(len(cols[1])):
            if j != (len(cols[1]) - 1):
                string = string + str(df[cols[1][j]].values[i]) + ','
            else:
                string = string + str(df[cols[1][j]].values[i])

        L.append(string)

    df['New'] = L
    lens = df['New'].str.split(',').map(len)

    df = pd.DataFrame({
        'Country': np.repeat(df[cols[0]], lens),
        'Lat': np.repeat(df[cols[-2]], lens),
        'Long_': np.repeat(df[cols[-1]], lens),
        'Count': chainer(df['New'])
    })
    df['Study'] = [cols[1][i] for i in range (len(cols[1]))] * (len(df.index) // len(cols[1]))

    return df

def create_data(df, study, color):
    countries = list(df['Country'].value_counts().index)
    data = []
    df.dropna(inplace = True)
    
    for country in countries:
        try:
            event_data = dict(
                lat=df.loc[(df['Study'] == study) & (df['Country'] == country), 'Lat'],
                lon=df.loc[(df['Study'] == study) & (df['Country'] == country), 'Long_'],
                name=f'{study}: {country}',
                marker={
                    'size': log(float(df.loc[(df['Study'] == study) & (df['Country'] == country), 'Count']), 1.5),
                    'opacity': 0.5,
                    'color': color
                },
                type='scattermapbox',
                hoverinfo='skip'
            )
            data.append(event_data)
        except:
            continue

    return data

# Graphing
def create_basic_layout(latitude, longitude):
    layout = {
        'height': 400,
        'margin': {'t': 0, 'b': 0, 'l': 0, 'r': 0},
        'font': {'color': '#FFFFFF', 'size': 15},
        'paper_bgcolor': '#000000',
        'showlegend': False,
        'mapbox': {
            'accesstoken': mapbox_access_token,
            'bearing': 0,
            'center': {'lat': latitude, 'lon': longitude},
            'pitch': 0,
            'zoom': 2
        }
    }
    return layout

def update_layout(study, layout):
    annotations = [{
        'text': f'{study.capitalize()} Cases',
        'font': {'color': '#FFFFFF', 'size': 14},
        'borderpad': 10,
        'x': 0.05,
        'y': 0.05,
        'xref': 'paper',
        'yref': 'paper',
        'align': 'left',
        'showarrow': False,
        'bgcolor': 'black'
    }]

    layout['title'] = f'{study.capitalize()} Cases'
    layout['annotations'] = annotations 

    return layout

def interactive_map(data, layout):
    figure = {
        'data': data,
        'layout': layout
    }

    return figure

def plot_study(starting_df, cols, study_dict, location='global'):
    color = study_dict['color']
    study = study_dict['study']
    latitude = 20.59
    longitude = 78.96
    if location != 'global' :
        latitude = int(country_cases_sorted.loc[(country_cases_sorted['country'] == location), 'Lat'])
        longitude = int(country_cases_sorted.loc[(country_cases_sorted['country'] == location), 'Long_'])

    df = convert_df(starting_df, cols)
    data = create_data(df, study, color)
    layout = create_basic_layout(latitude, longitude)
    updated_layout = update_layout(study, layout)
    figure = interactive_map(data, updated_layout)
    return figure

'''
Example:

confirmed = dict(study="confirmed",color="blue")
recovered = dict(study="recovered",color="pink")
deaths = dict(study="deaths",color="red")

columns = ["country", ["deaths", "confirmed", "recovered"], "Lat", "Long_"]

figure = plot_study(country_cases_sorted, columns, confirmed, "Japan")
py.iplot(figure)
'''
