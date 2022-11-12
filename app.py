# IMPORTS
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


# =============================================================================
# Dash App and Flask Server
# =============================================================================
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])
server = app.server 

# =============================================================================
# LAYOUT
# =============================================================================
# Sidebar
# TODO: create side bar component with different options: Company Financials (Tesla, Square), Collectibles, About Us, Contact

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

sidebar = html.Div(
    [
        html.Div([
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
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
                        html.I(className="fas fa-home me-2"), html.Span("Test 1"),
                    ],
                    href="/",
                    active="exact",
                ),
            dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"), html.Span("Test 2"),
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
                        html.I(className="fas fa-home me-2"), html.Span("Collectibles"),
                    ],
                    href="/collectibles",
                    active="exact",
                ),
            dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"), html.Span("Resources"),
                    ],
                    href="/resources",
                    active="exact",
                )
        ],
            vertical=True,
            pills=True
        ),
        html.Div([
                html.P("About Us", className="lead"),
            ],
            className='sidebar-header',
        ), 
        dbc.Nav(
        [
            dbc.NavLink(
                    [
                        html.I(className="bi bi-info-circle-fill me-2"), html.Span("Our mission"),
                    ],
                    href="/mission",
                    active="exact",
                ),
            dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"), html.Span("Contact us"),
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


#Navbar
# TODO: create upper bar with ring bell icon and a title
navbar = []

# Body
# TODO: it contains the different clickable pages that compose the web app
body = html.Div(id="page-content", style=CONTENT_STYLE)

# Footer
# TODO: bottom bar with company name, link to webpage and date
footer = []

# Container for app layout
app.layout = dbc.Container([sidebar, body, dash.page_container], fluid=True)





# =============================================================================
# CALLBACKS
# =============================================================================



# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    app.run_server(debug=False, port=8000)