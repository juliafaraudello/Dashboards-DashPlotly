import dash
import dash_bootstrap_components as dbc
import dash_html_components as html 

def createDash(flaskApp):
    dash_app = dash.Dash(__name__,routes_pathname_prefix='/dashTendencia/', server = flaskApp, external_stylesheets=[dbc.themes.BOOTSTRAP,
                                    'https://use.fontawesome.com/releases/v5.11.2/css/all.css',
                                    {'href': 'https://fonts.googleapis.com/icon?family=Material+Icons',
                                    'rel': 'stylesheet'}])
    dash_app.layout = html.H1(
        children='Hello tendencias'
    )
    return dash_app
