from dash import html
import dash

dash.register_page(__name__, path="/welcome")


layout = html.H1("Welcome to the Paris Housing Market Dashboard")