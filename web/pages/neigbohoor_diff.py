import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import html, dcc
import os
from dash.dependencies import Output, Input
import geopandas as gpd
from shapely import Point

dash.register_page(__name__, path="/map_arrondissements")


# Load your first dataset with coordinates and prices
data1 = pd.read_csv('D:/CPE/analise-airbnb-rentabilite/data/listings_process.csv')
data1 = data1.replace([np.inf, -np.inf], np.nan).dropna(subset=['price_per_m2', 'longitude', 'latitude'])

# Load your second dataset with coordinates and prices
data2 = pd.read_csv('D:/CPE/analise-airbnb-rentabilite/data/loyer_process.csv')
data2 = data2.replace([np.inf, -np.inf], np.nan).dropna(subset=['price_per_m2', 'geo_point_2d'])

# Convert the coordinates to GeoDataFrames
geometry1 = [Point(xy) for xy in zip(data1.longitude, data1.latitude)]
geo_data1 = gpd.GeoDataFrame(data1, geometry=geometry1)

geometry2 = [Point(float(xy.split(',')[1]), float(xy.split(',')[0])) for xy in data2['geo_point_2d']]
geo_data2 = gpd.GeoDataFrame(data2, geometry=geometry2)


# Load shapefile data for Paris neighborhoods from the /data folder
shapefile_path = os.path.join(os.path.dirname(__file__), '..','..', 'data', 'arrondissements.shp')
gdf = gpd.read_file("D:/CPE/analise-airbnb-rentabilite/data/arrondissements.shp")


# Perform the spatial join to get the arrondissement for each point
geo_data1 = gpd.sjoin(geo_data1, gdf, how='left')
geo_data2 = gpd.sjoin(geo_data2, gdf, how='left')


# Calculate the weighted average price per neighborhood for listings
geo_data1['weighted_price'] = geo_data1['price_per_m2'] * (geo_data1['availability_365'] / 365)
avg_price1 = geo_data1.groupby('index_right')['weighted_price'].mean().reset_index()
avg_price1.columns = ['index_right', 'weighted_price']

# Calculate the average availability per neighborhood for listings
avg_availability = geo_data1.groupby('index_right')['availability_365'].mean().reset_index() / 365 * 100
avg_availability.columns = ['index_right', 'avg_availability']

# Calculate the average price per neighborhood
avg_price2 = geo_data2.groupby('index_right')['price_per_m2'].mean().reset_index()

# Merge the average prices with the GeoDataFrame
gdf = gdf.merge(avg_price1, left_index=True, right_on='index_right', how='left')
gdf = gdf.merge(avg_availability, left_index=True, right_on='index_right', how='left')
gdf = gdf.merge(avg_price2, left_index=True, right_on='index_right', how='left', suffixes=('_listings', '_loyer'))

# Create the first map
fig1 = px.choropleth_mapbox(gdf, geojson=gdf.geometry, locations=gdf.index, color='weighted_price',
                            mapbox_style="carto-positron", center={"lat": 48.8566, "lon": 2.3522}, zoom=11,
                            opacity=0.5, hover_name='l_ar', labels={'weighted_price': 'Avg Price Listings'},
                            hover_data={'avg_availability': ':.2f', 'index_right': False})

# Create the second map
fig2 = px.choropleth_mapbox(gdf, geojson=gdf.geometry, locations=gdf.index, color='price_per_m2',
                            mapbox_style="carto-positron", center={"lat": 48.8566, "lon": 2.3522}, zoom=11,
                            opacity=0.5, hover_name='l_ar', labels={'price_per_m2_loyer': 'Avg Price Loyer'})

# Define the layout of the app
layout = html.Div([
    html.H1("Comparison of Average Prices in Paris Neighborhoods"),
    html.Div([
        html.Div([
            html.H2("Average Price Listings"),
            dcc.Graph(id='map_listings', figure=fig1, style={'height': '500px'})
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([
            html.H2("Average Price Loyer"),
            dcc.Graph(id='map_loyer', figure=fig2, style={'height': '500px'})
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),
    html.Div(id='details', style={'marginTop': '20px','display': 'flex', 'justifyContent': 'space-between'})
])

# Callback to update details when a neighborhood is clicked
@dash.callback(
    Output('details', 'children'),
    [Input('map_listings', 'clickData'), Input('map_loyer', 'clickData')]
)
def display_details(clickData_listings, clickData_loyer):
    details = []
    if clickData_listings:
        point = clickData_listings['points'][0]
        neighborhood = point['hovertext']
        avg_price = point['z']
        print(point.keys())
        avg_availability = point['customdata'][0]
        details.append(html.Div([
            html.H3(f"Details for {neighborhood} (airbnb)"),
            html.P(f"Average Price per m²: {avg_price:.2f}"),
            html.P(f"Average Availability: {avg_availability:.2f}%")

        ], style={'width': '48%'}))

    if clickData_loyer:
        point = clickData_loyer['points'][0]
        neighborhood = point['hovertext']
        avg_price = point['z']
        details.append(html.Div([
            html.H3(f"Details for {neighborhood} (Loyer)"),
            html.P(f"Average Price per m²: {avg_price:.2f}")
        ], style={'width': '48%'}))

    return details
