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

layout = dbc.Container(
    [
        dcc.Graph(id='test_scatter',
                  figure= plot_scatter())
    ]
)