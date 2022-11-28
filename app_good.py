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
    class_name='navbar rounded',
)

# =============================================================================
# Sidebar
# =============================================================================
sidebar = sidebar = html.Div(
    [
        html.Div([
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src="assets\EggLogo_white_transparency.png", style={"width": "3rem"}),
                html.H2("TMTS", className="display-4"),
            ], 
            className= 'sidebar-header',
        ),
        html.Hr(),
        html.Div([
                html.P("Company Financials", className="lead"),
            ],
            className='sidebar-header',
        ), 
        dbc.Nav(
        [
            dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"), html.Span(dash.page_registry['pages.tesla']['name']),
                    ],
                    href="/",
                    active="exact",
                ),
            dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"), html.Span(dash.page_registry['pages.base_company']['name']),
                    ],
                    href="/test_two",
                    active="exact",
                )
        ],
            vertical=True,
            pills=True,
        ),
        html.Div([
                html.P("Gallery", className="lead"),
            ],
            className='sidebar-header',
        ),            
        dbc.Nav(
        [
            dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"), html.Span(dash.page_registry['pages.collectibles']['name']),
                    ],
                    href="/collectibles",
                    active="exact",
                ),
            dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"), html.Span(dash.page_registry['pages.resources']['name']),
                    ],
                    href="/resources",
                    active="exact",
                )
        ],
            vertical=True,
            pills=True
        ),
        html.Div([
                html.I(className="fas fa-home me-2 lead"),
                html.P("About Us", className="lead"),
            ],
            className='sidebar-header',
        ), 
        dbc.Nav(
        [
            dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"), html.Span(dash.page_registry['pages.mission']['name']),
                    ],
                    href="/mission",
                    active="exact",
                ),
            dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"), html.Span(dash.page_registry['pages.contact']['name']),
                    ],
                    href="/contact",
                    active="exact",
                )
        ],
            vertical=True,
            pills=True
        ),        
    ],
    className="sidebar",
)

# =============================================================================
# Body
# =============================================================================
body = dbc.Row(
    [
        dbc.Col(id="page-content", children=[dash.page_container], width=12, className='my-5 p-4')
    ]
)

# =============================================================================
# Footer
# =============================================================================
footer_icon_twitter = dbc.NavLink([html.I(className="fa-brands fa-twitter")], class_name='footer', href='https://twitter.com/tmts_media', active='exact')
footer_icon_instragram = dbc.NavLink([html.I(className="fa-brands fa-instagram")], class_name='footer', style={'margin-left': '75px'}, href='https://www.instagram.com/tmtsmedia/?hl=es', active='exact')
footer_left = html.Div(
    [
        footer_icon_twitter,
        footer_icon_instragram
    ], className='hstack')
footer_right = html.P("TMTS media, 2022")


footer = html.Div(
        [
            dbc.Row(
            [
            dbc.Col(html.Div(''), width={"size": 2, "order": 1}, className='footer'),
            dbc.Col([footer_left], width={"size": 5, "order": 2, 'offset': 2}, className= 'footer'),
            dbc.Col([footer_right], width={"size": 5, "order": 3}, className= 'footer', style={'margin-left': '1500px'}),
            ],
            className="g-0 position-static"
            ),
        ],
        className='rounded'
)


# =============================================================================
# Layout 
# =============================================================================
app.layout = html.Div(
    [
        dbc.Row(
            [sidebar, navbar, html.Div(dash.page_container, className= 'mt-5 p-5 centered'), footer], align='center')
    ], className='overlay-two'
)

# =============================================================================
# Main 
# =============================================================================
if __name__ == "__main__":
    app.run_server(debug=True, port=3000)