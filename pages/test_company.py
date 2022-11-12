import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from example_plots import plot_scatter

dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Test 1',  # name of page, commonly used as name of link
                   title='Test Page 1',  # title that appears on browser's tab
                   image='twitter-icon.png',  # image in the assets folder
                   description='This is the first test plot'
)

layout = dbc.Container(
    [
        dcc.Graph(id='test_scatter',
                  figure= plot_scatter())
    ]
)