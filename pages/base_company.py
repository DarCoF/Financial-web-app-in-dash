import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from example_plots import plot_scatter

dash.register_page(__name__,
                   path='/base_company',  # '/' is home page and it represents the url
                   name='Base Company',  # name of page, commonly used as name of link
                   title='Base Company Page',  # title that appears on browser's tab
                   image='instagram-icon.png',  # image in the assets folder
                   description='This a generic page for a company financials'
)

layout = dbc.Container(
    [
        dcc.Graph(id='test_scatter',
                  figure= plot_scatter())
    ]
)