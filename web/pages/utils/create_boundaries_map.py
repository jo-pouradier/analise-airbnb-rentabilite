import geopandas as gpd
import plotly.graph_objects as go

def create_boundaries_map(path="D:/CPE/analise-airbnb-rentabilite/data/arrondissements.shp"):
    """
    Create a Plotly map with the boundaries of Paris neighborhoods.

    :param path: Path to the shapefile with the boundaries of Paris neighborhoods
    :return: A Plotly map object
    """
    # Load shapefile data for Paris neighborhoods from the /data folder
    gdf = gpd.read_file(path)

    lon = []
    centroid_lon, centroid_lat = [], []
    lat = []
    neighborhood_names = gdf['l_ar']  # Assuming the shapefile has a 'l_ar' column for neighborhood names
    for geom in gdf.geometry:
        if geom.is_empty:
            continue
        x, y = geom.exterior.xy
        lon.extend(x)
        lat.extend(y)
        lon.append(None)  # Add None to create a break in the line
        lat.append(None)
        centroid = geom.centroid
        centroid_lon.append(centroid.x)
        centroid_lat.append(centroid.y)

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
    return fig