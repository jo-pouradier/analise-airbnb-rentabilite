import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import html, dcc
import os
from dash.dependencies import Output, Input
import geopandas as gpd
from shapely import Point

dash.register_page(__name__, path="/map_arrondissements",suppress_callback_exceptions=True)


# Load your first dataset with coordinates and prices
data_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'pondered_listings_process.csv')
# data1 = pd.read_csv('./../../data/pondered_listings_process.csv')
data1 = pd.read_csv(data_path)

# Load your second dataset with coordinates and prices
data_path2 = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'loyer_process.csv')
data2 = pd.read_csv(data_path2)

# Convert the coordinates to GeoDataFrames
geometry1 = [Point(xy) for xy in zip(data1.longitude, data1.latitude)]
geo_data1 = gpd.GeoDataFrame(data1, geometry=geometry1)

geometry2 = [Point(float(xy.split(',')[1]), float(xy.split(',')[0])) for xy in data2['geo_point_2d']]
geo_data2 = gpd.GeoDataFrame(data2, geometry=geometry2)


# Load shapefile data for Paris neighborhoods from the /data folder
shapefile_path = os.path.join(os.path.dirname(__file__), '..','..', 'data','arrondissements', 'arrondissements.shp')
gdf = gpd.read_file(shapefile_path)

# Perform the spatial join to get the arrondissement for each point
geo_data1 = gpd.sjoin(geo_data1, gdf, how='left')
geo_data2 = gpd.sjoin(geo_data2, gdf, how='left')

# Calculate the average weighted price per neighborhood for listings

avg_price1 = geo_data1.groupby('index_right')['price_per_m2'].mean().reset_index()
avg_price1.columns = ['index_right', 'price_per_m2']
avg_price1_basics = geo_data1.groupby('index_right')['price_per_m2_pondered'].mean().reset_index()
avg_price1_basics.columns = ['index_right', 'price_per_m2_pondered']
# Calculate the average availability per neighborhood for listings
avg_availability = geo_data1.groupby('index_right')['percentage_unavailable'].mean().reset_index()
avg_availability.columns = ['index_right', 'avg_availability']

# Calculate the average price per neighborhood for loyer
avg_price2 = geo_data2.groupby('index_right')['price_per_m2'].mean().reset_index()
avg_price2.columns = ['index_right', 'price_per_m2']


# Merge the average prices and availability with the GeoDataFrame for listings
gdf_listings = gdf.merge(avg_price1, left_index=True, right_on='index_right', how='left')
gdf_listings = gdf_listings.merge(avg_availability, left_index=True, right_on='index_right', how='left', suffixes=('', '_availability'))
gdf_listings = gdf_listings.merge(avg_price1_basics, left_index=True, right_on='index_right', how='left', suffixes=('', '_price1_basics'))

gdf_loyer = gdf.merge(avg_price2, left_index=True, right_on='index_right', how='left')

# Create the first map
fig1 = px.choropleth_mapbox(gdf_listings, geojson=gdf.geometry, locations=gdf.index, color='price_per_m2',
                            mapbox_style="carto-positron", center={"lat": 48.8566, "lon": 2.3522}, zoom=11,
                            opacity=0.5, hover_name='l_ar', labels={'price_per_m2': 'Avg Price Listings', 'avg_availability': 'Avg Availability', 'price_per_m2_pondered': 'Weighted Price'},
                            hover_data={'avg_availability': ':.2f', 'price_per_m2': ':.2f', 'index_right': False, 'price_per_m2_pondered': ':.2f'})

# Create the second map
fig2 = px.choropleth_mapbox(gdf_loyer, geojson=gdf.geometry, locations=gdf.index, color='price_per_m2',
                            mapbox_style="carto-positron", center={"lat": 48.8566, "lon": 2.3522}, zoom=11,
                            opacity=0.5, hover_name='l_ar', labels={'price_per_m2': 'Avg Price Loyer'})

# Define the layout of the app
layout = html.Div([
    html.H1("Comparison of Average Prices in Paris Neighborhoods", style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            html.H2("Average Price Listings", style={'textAlign': 'center'}),
            dcc.Graph(id='map_listings', figure=fig1, style={'height': '500px'}),
            html.Div(id='details_listings', style={'textAlign': 'center', 'marginTop': '20px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20px'}),
        html.Div([
            html.H2("Average Price Loyer", style={'textAlign': 'center'}),
            dcc.Graph(id='map_loyer', figure=fig2, style={'height': '500px'}),
            html.Div(id='details_loyer', style={'textAlign': 'center', 'marginTop': '20px'})
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20px'})
    ], style={'display': 'flex', 'justifyContent': 'space-between'})
])

# Callback to update details when a neighborhood is clicked
@dash.callback(
    [Output('details_listings', 'children'), Output('details_loyer', 'children')],
    [Input('map_listings', 'clickData'), Input('map_loyer', 'clickData')]
)
def display_details(clickData_listings, clickData_loyer):
    details_listings = []
    details_loyer = []
    if clickData_listings:
        point = clickData_listings['points'][0]
        neighborhood = point['hovertext']
        weighted_price = point['customdata'][3]
        avg_price = point['z']
        avg_availability = point['customdata'][0]
        details_listings.append(html.Div([
            html.H3(f"Details for {neighborhood} (Airbnb)"),
            html.P(f"Occupancy rate: {avg_availability*100:.2f}%"),
            html.P(f"Average Price per m²: {avg_price:.2f}"),
            html.P(f"Average Price per m² based on Occupancy: {weighted_price:.2f}")
        ]))

    if clickData_loyer:
        point = clickData_loyer['points'][0]
        neighborhood = point['hovertext']
        avg_price = point['z']
        details_loyer.append(html.Div([
            html.H3(f"Details for {neighborhood} (Loyer)"),
            html.P(f"Average Price per m²: {avg_price:.2f}")
        ]))

    return details_listings, details_loyer

