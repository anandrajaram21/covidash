## Animations

# Imports

import sys
from datetime import datetime,date,timedelta
import pandas as pd
import numpy as np
import plotly.io as pio
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode

# To import the main.py file
sys.path.append('../')
from python_files import main

# Getting all the data
confirmed_global, deaths_global, recovered_global, country_cases = main.collect_data()

## BAR GRAPH

bar_df = confirmed_global.transpose()
l = [datetime.strptime(date,"%m/%d/%y").strftime("20%y-%m-%d") for date in bar_df.index[1:]]
l.insert(0,0)
bar_df.set_index(pd.Index(l),inplace=True)
L = pd.to_datetime(l,utc=False)

bar_df.set_index(pd.Index(L),inplace=True)
bar_df = bar_df.transpose()
pio.templates.default = "plotly"

def daterange(date1, date2,n):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(days=n)
        
def animated_barchart(dataset, categrical_col, start, end, title , frame_rate = 3):
    names = dataset[categrical_col]
    yvals = dataset.loc[:,start]
    def get_colors():
        r = np.random.randint(1,187)
        g = np.random.randint(1,187)
        b = np.random.randint(1,187)
        return [r,g,b]
    colors = []
    for i in range(len(names)):
        c = get_colors()
        colors.append("rgb(" + str(c[0]) + ","+ str(c[1]) + ","+ str(c[2]) + ")")
       
    def top_10(d):
        df = pd.DataFrame({"names":names, "pop":d, "color":colors})
        data = df.sort_values(by = "pop").iloc[-10:,]
        return data
    
    listOfFrames = []
    for i in daterange(start,end,frame_rate):
        d = bar_df.loc[:,str(i)]
        pdata = top_10(d)
        listOfFrames.append(go.Frame(data = [go.Bar(x = pdata["names"], y = pdata["pop"],
                                                    marker_color = pdata["color"], text = pdata["names"],
                                                    hoverinfo = "none",textposition = "outside",
                                                    texttemplate = "%{x}<br>%{y:s}",cliponaxis = False)],
                                     layout = go.Layout(
                                         font = {"size":20},
                                         height = 700,
                                         xaxis = {"showline":False,"tickangle":-90, "visible":False},
                                         yaxis = {"showline":False, "visible":False},
                                        title = title + " For: "+ str(i.date()))))

    fData = top_10(yvals)
    
    fig = go.Figure(
    data = [go.Bar(x = fData["names"], y = fData["pop"],
                   marker_color = fData["color"],text = fData["names"],
                  hoverinfo = "none",textposition = "outside",
                   texttemplate = "%{x}<br>%{y:s}",cliponaxis = False)],
    layout=go.Layout(
        title=title + " For: "+str(start.date()),
        font = {"size":20},
        height = 700,
        xaxis = {"showline":False,"tickangle":-90, "visible":False},
        yaxis = {"showline":False, "visible":False},
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play",
                          method="animate",
                          args=[None, {"frame": {"duration": 200},
                                "fromcurrent": True}]),{
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }])]
    ),
    frames=list(listOfFrames)
    )
    fig.show()

animated_barchart(bar_df, '1970-01-01',bar_df.columns[1],bar_df.columns[-1],title = "VIZUALIZATION OF TOP 10 BY COMPARISON", frame_rate = 24)
