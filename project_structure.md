# COVID-19 Exploratory Data Analysis

## Data Preprocessing and Collection

- Data from the John Hopkins University Dataset on GitHub
- https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series

## Data Visualization

- Global outbreak analysis

- Showing worst affected countries side by side for a direct comparison - Done

- Plotting chloropleths of the world map, for a nice interactive visualization (show details on hovering over the country)

- Data for each of the top 5 countries to be analyzed
    - Plot number of confirmed cases each day - 1 graph - Done
    - Plot number of deaths each day - 1 graph - Done
    - Recovery rate - 1 graph - Done
    
- Probably add some stuff

## Predictions

- Software to be used - Tensorflow, keras, sklearn

- Predictions for each country
    - Predict confirmed cases
    - Predict confirmed deaths
    - Recovery rate

- Models we can use:
    - Decision tree regressor
    - Random forest regressor
    - XGBoost regressor

- For each model, we must do these stuff
    - Plot predictions against actual values
    - Hyperparameter tuning for each model using GridSearchCV

- Artificial Neural Network
    - Try and maximize the accuracy for each country

## Streamlit

- To make an interactive dashboard, and display everything we analyzed, and everything we predicted
- Clickable chloropleth ( if possible )
- Update all data automatically

### Notes
- Add screenshots of the project taken at different times (to prove values are not hard coded)

### Timeframes
- Exploratory data analysis - 1 month
- Predictions - 1.5 month
- Plotly dash - 1 month

### Only if we have time ( in order of preference )

- State wise analysis on India, (and US too iff, time permits)
- Make inferences from the EDA
- Add countries to the detailed analysis
