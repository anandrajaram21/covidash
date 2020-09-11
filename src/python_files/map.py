# Interactive Maps Using Plotly Chart Studio and Mapbox
# Importing necessary libraries
import sys
import chart_studio.plotly as py
import chart_studio
import pandas as pd
import plotly
import numpy as np 
from math import log,e
from itertools import chain

# Importing main.py 
import main

# Setting up credentials for the map 
chart_studio.tools.set_credentials_file(username='chartstudiouser', api_key='m9KxT5JPEEukONNW8E50')
mapbox_access_token = 'pk.eyJ1IjoiY2hhcnRzdHVkaW91c2VyIiwiYSI6ImNrZXd3bTBoNTA4bnYyemw4N3l5aDN5azIifQ.7e-KoC1KMXr_EKbkahgAQQ'

# Getting country_cases_sorted 
confirmed_global, deaths_global, recovered_global, country_cases = main.collect_data()
country_cases_sorted = country_cases.sort_values('confirmed', ascending = False)
country_cases_sorted.index = [x for x in range(len(country_cases_sorted))]

def chainer(s):
    return list(chain.from_iterable(s.str.split(',')))

def convert_df(df,cols):
    """
    function takes in dataframe and converts it into the necessary format for plotting the map
    cols : a list of columns with the order :
    [location, list of studies (things to be plotted), latitude, longitude]
    """
    df.dropna(inplace = True)
    df.set_index(df[cols[0]].values)
    df.dropna(inplace = True)
    L=[]
    for i in range(len(df)):
        string = ''
        for j in range (len(cols[1])):
            if j != len(cols[1]) -1 :
                string = string + str(df[cols[1][j]].values[i])+','
            else :
                string = string + str(df[cols[1][j]].values[i])

        L.append(string)
    df['New']=L

    lens = df['New'].str.split(',').map(len)
    df = pd.DataFrame({'Country': np.repeat(df[cols[0]], lens),
                        'Lat': np.repeat(df[cols[-2]], lens),
                        'Long_': np.repeat(df[cols[-1]], lens),
                        'Count': chainer(df['New'])})
    df['Study']=[cols[1][i] for i in range (len(cols[1]))]*(len(df.index)//len(cols[1]))
    return df

def create_data(df,study,color):
    """
    creates and returns the data parameter for the plotly plot functio
    given the df, object of study and color of scatter plot
    """ 
    countries = list(df['Country'].value_counts().index)
    data = []
    df.dropna(inplace = True)
    
    for country in countries:

        try:
            event_data = dict(
                lat = df.loc[(df['Study'] == study) & (df["Country"] == country),'Lat'],
                lon = df.loc[(df['Study'] == study) & (df["Country"] == country),'Long_'],
                name = study + " : " + country,
                marker = dict(size = log(float(df.loc[(df['Study'] == study) & (df["Country"] == country),                                                              'Count']), 1.5), opacity = 0.5,color = color),
                type = 'scattermapbox',
                hoverinfo="skip"
            )
            data.append(event_data)
        except:
            continue
    return data

def create_basic_layout(latitude,longitude):
    """
    Creates a layout centred about the given latitude and longitude
    """
    layout = dict(
        height = 800,
        margin = dict(t=0, b=0, l=0, r=0),
        font = dict(color='#FFFFFF', size=15),
        paper_bgcolor = '#000000',
        showlegend = False,
        
        mapbox = dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat = latitude,
                lon = longitude
            ),
            pitch = 0,
            zoom = 2,
            style = 'dark'
        ),
    )
    return layout

def update_layout(study,layout):
    """
    updates attributes of layout that are not common to all plots given the object of study
    """
    annotations = [dict(text= study.capitalize() + " Cases", 
         font=dict(color='#FFFFFF',size=14), borderpad=10, 
         x=0.05, y=0.05, xref='paper', yref='paper', align='left', showarrow=False, bgcolor='black')]

    layout['title'] = study.capitalize() + "Cases"
    layout['annotations'] = annotations 
    return layout

def interactive_map(data, layout):
    """
    creates map object given data to plot and layout and plots it
    """
    figure = dict(data=data, layout=layout)
    
    return figure

def plot_study(starting_df,cols,study_dict,location = "global"):
    """
    given the dataframe to take data from, the columns containing objects of study and the study to be plotted,and the basic       map layout
    this function plots required data on an interactive map
    """
    color = study_dict["color"]
    study = study_dict["study"]
    latitude = 20.59
    longitude = 78.96
    if location != "global" :
        latitude = int(country_cases_sorted.loc[(country_cases_sorted["country"] == location),'Lat'])
        longitude = int(country_cases_sorted.loc[(country_cases_sorted["country"] == location),'Long_'])

    df = convert_df(starting_df,cols)
    data = create_data(df,study,color)
    layout = create_basic_layout(latitude,longitude)
    updated_layout = update_layout(study,layout)
    figure = interactive_map(data, updated_layout)
    return figure