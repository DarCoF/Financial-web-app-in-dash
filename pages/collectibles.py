from email import header
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from example_plots import plot_scatter

dash.register_page(__name__,
                   path='/collectibles',  # '/' is home page and it represents the url
                   name='Collectibles',  # name of page, commonly used as name of link
                   title='3D Collectibles',  # title that appears on browser's tab
                   image='twitter-icon.png',  # image in the assets folder
                   description='A gallery showing some of our 3D creations'
)

# GLOBAL CONSTANTS
CONTENT_FONT_SIZE = 24
TITLE_FONT_SIZE = 14

# GENERIC COLLECTIBLE CARD
def collectible_card(card_header, img, img_title, text):
    """A function returning a base body for a card.

    Args:
        img (string): Url string for image asset.
        img_title (string): Image title to be displayed when hovering over image.
        text (string): Brief descrition of image.

    Returns:
        object: Base body of collectible card (base component and subcomponents).
    """
    collectible = dbc.Card([
        html.P(card_header, style={'color': 'white', 'fontSize': CONTENT_FONT_SIZE}, className="mt-2 mb-0"),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                html.Img(src=img, title=img_title, className='border border-secondary image')
                ], width= 8),
            dbc.Col([
                html.P(text, style={'color': 'white', 'fontSize': TITLE_FONT_SIZE, 'text-align': 'justify'}, className="mt-2 mb-0"),
                html.Button('Descargar', id='download-button', style={'margin-top': '220px', 'margin-left': '75px'})
                ], width= 4)
        ])
    ], className= 'card', style={'width': '600px', 'height': '400px'})    
    return collectible

# COMPOSITE LAYOUT 
layout = dbc.Container(
    [
        dbc.Row(collectible_card('Sticker Tipo Serio', 'assets/CartoonFaces-TS2.png', 'Un sticker', 'Sticker de tipo serio. Algo poco común.'), className= 'mb-2'),
        dbc.Row(collectible_card('Sticker Tipo Mofa', 'assets/CartoonFaces-TM2.png', 'Un sticker', 'Sticker de tipo mofa. Algo muy poco común.'), className='mb-2')
    ], className= 'centered' # this css class positions the container in the web page
)