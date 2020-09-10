## Importing libraries

import sys
import pandas as pd
import numpy as np
import math
import plotly.graph_objects as go
from pmdarima import auto_arima
from sklearn.model_selection import train_test_split
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Ignoring warnings
import warnings
warnings.filterwarnings("ignore")

# To import the main.py file
sys.path.append('../')
from python_files import main

## Data Preprocessing Functions

def get_data():
    confirmed_global, deaths_global, recovered_global, country_cases = main.collect_data()
    
    recovered = recovered_global.groupby("country").sum().T
    deaths = deaths_global.groupby("country").sum().T
    confirmed = confirmed_global.groupby("country").sum().T
    
    deaths.index = pd.to_datetime(deaths.index, infer_datetime_format = True)
    recovered.index = pd.to_datetime(recovered.index, infer_datetime_format = True)
    confirmed.index = pd.to_datetime(confirmed.index, infer_datetime_format = True)
    
    return deaths, recovered, confirmed

def create_data_frame(dataframe,country):
    deaths, recovered, confirmed = get_data()
    if dataframe == 'deaths':
        data = pd.DataFrame(index = deaths.index, data = deaths[country].values, columns = ["Total"])

    elif dataframe == 'recovered':
        data = pd.DataFrame(index = recovered.index, data = recovered[country].values, columns = ["Total"])

    elif dataframe == 'confirmed':
        data = pd.DataFrame(index = confirmed.index, data = confirmed[country].values, columns = ["Total"])

    data = data[(data != 0).all(1)]
    
    data['Date'] = data.index
    cols = [data.columns[-1]] + [col for col in data if col != data.columns[-1]]
    data = data[cols]   

    return data

## Graphing Functions

def plot_forecast(data,forecast):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data["Date"], y=data["Total"],   
                            mode='lines',
                            name='Up till now '))
        
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast.values,   
                            mode='lines',
                            name='Prediction*'))

    fig.update_layout(title={
                'text': "Forecasted results",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
                        template = "plotly_dark",
                        xaxis_title="Date",
                        yaxis_title="Cases",
                        legend_title="Legend ",
                        font=dict(
                                family="Arial",
                                size=15,
                                color="white"
                                )
                        )
    return fig

## Functions to train and test the model

def find_params(train_set):
    stepwise_model = auto_arima(train_set, method='nm', start_p = 0, start_q = 0,
                               max_p = 2, max_q = 2, m = 7,
                               start_P = 0, max_P=0, start_Q=1, max_Q=1, seasonal = True,
                               d = None, D = 1, n_jobs=-1, trace = True,
                               error_action = 'ignore',  
                               suppress_warnings = True, 
                               stepwise = True)
    return stepwise_model

def Predict(stepwise_model,train,test):
    
    stepwise_model.fit(train)
    
    pred = stepwise_model.predict(n_periods=len(test))
    
    pred = pd.DataFrame(pred,index = test.index,columns=['Prediction'])
   
    return pred

## Error Function 

def mape(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

## Function for forecasting

def Future(df,order,seasonal_order,train,test,data):
    
    model = SARIMAX(df['Total'],  
                        order = order,  
                        seasonal_order = seasonal_order) 
    result = model.fit() 
  
    forecast = result.predict(start = len(df),  
                          end = (len(df)-1) + 14).rename('Forecast') 
    
 
    error_check = result.predict(start = len(train), end = len(train) - 1 +len(test))
    error = mape(error_check,test)
    error = error
    graph = plot_forecast(data,forecast)

    return forecast,graph,error

## Calling function

def arima_predict(df_name,country):
    data = create_data_frame(df_name,country)
    
    train = data["Total"][:len(data)*4//5]
    test = data["Total"][len(data)*4//5:]
    
    model = find_params(train)
    pred = Predict(model,train,test)
    mape_error = mape(test, pred["Prediction"])
    
    order=model.get_params()['order']
    seasonal_order=model.get_params()['seasonal_order']
    
    forecast,graph,error = Future(data,order, seasonal_order, train, test,data)
    
    return forecast,graph,(error + np.std([error, mape_error]))
