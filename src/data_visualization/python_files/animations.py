'''
# Animations
This file contains some animations visualizing the outbreak and spread of COVID-19 across the world.
'''

# Imports
import main
import copy
import sys
import os
from datetime import datetime
from datetime import date
from datetime import timedelta
import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

# Data Collection and Preprocessing
confirmed_global, deaths_global, recovered_global, country_cases = main.collect_data()

bar_df = confirmed_global.transpose()
l = [datetime.strptime(date, '%m/%d/%y').strftime('20%y-%m-%d') for date in bar_df.index[1:]]
l.insert(0, 0)
bar_df.set_index(pd.Index(l), inplace=True)

L = pd.to_datetime(l, utc=False)
bar_df.set_index(pd.Index(L), inplace=True)
bar_df = bar_df.transpose()
pio.templates.default = 'plotly'

def daterange(date1, date2,n):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(days=n)
        
def animated_barchart(dataset, categorical_col, start, end, title , frame_rate=3):
    names = dataset[categorical_col]
    yvals = dataset.loc[:, start]

    def get_colors():
        r = np.random.randint(1, 187)
        g = np.random.randint(1, 187)
        b = np.random.randint(1, 187)
        return [r, g, b]

    colors = []
    for i in range(len(names)):
        c = get_colors()
        colors.append(f'rgb({str(c[0])}, {str(c[1])}, {str(c[2])})')
       
    def top_10(d):
        df = pd.DataFrame({'names': names, 'pop': d, 'color': colors})
        data = df.sort_values(by='pop').iloc[-10:,]
        return data
    
    list_of_frames = []
    for i in daterange(start, end, frame_rate):
        d = bar_df.loc[:, str(i)]
        p_data = top_10(d)
        list_of_frames.append(
            go.Frame(
                data=[
                    go.Bar(
                        x=p_data['names'], y=p_data['pop'],
                        marker_color=p_data['color'], text=p_data['names'],
                        hoverinfo='none', textposition='outside',
                        texttemplate='%{x}<br>%{y:s}', cliponaxis=False
                    )
                ],
                layout=go.Layout(
                    font={'size': 20},
                    height=700,
                    xaxis={'showline': False,'tickangle': -90, 'visible': False},
                    yaxis={'showline': False, 'visible': False},
                    title=f'{title} For: {str(i.date())}'
                )
            )
        )

    f_data = top_10(yvals)

    fig = go.Figure(
        data=[
            go.Bar(
                x=f_data['names'], y=f_data['pop'],
                marker_color=f_data['color'], text=f_data['names'],
                hoverinfo='none', textposition='outside',
                texttemplate='%{x}<br>%{y:s}', cliponaxis=False
            )
        ],
        layout=go.Layout(
            font={'size': 20},
            height=700,
            xaxis={'showline': False,'tickangle': -90, 'visible': False},
            yaxis={'showline': False, 'visible': False},
            title=f'{title} For: {str(start.date())}',
            updatemenus=[
                dict(
                    type='buttons',
                    buttons=[
                        dict(
                            label='Play',
                            method='animate',
                            args=[
                                None, {
                                    'frame': {'duration': 200},
                                    'fromcurrent': True
                                }
                            ]
                        ),
                        {
                            'args': [
                                [None],
                                {
                                    'frame': {
                                        'duration': 0,
                                        'redraw': False
                                    },
                                    'mode': 'immediate',
                                    'transition': {'duration': 0}
                                }
                            ],
                            'label': 'Pause',
                            'method': 'animate'
                        }
                    ]
                )
            ]
        ),
        frames=list(list_of_frames)
    )
    return fig



animated_barchart(bar_df, '1970-01-01', bar_df.columns[1], bar_df.columns[-1], title="Top 10 Countries Visualization", frame_rate=24)
