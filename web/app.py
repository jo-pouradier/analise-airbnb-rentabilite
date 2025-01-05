from dash import Dash, html, dcc
import dash
import os


def create_app():
    app = Dash(__name__, use_pages=True)
    
    # Register all pages from the 'pages' folder
    pages_folder = os.path.join(os.path.dirname(__file__), 'pages')
    dash.register_page(pages_folder)
    
    # Create a navigation bar with links to all registered pages
    nav_links = [
        dcc.Link(f"{page['name']}", href=page["path"], className='nav-link')
        for page in dash.page_registry.values()
        if page["module"] != "pages.not_found_404"
    ]
    
    app.layout = html.Div(
        [
            html.Div(
                [
                    html.H1("Big Data Project",className='header-title'),
                    html.Div(nav_links)
                ],
                className='navbar'
            ),
            html.Hr(),
            dash.page_container,
        ]
    )

 
    return app


if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True)