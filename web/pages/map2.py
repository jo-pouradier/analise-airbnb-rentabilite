import dash
from dash import html, dcc
from .utils.create_boundaries_map import create_boundaries_map

# dash.register_page(__name__, path="/map2")

fig = create_boundaries_map()

# Define the layout of the app
layout = html.Div(
    [
    html.H1("Map of Paris with Neighborhoods", className='header-title',id='map2-title'),
    html.Div(
                    [
                        html.P("This map shows the neighborhoods of Paris with detailed boundaries. Use the interactive map below to explore the different areas.", 
                            className='description'),
                        dcc.Graph(id='map', figure=fig, className='map')
                    ],
                    className='map-container'
                )
            ],
            className='container'
                
    
)