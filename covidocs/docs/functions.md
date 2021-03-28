---
title: Functions and their Purpose
---

#### app.py
| SL.NO | FUNCTIONS | USES |
| --- | --- | --- |
| 1   | collect_data() | Retrieve and pre process data from the John Hopkins University Dataset on GitHub |
| 2   | get\_today\_data() | Retrieve today's data. |
| 3   | cases_object() | Create the cases object. |
| 4   | choose_country() | Choose a Country from the list of countries. |
| 5   | get\_final\_object() | Get the final object with data. |
| 6   | update_message() | Get the time of the most recent update of data. |
| 7   | update_graphs() | Plot the graphs on screen in accordance with the choice. |
| 8   | update_cases() | Get the latest number of cases. |
| 9   | update\_country\_message() | Get the time of the most recent update of the country's data. |
| 10  | update\_graphs\_country() | Plot the graphs on screen in accordance with the choice of country. |
| 11  | update\_cases\_country() | Get the latest number of cases of a country. |
| 12  | update_stats() | Get province wise details of a country. |
| 13  | forecast_cases() | Forecast the cases based on metric selected using the custom CNN Model. |
| 14  | display_page() | Display the page on the website based on the choice. |


#### cnn.py
| SL.NO | FUNCTIONS | USES |
| --- | --- | --- |
| 15  | get_data() | Get the required data from the original dataset. |
| 16  | create\_data\_frame() | Create a dataframe on which all operations would be conducted. |
| 17  | make_series() | Create a series of daily data from the cumulative data. |
| 18  | mase() | Return the mean absolute scaled error between the real and predicted values. |
| 19  | create\_param\_grid() | Create the grid with all the parameters for hyperparameter Tuning. |
| 20  | compile_model() | Compile the customised 1 Dimensional CNN Model with optimal parameters. |
| 21  | hyperparameter_tuning() | Original Implementation to tune the parameters which define the model architecture. |
| 22  | get\_best\_params() | Get the values with the least mean absolute scaled error. |
| 23  | test_model() | Test the predictions of the model on known data using MASE as the metric for evaluation. |
| 24  | make\_final\_model() | Generate the final model. |
| 25  | forecast() | Forecast unseen data using the model. |
| 26  | plot_graph() | Return a visual representation of the current situation for better understanding. |
| 27  | check_slope() | Check the slope and make sure it is not Zero. |
| 28  | naive_forecast() | Perform a naive forecast. |
| 29  | cnn_predict() | Perform the predictions such that if MASE is more than one, then a naive forecast is performed. |


#### country_visuals.py
| SL.NO | FUNCTIONS | USES |
| --- | --- | --- |
| 30  | get\_country\_frame() |  Get a dataframe with all the values required for a specific country.  |
| 31  | plot_province() | Get a visual representation of the provincial data. |
| 32  | table\_province\_data() | Get a tabulated representation of provincial data. |


#### maps.py
| SL.NO | FUNCTIONS | USES |
| --- | --- | --- |
| 33  | chainer() | To get a list from series of comma-separated strings. |
| 34  | convert_df() | To convert the dataframe to a form suitable to work with. |
| 35  | create_hovertemplate() | To create hovertemplates for the maps. |
| 36  | create_data() | To create the data object for the interactive map. |
| 37  | create\_basic\_layout() | To create the basic layout for the interactive map. |
| 38  | update_layout() | To create a modified layout. |
| 39  | get\_lat\_long() | To get the latitude and longitude of a country. |
| 40  | get\_country\_wise_data() | To get the data grouped by country. |
| 41  | interactive_map() | To create the interactive map. |
| 42  | plot_study() |  To plot the global map for a given study (confirmed/deaths/recovered)  |
| 43  | plot_country() | To plot the the given study (confirmed/deaths/recovered) for a particular country  |


#### timeseries.py
| SL.NO | FUNCTIONS | USES |
| --- | --- | --- |
| 44  | get\_new\_cases() | To get the new confirmed cases. |
| 45  | get\_new\_deaths() | To get the new deaths. |
| 46  | get\_new\_recoveries() | To get the new recoveries. |
| 47  | get_plot() | To get the graph for the required metric(confirmed,recovered,deaths). |
| 48  | plot_timeseries() | To plot the number of new cases of each day. |
| 49  | get\_world\_timeseries(). | To get a dataframe with global data |
| 50  | plot\_world\_timeseries(). | To create a chart of the global data |


#### animations.py
| SL.NO | FUNCTIONS | USES |
| --- | --- | --- |
| 51  | unpivot(). | to unpivot/melt the dataframe |
| 52  | take_top10(). |  To take the top ten countries with the highest number of cases of given study  |
| 53  | line\_comparison\_data() |  To create a static line chart for a given study(confirmed/deaths/recovered) for one or more countries|
| 54 | animated_barchart() | To create an animated barchart showing change in situation with time |