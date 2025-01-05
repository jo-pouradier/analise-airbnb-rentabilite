# import dash
# from dash import html, dcc
# from .utils.create_boundaries_map import create_boundaries_map
# import pandas as pd
# import numpy as np
# from shapely.geometry import Point
# import geopandas as gpd
# import plotly.graph_objects as go
# from scipy.stats import gaussian_kde


# dash.register_page(__name__, path="/paris_heatmap_diff")


# # Load your first dataset with coordinates and prices
# data1 = pd.read_csv("D:/CPE/analise-airbnb-rentabilite/data/listings_process.csv")
# data1 = data1.replace([np.inf, -np.inf], np.nan).dropna(
#     subset=["price_per_m2", "longitude", "latitude"]
# )

# # Load your second dataset with coordinates and prices
# data2 = pd.read_csv("D:/CPE/analise-airbnb-rentabilite/data/loyer_process.csv")
# data2 = data2.replace([np.inf, -np.inf], np.nan).dropna(
#     subset=["price_per_m2", "geo_point_2d"]
# )


# # Convert the coordinates to GeoDataFrames
# geometry1 = [Point(xy) for xy in zip(data1.longitude, data1.latitude)]
# geo_data1 = gpd.GeoDataFrame(data1, geometry=geometry1)

# geometry2 = [
#     Point(xy)
#     for xy in data2["geo_point_2d"].str.split(",", expand=True).astype(float).values
# ]
# geo_data2 = gpd.GeoDataFrame(data2, geometry=geometry2)


# # Extract coordinates and prices
# x1 = geo_data1.geometry.x
# y1 = geo_data1.geometry.y
# prices1 = geo_data1["price_per_m2"]

# x2 = geo_data2.geometry.x
# y2 = geo_data2.geometry.y
# prices2 = geo_data2["price_per_m2"]


# # # Perform kernel density estimation for both datasets
# xy1 = np.vstack([x1, y1])
# kde1 = gaussian_kde(xy1, weights=prices1, bw_method=0.1)
# xmin1, xmax1 = x1.min(), x1.max()
# ymin1, ymax1 = y1.min(), y1.max()
# xx1, yy1 = np.mgrid[xmin1:xmax1:100j, ymin1:ymax1:100j]
# positions1 = np.vstack([xx1.ravel(), yy1.ravel()])
# density1 = kde1(positions1).reshape(xx1.shape)

# xy2 = np.vstack([x2, y2])
# kde2 = gaussian_kde(xy2, weights=prices2, bw_method=0.1)
# xmin2, xmax2 = x2.min(), x2.max()
# ymin2, ymax2 = y2.min(), y2.max()
# xx2, yy2 = np.mgrid[xmin2:xmax2:100j, ymin2:ymax2:100j]
# positions2 = np.vstack([xx2.ravel(), yy2.ravel()])
# density2 = kde2(positions2).reshape(xx2.shape)

# fig_airbnb = create_boundaries_map()
# # Add heatmap for the first dataset
# fig_airbnb.add_trace(
#     go.Densitymapbox(
#         lon=xx1,
#         lat=yy1,
#         z=density1.ravel(),
#         radius=10,
#         opacity=0.5,
#         colorscale="Reds",
#         showscale=True,
#         colorbar=dict(
#             title="Price Density Airbnb",
#         ),
#     )
# )

# fig_loyer = create_boundaries_map()
# # Add heatmap for the second dataset
# fig_loyer.add_trace(
#     go.Densitymapbox(
#         lon=xx2,
#         lat=yy2,
#         z=density2.ravel(),
#         radius=10,
#         opacity=0.5,
#         colorscale="Blues",
#         showscale=True,
#         colorbar=dict(
#             title="Price Density Loyer",
#         ),
#     )
# )

# # Define the layout of the app
# layout = html.Div(
#     [
#         html.H1(
#             "Map of Paris with Neighborhoods", className="header-title", id="map2-title"
#         ),
#         html.Div(
#             [
#                 html.P(
#                     "This map shows the neighborhoods of Paris with detailed boundaries. Use the interactive map below to explore the different areas.",
#                     className="description",
#                 ),
#                 dcc.Graph(
#                     id="map_loyer",
#                     figure=fig_loyer,
#                     style={
#                         "height": "700px",
#                         "width": "50%",
#                         "display": "inline-block",
#                     },
#                 ),
#                 dcc.Graph(
#                     id="map_airbnb",
#                     figure=fig_airbnb,
#                     style={
#                         "height": "700px",
#                         "width": "50%",
#                         "display": "inline-block",
#                     },
#                 ),
#             ],
#             className="map-container",
#         ),
#     ],
#     className="container",
# )
