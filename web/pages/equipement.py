import dash
from dash import dcc, html
import plotly.graph_objects as go
import json
import os
dash.register_page(__name__, path="/equipement")

# Les données JSON
data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'equipement_price.json')
with open(data_path) as file:
    data = json.load(file)

# lets sort the data by the difference between price_with and price_without
data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1]["price_without"] - item[1]["price_with"])}

# Extraire les données
features = list(data.keys())
price_with = [item["price_with"] for item in data.values()]
price_without = [item["price_without"] for item in data.values()]


layout = html.Div([
    html.H1("Mean Price Per fonctionality"),
    dcc.Graph(
        id="bar-chart",
        figure={
            "data": [
                go.Bar(name="With fonctionality", x=features, y=price_with, marker_color="green"),
                go.Bar(name="Without fonctionality", x=features, y=price_without, marker_color="red"),
            ],
            "layout": go.Layout(
                # title="Comparaison des prix moyens avec et sans fonctionnalités, triées par différence de prix",
                title="Prices comparison with and without features, sorted by price difference",
                barmode="group",
                xaxis={"title": "Fonctionalities"},
                yaxis={"title": "Mean Price"},
                template="plotly_white"
            )
        }
    )
])

