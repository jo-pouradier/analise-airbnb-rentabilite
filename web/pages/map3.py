# import dash
# from dash import html, dcc
# import pandas as pd
# import numpy as np
# from shapely.geometry import Point
# import geopandas as gpd
# import plotly.graph_objects as go
# from scipy.stats import gaussian_kde
# from matplotlib.colors import Normalize
# from .utils.create_boundaries_map import create_boundaries_map

# dash.register_page(__name__, path="/paris_heatmap_diff2")

# # Load the shapefile of Paris arrondissements
# shapefile_path = 'D:/CPE/analise-airbnb-rentabilite/data/arrondissements.shp'
# arrondissements = gpd.read_file(shapefile_path)

# # Load your first dataset with coordinates and prices
# data1 = pd.read_csv('D:/CPE/analise-airbnb-rentabilite/data/listings_process.csv')
# data1 = data1.replace([np.inf, -np.inf], np.nan).dropna(subset=['price_per_m2', 'longitude', 'latitude'])

# # Load your second dataset with coordinates and prices
# data2 = pd.read_csv('D:/CPE/analise-airbnb-rentabilite/data/loyer_process.csv')
# data2 = data2.replace([np.inf, -np.inf], np.nan).dropna(subset=['price_per_m2', 'geo_point_2d'])

# # Convert the coordinates to GeoDataFrames
# geometry1 = [Point(xy) for xy in zip(data1.longitude, data1.latitude)]
# geo_data1 = gpd.GeoDataFrame(data1, geometry=geometry1)

# geometry2 = [Point(float(xy.split(',')[1]), float(xy.split(',')[0])) for xy in data2['geo_point_2d']]
# geo_data2 = gpd.GeoDataFrame(data2, geometry=geometry2)

# # Perform the spatial join to get the arrondissement for each point
# geo_data1 = gpd.sjoin(geo_data1, arrondissements, how='left')
# geo_data2 = gpd.sjoin(geo_data2, arrondissements, how='left')

# # Extract coordinates and prices
# x1 = geo_data1.geometry.x
# y1 = geo_data1.geometry.y
# prices1 = geo_data1['price_per_m2']

# x2 = geo_data2.geometry.x
# y2 = geo_data2.geometry.y
# prices2 = geo_data2['price_per_m2']

# # Perform kernel density estimation for both datasets
# xy1 = np.vstack([x1, y1])
# kde1 = gaussian_kde(xy1, weights=prices1, bw_method=0.2)
# xmin, xmax = min(x1.min(), x2.min()), max(x1.max(), x2.max())
# ymin, ymax = min(y1.min(), y2.max()), max(y1.max(), y2.max())
# xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
# positions = np.vstack([xx.ravel(), yy.ravel()])
# density1 = kde1(positions).reshape(xx.shape)

# xy2 = np.vstack([x2, y2])
# kde2 = gaussian_kde(xy2, weights=prices2, bw_method=0.2)
# density2 = kde2(positions).reshape(xx.shape)

# # Calculate the difference in densities
# density_diff = density1 - density2

# # Create a Plotly map with boundaries and heatmaps
# fig = create_boundaries_map()

# # Add heatmap for the density difference
# norm = Normalize(vmin=-np.max(np.abs(density_diff)), vmax=np.max(np.abs(density_diff)))
# colorscale = [[0, 'red'], [0.5, 'white'], [1, 'green']]  # Red for negative, white for zero, green for positive

# fig.add_trace(go.Densitymapbox(
#     lon=xx.ravel(),
#     lat=yy.ravel(),
#     z=density_diff.ravel(),
#     radius=10,
#     opacity=0.6,
#     colorscale=colorscale,
#     showscale=True,
#     colorbar=dict(
#         title='Price Difference Density',
#         tickvals=[-np.max(np.abs(density_diff)), 0, np.max(np.abs(density_diff))],
#         ticktext=['Dataset 2 > Dataset 1', 'Equal', 'Dataset 1 > Dataset 2']
#     )
# ))

# # Add labels for arrondissements
# for idx, row in arrondissements.iterrows():
#     fig.add_trace(go.Scattermapbox(
#         mode="text",
#         lon=[row.geometry.centroid.x],
#         lat=[row.geometry.centroid.y],
#         text=[row['l_ar']],
#         hoverinfo='none',
#         textfont={'size': 12, 'color': 'blue'}
#     ))

# fig.update_layout(
#     mapbox_style="carto-positron",
#     mapbox_center={"lat": 48.8566, "lon": 2.3522},
#     mapbox_zoom=11,
#     height=700
# )

# # Define the layout of the app
# layout = html.Div([
#     html.H1("Comparison of Prices in Paris with Arrondissements", style={'textAlign': 'center', 'color': '#4CAF50', 'marginBottom': '20px'}),
#     html.Div(
#         [
#             html.P("This map shows the neighborhoods of Paris with detailed boundaries. Use the interactive map below to explore the different areas.", 
#                    style={'textAlign': 'center', 'color': '#555', 'fontSize': '16px', 'marginBottom': '30px'}),
#             dcc.Graph(id='map', figure=fig, style={'height': '700px', 'border': '1px solid #ddd', 'borderRadius': '10px'})
#         ],
#         style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'}
#     )
# ], style={'backgroundColor': '#f0f0f0', 'padding': '50px 0'})