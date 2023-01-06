from pydoc import classname
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from example_plots import plot_scatter

dash.register_page(__name__,
                   path='/bug',  # '/' is home page and it represents the url
                   name='Report bug',  # name of page, commonly used as name of link
                   title='Report bug',  # title that appears on browser's tab
                   image='twitter-icon.png',  # image in the assets folder
                   description='Report bugs to us page'
)

# GLOBAL CONSTANTS
CONTENT_FONT_SIZE = 24
TITLE_FONT_SIZE = 14

# LAYOUT COMPONENTS
report_card = dbc.Card([
    html.Div([html.I(className="fa fa-bug", style={'font-size': '1.5rem', 'margin-top':'5px'}), 
    html.P("¿Has encontrado un error?", style={'color': 'white', 'fontSize': CONTENT_FONT_SIZE}, className="mt-1 mb-0 ms-3")], className='hstack', style={'margin-left': '150px'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Input(id="input1", type="text", placeholder="Resumen del error", style={'marginRight':'10px', 'marginBottom': '10px', 'width': '400px'}),
            dcc.Textarea(id="message", placeholder="Descripción del error", style={'marginRight':'10px', 'marginBottom': '10px', 'width': '400px', 'height': '225px', 'text-align':'top', 'resize': 'none'})
        ], width= 8),
        dbc.Col([
            html.P('Si hay encontrado algún error, háznoslo saber. No somos omnipresentes, así que vuestra ayuda es bienvenida.', style={'text-align': 'justify', 'margin-right': '20px'}),
            html.Button('Enviar', id='contact-button', style={'margin-top': '80px', 'margin-left': '140px', 'margin-right': '150px'})
        ], width= 4)
    ])
], class_name= "card")

layout = dbc.Container(
    [
        report_card
    ]
, class_name='center-screen body-content', style={'width': '800px', 'height': '400px'})