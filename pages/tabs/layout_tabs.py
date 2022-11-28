import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc

def get_dummy_body(tab_name: str):    
    body = [html.P("This is tab {}!".format(tab_name), className="card-text"),
            dbc.Button("Click here", color="", id='button'),
            html.Div(id='example_output', children=''),
            dcc.Dropdown(id='dropdown',
            options=
                [
                {'label': 'Success', 'value': 'Success'}, 
                {'label': 'Fail', 'value': 'Fail'}
                ], 
            value='',
            placeholder='Mi rabo'
            ),
            ]
    return body

def render_tab(tab_body):
    """
    Return the body composing a single tab. 
    Params:
        - tab_body: method calling layout and components of a certain page.

    Return:
        - Page body with specific components.
    """
    tab_name = dbc.Card(
    dbc.CardBody(
            tab_body
    ),
    className="mt-3",
    )
    return tab_name

def summary():
    """
    A method that renders a basic layout for Summary page.
    """
    return render_tab(get_dummy_body('Summary'))

def fundamentals():
    """
    A method that renders a basic layout for Fundamentals page.
    """
    return render_tab(get_dummy_body('Fundamentals'))

def liquidity_solvency():
    """
    A method that renders a basic layout for Liquidity&Solvency page.
    """
    return render_tab(get_dummy_body('Liquidity&Solvency'))

def growth_metrics():
    """
    A method that renders a basic layout for Growth Metrics page.
    """
    return render_tab(get_dummy_body('Growth Metrics'))

def performance_metrics():
    """
    A method that renders a basic layout for Performance Metrics page.
    """
    return render_tab(get_dummy_body('Performance Metric'))

def equity():
    """
    A method that renders a basic layout for Equity Structure page.
    """
    return render_tab(get_dummy_body('Equity Structure'))

def price_forecast():
    """
    A method that renders a basic layout for Price Forecast page.
    """
    return render_tab(get_dummy_body('Price Forecast'))