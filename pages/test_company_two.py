import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from example_plots import plot_scatter

dash.register_page(__name__,
                   path='/test_two',  # '/' is home page and it represents the url
                   name='Test 2',  # name of page, commonly used as name of link
                   title='Test Page 2',  # title that appears on browser's tab
                   image='instagram-icon.png',  # image in the assets folder
                   description='This is the second test plot'
)

layout = dbc.Container(
    [
        dcc.Graph(id='test_scatter',
                  figure= plot_scatter())
    ]
)