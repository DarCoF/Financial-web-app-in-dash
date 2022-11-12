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

layout = dbc.Container(
    [
        dcc.Graph(id='test_scatter',
                  figure= plot_scatter())
    ]
)