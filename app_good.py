# =============================================================================
# Import libraries
# =============================================================================
import dash 
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output


# =============================================================================
# Instantiate  Dash App and Flask Server 
# =============================================================================
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# =============================================================================
# Layout components
# =============================================================================
# =============================================================================
# Navbar
# =============================================================================
navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem('Contact us', href=dash.page_registry['pages.contact']['path']),
            dbc.DropdownMenuItem('User account', href=dash.page_registry['pages.user_account']['path'])
    ],
    nav=True,
    label='Config',
    ),
    brand='',
    color='dark',
    dark=True,
    class_name='mb-2',
)

# =============================================================================
# Sidebar
# =============================================================================
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
sidebar = sidebar = html.Div(
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

# =============================================================================
# Body
# =============================================================================
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
body = html.Div(id="page-content", style=CONTENT_STYLE)

# =============================================================================
# Footer
# =============================================================================
footer_left = html.A("@tmts_media, TMTS Media",
		href = "https://twitter.com/tmts_media", 
		target = "_blank")

footer_right = html.P("2022")


footer = html.Footer(
    [
    dbc.Col(footer_left, width=10),
    dbc.Col(footer_right, width=2),
    ]
)



# =============================================================================
# Layout 
# =============================================================================
#app.layout = dbc.Container([
 #   dbc.Row([navbar]),
  #  dbc.Row([
   #     dbc.Col([sidebar]),
    #    dbc.Col([body, dash.page_container])
    #]),
   # footer,
#], fluid = True)

app.layout = dbc.Container([navbar, sidebar, footer, dash.page_container], fluid=True)
# =============================================================================
# Main 
# =============================================================================
if __name__ == "__main__":
    app.run_server(debug=True, port=3000)