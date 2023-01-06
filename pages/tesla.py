from enum import Enum
from textwrap import fill
from turtle import bgcolor, fillcolor, width
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.exceptions import PreventUpdate
from pages.tabs import layout_tabs as lt
from pipeline.data_processing import TeslaFinancials

from alpha_vantage.timeseries import TimeSeries  

# Register page into Dash register.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Tesla',  # name of page, commonly used as name of link
                   title='Tesla Page',  # title that appears on browser's tab
                   image='twitter-icon.png',  # image in the assets folder
                   description='Summary of Tesla stock'
)

# -----------------------------------------------------------------------------------
# LOCAL VARIABLES
# -----------------------------------------------------------------------------------
class figure_settings(Enum):
    BACKGROUND = 'rgba(0,0,0,0)'
    TEXT_COLOR = '#e4e4e4'
    MARKER_COLOR = '#cc0000'
    BORDER_COLOR = '#990202'
    Y_GRID_COLOR = '#333333'
    HOVER_LABEL_BG_COLOR = 'rgba(133,0,0,0.75)'
    HOVER_LABEL_BORDER_COLOR = 'rgba(0,0,0,0)'
    TEXT_SIZE = 12
    TITLE_TEXT_SIZE = 16
    TEXT_FONT = 'Brand'
    OPACITY = 0.6
    TITLE_POSITION = 0.5
    LINE_WIDTH = 0.5
    TYPES_SH = ['institutional', 'insider', 'retail']
    PERCENTAGE_SH = [43.00, 14.39, 42.61] # Institutional, insiders and retail.
# -----------------------------------------------------------------------------------
# GENERAL METHODS
# -----------------------------------------------------------------------------------
def get_layout(func):
    layout = dbc.Row([
        dbc.Col(width=1),
        dbc.Col([
        dbc.Card(
            dbc.CardBody(
                func
            ), className="mt-3 p-4")], width= 10)
    ])
    return layout

def get_bar_plot(df, x, y, yaxis_title, xaxis_title, plot_title):
        """_summary_

        Args:
            df (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
            yaxis_title (_type_): _description_
            xaxis_title (_type_): _description_
            plot_title (_type_): _description_

        Returns:
            _type_: _description_
        """
         # Instantiate figure object
        fig = go.Figure()
        # Add trace to figure object containing scatter plot
        fig.add_trace(go.Bar(
                x= df[x],
                y= df[y],
                orientation="v",              # 'v','h': orientation of the marks
        )) 
        #fig.update_layout(xaxis_title='Year', yaxis_title='Revenue (in millions of $)', plot_bgcolor= 'grey')
        fig.update_layout(paper_bgcolor= figure_settings.BACKGROUND.value, 
                        plot_bgcolor= figure_settings.BACKGROUND.value,
                        xaxis_title= xaxis_title,
                        yaxis_title= yaxis_title,
                        font={
                            'color': figure_settings.TEXT_COLOR.value,
                            'family':figure_settings.TEXT_FONT.value,
                            'size': figure_settings.TEXT_SIZE.value
                        },
                        title= {
                            'text': plot_title,
                            'x': figure_settings.TITLE_POSITION.value
                            },
                        title_font= {
                            'size': figure_settings.TITLE_TEXT_SIZE.value,
                            'color': figure_settings.TEXT_COLOR.value,
                            'family': figure_settings.TEXT_FONT.value
                        },
                        title_pad= {
                            't': 10
                        },
                        hoverlabel= dict(
                            bgcolor= figure_settings.HOVER_LABEL_BG_COLOR.value,
                            bordercolor= figure_settings.HOVER_LABEL_BORDER_COLOR.value,
                            font = dict(family= figure_settings.TEXT_FONT.value, color= figure_settings.TEXT_COLOR.value)
                        )
                        )
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor= figure_settings.Y_GRID_COLOR.value)
        fig.update_xaxes(showline=True, linewidth=1, linecolor= figure_settings.TEXT_COLOR.value)
        fig.update_traces(overwrite=True,
            marker= dict(
                line= dict(
                    width= figure_settings.LINE_WIDTH.value,
                    color= figure_settings.MARKER_COLOR.value
                ),
                color= figure_settings.BORDER_COLOR.value,
                opacity= figure_settings.OPACITY.value
            )
        )
        return fig

def get_scatter_plot(df, x, y, yaxis_title, xaxis_title, plot_title, hover_label_text, flag_legend = False, legend_title = 'default'):
        """_summary_

        Args:
            df (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
            yaxis_title (_type_): _description_
            xaxis_title (_type_): _description_
            plot_title (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Instantiate figure object
        fig = go.Figure()
        # Add trace to figure object containing scatter plot
        fig.add_trace(go.Scatter(
                x= df[x],
                y= df[y],
                showlegend= flag_legend,
                name = y
        ))
        # Select background colors and modify axis attributes.
        fig.update_layout(paper_bgcolor= figure_settings.BACKGROUND.value, 
                        plot_bgcolor= figure_settings.BACKGROUND.value,
                        xaxis_title= xaxis_title,
                        yaxis_title= yaxis_title,
                        font={
                            'color': figure_settings.TEXT_COLOR.value,
                            'family':figure_settings.TEXT_FONT.value,
                            'size': figure_settings.TEXT_SIZE.value
                        },
                        title= {
                            'text': plot_title,
                            'x': figure_settings.TITLE_POSITION.value
                            },
                        title_font= {
                            'size': figure_settings.TITLE_TEXT_SIZE.value,
                            'color': figure_settings.TEXT_COLOR.value,
                            'family': figure_settings.TEXT_FONT.value
                        },
                        title_pad= {
                            't': 10
                        },
                        hoverlabel= dict(
                            bgcolor= figure_settings.HOVER_LABEL_BG_COLOR.value,
                            bordercolor= figure_settings.HOVER_LABEL_BORDER_COLOR.value,
                            font = dict(family= figure_settings.TEXT_FONT.value, color= figure_settings.TEXT_COLOR.value)
                        ),
                        legend = dict(title = legend_title)
                        )
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor= figure_settings.Y_GRID_COLOR.value)
        fig.update_xaxes(showline=True, linewidth=1, linecolor=figure_settings.TEXT_COLOR.value, showgrid=False)
        fig.update_traces(
            mode= 'lines',
            line= dict(width= figure_settings.LINE_WIDTH.value),
            line_color= figure_settings.MARKER_COLOR.value,
            fill='tonexty',
            opacity= figure_settings.OPACITY.value,
            text = hover_label_text,
            hoveron= 'points',
            hoverinfo= 'text+x+y'
        )
        return fig

def get_pie_plot(labels, values, plot_title):
        # Instantiate figure object
        fig = go.Figure()
        # Add trace to figure object containing scatter plot
        fig.add_trace(go.Pie(
                labels= labels,
                values= values,
                opacity = figure_settings.OPACITY.value
        ))
        # Select background colors and modify axis attributes.
        fig.update_layout(paper_bgcolor= figure_settings.BACKGROUND.value, 
                        plot_bgcolor= figure_settings.BACKGROUND.value,
                        font={
                            'color': figure_settings.TEXT_COLOR.value,
                            'family':figure_settings.TEXT_FONT.value,
                            'size': figure_settings.TEXT_SIZE.value
                        },
                        title= {
                            'text': plot_title,
                            'x': figure_settings.TITLE_POSITION.value
                            },
                        title_font= {
                            'size': figure_settings.TITLE_TEXT_SIZE.value,
                            'color': figure_settings.TEXT_COLOR.value,
                            'family': figure_settings.TEXT_FONT.value
                        },
                        title_pad= {
                            't': 10
                        },
                        hoverlabel= dict(
                            bgcolor= figure_settings.HOVER_LABEL_BG_COLOR.value,
                            bordercolor= figure_settings.HOVER_LABEL_BORDER_COLOR.value,
                            font = dict(family= figure_settings.TEXT_FONT.value, color= figure_settings.TEXT_COLOR.value)
                        )
        )
        fig.update_traces(
            marker= dict(
                colors = [figure_settings.MARKER_COLOR.value, figure_settings.BORDER_COLOR.value, figure_settings.HOVER_LABEL_BG_COLOR.value]
            )
        )
        return fig

def get_line_plot(df, x, y, yaxis_title, xaxis_title, plot_title, hover_label_text, flag_legend = True):
        """_summary_

        Args:
            df (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
            yaxis_title (_type_): _description_
            xaxis_title (_type_): _description_
            plot_title (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Instantiate figure object
        fig = go.Figure()
        # Add trace to figure object containing scatter plot
        fig.add_trace(go.Line(
                x= df[x],
                y= df[y],
                showlegend= flag_legend,
                name = y

        ))
        # Select background colors and modify axis attributes.
        fig.update_layout(paper_bgcolor= figure_settings.BACKGROUND.value, 
                        plot_bgcolor= figure_settings.BACKGROUND.value,
                        xaxis_title= xaxis_title,
                        yaxis_title= yaxis_title,
                        font={
                            'color': figure_settings.TEXT_COLOR.value,
                            'family':figure_settings.TEXT_FONT.value,
                            'size': figure_settings.TEXT_SIZE.value
                        },
                        title= {
                            'text': plot_title,
                            'x': figure_settings.TITLE_POSITION.value
                            },
                        title_font= {
                            'size': figure_settings.TITLE_TEXT_SIZE.value,
                            'color': figure_settings.TEXT_COLOR.value,
                            'family': figure_settings.TEXT_FONT.value
                        },
                        title_pad= {
                            't': 10
                        },
                        hoverlabel= dict(
                            bgcolor= figure_settings.HOVER_LABEL_BG_COLOR.value,
                            bordercolor= figure_settings.HOVER_LABEL_BORDER_COLOR.value,
                            font = dict(family= figure_settings.TEXT_FONT.value, color= figure_settings.TEXT_COLOR.value)
                        )
                        )
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor= figure_settings.Y_GRID_COLOR.value)
        fig.update_xaxes(showline=True, linewidth=1, linecolor=figure_settings.TEXT_COLOR.value, showgrid=False)
        fig.update_traces(
            mode= 'lines',
            line= dict(width= 2),
            line_color= figure_settings.MARKER_COLOR.value,
            opacity= figure_settings.OPACITY.value,
            text = hover_label_text,
            hoveron= 'points',
            hoverinfo= 'text+x+y'
        )
        return fig
# -----------------------------------------------------------------------------------
# SUMMARY LAYOUT
# -----------------------------------------------------------------------------------
# Set up initial key from Alpha Vantage
key = 'GT2GC7QRH5M73XCF'
# Instantiate TimeSeries class and select output data type.
ts = TimeSeries(key, output_format='pandas')

def get_summary_body() -> list:
    body = [
        dcc.Interval(
            id='my_interval',
            n_intervals=0,       # number of times the interval was activated
            interval=120*1000,   # update every 2 minutes
        ),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='tesla-stock')
            ], width= 10)
        ], justify= 'center'),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P(id="target-price", style={'color': 'white', 'fontSize': 14}, className='mt-3')
                    ])
                ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
            ], width= 5),
            dbc.Col([
                 dbc.Card([
                     dbc.CardBody([
                        html.P(id="stock-movement", style={'color': 'white', 'fontSize': 14}, className='mt-0')
                     ])
                 ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
            ], width= 5)
        ], justify= 'center')
    ]
    return body

summary_layout = get_layout(get_summary_body())

# -----------------------------------------------------------------------------------
# FUNDAMENTALS LAYOUT
# -----------------------------------------------------------------------------------
def get_fundamentals_body() -> list:
    body = [
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='freq-dropdown',options=['QoQ', 'TTM'], value='QoQ', placeholder='Select timescale...', className= 'button-dropdown mb-2')
            ], width= 2),
            dbc.Col([], width=8),
            dbc.Col([
                dcc.Dropdown(id='fund-metric', options=['Revenue', 'Gross Profit', 'Income from Operations', 'Net Income', 'Adj EBITDA', 'FcF'], value='Revenue', placeholder='Select metric...', className= 'button-dropdown mb-2')
            ], width=2)
        ], justify='end'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='fund-bar')
            ], width=10)
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='margin-metric', options=['Gross Profit Margin', 'Operating Income Margin', 'Net Income Margin', 'Adj EBITDA Margin'], value='Gross Profit Margin', placeholder='Select margin...', className= 'button-dropdown mb-2 mt-2')
            ], width=2)
        ], justify='end'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='margin-line')
            ], width=10)
        ], justify='center')
    ]
    return body

fundamentals_layout = get_layout(get_fundamentals_body())

# -----------------------------------------------------------------------------------
# LIQUIDITY&SOLVENCY LAYOUT
# -----------------------------------------------------------------------------------
def get_liq_solvency_body() -> list:
    body = [
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='liq-ratio', options=['Current Ratio', 'Quick Ratio', 'Debt to Equity Ratio', 'Debt to Assets Ratio', 'Equity Ratio'], value='Current Ratio', placeholder='Select ratio...', className= 'button-dropdown mb-2')
            ], width=2)
        ], justify='end'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='ratio-graph')
            ], width= 10)
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P(id="ratio-definition", style={'color': 'white', 'fontSize': 14}, className='mt-3')
                    ])
                ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)                
            ], width= 6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Link(id='ref-link', href='')
                    ])
                ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
            ], width= 4)
        ], justify= 'center')
    ]
    return body

liq_solvency_layout = get_layout(get_liq_solvency_body())

# -----------------------------------------------------------------------------------
# GROWTH METRICS LAYOUT
# -----------------------------------------------------------------------------------
def get_growth_body() -> list:
    body = [
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='freq-dropdown-2',options=['QoQ', 'YoY'], value='QoQ', placeholder='Select timescale...', className= 'button-dropdown mb-2')
            ], width= 2),
            dbc.Col([], width=8),
            dbc.Col([
                dcc.Dropdown(id='growth-metric', options=['Revenue Growth', 'Gross Profit Growth', 'Income from Operations Growth', 'Net Income Growth', 'Adj EBITDA Growth', 'FcF Growth'], value='Revenue Growth', placeholder='Select metric...', className= 'button-dropdown mb-2')
            ], width=2)
        ], justify='end'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='growth-graph')
            ], width=10)
        ], justify='center')
    ]
    return body

growth_metrics_layout = get_layout(get_growth_body())

# -----------------------------------------------------------------------------------
# PERFORMANCE LAYOUT
# -----------------------------------------------------------------------------------
def get_performance_body() -> list:
    body = [
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='freq-dropdown-3',options=['QoQ', 'TTM'], value='QoQ', placeholder='Select timescale...', className= 'button-dropdown mb-2')
            ], width= 2),
            dbc.Col([], width=8),
            dbc.Col([
                dcc.Dropdown(id='perf-metric', options=['Invested Capital', 'Total Assets', 'ROE', 'ROA', 'Operating ROIC', 'FcF ROIC', 'WACC'], value='Invested Capital', placeholder='Select metric...', className= 'button-dropdown mb-2')
            ], width=2)
        ], justify='end'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='perf-graph')
            ], width=10)
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P(id="perf-definition", style={'color': 'white', 'fontSize': 14}, className='mt-1')
                    ])                    
                ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P(id="perf-formula", style={'color': 'white', 'fontSize': 14}, className='mt-1')                       
                    ])
                ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
            ], width= 3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.CardLink([html.P(id= 'link-def', style={'color': 'white', 'fontSize': 14}, className='mt-1')], id='perf-link')
                    ])

                ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
            ], width= 3)
        ], justify = 'center')
    ]
    return body

performance_metrics_layout = get_layout(get_performance_body())

# -----------------------------------------------------------------------------------
# EQUITY LAYOUT
# -----------------------------------------------------------------------------------
# Instantiate locally tesla class
tesla = TeslaFinancials()

# Get outstanding shares dict
data = tesla.get_outstanding_shares()
df = pd.DataFrame.from_dict(data).sort_index(ascending=False)

# Create scatter charts
fig = go.Figure()
fig = get_scatter_plot(df, 'date', 'WeightedAverageSharesBasic', 'Shares (in millions)', 'Quarter', '<b>Tesla · QoQ Revenue Growth<b>', 'SHBas', True, 'Types of shares')
fig.add_trace(go.Scatter(
                x= df['date'],
                y= df['WeightedAverageSharesDiluted'],
                name= 'WeightedAverageSharesDiluted',
                mode= 'lines',
                line= dict(width= figure_settings.LINE_WIDTH.value),
                line_color= figure_settings.HOVER_LABEL_BG_COLOR.value,
                fill='tonexty',
                fillcolor= figure_settings.HOVER_LABEL_BG_COLOR.value,
                opacity= figure_settings.OPACITY.value,
                text = 'SHDil',
                hoveron= 'points',
                hoverinfo= 'text+x+y'
        ))
        
# Create pie chart
# TODO: add data to ddbb. For now, random data as placeholder.
fig_pie = get_pie_plot(figure_settings.TYPES_SH.value, figure_settings.PERCENTAGE_SH.value, 'Institutional vs Retail vs Insider share distribution')


def equity_body() -> list:
    body = [
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id= 'pie-chart', figure= fig_pie)
                    ])
                ], justify= 'center'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.P('Tesla current credit rating is BBB'),
                                dbc.CardLink('See more in S&P Global Ratings', id='equity-link', href='https://disclosure.spglobal.com/ratings/es/regulatory/search-result', className='mt-1')
                            ])
                        ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
                    ])
                ], justify= 'center')
            ], width= 5),
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id='shares-graph', figure = fig)
                    ])
                ], justify= 'end'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                           # dbc.CardBody([
                            #    dash_table.DataTable(df_solar.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
                            #])
                        ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
                    ])
                ], justify= 'end')
            ], width= 7)
        ])
    ]
    return body

equity_layout = get_layout(equity_body())


# -----------------------------------------------------------------------------------
# PRICE FORECAST LAYOUT
# -----------------------------------------------------------------------------------
def price_forecast_body() -> list:
    body = [
        dbc.Row([
            dbc.Col([], width=10),
            dbc.Col([
                dcc.Dropdown(id='forecast-metric', options=['4 qtr rate FcF ROIC', '4qtr rate Invested Capital'], value='4 qtr rate FcF ROIC', placeholder='Select metric...', className= 'button-dropdown mb-2')
            ], width=2)
        ], justify='end'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='forecast-graph')
            ], width= 10)
        ], justify= 'center'),
        dbc.Row([
            dbc.Col([], width=10),
            dbc.Col([
                dcc.Dropdown(id='forecast-timescale', options=['QoQ', 'YoY'], value='QoQ', placeholder='Select timescale...', className= 'button-dropdown mt-2 mb-2')
            ], width=2)
        ], justify='end'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='forecast-bargraph')
            ], width= 10)
        ], justify= 'center'),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P('DISCLAIMER: The forecast is a simple predictive model based on a 4 quarter moving window of FcF and Invested capital rates of change. It considers how {} has increased its invested capital per quarter or annum as well as how free cash flow has compounded on top. As a conservative measure, free cash flow growth is capped at 40% (rate of growth equal to 0). The model does not factor in any cash outflows like dividends or share buybacks.'.format(dash.page_registry['pages.tesla']['name']), id="forecast-model", style={'color': 'white', 'fontSize': 14}, className='mt-1')                       
                    ])
                ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
            ], width= 7),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.P(['{} price target for 2030'.format(dash.page_registry['pages.tesla']['name'])], style={'color': 'white', 'fontSize': 14}, className='text-center mt-1 mb-0')
                    ),
                    html.Hr(),
                    dbc.CardBody([
                        html.P('{} $/share'.format('1820'), id='target-id', style={'color': 'white', 'fontSize': 20}, className='mt-1')
                    ]),
                    dbc.CardFooter(html.P(['* Number of weighted diluted outstanding shares: {}. Price multiple: {}.'.format('3.460.000.000', '35')], 
                                    style={'color': 'white', 'fontSize': 10}, className='text-center mt-1 mb-0'))
                ], class_name='mt-2 bg-secondary', color= 'dark', outline=True)
            ], width= 3)
        ], justify= 'center')

    ]

    return body

price_forecast_layout = get_layout(price_forecast_body())


# -----------------------------------------------------------------------------------
# TABS LAYOUT FOR TESLA
# -----------------------------------------------------------------------------------
layout = dbc.Tabs(
    [
        dbc.Tab(summary_layout, label="Summary"),
        dbc.Tab(fundamentals_layout, label="Fundamentals"),
        dbc.Tab(liq_solvency_layout, label="Liquidity&Solvency"),
        dbc.Tab(growth_metrics_layout, label="Growth Metrics"),
        dbc.Tab(performance_metrics_layout, label="Performance Metrics"),
        dbc.Tab(equity_layout, label="Equity Structure"),
        dbc.Tab(price_forecast_layout, label="Price Forecast"),
    ],
    class_name='ms-5 me-5 center-screen-tabs'
)


# -----------------------------------------------------------------------------------
# CALLBACKS
# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# Instantiate data class
# -----------------------------------------------------------------------------------
tesla = TeslaFinancials()

#-----------------------------------------------------------------------------
# SUMMARY CALLBACKS
# -----------------------------------------------------------------------------------
@callback(
    Output(component_id='tesla-stock', component_property='figure'),
    [Input(component_id='my_interval', component_property='n_intervals')]
)
def update_graph(n):
    """ Pull financial data from Alpha Vantage and update graph every 2 minutes

    Args:
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Retreive data from Alpha Vantage API
    ttm_data, ttm_meta_data = ts.get_intraday(symbol='TSLA',interval='15min',outputsize='compact')
    df = ttm_data.copy()
    df=df.transpose()
    df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
                     "4. close":"close","5. volume":"volume"},inplace=True)
    df=df.reset_index().rename(columns={'index': 'indicator'})
    df = pd.melt(df,id_vars=['indicator'],var_name='date',value_name='rate')
    df = df[df['indicator']!='volume']

    # Plot line graph
    fig = get_line_plot(df, 'date', 'rate', 'Share value ($)', 'hour', '<b>"Symbol: ${}"<b>'.format(ttm_meta_data['2. Symbol']), '$TSLA')
    return fig

@callback([
    Output(component_id='target-price', component_property='children'),
    Output(component_id='stock-movement', component_property='children')],
    [Input(component_id='my_interval', component_property='n_intervals')]
)
def update_footer(n):
    """Pull financial data from Alpha Vantage and update graph every 2 minutes"""
    ttm_data, ttm_meta_data = ts.get_intraday(symbol='TSLA',interval='1min',outputsize='compact')
    df = ttm_data.copy()
    df=df.transpose()
    df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
                     "4. close":"close","5. volume":"volume"},inplace=True)
    df=df.reset_index().rename(columns={'index': 'indicator'})
    df = pd.melt(df,id_vars=['indicator'],var_name='date',value_name='rate')
    return ["Stock price at close on {}: {}".format(df['date'].iloc[0], df.loc[df['indicator'] == 'close', 'rate'].iloc[0])], ["Open at {}. High price in period: {}. Low price in period: {}".format(df.loc[df['indicator'] == 'open', 'rate'].iloc[0], df.loc[df['indicator'] == 'high', 'rate'].iloc[0], df.loc[df['indicator'] == 'low', 'rate'].iloc[0])]

#-----------------------------------------------------------------------------
# FUNDAMENTALS CALLBACKS
# -----------------------------------------------------------------------------------
@callback(
    Output('fund-bar', 'figure'),
    [Input('freq-dropdown', 'value'),
    Input('fund-metric', 'value')]
)
def update_fund_graph(input_1, input_2):

    if input_1 == 'QoQ' and input_2 == 'Revenue':
        data = tesla.get_revenue(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'TotalRevenues', 'Revenue (m$)', 'Quarter', '<b>Tesla · Revenue<b>')

    elif input_1 == 'QoQ' and input_2 == 'Gross Profit':
        data = tesla.get_gross_profit(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'GrossProfit', 'Gross Profit (m$)', 'Quarter', '<b>Tesla · Gross Profit<b>')

    elif input_1 == 'QoQ' and input_2 == 'Income from Operations':
        data = tesla.get_income_ops(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'IncomeFromOperations', 'Income Ops (m$)', 'Quarter', '<b>Tesla · Income Operations<b>')

    elif input_1 == 'QoQ' and input_2 == 'Net Income':
        data = tesla.get_net_income(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'NetIncome', 'Net Income (m$)', 'Quarter', '<b>Tesla · Net Income<b>')
        
    elif input_1 == 'QoQ' and input_2 == 'Adj EBITDA':
        data = tesla.get_adj_ebitda(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'AdjustedEBITDA', 'Adj EBITDA (m$)', 'Quarter', '<b>Tesla · Adj EBITDA<b>')
        
    elif input_1 == 'QoQ' and input_2 == 'FcF':
        data = tesla.get_fcf(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'FcF', 'FCF (m$)', 'Quarter', '<b>Tesla · FCF<b>')
        
    elif input_1 == 'TTM' and input_2 == 'Revenue':
        data = tesla.get_revenue(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'TTMTotalRevenues', 'TTM Revenue (m$)', 'Quarter', '<b>Tesla · TTM Revenue<b>')

    elif input_1 == 'TTM' and input_2 == 'Gross Profit':
        data = tesla.get_gross_profit(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'TTMGrossProfit', 'TTM Gross Profit (m$)', 'Quarter', '<b>Tesla · TTM Gross Profit<b>')

    elif input_1 == 'TTM' and input_2 == 'Income from Operations':
        data = tesla.get_income_ops(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'TTMIncomeFromOperations', 'TTM Income Ops (m$)', 'Quarter', '<b>Tesla · TTM Income Operations<b>')
        
    elif input_1 == 'TTM' and input_2 == 'Net Income':
        data = tesla.get_net_income(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'TTMNetIncome', 'TTMNetIncome (m$)', 'Quarter', '<b>Tesla · TTM Net Income<b>')
        
    elif input_1 == 'TTM' and input_2 == 'Adj EBITDA':
        data = tesla.get_adj_ebitda(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'TTMAdjustedEBITDA', 'TTMAdjEBITDA (m$)', 'Quarter', '<b>Tesla · TTM Adjusted EBITDA<b>')
        
    else:
        data = tesla.get_fcf(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'TTMFcF', 'TTM FCF (m$)', 'Quarter', '<b>Tesla · TTM FCF<b>')
    return fig

@callback(
    Output('margin-line', 'figure'),
    [Input('freq-dropdown', 'value'),
    Input('margin-metric', 'value')]
)
def update_fund_margin_graph(input_1, input_2):

    if input_1 == 'QoQ' and input_2 == 'Gross Profit Margin':
        data = tesla.get_gross_profit_margin(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioGrossProfit/TotalRevenues', 'Gross profit margin (%)', 'Quarter', '<b>Tesla · Gross Profit Margin<b>', '%GM')

    elif input_1 == 'QoQ' and input_2 == 'Operating Income Margin':
        data = tesla.get_income_ops_margin(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioIncomeFromOperations/TotalRevenues', 'Income ops margin (%)', 'Quarter', '<b>Tesla · Income Operations Margin<b>', '%IOps')

    elif input_1 == 'QoQ' and input_2 == 'Net Income Margin':
        data = tesla.get_net_income_margin(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioNetIncome/TotalRevenues', 'Net Income margin (%)', 'Quarter', '<b>Tesla · Net Income Margin<b>', '%NI')

    elif input_1 == 'QoQ' and input_2 == 'Adj EBITDA Margin':
        data = tesla.get_adj_ebitda_margin(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioAdjustedEBITDA/TotalRevenues', 'Adj EBITDA margin (%)', 'Quarter', '<b>Tesla · Adjusted EBITDA Margin<b>', '%AEBITDA')

    elif input_1 == 'TTM' and input_2 == 'Gross Profit Margin':
        data = tesla.get_gross_profit_margin(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioTTMGrossProfit/TTMTotalRevenues', 'TTM Gross profit margin (%)', 'Quarter', '<b>Tesla · TTM Gross Profit Margin<b>', '%TTMGM')

    elif input_1 == 'TTM' and input_2 == 'Operating Income Margin':
        data = tesla.get_income_ops_margin(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioTTMIncomeFromOperations/TTMTotalRevenues', 'TTM Income ops margin (%)', 'Quarter', '<b>Tesla · TTM Income Operations Margin<b>', '%TTMIOps')

    elif input_1 == 'TTM' and input_2 == 'Net Income Margin':
        data = tesla.get_net_income_margin(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioTTMNetIncome/TTMTotalRevenues', 'TTM Net Income margin (%)', 'Quarter', '<b>Tesla · TTM Net Income Margin<b>', '%TTMNI')

    else:
        data = tesla.get_adj_ebitda_margin(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioTTMAdjustedEBITDA/TTMTotalRevenues', 'TTM Adj EBITDA margin (%)', 'Quarter', '<b>Tesla · TTM Adjusted EBITDA Margin<b>', '%TTMAEBITDA')

    return fig


#-----------------------------------------------------------------------------
# LIQUIDITY&SOLVENCY CALLBACKS
# -----------------------------------------------------------------------------------
@callback(
    Output('ratio-graph', 'figure'),
    Input('liq-ratio', 'value')
)
def update_ratio_graph(input):

    if input == 'Current Ratio':
        data = tesla.get_current_ratio()
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioTotalCurrentAssets/TotalCurrentLiabilities', 'Current Ratio', 'Quarter', '<b>Tesla · Current Ratio<b>', 'CR')

    elif input == 'Quick Ratio':
        data = tesla.get_quick_ratio()
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'QuickRatio', 'Quick Ratio', 'Quarter', '<b>Tesla · Quick Ratio<b>', 'QR')

    elif input == 'Debt to Equity Ratio':
        fig = ''

    elif input == 'Debt to Assets Ratio':
        fig = ''
    else:
        data = tesla.get_equity_ratio()
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RatioTotalStockholdersEquity/TotalAssets', 'Equity Ratio', 'Quarter', '<b>Tesla · Equity Ratio<b>', 'ER')

    return fig

@callback(
    [Output('ref-link', 'children'),
    Output('ref-link', 'href'),
    Output('ratio-definition', 'children')],
    Input('liq-ratio', 'value')
)
def update_footer(input):
    if input == 'Current Ratio':
        children = ['The current ratio is a liquidity ratio that measures a company’s ability to pay short-term obligations or those due within one year.'
                    'It tells investors and analysts how a company can maximize the current assets on its balance sheet to satisfy its current debt and other payables.']
        href = 'https://www.investopedia.com/terms/c/currentratio.asp'
        children_link = 'See more about {} here'.format(input)
    elif input == 'Quick Ratio':
        children = ['The quick ratio is an indicator of a company’s short-term liquidity position and measures a company’s ability to meet its short-term obligations with its most liquid assets.' 
                    'Since it indicates the company’s ability to instantly use its near-cash assets (assets that can be converted quickly to cash) to pay down its current liabilities,'
                    ' it is also called the acid test ratio. An "acid test" is a slang term for a quick test designed to produce instant results.']
        href = 'https://www.investopedia.com/terms/q/quickratio.asp'
        children_link = 'See more about {} here'.format(input)
    elif input == 'Debt to Equity Ratio':
        children = ['The debt-to-equity ratio, or D/E ratio, is a leverage ratio that measures how much debt a company is using by comparing its total liabilities to its shareholder equity. The D/E ratio can be used to assess the amount of risk currently embedded in a companys capital structure.'
                    'The debt-to-equity ratio reveals how much of a companys capital structure is comprised of debts, in relation to equity. An investor, company stakeholder, or potential lender may compare a companys debt-to-equity ratio to historical levels or those of peers.']
        href = 'https://seekingalpha.com/article/4460099-debt-to-equity-ratio?gclid=Cj0KCQiAg_KbBhDLARIsANx7wAzDTvOleHkgpO5dYMVOVqG35murDGiBqVy59nfCvZSSmoZz4P2jb8waAlQIEALw_wcB&internal_promotion=true&utm_campaign=16160107183&utm_medium=cpc&utm_source=google&utm_term=138882502731%5Eaud-1455154863260%3Adsa-1485125208378%5E%5E581249221566%5E%5E%5Eg'
        children_link = 'See more about {} here'.format(input)
    elif input == 'Debt to Assets Ratio':
        children = ['Total-debt-to-total-assets is a leverage ratio that defines the total amount of debt relative to assets owned by a company. Using this metric, analysts can compare one companys leverage with that of other companies in the same industry.' 
                    'This information can reflect how financially stable a company is. The higher the ratio, the higher the degree of leverage (DoL) and, consequently, the higher the risk of investing in that company.']
        href = 'https://www.investopedia.com/terms/t/totaldebttototalassets.asp'
        children_link = 'See more about {} here'.format(input)
    else:
        children = ['The shareholder equity ratio indicates how much of a companys assets have been generated by issuing equity shares rather than by taking on debt. The lower the ratio result, the more debt a company has used to pay for its assets.' 
                    'It also shows how much shareholders might receive in the event that the company is forced into liquidation.']
        href = 'https://www.investopedia.com/terms/s/shareholderequityratio.asp'
        children_link = 'See more about {} here'.format(input)
    return children_link, href, children


#-----------------------------------------------------------------------------
# GROWTH METRICS CALLBACKS
# -----------------------------------------------------------------------------------
@callback(
    Output('growth-graph', 'figure'),
    [Input('freq-dropdown-2', 'value'),
    Input('growth-metric', 'value')]
)
def update_growth_chart(input_1, input_2):

    # 'Revenue Growth', 'Gross Profit Growth', 'Income from Operations Growth', 'Net Income Growth', 'Adj EBITDA Growth', 'EPS Growth', 'FcF Growth'
    if input_1 == 'QoQ' and input_2 == 'Revenue Growth':
        data = tesla.get_revenue_growth(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'GrowthRatio', 'Revenue Growth (%)', 'Quarter', '<b>Tesla · QoQ Revenue Growth<b>', '%RG')
        
    elif input_1 == 'QoQ' and input_2 == 'Gross Profit Growth':
        data = tesla.get_gross_profit_growth(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'GrowthRatio', 'Gross Profit Growth (%)', 'Quarter', '<b>Tesla · QoQ Gross Profit Growth<b>', '%GPG')
        
    elif input_1 == 'QoQ' and input_2 == 'Income from Operations Growth':
        data = tesla.get_income_ops_growth(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'GrowthRatio', 'Income Ops Growth (%)', 'Quarter', '<b>Tesla · QoQ Income Operations Growth<b>', '%IOG')
        
    elif input_1 == 'QoQ' and input_2 == 'Net Income Growth':
        data = tesla.get_net_income_growth(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'GrowthRatio', 'Net Income Growth', 'Quarter', '<b>Tesla · QoQ Net Income Growth<b>', '%NIG')
        
    elif input_1 == 'QoQ' and input_2 == 'Adj EBITDA Growth':
        data = tesla.get_adj_ebitda_growth(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'GrowthRatio', 'Adj EBITDA Growth', 'Quarter', '<b>Tesla · QoQ Adjusted EBITDA Growth<b>', '%AEG')
        
    elif input_1 == 'QoQ' and input_2 == 'FcF Growth':
        data = tesla.get_fcf_growth(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'GrowthRatio', 'FCF Growth', 'Quarter', '<b>Tesla · QoQ FCF Growth<b>', '%FCFG')
        
    elif input_1 == 'YoY' and input_2 == 'Revenue Growth':
        data = tesla.get_revenue_growth(timescale= 'YoY')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'Year', 'GrowthRatio', 'Revenue Growth', 'Quarter', '<b>Tesla · YoY Revenue Growth<b>', '%RG')
        
    elif input_1 == 'YoY' and input_2 == 'Gross Profit Growth':
        data = tesla.get_gross_profit_growth(timescale= 'YoY')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'Year', 'GrowthRatio', 'Gross Profit Growth (%)', 'Quarter', '<b>Tesla · YoY Gross Profit Growth<b>', '%GPG')
        
    elif input_1 == 'YoY' and input_2 == 'Income from Operations Growth':
        data = tesla.get_income_ops_growth(timescale= 'YoY')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'Year', 'GrowthRatio', 'Income Ops Growth (%)', 'Quarter', '<b>Tesla · YoY Income Operations Growth<b>', '%IOG')
        
    elif input_1 == 'YoY' and input_2 == 'Net Income Growth':
        data = tesla.get_net_income_growth(timescale= 'YoY')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'Year', 'GrowthRatio', 'Net Income Growth', 'Quarter', '<b>Tesla · YoY Net Income Growth<b>', '%NIG')
        
    elif input_1 == 'YoY' and input_2 == 'Adj EBITDA Growth':
        data = tesla.get_adj_ebitda_growth(timescale= 'YoY')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'Year', 'GrowthRatio', 'Adj EBITDA Growth', 'Quarter', '<b>Tesla · YoY Adjusted EBITDA Growth<b>', '%AEG')
        
    else:
        data = tesla.get_fcf_growth(timescale= 'YoY')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'Year', 'GrowthRatio', 'FCF Growth', 'Quarter', '<b>Tesla · YoY FCF Growth<b>', '%FCFG')
        
    return fig


#------------------------------------------------------------------------------------
# PERFORMANCE METRICS CALLBACKS
# -----------------------------------------------------------------------------------
@callback(
    Output('perf-graph', 'figure'),
    [Input('freq-dropdown-3', 'value'),
    Input('perf-metric', 'value')]
)
def update_perf_graph(input_1, input_2):
    if input_1 == 'QoQ' and input_2 == 'Invested Capital':
        data = tesla.get_invested_capital(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'InvestedCapital', 'Invested Capital (m$)', 'Quarter', '<b>Tesla · Invested Capital<b>')
        
    elif input_1 == 'QoQ' and input_2 == 'Total Assets':
        data = tesla.get_total_assets(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'TotalAssets', 'Total Assets (m$)', 'Quarter', '<b>Tesla · Total Assets<b>')
        
    elif input_1 == 'QoQ' and input_2 == 'ROE':
        data = tesla.get_return_on_equity(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'RatioNetIncome/TotalStockholdersEquity', 'ROE (%)', 'Quarter', '<b>Tesla · ROE<b>')
        
    elif input_1 == 'QoQ' and input_2 == 'ROA':
        data = tesla.get_return_on_assets(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'RatioNetIncome/TotalAssets', 'ROA (%)', 'Quarter', '<b>Tesla · ROA<b>')
        
    elif input_1 == 'QoQ' and input_2 == 'Operating ROIC':
        data = tesla.get_nopat_roic(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'RatioNOPAT/InvestedCapital', 'NOPAT ROIC (%)', 'Quarter', '<b>Tesla · Quarter NOPAT ROIC<b>')
        
    elif input_1 == 'QoQ' and input_2 == 'FcF ROIC':
        data = tesla.get_fcf_roic(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'RatioFcF/InvestedCapital', 'FcF ROIC (%)', 'Quarter', '<b>Tesla · Quarter FcF ROIC<b>')
        
    elif input_1 == 'QoQ' and input_2 == 'WACC':
        fig = ''
        
    elif input_1 == 'TTM' and input_2 == 'Invested Capital':
        data = tesla.get_invested_capital(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'InvestedCapital', 'TTM Invested Capital (m$)', 'Quarter', '<b>Tesla · TTM Invested Capital<b>')
        
    elif input_1 == 'TTM' and input_2 == 'Total Assets':
        data = tesla.get_total_assets(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'TTMTotalAssets', 'TTM Total Assets (m$)', 'Quarter', '<b>Tesla · TTM Total Assets<b>')
        
    elif input_1 == 'TTM' and input_2 == 'ROE':
        data = tesla.get_return_on_equity(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'RatioTTMNetIncome/TTMTotalStockholdersEquity', 'TTM ROE (%)', 'Quarter', '<b>Tesla · TTM ROE<b>')
        
    elif input_1 == 'TTM' and input_2 == 'ROA':
        data = tesla.get_return_on_assets(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'RatioTTMNetIncome/TTMTotalAssets', 'TTM ROA (%)', 'Quarter', '<b>Tesla · TTM ROA<b>')
        
    elif input_1 == 'TTM' and input_2 == 'Operating ROIC':
        data = tesla.get_nopat_roic(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'RatioNOPAT/InvestedCapital', 'TTM NOPAT ROIC (%)', 'Quarter', '<b>Tesla · TTM NOPAT ROIC<b>')
        
    elif input_1 == 'TTM' and input_2 == 'FcF ROIC':
        data = tesla.get_fcf_roic(timescale= 'TTM')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_bar_plot(df, 'date', 'RatioFcF/InvestedCapital', 'TTM FcF ROIC (%)', 'Quarter', '<b>Tesla · TTM FcF ROIC<b>')
        
    else:
        fig = ''
    return fig

@callback(
    [Output('perf-definition', 'children'),
    Output('perf-formula', 'children'),
    Output('perf-link', 'href'),
    Output('link-def', 'children')],
    Input('perf-metric', 'value')
)
def update_footer_perf(input):
    children_link = 'See more about {} here'.format(input)
    if input == 'Invested Capital':
        children_def = ['Invested capital is the total amount of money raised by a company by issuing securities to equity shareholders and debt to bondholders, where the total debt and capital lease obligations are added to the amount of equity issued to investors. Invested capital is not a line item in the companys financial statement because debt, capital leases, and stockholder’s equity are each listed separately in the balance sheet.']
        children_formula = ['Aquí va una imagen de la fórmula']
        href = 'https://www.investopedia.com/terms/i/invested-capital.asp#:~:text=Invested%20capital%20is%20the%20total,of%20equity%20issued%20to%20investors.'
        children_link = children_link
    elif input == 'Total Assets':
        children_def = ['Total assets refers to the total amount of assets owned by a person or entity. Assets are items of economic value, which are expended over time to yield a benefit for the owner. If the owner is a business, these assets are usually recorded in the accounting records and appear in the balance sheet of the business. Typical categories in which these assets may be found include cash, marketable securities, accounts receivable, prepaid expenses, inventory, fixed assets, intangible assets, goodwill, and other assets.']
        children_formula = ['Aquí va una imagen de la fórmula']
        href = 'https://www.accountingtools.com/articles/total-assets#:~:text=Total%20assets%20refers%20to%20the,balance%20sheet%20of%20the%20business.'
        children_link = children_link
    elif input == 'ROE':
        children_def = ['Return on equity (ROE) is a ratio that provides investors with insight into how efficiently a company (or more specifically, its management team) is handling the money that shareholders have contributed to it. In other words, return on equity measures the profitability of a corporation in relation to stockholders’ equity. The higher the ROE, the more efficient a companys management is at generating income and growth from its equity financing. ']
        children_formula = ['Aquí va una imagen de la fórmula']
        href = 'https://www.investopedia.com/ask/answers/070914/how-do-you-calculate-return-equity-roe.asp'
        children_link = children_link
    elif input == 'ROA':
        children_def = ['The term return on assets (ROA) refers to a financial ratio that indicates how profitable a company is in relation to its total assets. Corporate management, analysts, and investors can use ROA to determine how efficiently a company uses its assets to generate a profit.'
                        'The metric is commonly expressed as a percentage by using a companys net income and its average assets. A higher ROA means a company is more efficient and productive at managing its balance sheet to generate profits while a lower ROA indicates there is room for improvement.']
        children_formula = ['Aquí va una imagen de la fórmula']
        href = 'https://www.investopedia.com/terms/r/returnonassets.asp'
        children_link = children_link
    elif input == 'Operating ROIC':
        children_def = ['Operating return on invested capital (ROIC) is a calculation used to assess a companys efficiency in allocating capital to profitable investments. The ROIC formula involves dividing net operating profit after tax (NOPAT) by invested capital.'
                        'ROIC gives a sense of how well a company is using its capital to generate profits. Comparing a companys ROIC with its weighted average cost of capital (WAAC) reveals whether invested capital is being used effectively.']
        children_formula = ['Aquí va una imagen de la fórmula']
        href = 'https://www.investopedia.com/terms/r/returnoninvestmentcapital.asp#:~:text=Return%20on%20invested%20capital%20(ROIC)%20is%20a%20calculation%20used%20to,its%20capital%20to%20generate%20profits.'
        children_link = children_link
    elif input == 'FcF ROIC':
        children_def = ['FcF return on invested capital (ROIC) is a calculation used to assess a companys efficiency in allocating capital to profitable investments. The ROIC formula involves dividing free cash flow  by invested capital.'
                        'ROIC gives a sense of how well a company is using its capital to generate profits. Comparing a companys ROIC with its weighted average cost of capital (WAAC) reveals whether invested capital is being used effectively.']
        children_formula = ['Aquí va una imagen de la fórmula']
        href = 'https://www.investopedia.com/terms/r/returnoninvestmentcapital.asp#:~:text=Return%20on%20invested%20capital%20(ROIC)%20is%20a%20calculation%20used%20to,its%20capital%20to%20generate%20profits.'
        children_link = children_link
    else:
        children_def = ['Weighted average cost of capital (WACC) represents a firm’s average after-tax cost of capital from all sources, including common stock, preferred stock, bonds, and other forms of debt. WACC is the average rate that a company expects to pay to finance its assets.'
                        'WACC is a common way to determine required rate of return (RRR) because it expresses, in a single number, the return that both bondholders and shareholders demand to provide the company with capital. A firm’s WACC is likely to be higher if its stock is relatively volatile or if its debt is seen as risky because investors will require greater returns.']
        children_formula = ['Aquí va una imagen de la fórmula']
        href = 'https://www.investopedia.com/terms/w/wacc.asp'
        children_link = children_link

    return children_def, children_formula, href, children_link


#------------------------------------------------------------------------------------
# PRICE FORECAST CALLBACKS
# -----------------------------------------------------------------------------------
@callback(
    Output('forecast-graph', 'figure'),
    Input('forecast-metric', 'value')
)
def update_forecast_upper_graph(input):
    if input == '4 qtr rate FcF ROIC':
        data = tesla._get_rate_fcf_roic(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RateTTM', 'TTM Rate (%)', 'Quarter', '<b>Tesla · TTM Rate of change of FcF ROIC<b>', '%TTMRateFcF')
        
    else:
        data = tesla._get_rate_invested_capital(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=False)
        fig = get_scatter_plot(df, 'date', 'RateTTM', 'TTM Rate (%)', 'Quarter', '<b>Tesla · TTM Rate of change of Invested Capital<b>', '%TTMRateFcF')
        
    return fig

@callback(
    Output('forecast-bargraph', 'figure'),
    Input('forecast-timescale', 'value')
)
def update_forecast_bottom_graph(input):
    if input == 'QoQ':
        data = tesla.projected_fcf(timescale= 'QoQ')
        df = pd.DataFrame.from_dict(data).sort_index(ascending=True)
        fig = get_bar_plot(df, 'Quarter', 'FcFProjected', 'FCF (m$)', 'Quarter', '<b>Tesla · Projected Quarterly FcF (Non Adj.)<b>')

    else:
        fig = ''
    return fig