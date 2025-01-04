import dash
from dash import html, dcc
from .utils.create_boundaries_map import create_boundaries_map

dash.register_page(__name__, path="/map2")

fig = create_boundaries_map()

# Define the layout of the app
layout = html.Div([
    html.H1("Map of Paris with Neighborhoods"),
    dcc.Graph(id='map', figure=fig, style={'height': '700px'})  # Adjust the height here
])