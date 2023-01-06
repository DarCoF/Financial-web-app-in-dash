# =============================================================================
# Import libraries
# =============================================================================
from enum import auto
from turtle import width
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output


# =============================================================================
# Instantiate  Dash App and Flask Server 
# =============================================================================
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY, dbc.icons.FONT_AWESOME])
server = app.server
print(server)

# =============================================================================
# Layout components
# =============================================================================
# =============================================================================
# Navbar
# =============================================================================
navbar = dbc.NavbarSimple(
    children=[
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(dash.page_registry['pages.user_account']['name'], href=dash.page_registry['pages.user_account']['path']),
                dbc.DropdownMenuItem(dash.page_registry['pages.report_bug']['name'], href=dash.page_registry['pages.report_bug']['path'])
            ],
            nav=True,
            in_navbar=True,
            label="Config",
        ),
    ],
    brand="",
    brand_href="#",
    color="navbar",
    dark=True,
    class_name='navbar rounded border-bottom border-dark',
)

# =============================================================================
# Sidebar
# =============================================================================
sidebar = sidebar = html.Div(
    [
        html.Div([
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src="assets\\logo.png", style={"width": "4.15rem"}, className= 'centered'),
                html.H2("", className="display-8"),
            ], 
            className= 'sidebar-header',
        ),
        html.Hr(),
        html.Div([
                html.I(className="fa fa-line-chart ms-3 mt-1"),
                html.P("Financials", className="lead mt-1"),
            ],
            className='sidebar-header',
        ), 
        dbc.Nav(
        [
            dbc.NavLink(
                    [
                        html.I(className="fa fa-car me-2"), html.Span(dash.page_registry['pages.tesla']['name'])
                    ],
                    href="/",
                    active="exact",
                ),
            dbc.NavLink(
                    [
                        html.I(className="fa fa-building me-2"), html.Span(dash.page_registry['pages.base_company']['name']),
                    ],
                    href="/test_two",
                    active="exact",
                )
        ],
            vertical=True,
            pills=True,
        ),
        html.Div([
                html.I(className="fa fa-camera ms-3 mt-3"),
                html.P("Gallery", className="lead mt-3"),
            ],
            className='sidebar-header',
        ),            
        dbc.Nav(
        [
            dbc.NavLink(
                    [
                        html.I(className="fa fa-gift me-2"), html.Span(dash.page_registry['pages.collectibles']['name']),
                    ],
                    href="/collectibles",
                    active="exact",
                ),
            dbc.NavLink(
                    [
                        html.I(className="fa fa-book me-2"), html.Span(dash.page_registry['pages.resources']['name']),
                    ],
                    href="/resources",
                    active="exact",
                )
        ],
            vertical=True,
            pills=True
        ),
        html.Div([
                html.I(className="fa fa-users ms-3 mt-3"),
                html.P("About Me", className="lead mt-3"),
            ],
            className='sidebar-header',
        ), 
        dbc.Nav(
        [
            dbc.NavLink(
                    [
                        html.I(className="fa fa-bullseye me-2"), html.Span(dash.page_registry['pages.mission']['name']),
                    ],
                    href="/mission",
                    active="exact",
                ),
            dbc.NavLink(
                    [
                        html.I(className="fa fa-commenting me-2"), html.Span(dash.page_registry['pages.contact']['name']),
                    ],
                    href="/contact",
                    active="exact",
                )
        ],
            vertical=True,
            pills=True
        ),        
    ],
    className="sidebar border-end border-dark",
)

# =============================================================================
# Body
# =============================================================================
body = dbc.Row(
    [
        dbc.Col(id="page-content", children=[dash.page_container], width=12, className='content')
    ]
)

# =============================================================================
# Footer
# =============================================================================
footer_icon_twitter = dbc.NavLink([html.I(className="fa-brands fa-twitter")], class_name='align-middle', href='https://twitter.com/tmts_media', active='exact')
footer_icon_instragram = dbc.NavLink([html.I(className="fa-brands fa-instagram")], class_name='align-middle', href='https://www.instagram.com/tmtsmedia/?hl=es', active='exact')
footer_left = html.Div(
    [
        footer_icon_twitter,
        footer_icon_instragram
    ], className='hstack')
footer_name = html.P(id='footer', children='The Rabbit Hole 2022', className='mt-2', style={'padding-left': '25px', 'padding-top': '5px'})

footer = html.Footer(children = html.Div(
    children=[
        footer_icon_twitter,
        footer_icon_instragram,
        footer_name
        ],
    className='hstack position-absolute top-50 start-50 translate-middle',
), className='footer border-top border-dark')

# =============================================================================
# Layout 
# =============================================================================
app.layout = html.Div(
    [
        dbc.Row(
            [sidebar, html.Div(dash.page_container, className= 'mt-5 p-5 centered content'), footer, navbar], align='center')], className='overlay-two')

# =============================================================================
# Main 
# =============================================================================
if __name__ == "__main__":
    app.run_server(debug=True, port=3000)