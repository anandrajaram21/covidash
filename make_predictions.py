from src import cnn
import pickle

countries = ["India", "US", "Brazil", "Canada", "United Kingdom"]


def store_predictions_and_graphs(country_name):
    dfs = ["confirmed","deaths","recovered"]
    with open(f"{country_name}.pkl","wb") as fh:
        for df in dfs:
            fig, _, predictions =  cnn.cnn_predict(df, country_name)
            d = {"predictions":predictions,"graph":fig}
            pickle.dump(d,fh)
            # so order of reading will be 3 dictionaries -> confirmed , deaths and recovered
            # dictionary will be of the format {"predictions":predictions,"graph":fig}
    return None

for country in countries:
    # takes about 20-30 min ig (without gpu)
    store_predictions_and_graphs(country)