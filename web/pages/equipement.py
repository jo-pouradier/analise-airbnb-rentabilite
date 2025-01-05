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

# Extraire les données
features = list(data.keys())
price_with = [item["price_with"] for item in data.values()]
price_without = [item["price_without"] for item in data.values()]


layout = html.Div([
    html.H1("Prix moyens par fonctionnalité"),
    dcc.Graph(
        id="bar-chart",
        figure={
            "data": [
                go.Bar(name="Avec fonctionnalité", x=features, y=price_with, marker_color="green"),
                go.Bar(name="Sans fonctionnalité", x=features, y=price_without, marker_color="red"),
            ],
            "layout": go.Layout(
                title="Comparaison des prix moyens avec et sans fonctionnalités",
                barmode="group",
                xaxis={"title": "Fonctionnalités"},
                yaxis={"title": "Prix moyen"},
                template="plotly_white"
            )
        }
    )
])

