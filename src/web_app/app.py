import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pyarrow as pa
import redis
import animations
import map
import arima

external_stylesheets = [dbc.themes.BOOTSTRAP]

# Starting a Redis connection to cache data
r = redis.Redis()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def collect_data():
    context = pa.default_serialization_context()

    if r.exists("confirmed_global") and r.exists("recovered_global") and r.exists("deaths_global"):
        return (context.deserialize(r.get("confirmed_global")), context.deserialize(r.get("deaths_global")), context.deserialize(r.get("recovered_global")), context.deserialize(r.get("country_cases")))

    else:
        filenames = ['time_series_covid19_confirmed_global.csv',
                     'time_series_covid19_deaths_global.csv',
                     'time_series_covid19_recovered_global.csv']

        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'

        confirmed_global = pd.read_csv(url + filenames[0])
        deaths_global = pd.read_csv(url + filenames[1])
        recovered_global = pd.read_csv(url + filenames[2])
        country_cases = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')

        confirmed_global.drop(columns = ['Province/State', 'Lat', 'Long'], inplace = True)
        deaths_global.drop(columns = ['Province/State', 'Lat', 'Long'], inplace = True)
        recovered_global.drop(columns = ['Province/State', 'Lat', 'Long'], inplace = True)
        country_cases.drop(columns = ['Last_Update', 'Incident_Rate', 'People_Tested', 'People_Hospitalized', 'UID'], inplace = True)

        confirmed_global.rename(columns = {"Country/Region": "country"}, inplace = True)
        deaths_global.rename(columns = {"Country/Region": "country"}, inplace = True)
        recovered_global.rename(columns = {"Country/Region": "country"}, inplace = True)

        country_cases.rename(columns = {
            "Country_Region" : "country",
            "Confirmed": "confirmed",
            "Deaths": "deaths",
            "Recovered" : "recovered",
            "Active" : "active",
            "Mortality_Rate": "mortality"
        }, inplace = True)

        confirmed_global = confirmed_global.groupby(['country'], as_index = False).sum()
        deaths_global = deaths_global.groupby(['country'], as_index = False).sum()
        recovered_global = recovered_global.groupby(['country'], as_index = False).sum()

        confirmed_global.at[178, '5/20/20'] = 251667

        r.set("confirmed_global", context.serialize(confirmed_global).to_buffer().to_pybytes())
        r.expire("confirmed_global", 43200)
        r.set("deaths_global", context.serialize(deaths_global).to_buffer().to_pybytes())
        r.expire("deaths_global", 43200)
        r.set("recovered_global", context.serialize(recovered_global).to_buffer().to_pybytes())
        r.expire("recovered_global", 43200)
        r.set("country_cases", context.serialize(country_cases).to_buffer().to_pybytes())
        r.expire("country_cases", 43200)

        return (confirmed_global, deaths_global, recovered_global, country_cases)

app.layout = dbc.Container(
    dbc.Alert("Hello Bootstrap!", color="success"),
    className="p-5",
)

confirmed_global, deaths_global, recovered_global, country_cases = collect_data()

if __name__ == "__main__":
    app.run_server()
