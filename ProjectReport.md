## ACKNOWLEDGEMENT

The success of a project depends upon the persistent efforts of an individual along with the sustained support received from others. My strength is all due to my honorable Principal, who has been an unending source of inspiration and support towards the accomplishment of this project.

I would like to express my deepest sense of gratitude to my computer teacher without whom I could not have successfully completed this project.

Finally, my personal gratitude is extended towards my parents who have been a constant source of encouragement and support in the success of this project.

## SYNOPSIS

The rapid spread of COVID-19 across the globe is affecting millions of people and is at the same time resulting in the spread of information, misinformation (false information spread without malicious intent) and disinformation (false information spread with the intent to deceive). Our intention is not to create additional information, but to bring together credible COVID-19 related information that is easy to access, understand and act upon.

The project is mainly based on Machine Learning, with a custom model built specifically for the task at hand i.e. to analyze and predict the cases in the near future.

The model used is a 1-Dimensional Convolutional Neural Network for identifying patterns, and an Artificial Neural Network Hybrid for the prediction

## HARDWARE AND SOFTWARE SPECIFICATIONS

#### MINIMUM REQUIREMENTS

- Processor : Intel® CoreTM i3 CPU
- CPU Speed : 2.2 GHz
- RAM : 4GB

#### RECOMMENDED REQUIREMENTS

- Processor : Intel® CoreTM i5 CPU
- CPU Speed : 2.8 GHz
- RAM : 8GB

#### SOFTWARE

❖ Operating System : Any 64 bit OS
❖ Software : Python 3.8, Chrome or Firefox (works with Safari too, but loading speeds are a lot slower), pip

## SYSTEM DESIGN

### LIBRARY MODULES AND THEIR PURPOSE

| SL.NO | LIBRARY MODULES | PURPOSE |
| --- | --- | --- |
| 1   | dash | To create a visually appealing website. |
| 2   | plotly | To create beautiful, fully extensible, and interactive graphs. |
| 3   | pandas | To allow smooth handling of data. |
| 4   | datetime | To provide functions for working with dates and time. |
| 5   | requests | To send HTTP requests using Python. |
| 6   | os  | To provide functions for interacting with the operating system. |
| 7   | flask_caching | To increase program efficiency with the help of caching. |
| 8   | time | To provide various time-related functions. |
| 9   | pickle | To work with binary files. |
| 10  | numpy | To provide functions for working with arrays. |
| 11  | collections | To provide different types of containers. |
| 12  | TSErrors | To analyse time series prediction errors. |
| 13  | sklearn | To provide powerful machine learning tools for data analysis. |
| 14  | keras | To develop and evaluate deep learning models. |
| 15  | chart_studio | To make interactive, publication-quality graphs online. |
| 16  | itertools | To provide a collection of tools for handling iterators. |
| 17  | math | To access mathematical functions in Python. |
| 18  | app_vars | To allow reusability of variables (custom module). |
| 19  | time_series | To provide functions for working with timeseries (custom module). |

### FUNCTIONS AND THEIR PURPOSE

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
| 30  | get\_country\_frame() |  Get a dataframe with all the values required for a specific country.  |
| 31  | plot_province() | Get a visual representation of the provincial data. |
| 32  | table\_province\_data() | Get a tabulated representation of provincial data. |
| 33  | chainer() | To get a list from series of comma-separated strings. |
| 34  | convert_df() | To convert the dataframe to a form suitable to work with. |
| 35  | create_hovertemplate() | To create hovertemplates for the maps. |
| 36  | create_data() | To create the data object for the interactive map. |
| 37  | create\_basic\_layout() | To create the basic layout for the interactive map. |
| 38  | update_layout() | To create a modified layout. |
| 39  | get\_lat\_long() | To get the latitude and longitude of a country. |
| 40  | get\_country\_wise_data() | To get the data grouped by country. |
| 41  | interactive_map() | To create the interactive map. |
| 42  | plot_study() |  Arun please fill this in  |
| 43  | plot_country() | To plot the situation of the country. |
| 44  | get\_new\_cases() | To get the new confirmed cases. |
| 45  | get\_new\_deaths() | To get the new deaths. |
| 46  | get\_new\_recoveries() | To get the new recoveries. |
| 47  | get_plot() | To get the graph for the required metric(confirmed,recovered,deaths). |
| 48  | plot_timeseries() | To plot the number of new cases of each day. |
| 49  | get\_world\_timeseries(). | To get a dataframe with global data |
| 50  | plot\_world\_timeseries(). | To create a chart of the global data |
| 51  | unpivot(). | to unpivot the dataframe |
| 52  | take_top10(). |   Arun fill this in please  |
| 53  | line\_comparison\_data() |  Arun fill this in please   |
| 54  | compare() |   Arun fill this in please  |
| 55  | animated_barchart() | To create an animated barchart showing change in situation with time |
| 56  | make_column() | To add a column in the dataframe with relevant stats |
| 57  | get() |   Arun fill this in please  |

## DATA DICTIONARY

The data files that have been used in the project are:

| SL.NO | LIBRARY MODULES | PURPOSE |
| --- | --- | --- |
| 1   | confirmed_global.csv | To provide the global data for confirmed cases |
| 2   | country_cases.csv | To provide country wise data |
| 3   | deaths_global.csv | To provide the global data for deaths |
| 4   | recovered_global.csv | To provide the global data for recoveries |

## SOURCE CODE

```python
    # Imports and data preprocessing
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    import dash_bootstrap_components as dbc
    import plotly.express as px
    import plotly.graph_objects as go
    import pandas as pd
    from datetime import date
    import requests
    from datetime import timedelta
    import plotly.io as pio
    import os
    from flask_caching import Cache
    import app_vars as av
    import time
    import datetime
    import pickle

    pio.templates.default = "plotly_dark"

    external_stylesheets = [dbc.themes.CYBORG]

    app = dash.Dash(
        __name__,
        external_stylesheets=external_stylesheets,
        meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    )

    server = app.server

    cache = Cache(
        server,
        config={
            "CACHE_TYPE": "simple",
        },
    )


    TIMEOUT = 3600


    @cache.memoize(timeout=TIMEOUT)
    def collect_data():
        filenames = [
            "time_series_covid19_confirmed_global.csv",
            "time_series_covid19_deaths_global.csv",
            "time_series_covid19_recovered_global.csv",
        ]
        url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
        confirmed_global = pd.read_csv(url + filenames[0])

        deaths_global = pd.read_csv(url + filenames[1])

        recovered_global = pd.read_csv(url + filenames[2])

        country_cases = pd.read_csv(
            "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
        )

        confirmed_global.drop(columns=["Province/State", "Lat", "Long"], inplace=True)

        deaths_global.drop(columns=["Province/State", "Lat", "Long"], inplace=True)

        recovered_global.drop(columns=["Province/State", "Lat", "Long"], inplace=True)

        country_cases.drop(
            columns=[
                "Last_Update",
                "Incident_Rate",
                "People_Tested",
                "People_Hospitalized",
                "UID",
            ],
            inplace=True,
        )

        confirmed_global.rename(columns={"Country/Region": "country"}, inplace=True)
        deaths_global.rename(columns={"Country/Region": "country"}, inplace=True)
        recovered_global.rename(columns={"Country/Region": "country"}, inplace=True)

        country_cases.rename(
            columns={
                "Country_Region": "country",
                "Confirmed": "confirmed",
                "Deaths": "deaths",
                "Recovered": "recovered",
                "Active": "active",
                "Mortality_Rate": "mortality",
            },
            inplace=True,
        )

        confirmed_global = confirmed_global.groupby(["country"], as_index=False).sum()
        deaths_global = deaths_global.groupby(["country"], as_index=False).sum()
        recovered_global = recovered_global.groupby(["country"], as_index=False).sum()

        country_cases_sorted = country_cases.sort_values("confirmed", ascending=False)
        country_cases_sorted.index = [x for x in range(len(country_cases_sorted))]

        return (confirmed_global, deaths_global, recovered_global, country_cases_sorted)


    @cache.memoize(timeout=TIMEOUT)
    def get_today_data():
        today_data = requests.get("https://corona.lmao.ninja/v2/all?yesterday")
        today_country_data = requests.get("https://corona.lmao.ninja/v2/jhucsse")

        today_data = today_data.json()
        today_country_data = today_country_data.json()

        return today_data, today_country_data


    def cases_object(array):
        obj1 = {
            study: sum([(i["stats"][study]) for i in array])
            for study in ["confirmed", "deaths", "recovered"]
        }
        return {**obj1, "updatedAt": [i["updatedAt"] for i in array]}


    def choose_country(array, country):
        return [i for i in array if (i["country"] == country)]


    def get_final_object(country, array):
        return cases_object(choose_country(array, country))


    (
        today_data,
        today_country_data,
    ) = get_today_data()

    (
        av.confirmed_global,
        av.deaths_global,
        av.recovered_global,
        av.country_cases,
    ) = collect_data()

    av.country_cases_sorted = av.country_cases

    (
        confirmed_global,
        deaths_global,
        recovered_global,
        country_cases,
        country_cases_sorted,
    ) = (
        av.confirmed_global,
        av.deaths_global,
        av.recovered_global,
        av.country_cases,
        av.country_cases_sorted,
    )

    # Importing these modules later as they rely on having data stored

    import animations
    import maps
    import country_visuals as cv
    import timeseries

    import cnn

    # Making the Graphs and Declaring the Variables Required for the Pages

    animations_figure = animations.animated_barchart(confirmed_global, "confirmed")

    confirmed = dict(study="confirmed", color="#45a2ff")
    recovered = dict(study="recovered", color="#42f587")
    deaths = dict(study="deaths", color="#f54842")

    columns = ["country", ["deaths", "confirmed", "recovered"], "Lat", "Long_"]

    world_map = maps.plot_study(country_cases_sorted, columns, confirmed)

    confirmed_timeseries = timeseries.plot_world_timeseries(
        confirmed_global, "confirmed", n=-20, daily=True
    )

    country_list = confirmed_global["country"]

    today = date.today()

    world_timeseries_confirmed = timeseries.get_world_timeseries(confirmed_global)
    world_timeseries_deaths = timeseries.get_world_timeseries(deaths_global)
    world_timeseries_recovered = timeseries.get_world_timeseries(recovered_global)

    confirmed_global_cases_today = format(today_data["cases"], ",d")
    confirmed_recovered_cases_today = format(today_data["recovered"], ",d")
    confirmed_deaths_cases_today = format(today_data["deaths"], ",d")

    # Making the Individual Pages

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Global Situation", href="/global")),
            dbc.NavItem(dbc.NavLink("Country Analysis", href="/country")),
            dbc.NavItem(dbc.NavLink("Forecasts", href="/forecast")),
            dbc.NavItem(dbc.NavLink("Preventive Measures", href="/prevent")),
        ],
        dark=True,
        color="dark",
        brand="Covidash",
        brand_href="/",
    )

    home_page = dbc.Container(
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Img(
                                                src="https://fourremovalsolutions.sg/wp-content/uploads/2020/04/Four-Solutions-Disinfecting-Spraying-01.png",
                                                height="100%",
                                                width="100%",
                                                style={"border-radius": "2rem"},
                                            ),
                                            sm=12,
                                            md=8,
                                            lg=9,
                                        ),
                                        dbc.Col(
                                            [
                                                html.H4(
                                                    "Save yourself",
                                                    style={
                                                        "text-align": "left",
                                                        "padding-top": "5%",
                                                        "font-size": "1.4rem",
                                                    },
                                                ),
                                                html.H4(
                                                    "Save the world.",
                                                    style={
                                                        "text-align": "left",
                                                        "font-size": "1.4rem",
                                                    },
                                                ),
                                                html.Br(),
                                                html.P(
                                                    "Coronavirus disease 2019 (COVID-19) is an infectious disease caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). It was first identified in December 2019 in Wuhan, Hubei, China, and has resulted in an ongoing pandemic.",
                                                    style={"text-align": "left"},
                                                ),
                                                html.Br(),
                                                dbc.Button(
                                                    "Preventive Measures",
                                                    color="danger",
                                                    className="mr-1",
                                                    style={"border-radius": "1rem"},
                                                    id="prevent-button",
                                                    href="/prevent",
                                                ),
                                            ],
                                            sm=12,
                                            md=4,
                                            lg=3,
                                        ),
                                    ],
                                ),
                            ],
                            className="clearfix",
                        )
                    ]
                ),
                style={
                    "width": "100%",
                    "display": "flex",
                    "flex": "1 1 auto",
                    "margin-top": "5%",
                    "margin-bottom": "5%",
                    "border-radius": "2rem",
                    "background-color": "#060606",
                },
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Symptoms of COVID-19",
                                        className="card-title",
                                        style={
                                            "text-align": "center",
                                            "font-weight": "bold",
                                        },
                                    ),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Img(
                                                        src="https://image.freepik.com/free-vector/coronavirus-symptoms-concept_23-2148496136.jpg",
                                                        height="100%",
                                                        width="100%",
                                                        className="img-fluid",
                                                        style={
                                                            "padding-bottom": "10%",
                                                            "border-radius": "5rem",
                                                        },
                                                    ),
                                                    sm=8,
                                                    lg=6,
                                                    md=12,
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                    },
                                                ),
                                                dbc.Col(
                                                    html.P(
                                                        "Common symptoms include fever, cough, fatigue, shortness of breath, and loss of smell and taste. While the majority of cases result in mild symptoms, some progress to acute respiratory distress syndrome (ARDS) possibly precipitated by cytokine storm, multi-organ failure, septic shock, and blood clots. The time from exposure to onset of symptoms is typically around five days, but may range from two to fourteen days.",
                                                        style={
                                                            "text-align": "left",
                                                            "font-size": "large",
                                                        },
                                                    ),
                                                    sm=12,
                                                    md=12,
                                                    lg=6,
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                    },
                                                ),
                                            ]
                                        ),
                                        className="clearfix",
                                    ),
                                ]
                            ),
                            style={
                                "width": "100%",
                                "display": "flex",
                                "flex": "1 1 auto",
                                "margin-top": "5%",
                                "margin-bottom": "5%",
                                "border-radius": "2rem",
                                "background-color": "#f5f5f5",
                                "color": "black",
                            },
                        ),
                        lg=8,
                        md=8,
                        sm=12,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Treatment",
                                        className="card-title",
                                        style={
                                            "text-align": "center",
                                            "font-weight": "bold",
                                        },
                                    ),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Img(
                                                        src="https://image.freepik.com/free-vector/scientists-working-creating-covid-19-vaccine_23-2148551283.jpg",
                                                        height="100%",
                                                        width="100%",
                                                        className="img-fluid",
                                                        style={
                                                            "padding-bottom": "10%",
                                                            "border-radius": "5rem",
                                                        },
                                                    ),
                                                    sm=8,
                                                    lg=6,
                                                    md=12,
                                                ),
                                                dbc.Col(
                                                    html.P(
                                                        "    There are no vaccines nor specific antiviral treatments for COVID-19. Management involves the treatment of symptoms, supportive care, isolation, and experimental measures. The World Health Organization (WHO) declared the COVID‑19 outbreak a public health emergency of international concern (PHEIC) on 30 January 2020 and a pandemic on 11 March 2020. Local transmission of the disease has occurred in most countries across all six WHO regions.",
                                                        style={
                                                            "text-align": "left",
                                                            "font-size": "large",
                                                        },
                                                    ),
                                                    sm=12,
                                                    md=12,
                                                    lg=6,
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                    },
                                                ),
                                            ]
                                        ),
                                        className="clearfix",
                                    ),
                                ]
                            ),
                            style={
                                "width": "100%",
                                "display": "flex",
                                "flex": "1 1 auto",
                                "margin-top": "5%",
                                "margin-bottom": "5%",
                                "border-radius": "2rem",
                                "background-color": "#f5f5f5",
                                "color": "black",
                            },
                        ),
                        lg=8,
                        md=8,
                        sm=12,
                    ),
                ],
                style={"justify-content": "center"},
            ),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H5(
                                                    "Global Situation",
                                                    className="card-title",
                                                    style={"text-align": "center"},
                                                ),
                                                html.P(
                                                    "See the statistics for the global situation",
                                                    className="card-text",
                                                ),
                                                dbc.Button(
                                                    "Global Situation",
                                                    href="/global",
                                                    style={
                                                        "text-align": "center",
                                                        "background-color": "#322daa",
                                                        "border-color": "transparent",
                                                        "border-radius": "1rem",
                                                    },
                                                    className="mr-1",
                                                    block=True,
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={
                                        "border-radius": "2rem",
                                        "border-color": "#322daa",
                                        "background-color": "#000000",
                                        "border-style": "solid",
                                        "border-width": "medium",
                                    },
                                    inverse=True,
                                    className="mb-4",
                                ),
                                sm=12,
                                md=12,
                                lg=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H5(
                                                    "Country Analysis",
                                                    className="card-title",
                                                    style={"text-align": "center"},
                                                ),
                                                html.P(
                                                    "See the statistics for your country",
                                                    className="card-text",
                                                ),
                                                dbc.Button(
                                                    "Country Analysis",
                                                    href="/country",
                                                    style={
                                                        "text-align": "center",
                                                        "background-color": "#322daa",
                                                        "border-color": "transparent",
                                                        "border-radius": "1rem",
                                                    },
                                                    className="mr-1",
                                                    block=True,
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={
                                        "border-radius": "2rem",
                                        "border-color": "#322daa",
                                        "background-color": "#000000",
                                        "border-style": "solid",
                                        "border-width": "medium",
                                    },
                                    inverse=True,
                                ),
                                sm=12,
                                md=12,
                                lg=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.H5(
                                                    "Forecasts",
                                                    className="card-title",
                                                    style={"text-align": "center"},
                                                ),
                                                html.P(
                                                    "Generate forecasts for your country",
                                                    className="card-text",
                                                ),
                                                dbc.Button(
                                                    "Forecast",
                                                    href="/forecast",
                                                    style={
                                                        "text-align": "center",
                                                        "background-color": "#322daa",
                                                        "border-color": "transparent",
                                                        "border-radius": "1rem",
                                                    },
                                                    className="mr-1",
                                                    block=True,
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={
                                        "border-radius": "2rem",
                                        "border-color": "#322daa",
                                        "background-color": "#000000",
                                        "border-style": "solid",
                                        "border-width": "medium",
                                    },
                                    inverse=True,
                                ),
                                sm=12,
                                md=12,
                                lg=4,
                            ),
                        ],
                        className="mb-4",
                    ),
                ],
            ),
        ],
        className="mt-5",
    )

    global_page = html.Div(
        children=[
            dbc.Row(
                children=[
                    dbc.Col(
                        dbc.Button(
                            "Confirmed Cases",
                            size="lg",
                            id="confirmed",
                            color="primary",
                            block=True,
                            outline=True,
                        ),
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Recoveries",
                            size="lg",
                            id="recoveries",
                            color="success",
                            block=True,
                            outline=True,
                        ),
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Deaths",
                            size="lg",
                            id="deaths",
                            color="danger",
                            block=True,
                            outline=True,
                        ),
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="mb-4",
                    ),
                ]
            ),
            dbc.Row(html.H3(id="global-message"), className="mt-5 justify-content-center"),
            dbc.Row(
                dbc.Col(
                    dcc.Loading(dcc.Graph(id="metric-output"), id="map-loading"), width=12
                ),
                className="mt-5 justify-content-center",
            ),
            dbc.Row(html.H3("Time Series"), className="mt-5 justify-content-center"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(dcc.Graph(id="timeseries-output"), id="ts-loading"),
                        sm=12,
                        md=12,
                        lg=8,
                        xl=8,
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.Row(html.H4("Today"), className="ml-3 mt-2"),
                                    dbc.Row(html.H5(id="today"), className="ml-3 mb-2"),
                                ],
                                style={
                                    "borderRadius": "30px",
                                    "backgroundColor": "#8634eb",
                                },
                                className="mt-3 p-3",
                            ),
                            html.Div(
                                [
                                    dbc.Row(html.H4("Last Week"), className="ml-3 mt-2"),
                                    dbc.Row(
                                        [
                                            html.H5(id="lastweek"),
                                            html.H5(
                                                id="lastweek-diff",
                                                style={"color": "red"},
                                                className="ml-3",
                                            ),
                                        ],
                                        className="ml-3 mb-2",
                                    ),
                                ],
                                style={
                                    "borderRadius": "30px",
                                    "backgroundColor": "#8634eb",
                                },
                                className="mt-3 p-3",
                            ),
                            html.Div(
                                [
                                    dbc.Row(html.H4("Last Month"), className="ml-3 mt-2"),
                                    dbc.Row(
                                        [
                                            html.H5(id="lastmonth"),
                                            html.H5(
                                                id="lastmonth-diff",
                                                style={"color": "red"},
                                                className="ml-3",
                                            ),
                                        ],
                                        className="ml-3 mb-2",
                                    ),
                                ],
                                style={
                                    "borderRadius": "30px",
                                    "backgroundColor": "#8634eb",
                                },
                                className="mt-3 p-3",
                            ),
                        ],
                        className="align-items-center",
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                    ),
                ],
                className="mt-5 align-items-center",
            ),
            dbc.Row(html.H3("Animation"), className="mt-5 justify-content-center"),
            dbc.Row(
                dbc.Col(
                    dcc.Loading(dcc.Graph(id="animation-output"), id="animation-loading"),
                    sm=12,
                    md=12,
                    lg=12,
                    xl=12,
                ),
                className="m-5 justify-content-center align-items-center",
            ),
        ],
        className="m-5",
    )

    country_page = html.Div(
        children=[
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                        id="country-dropdown",
                        options=[
                            {"label": country_name, "value": country_name}
                            for country_name in country_list
                        ],
                        value="India",
                        style={"color": "black"},
                    ),
                ),
                className="m-5",
            ),
            dbc.Row(
                children=[
                    dbc.Col(
                        dbc.Button(
                            "Confirmed Cases",
                            size="lg",
                            id="confirmed-country",
                            color="primary",
                            block=True,
                            outline=True,
                        ),
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Recoveries",
                            size="lg",
                            id="recoveries-country",
                            color="success",
                            block=True,
                            outline=True,
                        ),
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Deaths",
                            size="lg",
                            id="deaths-country",
                            color="danger",
                            block=True,
                            outline=True,
                        ),
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="mb-4",
                    ),
                ]
            ),
            dbc.Row(html.H3(id="country-message"), className="mt-5 justify-content-center"),
            dbc.Row(
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(id="metric-output-country"), id="map-loading-country"
                    ),
                    width=12,
                ),
                className="mt-5 justify-content-center",
            ),
            dbc.Row(html.H3("Statistics"), className="mt-5 justify-content-center"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(id="stats-graph", className="justify-content-center"),
                        sm=12,
                        md=12,
                        lg=12,
                        xl=12,
                        className="justify-content-center align-items-center",
                    ),
                ],
                className="mt-5 justify-content-center",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Loading(
                                id="stats-table", className="justify-content-center"
                            ),
                        ],
                        id="stats-table-container",
                        sm=12,
                        md=12,
                        lg=12,
                        xl=12,
                        className="justify-content-center align-items-center",
                    ),
                ],
                className="mt-5 justify-content-center",
            ),
            dbc.Row(html.H3("Time Series"), className="mt-5 justify-content-center"),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            dcc.Graph(id="timeseries-output-country"),
                            id="ts-loading-country",
                        ),
                        sm=12,
                        md=12,
                        lg=8,
                        xl=8,
                    ),
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.Row(html.H4("Today"), className="ml-3 mt-2"),
                                    dbc.Row(
                                        html.H5(id="today-country"), className="ml-3 mb-2"
                                    ),
                                ],
                                style={
                                    "borderRadius": "30px",
                                    "backgroundColor": "#8634eb",
                                },
                                className="mt-3 p-3",
                            ),
                            html.Div(
                                [
                                    dbc.Row(html.H4("Last Week"), className="ml-3 mt-2"),
                                    dbc.Row(
                                        [
                                            html.H5(id="lastweek-country"),
                                            html.H5(
                                                id="lastweek-country-diff",
                                                style={"color": "red"},
                                                className="ml-3",
                                            ),
                                        ],
                                        className="ml-3 mb-2",
                                    ),
                                ],
                                style={
                                    "borderRadius": "30px",
                                    "backgroundColor": "#8634eb",
                                },
                                className="mt-3 p-3",
                            ),
                            html.Div(
                                [
                                    dbc.Row(html.H4("Last Month"), className="ml-3 mt-2"),
                                    dbc.Row(
                                        [
                                            html.H5(id="lastmonth-country"),
                                            html.H5(
                                                id="lastmonth-country-diff",
                                                style={"color": "red"},
                                                className="ml-3",
                                            ),
                                        ],
                                        className="ml-3 mb-2",
                                    ),
                                ],
                                style={
                                    "borderRadius": "30px",
                                    "backgroundColor": "#8634eb",
                                },
                                className="mt-3 p-3",
                            ),
                        ],
                        className="align-items-center",
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                    ),
                ],
                className="mt-5 align-items-center",
            ),
        ],
        className="m-5",
    )

    forecast_page = html.Div(
        [
            dbc.Row(
                dbc.Col(
                    dcc.Dropdown(
                        id="country-dropdown-prediction",
                        options=[
                            {"label": country_name, "value": country_name}
                            for country_name in country_list
                        ],
                        value="India",
                        style={"color": "black"},
                    ),
                ),
                className="m-5",
            ),
            dbc.Row(
                [
                    html.H3("Predictions for the Following Week"),
                ],
                className="mt-5 justify-content-center",
            ),
            dbc.Row(
                [
                    html.H5(
                        "It can take upto 2 minutes for our bots to generate the predictions.",
                    ),
                ],
                className="mt-5 justify-content-center",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "Forecast confirmed cases",
                            size="lg",
                            id="forecast-confirmed",
                            color="primary",
                            block=True,
                        ),
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Forecast recoveries",
                            size="lg",
                            id="forecast-recoveries",
                            color="success",
                            block=True,
                        ),
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="mb-4",
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Forecast Deaths",
                            size="lg",
                            id="forecast-deaths",
                            color="danger",
                            block=True,
                        ),
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="mb-4",
                    ),
                ],
                className="mt-5 justify-content-center",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Loading(id="predictions-table"),
                        ],
                        id="predictions-table-container",
                        sm=12,
                        md=12,
                        lg=4,
                        xl=4,
                        className="align-items-center",
                    ),
                    dbc.Col(
                        dcc.Loading(
                            id="predictions-graph",
                        ),
                        id="predictions-graph-container",
                        sm=12,
                        md=12,
                        lg=8,
                        xl=8,
                    ),
                ],
                className="mt-5 justify-content-center",
            ),
        ],
        className="m-5",
    )

    preventive_page = dbc.Container(
        children=[
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Wash Your Hands",
                                        className="card-title",
                                        style={
                                            "text-align": "center",
                                            "font-weight": "bold",
                                        },
                                    ),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Img(
                                                        src="https://api.pcloud.com/getpubthumb?code=XZuvpQXZsR3nbzh8S9j61OE1DfDCHbAVIOdk&linkpassword=undefined&size=413x460&crop=0&type=auto",
                                                        height="100%",
                                                        width="100%",
                                                        className="img-fluid",
                                                        style={
                                                            "padding-bottom": "10%",
                                                            "border-radius": "5rem",
                                                        },
                                                    ),
                                                    sm=8,
                                                    lg=6,
                                                    md=8,
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                    },
                                                ),
                                                dbc.Col(
                                                    html.P(
                                                        """Wash your hands often with soap and water for at least 20 seconds especially after you have been in a public place, or after blowing your nose, coughing, or sneezing.
        Cover all surfaces of your hands and rub them together until they feel dry.
        Avoid touching your eyes, nose, and mouth with unwashed hands.""",
                                                        style={
                                                            "text-align": "left",
                                                            "font-size": "large",
                                                        },
                                                    ),
                                                    sm=12,
                                                    md=12,
                                                    lg=6,
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                    },
                                                ),
                                            ]
                                        ),
                                        className="clearfix",
                                    ),
                                ]
                            ),
                            style={
                                "width": "100%",
                                "display": "flex",
                                "flex": "1 1 auto",
                                "margin-top": "5%",
                                "margin-bottom": "5%",
                                "border-radius": "2rem",
                                "background-color": "#f5f5f5",
                                "color": "black",
                            },
                        ),
                        lg=8,
                        md=8,
                        sm=12,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Clean Surfaces In Contact",
                                        className="card-title",
                                        style={
                                            "text-align": "center",
                                            "font-weight": "bold",
                                        },
                                    ),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Img(
                                                        src="https://api.pcloud.com/getpubthumb?code=XZ7ipQXZ5KUuyw3hghJcuqkGaMUU1VQJqyOk&linkpassword=undefined&size=430x365&crop=0&type=auto",
                                                        height="100%",
                                                        width="100%",
                                                        className="img-fluid",
                                                        style={
                                                            "padding-bottom": "10%",
                                                            "border-radius": "5rem",
                                                        },
                                                    ),
                                                    sm=8,
                                                    lg=6,
                                                    md=8,
                                                ),
                                                dbc.Col(
                                                    html.P(
                                                        """Clean and disinfect frequently touched surfaces daily. This includes tables, doorknobs, light switches, countertops, handles, desks, phones, keyboards, toilets, faucets, and sinks.
        - If surfaces are dirty, clean them. Use detergent or soap and water prior to disinfection.
        - Then, use a household disinfectant. Most common EPA-registered household disinfectants will work. """,
                                                        style={
                                                            "text-align": "left",
                                                            "font-size": "large",
                                                        },
                                                    ),
                                                    sm=12,
                                                    md=12,
                                                    lg=6,
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                    },
                                                ),
                                            ]
                                        ),
                                        className="clearfix",
                                    ),
                                ]
                            ),
                            style={
                                "width": "100%",
                                "display": "flex",
                                "flex": "1 1 auto",
                                "margin-top": "5%",
                                "margin-bottom": "5%",
                                "border-radius": "2rem",
                                "background-color": "#f5f5f5",
                                "color": "black",
                            },
                        ),
                        lg=8,
                        md=8,
                        sm=12,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(
                                        "Always Cover Your Mouth",
                                        className="card-title",
                                        style={
                                            "text-align": "center",
                                            "font-weight": "bold",
                                        },
                                    ),
                                    html.Div(
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Img(
                                                        src="https://api.pcloud.com/getpubthumb?code=XZY9HQXZEKg6hUK7fay5q06RYI65GJ5OXVay&linkpassword=undefined&size=499x499&crop=0&type=auto",
                                                        height="100%",
                                                        width="100%",
                                                        className="img-fluid",
                                                        style={
                                                            "padding-bottom": "10%",
                                                            "border-radius": "5rem",
                                                        },
                                                    ),
                                                    sm=8,
                                                    lg=6,
                                                    md=8,
                                                ),
                                                dbc.Col(
                                                    html.P(
                                                        """You could spread COVID-19 to others even if you do not feel sick.
        The cloth face cover is meant to protect other people in case you are infected.
        Everyone should wear a cloth face cover in public settings and when around people who don’t live in your household, especially when other social distancing measures are difficult to maintain.
        The cloth face cover is not a substitute for social distancing. """,
                                                        style={
                                                            "text-align": "left",
                                                            "font-size": "large",
                                                        },
                                                    ),
                                                    sm=12,
                                                    md=12,
                                                    lg=6,
                                                    style={
                                                        "display": "flex",
                                                        "align-items": "center",
                                                    },
                                                ),
                                            ]
                                        ),
                                        className="clearfix",
                                    ),
                                ]
                            ),
                            style={
                                "width": "100%",
                                "display": "flex",
                                "flex": "1 1 auto",
                                "margin-top": "5%",
                                "margin-bottom": "5%",
                                "border-radius": "2rem",
                                "background-color": "#f5f5f5",
                                "color": "black",
                            },
                        ),
                        lg=8,
                        md=8,
                        sm=12,
                    ),
                ],
                style={"justify-content": "center"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src="https://api.pcloud.com/getpubthumb?code=XZlEpQXZpJuyvwybNSmg8RVr1VPyxYcWDHCX&linkpassword=undefined&size=279x382&crop=0&type=auto",
                            height="60%",
                            width="90%",
                            style={"margin-top": "25%", "width": "125%"},
                        ),
                        align="start",
                        width=3,
                    ),
                    dbc.Col(
                        html.Img(
                            src="https://api.pcloud.com/getpubthumb?code=XZScpQXZAAbOx5c5QeRUQzz7ji6jqFkeEJKk&linkpassword=undefined&size=387x99&crop=0&type=auto",
                            width="100%",
                        ),
                        align="center",
                        width=6,
                    ),
                    dbc.Col(
                        html.Img(
                            src="https://api.pcloud.com/getpubthumb?code=XZfOpQXZdAvDtsdvjX0Rg6RWhabgDk11fMTy&linkpassword=undefined&size=218x433&crop=0&type=auto",
                            height="45%",
                            width="100%",
                            style={"float": "right"},
                        ),
                        align="end",
                        width=3,
                    ),
                ]
            ),
        ],
    )

    app.layout = html.Div(
        [dcc.Location(id="url", refresh=False), navbar, html.Div(id="page-content")]
    )

    # Callbacks for the Global Situation Page

    # Updates the message on top of the page
    @app.callback(
        dash.dependencies.Output("global-message", "children"),
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    )
    def update_message(btn1, btn2, btn3):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        time_updated = datetime.datetime.fromtimestamp(
            today_data["updated"] / 1000
        ).strftime("%H:%M")
        date_updated = datetime.datetime.fromtimestamp(
            today_data["updated"] / 1000
        ).strftime("%d %B %Y")
        output_str = "Globally, as of {time}, {date}, there have been {cases} {res_str}"

        if "confirmed" in changed_id:
            return output_str.format(
                time=time_updated,
                date=date_updated,
                cases=format(today_data["cases"], ",d"),
                res_str="confirmed cases",
            )
        elif "recoveries" in changed_id:
            return output_str.format(
                time=time_updated,
                date=date_updated,
                cases=format(today_data["recovered"], ",d"),
                res_str="recoveries",
            )
        elif "deaths" in changed_id:
            return output_str.format(
                time=time_updated,
                date=date_updated,
                cases=format(today_data["deaths"], ",d"),
                res_str="deaths",
            )
        else:
            return output_str.format(
                time=time_updated,
                date=date_updated,
                cases=format(today_data["cases"], ",d"),
                res_str="confirmed cases",
            )


    # Updates the huge world map, the animation, and the time series on the page
    @app.callback(
        dash.dependencies.Output("metric-output", "figure"),
        dash.dependencies.Output("animation-output", "figure"),
        dash.dependencies.Output("timeseries-output", "figure"),
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    )
    @cache.memoize(timeout=TIMEOUT)
    def update_graphs(btn1, btn2, btn3):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

        if "confirmed" in changed_id:
            return (
                maps.plot_study(country_cases_sorted, columns, confirmed),
                animations.animated_barchart(df=confirmed_global, name="confirmed"),
                timeseries.plot_world_timeseries(
                    confirmed_global, "confirmed", n=-20, daily=True
                ),
            )
        elif "recoveries" in changed_id:
            return (
                maps.plot_study(country_cases_sorted, columns, recovered),
                animations.animated_barchart(df=recovered_global, name="recovered"),
                timeseries.plot_world_timeseries(
                    recovered_global, "recovered", n=-20, daily=True
                ),
            )
        elif "deaths" in changed_id:
            return (
                maps.plot_study(country_cases_sorted, columns, deaths),
                animations.animated_barchart(df=deaths_global, name="deaths"),
                timeseries.plot_world_timeseries(
                    deaths_global, "deaths", n=-20, daily=True
                ),
            )
        else:
            return (
                maps.plot_study(country_cases_sorted, columns, confirmed),
                animations.animated_barchart(df=confirmed_global, name="confirmed"),
                timeseries.plot_world_timeseries(
                    confirmed_global, "confirmed", n=-20, daily=True
                ),
            )


    # Updates the text and stats on the page
    @app.callback(
        dash.dependencies.Output("today", "children"),
        dash.dependencies.Output("lastweek", "children"),
        dash.dependencies.Output("lastweek-diff", "children"),
        dash.dependencies.Output("lastmonth", "children"),
        dash.dependencies.Output("lastmonth-diff", "children"),
        dash.dependencies.Input("confirmed", "n_clicks"),
        dash.dependencies.Input("recoveries", "n_clicks"),
        dash.dependencies.Input("deaths", "n_clicks"),
    )
    @cache.memoize(timeout=TIMEOUT)
    def update_cases(btn1, btn2, btn3):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

        lastweek = today - timedelta(weeks=1)
        lastmonth = today - timedelta(days=30)

        if "confirmed" in changed_id:
            lastweek_cases = world_timeseries_confirmed.at[
                lastweek.strftime("%-m/%-d/%y"), "Cases"
            ]
            lastmonth_cases = world_timeseries_confirmed.at[
                lastmonth.strftime("%-m/%-d/%y"), "Cases"
            ]
            return (
                confirmed_global_cases_today,
                format(lastweek_cases, ",d"),
                "+" + format(today_data["cases"] - lastweek_cases, ",d"),
                format(lastmonth_cases, ",d"),
                "+" + format(today_data["cases"] - lastmonth_cases, ",d"),
            )
        elif "recoveries" in changed_id:
            lastweek_cases = world_timeseries_recovered.at[
                lastweek.strftime("%-m/%-d/%y"), "Cases"
            ]
            lastmonth_cases = world_timeseries_recovered.at[
                lastmonth.strftime("%-m/%-d/%y"), "Cases"
            ]
            return (
                confirmed_recovered_cases_today,
                format(lastweek_cases, ",d"),
                "+" + format(today_data["recovered"] - lastweek_cases, ",d"),
                format(lastmonth_cases, ",d"),
                "+" + format(today_data["recovered"] - lastmonth_cases, ",d"),
            )
        elif "deaths" in changed_id:
            lastweek_cases = world_timeseries_deaths.at[
                lastweek.strftime("%-m/%-d/%y"), "Cases"
            ]
            lastmonth_cases = world_timeseries_deaths.at[
                lastmonth.strftime("%-m/%-d/%y"), "Cases"
            ]
            return (
                confirmed_deaths_cases_today,
                format(lastweek_cases, ",d"),
                "+" + format(today_data["deaths"] - lastweek_cases, ",d"),
                format(lastmonth_cases, ",d"),
                "+" + format(today_data["deaths"] - lastmonth_cases, ",d"),
            )
        else:
            lastweek_cases = world_timeseries_confirmed.at[
                lastweek.strftime("%-m/%-d/%y"), "Cases"
            ]
            lastmonth_cases = world_timeseries_confirmed.at[
                lastmonth.strftime("%-m/%-d/%y"), "Cases"
            ]
            return (
                confirmed_global_cases_today,
                format(lastweek_cases, ",d"),
                "+" + format(today_data["cases"] - lastweek_cases, ",d"),
                format(lastmonth_cases, ",d"),
                "+" + format(today_data["cases"] - lastmonth_cases, ",d"),
            )


    # Callbacks for the Country Analysis Page

    # Updates the message on top of the page for the country selected in the dropdown
    @app.callback(
        dash.dependencies.Output("country-message", "children"),
        dash.dependencies.Input("country-dropdown", "value"),
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    )
    def update_country_message(value, btn1, btn2, btn3):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        country_stats = get_final_object(value, today_country_data)
        date_obj = datetime.datetime.strptime(
            country_stats["updatedAt"][0], "%Y-%m-%d %H:%M:%S"
        )
        time_updated = date_obj.strftime("%H:%M")
        date_updated = date_obj.strftime("%d %B %Y")
        output_str = (
            "In {country_name}, as of {time}, {date}, there have been {cases} {res_str}"
        )

        if "confirmed-country" in changed_id:
            return output_str.format(
                country_name=value,
                time=time_updated,
                date=date_updated,
                cases=format(country_stats["confirmed"], ",d"),
                res_str="confirmed cases",
            )
        elif "recoveries-country" in changed_id:
            return output_str.format(
                country_name=value,
                time=time_updated,
                date=date_updated,
                cases=format(country_stats["recovered"], ",d"),
                res_str="recoveries",
            )
        elif "deaths-country" in changed_id:
            return output_str.format(
                country_name=value,
                time=time_updated,
                date=date_updated,
                cases=format(country_stats["deaths"], ",d"),
                res_str="deaths",
            )
        else:
            return output_str.format(
                country_name=value,
                time=time_updated,
                date=date_updated,
                cases=format(country_stats["confirmed"], ",d"),
                res_str="confirmed cases",
            )


    # Updates the graphs shown on the page for the country chosen in the dropdown
    @app.callback(
        dash.dependencies.Output("metric-output-country", "figure"),
        dash.dependencies.Output("timeseries-output-country", "figure"),
        dash.dependencies.Input("country-dropdown", "value"),
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    )
    def update_graphs_country(value, btn1, btn2, btn3):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

        if "confirmed-country" in changed_id:
            try:
                return (
                    maps.plot_country(value, today_country_data, "Confirmed"),
                    timeseries.plot_timeseries(
                        value,
                        timeseries.get_new_cases,
                        "Confirmed Cases",
                        n=-20,
                        daily=True,
                    ),
                )
            except:
                return (
                    maps.plot_study(country_cases_sorted, columns, confirmed, value),
                    timeseries.plot_timeseries(
                        value,
                        timeseries.get_new_cases,
                        "Confirmed Cases",
                        n=-20,
                        daily=True,
                    ),
                )
        elif "recoveries-country" in changed_id:
            try:
                return (
                    maps.plot_country(value, today_country_data, "Recoveries"),
                    timeseries.plot_timeseries(
                        value,
                        timeseries.get_new_recoveries,
                        "Recoveries",
                        n=-20,
                        daily=True,
                    ),
                )
            except:
                return (
                    maps.plot_study(country_cases_sorted, columns, recovered, value),
                    timeseries.plot_timeseries(
                        value,
                        timeseries.get_new_recoveries,
                        "Recoveries",
                        n=-20,
                        daily=True,
                    ),
                )
        elif "deaths-country" in changed_id:
            try:
                return (
                    maps.plot_country(value, today_country_data, "deaths"),
                    timeseries.plot_timeseries(
                        value,
                        timeseries.get_new_deaths,
                        "Deaths",
                        n=-20,
                        daily=True,
                    ),
                )
            except:
                return (
                    maps.plot_country(value, today_country_data, "deaths"),
                    timeseries.plot_timeseries(
                        value,
                        timeseries.get_new_deaths,
                        "Deaths",
                        n=-20,
                        daily=True,
                    ),
                )
        else:
            try:
                return (
                    maps.plot_country(value, today_country_data, "Confirmed"),
                    timeseries.plot_timeseries(
                        value,
                        timeseries.get_new_cases,
                        "Confirmed Cases",
                        n=-20,
                        daily=True,
                    ),
                )
            except:
                return (
                    maps.plot_study(country_cases_sorted, columns, confirmed, value),
                    timeseries.plot_timeseries(
                        value,
                        timeseries.get_new_cases,
                        "Confirmed Cases",
                        n=-20,
                        daily=False,
                    ),
                )


    # Update the stats shown on the page
    @app.callback(
        dash.dependencies.Output("today-country", "children"),
        dash.dependencies.Output("lastweek-country", "children"),
        dash.dependencies.Output("lastweek-country-diff", "children"),
        dash.dependencies.Output("lastmonth-country", "children"),
        dash.dependencies.Output("lastmonth-country-diff", "children"),
        dash.dependencies.Input("country-dropdown", "value"),
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    )
    def update_cases_country(value, btn1, btn2, btn3):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]

        country_stats = get_final_object(value, today_country_data)
        cases = format(country_stats["confirmed"], ",d")
        recovered = format(country_stats["recovered"], ",d")
        deaths = format(country_stats["deaths"], ",d")

        country_time_series = animations.line_comparison_data(value)
        country_time_series.index = country_time_series["dates"]

        lastweek = today - timedelta(weeks=1)
        lastmonth = today - timedelta(days=30)

        if "confirmed-country" in changed_id:
            lastweek_cases = country_time_series.at[
                lastweek.strftime("%-m/%-d/%y"), "confirmed"
            ]
            lastmonth_cases = country_time_series.at[
                lastmonth.strftime("%-m/%-d/%y"), "confirmed"
            ]
            return (
                cases,
                format(lastweek_cases, ",d"),
                "+" + format(country_stats["confirmed"] - lastweek_cases, ",d"),
                format(lastmonth_cases, ",d"),
                "+" + format(country_stats["confirmed"] - lastmonth_cases, ",d"),
            )
        elif "recoveries-country" in changed_id:
            lastweek_cases = country_time_series.at[
                lastweek.strftime("%-m/%-d/%y"), "recovered"
            ]
            lastmonth_cases = country_time_series.at[
                lastmonth.strftime("%-m/%-d/%y"), "recovered"
            ]
            return (
                recovered,
                format(lastweek_cases, ",d"),
                "+" + format(country_stats["recovered"] - lastweek_cases, ",d"),
                format(lastmonth_cases, ",d"),
                "+" + format(country_stats["recovered"] - lastmonth_cases, ",d"),
            )
        elif "deaths-country" in changed_id:
            lastweek_cases = country_time_series.at[
                lastweek.strftime("%-m/%-d/%y"), "deaths"
            ]
            lastmonth_cases = country_time_series.at[
                lastmonth.strftime("%-m/%-d/%y"), "deaths"
            ]
            return (
                deaths,
                format(lastweek_cases, ",d"),
                "+" + format(country_stats["deaths"] - lastweek_cases, ",d"),
                format(lastmonth_cases, ",d"),
                "+" + format(country_stats["deaths"] - lastmonth_cases, ",d"),
            )
        else:
            lastweek_cases = country_time_series.at[
                lastweek.strftime("%-m/%-d/%y"), "confirmed"
            ]
            lastmonth_cases = country_time_series.at[
                lastmonth.strftime("%-m/%-d/%y"), "confirmed"
            ]
            return (
                cases,
                format(lastweek_cases, ",d"),
                "+" + format(country_stats["confirmed"] - lastweek_cases, ",d"),
                format(lastmonth_cases, ",d"),
                "+" + format(country_stats["confirmed"] - lastmonth_cases, ",d"),
            )


    @app.callback(
        dash.dependencies.Output("stats-graph", "children"),
        dash.dependencies.Output("stats-table", "children"),
        dash.dependencies.Input("country-dropdown", "value"),
        dash.dependencies.Input("confirmed-country", "n_clicks"),
        dash.dependencies.Input("recoveries-country", "n_clicks"),
        dash.dependencies.Input("deaths-country", "n_clicks"),
    )
    def update_stats(value, btn1, btn2, btn3):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        country_stats = maps.get_country_frame(
            maps.choose_country(today_country_data, value)
        )

        try:
            if "confirmed-country" in changed_id:
                return (
                    dcc.Graph(
                        figure=cv.plot_province(
                            country_stats, "Confirmed", "Confirmed Cases"
                        )
                    ),
                    dbc.Table.from_dataframe(
                        cv.table_province_data(country_stats, "Confirmed"),
                        striped=True,
                        bordered=True,
                        hover=True,
                    ),
                )
            elif "recoveries-country" in changed_id:
                return (
                    dcc.Graph(
                        figure=cv.plot_province(country_stats, "Recoveries", "Recoveries")
                    ),
                    dbc.Table.from_dataframe(
                        cv.table_province_data(country_stats, "Recoveries"),
                        striped=True,
                        bordered=True,
                        hover=True,
                    ),
                )
            elif "deaths-country" in changed_id:
                return (
                    dcc.Graph(figure=cv.plot_province(country_stats, "Deaths", "Deaths")),
                    dbc.Table.from_dataframe(
                        cv.table_province_data(country_stats, "Deaths"),
                        striped=True,
                        bordered=True,
                        hover=True,
                    ),
                )
            else:
                return (
                    dcc.Graph(
                        figure=cv.plot_province(
                            country_stats, "Confirmed", "Confirmed Cases"
                        )
                    ),
                    dbc.Table.from_dataframe(
                        cv.table_province_data(country_stats, "Confirmed"),
                        striped=True,
                        bordered=True,
                        hover=True,
                    ),
                )
        except:
            return (
                html.H5(
                    "Sorry! Unfortunately we do not have sufficient data at the moment."
                ),
                None,
            )


    # Callbacks for the Forecasts Page


    @app.callback(
        dash.dependencies.Output("predictions-graph", "children"),
        dash.dependencies.Output("predictions-table", "children"),
        dash.dependencies.Input("forecast-confirmed", "n_clicks"),
        dash.dependencies.Input("forecast-recoveries", "n_clicks"),
        dash.dependencies.Input("forecast-deaths", "n_clicks"),
        dash.dependencies.State("country-dropdown-prediction", "value"),
        prevent_initial_call=True,
    )
    def forecast_cases(btn1, btn2, btn3, value):
        changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
        if "forecast-confirmed" in changed_id:
            try:
                response = requests.get(
                    f"https://github.com/anandrajaram21/covidash/raw/web_app/output/{value}-confirmed.pkl"
                )
                with open("temp.pkl", "wb") as fh:
                    fh.write(response.content)
                with open("temp.pkl", "rb") as fh:
                    data = pickle.load(fh)
                    return (
                        dcc.Graph(figure=data["fig"]),
                        dbc.Table.from_dataframe(
                            data["predictions"], striped=True, bordered=True, hover=True
                        ),
                    )
                os.remove("temp.pkl")
            except:
                preds, _, fig = cnn.cnn_predict("confirmed", value)
                return (
                    dcc.Graph(figure=fig),
                    dbc.Table.from_dataframe(
                        preds, striped=True, bordered=True, hover=True
                    ),
                )
        elif "forecast-recoveries" in changed_id:
            try:
                response = requests.get(
                    f"https://github.com/anandrajaram21/covidash/raw/web_app/output/{value}-recovered.pkl"
                )
                with open("temp.pkl", "wb") as fh:
                    fh.write(response.content)
                with open("temp.pkl", "rb") as fh:
                    data = pickle.load(fh)
                    return (
                        dcc.Graph(figure=data["fig"]),
                        dbc.Table.from_dataframe(
                            data["predictions"], striped=True, bordered=True, hover=True
                        ),
                    )
                os.remove("temp.pkl")
            except:
                preds, _, fig = cnn.cnn_predict("recovered", value)
                return (
                    dcc.Graph(figure=fig),
                    dbc.Table.from_dataframe(
                        preds, striped=True, bordered=True, hover=True
                    ),
                )
        elif "forecast-deaths" in changed_id:
            try:
                response = requests.get(
                    f"https://github.com/anandrajaram21/covidash/raw/web_app/output/{value}-deaths.pkl"
                )
                with open("temp.pkl", "wb") as fh:
                    fh.write(response.content)
                with open("temp.pkl", "rb") as fh:
                    data = pickle.load(fh)
                    return (
                        dcc.Graph(figure=data["fig"]),
                        dbc.Table.from_dataframe(
                            data["predictions"], striped=True, bordered=True, hover=True
                        ),
                    )
                os.remove("temp.pkl")
            except:
                preds, _, fig = cnn.cnn_predict("deaths", value)
                return (
                    dcc.Graph(figure=fig),
                    dbc.Table.from_dataframe(
                        preds, striped=True, bordered=True, hover=True
                    ),
                )


    @app.callback(
        dash.dependencies.Output("page-content", "children"),
        [dash.dependencies.Input("url", "pathname")],
    )
    def display_page(pathname):
        if pathname == "/":
            return home_page
        elif pathname == "/global":
            return global_page
        elif pathname == "/country":
            return country_page
        elif pathname == "/prevent":
            return preventive_page
        elif pathname == "/forecast":
            return forecast_page


    if __name__ == "__main__":
        app.run_server()
```

## Scope for Improvement

The model can be improved for better results by utilizing more information to get a better overview of the situation.
