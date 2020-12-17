def get_predictions_and_graphs(country_name):
    # Generate the predictions and graphs here for each country and all the metrics (confirmed, recovered, deaths)
    # Return the data in this format
    # ((predictions_confirmed, graph_confirmed), (predictions_recovered, graph_recovered), (predictions_deaths, graph_deaths))

countries = ["India", "US", "Brazil", "Canada", "United Kingdom"]
for i in countries:
    ((predictions_confirmed, graph_confirmed), (predictions_recovered, graph_recovered), (predictions_deaths, graph_deaths)) = get_predictions_and_graphs(i)

# I think thats basically it
