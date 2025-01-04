import dash
from dash import html, dcc
import geopandas as gpd
import os
import plotly.graph_objects as go

dash.register_page(__name__, path="/map2")

# Load shapefile data for Paris neighborhoods from the /data folder
shapefile_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'arrondissements.shp')
gdf = gpd.read_file("D:/CPE/analise-airbnb-rentabilite/data/arrondissements.shp")

lon = []
lat = []
for geom in gdf.geometry:
    if geom.is_empty:
        continue
    x, y = geom.exterior.xy
    lon.extend(x)
    lat.extend(y)
    lon.append(None)  # Add None to create a break in the line
    lat.append(None)

# Calculate centroids for text labels
centroids = gdf.geometry.centroid
centroid_lon = centroids.x
centroid_lat = centroids.y
neighborhood_names = gdf['l_ar']  # Assuming the shapefile has a 'l_ar' column for neighborhood names


# Create a Plotly map with only the boundaries
fig = go.Figure(go.Scattermapbox(
    mode="lines",
    lon=lon,
    lat=lat,
    hoverinfo='none',
    marker={'size': 1, 'color': 'black'}
))

# Add text labels to the map
fig.add_trace(go.Scattermapbox(
    mode="text",
    lon=centroid_lon,
    lat=centroid_lat,
    text=neighborhood_names,
    hoverinfo='none',
    textfont={'size': 12, 'color': 'black'}
))

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_center={"lat": 48.8566, "lon": 2.3522},
    mapbox_zoom=11,
    height=700
)

# Define the layout of the app
layout = html.Div([
    html.H1("Map of Paris with Neighborhoods"),
    dcc.Graph(id='map', figure=fig, style={'height': '700px'})  # Adjust the height here
])