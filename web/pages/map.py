import dash
from dash import html, dcc

import geopandas as gpd
import os
import plotly.express as px

dash.register_page(__name__, path="/map")


# Load shapefile data for Paris neighborhoods from the /data folder
shapefile_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'arrondissements.shp')
gdf = gpd.read_file("D:/CPE/analise-airbnb-rentabilite/data/arrondissements.shp")


# Create a Plotly Express map
fig = px.choropleth_mapbox(gdf, geojson=gdf.geometry, locations=gdf.index, color=gdf.index,
                           mapbox_style="carto-positron", center={"lat": 48.8566, "lon": 2.3522}, zoom=11,
                           opacity=0.5,hover_name='l_ar')

# Define the layout of the app
layout = html.Div([
    html.H1("Map of Paris with Neighborhoods"),
    dcc.Graph(id='map', figure=fig, style={'height': '700px'})  # Adjust the)
])

