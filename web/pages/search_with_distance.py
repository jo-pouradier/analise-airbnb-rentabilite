import math
import random

import dash
from dash import html, dcc

import geopandas as gpd
import os
import plotly.express as px
import plotly.figure_factory as ff

import dash_ag_grid as dag
import numpy as np
import pages.utils.location_search as location_search


def apply_post_process(listings_search, loyer_search):
    mixed_dataset = listings_search[['latitude', 'longitude', 'price_per_m2']]
    mixed_dataset['rent_type'] = ['listings'] * listings_search.shape[0]
    loyer_data = loyer_search.copy()
    loyer_data['latitude'] = loyer_data['latitude'] + np.random.normal(0, 0.002, loyer_data.shape[0])
    loyer_data['longitude'] = loyer_data['longitude'] + np.random.normal(0, 0.002, loyer_data.shape[0])
    loyer_data['rent_type'] = ['loyer'] * loyer_data.shape[0]
    mixed_dataset = mixed_dataset._append(
        loyer_data[['latitude', 'longitude', 'price_per_m2', 'rent_type']])
    return mixed_dataset


dash.register_page(__name__, path="/distance_filter")

mixed_dataset = apply_post_process(location_search.listings_data, location_search.loyer_data)
fig_listings = px.scatter_mapbox(mixed_dataset.loc[mixed_dataset['rent_type'] == "listings"], lat="latitude",
                                 lon="longitude", color="price_per_m2",
                                 zoom=11, center={"lat": 48.8566, "lon": 2.3522},
                                 hover_name="price_per_m2", mapbox_style="carto-positron")

fig_loyer = px.scatter_mapbox(mixed_dataset.loc[mixed_dataset['rent_type'] == "loyer"], lat="latitude", lon="longitude",
                              color="price_per_m2",
                              zoom=11, center={"lat": 48.8566, "lon": 2.3522},
                              hover_name="price_per_m2", mapbox_style="carto-positron")

fig_combined = px.scatter_mapbox(mixed_dataset, lat="latitude", lon="longitude", color="rent_type", zoom=11,
                                 center={"lat": 48.8566, "lon": 2.3522},
                                 hover_name="price_per_m2", mapbox_style="carto-positron", size_max=15)
layout = html.Div([
    html.H1("Please enter the latitude, longitude and distance in meters to search for listings and loyer data"),
    html.I(
        "**Please be aware that loyer latitude and longitude are randomly generated around the approximate location"),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Label("Latitude"),
    dcc.Input(id="latitude", type="number", placeholder="", style={'marginRight': '10px'}),
    html.Label("Longitude"),
    dcc.Input(id="longitude", type="number", placeholder="", style={'marginRight': '10px'}),
    html.Label("Distance (m)"),
    dcc.Input(id="distance", type="number", placeholder="", style={'marginRight': '10px'}),
    html.Div([
        dcc.Graph(id='fig-listings-map', figure=fig_listings, style={'height': '450px'}),
        dcc.Graph(id='fig-loyer-map', figure=fig_loyer, style={'height': '450px'}),
    ],
        style={'display': 'grid', 'grid-template-columns': '50% 50%'}
    ),
    html.Div([
        dcc.Graph(id='fig-combined-map', figure=fig_combined, style={'height': '600px'}),
        html.Div([
            html.Div([
                html.H2("Average Price Listings", style={'textAlign': 'center'}),
                html.Div(id='details_listings_2', style={'textAlign': 'center', 'marginTop': '20px'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20px'}),
            html.Div([
                html.H2("Average Price Loyer", style={'textAlign': 'center'}),
                html.Div(id='details_loyer_2', style={'textAlign': 'center', 'marginTop': '20px'})
            ], style={'width': '48%', 'display': 'inline-block', 'padding': '0 20px'})
        ]),
    ],
        style={'display': 'grid', 'grid-template-columns': '70% 50%'}
    ),

])


@dash.callback(
    dash.Output('fig-combined-map', 'figure'),
    dash.Output('fig-listings-map', 'figure'),
    dash.Output('fig-loyer-map', 'figure'),
    dash.Output('details_listings_2', 'children'),
    dash.Output('details_loyer_2', 'children'),
    dash.Input('latitude', 'value'),
    dash.Input('longitude', 'value'),
    dash.Input('distance', 'value')
)
def update_map(latitude, longitude, distance):
    if latitude is None or longitude is None or distance is None:
        return fig_combined, fig_listings, fig_loyer, [], []
    if latitude == '' or longitude == '' or distance == '':
        return fig_combined, fig_listings, fig_loyer, [], []
    print("Updating map with new location: ", latitude, longitude, distance)

    listings_search, loyer_search = location_search.location_search(float(latitude), float(longitude), int(distance))
    merged_dataset_tmp = apply_post_process(listings_search, loyer_search)
    fig_listings_ret = px.scatter_mapbox(merged_dataset_tmp.loc[merged_dataset_tmp['rent_type'] == "listings"],
                                         lat="latitude",
                                         lon="longitude",
                                         zoom=13,
                                         color="price_per_m2",
                                         center={"lat": float(latitude), "lon": float(longitude)},
                                         size="price_per_m2",
                                         hover_name="price_per_m2", mapbox_style="carto-positron", size_max=20)
    fig_listings_ret.update_layout(transition_duration=500)

    fig_loyer_ret = px.scatter_mapbox(merged_dataset_tmp.loc[merged_dataset_tmp['rent_type'] == "loyer"],
                                      lat="latitude",
                                      lon="longitude",
                                      zoom=13,
                                      color="price_per_m2",
                                      center={"lat": float(latitude), "lon": float(longitude)},
                                      size="price_per_m2",
                                      hover_name="price_per_m2", mapbox_style="carto-positron", size_max=15)
    fig_loyer_ret.update_layout(transition_duration=500)
    fig_combined_ret = px.scatter_mapbox(merged_dataset_tmp, lat="latitude",
                                         lon="longitude", color="rent_type",
                                         zoom=13,
                                         center={"lat": float(latitude), "lon": float(longitude)},
                                         size="price_per_m2",
                                         hover_name="price_per_m2", mapbox_style="carto-positron", size_max=20)
    fig_combined_ret.update_layout(transition_duration=500)

    details_listings = html.Div([
        html.P(f"Number of AirBnBxxx: {len(listings_search)}"),
        html.P(f"Average Price per m²: {listings_search['price_per_m2'].mean():.2f}"),
    ])

    details_loyer = html.Div([
        html.P(f"Number of loyer: {len(loyer_search)}"),
        html.P(f"Average Price per m²: {loyer_search['price_per_m2'].mean():.2f}"),
    ])

    return fig_combined_ret, fig_listings_ret, fig_loyer_ret, details_listings, details_loyer
