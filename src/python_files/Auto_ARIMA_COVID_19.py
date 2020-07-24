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
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima

# To import the main.py file
sys.path.append('../')
from python_files import main

# Getting all the data
confirmed_global, deaths_global, recovered_global, country_cases = main.collect_data()
rec = recovered_global.groupby("country").sum().T

rec.index = pd.to_datetime(rec.index, infer_datetime_format = True)

# Creating a dataframe with Total number of cases everyday in a column
data = pd.DataFrame(index = rec.index, data = rec["India"].values, columns = ["Total"])
data['Date'] = data.index

# Setting Date column as index
data=data.set_index('Date', drop=True)
print(data)

# Plotting the Data
px.line(data, template = 'plotly_dark')

# Setting a Split date for test and train datasets
split_date = pd.Timestamp('2020-05-17')
# Making sure no zeroes exist in dataframe
data = data[(data != 0).all(1)]

stepwise_model = auto_arima(data, start_p = 1, start_q = 1,
                           max_p = 3, max_q = 3, m = 12,
                           start_P = 0, seasonal = True,
                           d = 1, D = 1, trace = True,
                           error_action = 'ignore',  
                           suppress_warnings = True, 
                           stepwise = True)
# Finding the pest p,d,q parametes for the model
print(stepwise_model.aic())

# Splitting into test and train dataset
train = data.loc[:split_date]
test = data.loc[split_date:]
print('Test shape:',test.shape)
print('Train shape:',train.shape)
print(f'Min date from train set: {train.index.min().date()}')
print(f'Max date from train set:{train.index.max().date()}')
print(f'Min date from test set: {test.index.min().date()}')
print(f'Max date from test set: {test.index.max().date()}')

# Fitting the model with train dataset
stepwise_model.fit(train)

# Forecasting
future_forecast = stepwise_model.predict(n_periods=len(test))

# This returns an array of predictions:
print(future_forecast)
future_forecast = pd.DataFrame(future_forecast,index = test.index,columns=['Prediction'])

# Plotting the predicted values and actual values
px.line(pd.concat([data,future_forecast],axis=1), template = 'plotly_dark')

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

print(mean_absolute_percentage_error(test,future_forecast))

future_forecast['Actual']=test.Total
print(future_forecast)