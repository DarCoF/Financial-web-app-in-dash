from pydoc import classname
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from example_plots import plot_scatter

dash.register_page(__name__,
                   path='/mission',  # '/' is home page and it represents the url
                   name='Our mission',  # name of page, commonly used as name of link
                   title='This is our mission',  # title that appears on browser's tab
                   image='twitter-icon.png',  # image in the assets folder
                   description='Brief description of TMTS mission'
)

CONTENT_FONT_SIZE = 30
TITLE_FONT_SIZE = 14

def get_card(img_url, title, content):
    card = dbc.Card([
        dbc.CardHeader([
            html.Img(src=img_url),
            html.P(title, style={'color': 'white', 'fontSize': CONTENT_FONT_SIZE})
        ]),
        html.Hr(),
        dbc.CardBody([html.P(content, style={'color': 'white', 'fontSize': TITLE_FONT_SIZE})])
    ], className='card')
    return card

layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([get_card('', 'Sobre mi', 'Su biografía')],  width= 8, class_name= 'mb-2'),
            dbc.Col([get_card('', 'Mi pequeña historia', 'Aquí va el contenido')], width= 8, className='mb-2'),
            dbc.Col([get_card('', '¿Qué es esta web-app?', 'Aquí va el contenido')],  width= 8, className='mb-2')
        ])       
    ], className= 'center-screen ', style={'width': 'auto'}
)