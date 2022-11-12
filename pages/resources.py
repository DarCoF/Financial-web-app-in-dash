import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from example_plots import plot_scatter

dash.register_page(__name__,
                   path='/resources',  # '/' is home page and it represents the url
                   name='Resources',  # name of page, commonly used as name of link
                   title='Educational resources',  # title that appears on browser's tab
                   image='twitter-icon.png',  # image in the assets folder
                   description='Curated archive of educational resources: links to websites, articles, posts, books, etc.'
)

layout = dbc.Container(
    [
        dcc.Graph(id='test_scatter',
                  figure= plot_scatter())
    ]
)