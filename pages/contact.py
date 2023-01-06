import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from example_plots import plot_scatter

dash.register_page(__name__,
                   path='/contact',  # '/' is home page and it represents the url
                   name='Contact us',  # name of page, commonly used as name of link
                   title='Contact us',  # title that appears on browser's tab
                   image='twitter-icon.png',  # image in the assets folder
                   description='Our rrss and contact emails'
)

# GLOBAL CONSTANTS
CONTENT_FONT_SIZE = 36
TITLE_FONT_SIZE = 14

# LAYOUT COMPONENTS
upper_card = dbc.Card([
    html.P("¿Alguna duda?", style={'color': 'white', 'fontSize': CONTENT_FONT_SIZE}, className="mt-2 mb-0"),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Input(id="input1", type="text", placeholder="Nombre y apellidos", style={'marginRight':'10px', 'marginBottom': '10px', 'width': '400px'}),
            dcc.Input(id="input2", type="text", placeholder="Email", style={'marginRight':'10px', 'marginBottom': '10px', 'width': '400px'}),
            dcc.Textarea(id="message", placeholder="Mensaje", style={'marginRight':'10px', 'marginBottom': '10px', 'width': '400px', 'height': '200px', 'text-align':'top', 'resize': 'none'})
        ], width= 8),
        dbc.Col([
            html.P('Envíanos cualquier duda que tengas y te responderemos lo antes posible. A veces tardamos un poco, mucho ajetreo en nuestra vida. Recuerda que la paciencia es una virtud.', style={'text-align': 'justify'}),
            html.Button('Enviar', id='contact-button', style={'margin-top': '40px', 'margin-left': '140px'})
        ], width= 4)
    ])
], class_name= "card", style={'width': '800px', 'height': '400px'})

lower_card = dbc.Card([
    html.P("Nuestras RRSS", style={'color': 'white', 'fontSize': CONTENT_FONT_SIZE}, className="mt-3 mb-0"),
    html.Hr(),
    dbc.Row([
        dbc.Col([dbc.NavLink([html.I(className="fa-brands fa-twitter")], class_name='mt-2', href='https://twitter.com/tmts_media', active='exact', style={'font-size': '2rem', 'color':'white'})], width= 4),
        dbc.Col([dbc.NavLink([html.I(className="fa-brands fa-instagram")], class_name='mt-2', href='https://www.instagram.com/tmtsmedia/?hl=es', active='exact', style={'font-size': '2rem', 'color':'white'})], width= 4),
        dbc.Col([dbc.NavLink([html.I(className="fa fa-envelope")], class_name='mt-2', href='mailto:tiposerio@tmtsmedia.com', active='exact', style={'font-size': '2rem', 'color':'white'})], width= 4)
    ])
], class_name= "card", style={'width': '800px', 'height': '200px'}) # "card" css class stilizes the card. With style prop individual features are fine-tuned for each card instance.

# COMPOSITE LAYOUT 
layout = dbc.Container(
    [
        dbc.Row(upper_card),
        dbc.Row(lower_card, className='mt-2')
    ], className= 'centeder body-content', style= {'width': '700px'} # this css class positions the container in the web page
)


# TODO: Crear el callback que devuelva lo que el usuario ha escrito y envíe un correo electrónico.
# El siguiente snippet es un ejemplo sencillo de como crear un callback que capture el texto introducido:

# app.layout = html.Div([
#     dcc.Textarea(
#         id='textarea-state-example',
#         value='Textarea content initialized\nwith multiple lines of text',
#         style={'width': '100%', 'height': 200},
#     ),
#     html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
#     html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'})
# ])

# @app.callback(
#     Output('textarea-state-example-output', 'children'),
#     Input('textarea-state-example-button', 'n_clicks'),
#     State('textarea-state-example', 'value')
# )
# def update_output(n_clicks, value):
#     if n_clicks > 0:
#         return 'You have entered: \n{}'.format(value)