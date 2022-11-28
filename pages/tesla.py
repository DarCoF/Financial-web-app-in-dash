import pandas as pd
import plotly
import plotly.express as px

import dash
from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.exceptions import PreventUpdate
from pages.tabs import layout_tabs as lt

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
                dcc.Dropdown(id='freq-dropdown',options=['QoQ', 'TTM'], value='QoQ', placeholder='Select timescale...', className= 'mb-2')
            ], width= 2),
            dbc.Col([], width=8),
            dbc.Col([
                dcc.Dropdown(id='fund-metric', options=['Revenue', 'Gross Profit', 'Income from Operations', 'Net Income', 'Adj EBITDA', 'FcF'], value='Revenue', placeholder='Select metric...', className= 'mb-2')
            ], width=2)
        ], justify='end'),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='fund-bar')
            ], width=10)
        ], justify='center'),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='margin-metric', options=['Gross Profit Margin', 'Operating Income Margin', 'Net Income Margin', 'Adj EBITDA Margin'], value='Gross Profit Margin', placeholder='Select margin...', className= 'mb-2 mt-2')
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
                dcc.Dropdown(id='liq-ratio', options=['Current Ratio', 'Quick Ratio', 'Debt to Equity Ratio', 'Debt to Assets Ratio', 'Equity Ratio'], value='Current Ratio', placeholder='Select ratio...', className= 'mb-2')
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
                dcc.Dropdown(id='freq-dropdown-2',options=['QoQ', 'YoY'], value='QoQ', placeholder='Select timescale...', className= 'mb-2')
            ], width= 2),
            dbc.Col([], width=8),
            dbc.Col([
                dcc.Dropdown(id='growth-metric', options=['Revenue Growth', 'Gross Profit Growth', 'Income from Operations Growth', 'Net Income Growth', 'Adj EBITDA Growth', 'EPS Growth', 'FcF Growth'], value='Revenue', placeholder='Select metric...', className= 'mb-2')
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
                dcc.Dropdown(id='freq-dropdown-3',options=['YoY', 'TTM'], value='YoY', placeholder='Select timescale...', className= 'mb-2')
            ], width= 2),
            dbc.Col([], width=8),
            dbc.Col([
                dcc.Dropdown(id='perf-metric', options=['Invested Capital', 'Total Assets', 'ROE', 'ROA', 'Operating ROIC', 'FcF ROIC', 'WACC'], value='Invested Capital', placeholder='Select metric...', className= 'mb-2')
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
df = pd.read_csv("docs/Caste.csv")
df = df[df['state_name']=='Maharashtra']
df = df.groupby(['year','gender',], as_index=False)[['detenues','under_trial','convicts','others']].sum()
fig = px.pie(
        data_frame=df,
        names="gender",
        values="convicts",
        color="gender",               # differentiate color of marks
        opacity=0.9,                  # set opacity of markers (from 0 to 1)
        labels={"convicts":"Convicts in Maharashtra",
                "gender":"Gender"},           # map the labels of the figure
        title='Indian Prison Statistics', # figure title
        template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        )

df_solar = pd.read_csv('docs/solar.csv')

def equity_body() -> list:
    body = [
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id= 'pie-chart', figure= fig)
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
                        dcc.Graph(id='shares-graph')
                    ])
                ], justify= 'end'),
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dash_table.DataTable(df_solar.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
                            ])
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
                dcc.Dropdown(id='forecast-metric', options=['4 qtr rate FcF ROIC', '4qtr rate Invested Capital'], value='4 qtr rate FcF ROIC', placeholder='Select metric...', className= 'mb-2')
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
                dcc.Dropdown(id='forecast-timescale', options=['QoQ', 'YoY'], value='QoQ', placeholder='Select timescale...', className= 'mt-2 mb-2')
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
                        html.P(['{} price target for 2030'.format(dash.page_registry['pages.tesla']['name'])], style={'color': 'white', 'fontSize': 18}, className='text-center mt-1 mb-0')
                    ),
                    html.Hr(),
                    dbc.CardBody([
                        html.P('{} $/share'.format('PLACEHOLDER PRICE/SHARE'), id='target-id', style={'color': 'white', 'fontSize': 14}, className='mt-1')
                    ]),
                    dbc.CardFooter(html.P(['* Number of shares outstanding equal to {}. Multiple considered to arrive at estimated share price equal to {}'.format('PLACEHOLDER SHARESOUTSTANDING', 'PLACEHOLDER MULTIPLE')], 
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
#-----------------------------------------------------------------------------
# SUMMARY CALLBACKS
# -----------------------------------------------------------------------------------
@callback(
    Output(component_id='tesla-stock', component_property='figure'),
    [Input(component_id='my_interval', component_property='n_intervals')]
)
def update_graph(n):
    """Pull financial data from Alpha Vantage and update graph every 2 minutes"""
    ttm_data, ttm_meta_data = ts.get_intraday(symbol='TSLA',interval='1min',outputsize='compact')
    df = ttm_data.copy()
    df=df.transpose()
    df.rename(index={"1. open":"open", "2. high":"high", "3. low":"low",
                     "4. close":"close","5. volume":"volume"},inplace=True)
    df=df.reset_index().rename(columns={'index': 'indicator'})
    df = pd.melt(df,id_vars=['indicator'],var_name='date',value_name='rate')
    df = df[df['indicator']!='volume']
    line_chart = px.line(
                    data_frame=df,
                    x='date',
                    y='rate',
                    color='indicator',
                    title="Stock: {}".format(ttm_meta_data['2. Symbol'])
                 )
    return (line_chart)

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
    
    df = pd.read_csv("docs/Caste.csv")
    df = df[df['state_name']=='Maharashtra']
    df = df.groupby(['year','gender',], as_index=False)[['detenues','under_trial','convicts','others']].sum()

    if input_1 == 'QoQ' and input_2 == 'Revenue':
        fig = px.bar(
                data_frame=df,
                x="year",
                y="convicts",
                color="gender",               # differentiate color of marks
                opacity=0.9,                  # set opacity of markers (from 0 to 1)
                orientation="v",              # 'v','h': orientation of the marks
                barmode='relative',           # in 'overlay' mode, bars are top of one another.
                labels={"convicts":"Convicts in Maharashtra",
                        "gender":"Gender"},           # map the labels of the figure
                title='Indian Prison Statistics', # figure title
                template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        )
        fig.update
    elif input_1 == 'QoQ' and input_2 == 'Gross Profit':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'Income from Operations':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'Net Income':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'Adj EBITDA':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'FcF':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Revenue':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Gross Profit':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Income from Operations':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Net Income':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Adj EBITDA':
        fig = ''
    else:
        fig = ''
    return fig

@callback(
    Output('margin-line', 'figure'),
    [Input('freq-dropdown', 'value'),
    Input('margin-metric', 'value')]
)
def update_fund_graph(input_1, input_2):
    df = pd.read_csv("docs/Caste.csv")
    df = df[df['state_name']=='Maharashtra']
    df = df.groupby(['year','gender',], as_index=False)[['detenues','under_trial','convicts','others']].sum()

    if input_1 == 'QoQ' and input_2 == 'Gross Profit Margin':
        fig = px.bar(
                data_frame=df,
                x="year",
                y="convicts",
                color="gender",               # differentiate color of marks
                opacity=0.9,                  # set opacity of markers (from 0 to 1)
                orientation="v",              # 'v','h': orientation of the marks
                barmode='relative',           # in 'overlay' mode, bars are top of one another.
                labels={"convicts":"Convicts in Maharashtra",
                        "gender":"Gender"},           # map the labels of the figure
                title='Indian Prison Statistics', # figure title
                template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        )
        fig.update
    elif input_1 == 'QoQ' and input_2 == 'Operating Income Margin':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'Net Income Margin':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'Adj EBITDA Margin':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Gross Profit Margin':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Operating Income Margin':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Net Income Margin':
        fig = ''
    else:
        fig = ''
    return fig


#-----------------------------------------------------------------------------
# LIQUIDITY&SOLVENCY CALLBACKS
# -----------------------------------------------------------------------------------
@callback(
    Output('ratio-graph', 'figure'),
    Input('liq-ratio', 'value')
)
def update_ratio_graph(input):
    df = pd.read_csv("docs/Caste.csv")
    df = df[df['state_name']=='Maharashtra']
    df = df.groupby(['year','gender',], as_index=False)[['detenues','under_trial','convicts','others']].sum()
    df.drop(df[df['gender'] == 'Female'].index, inplace = True)

    if input == 'Current Ratio':
        fig = px.line(
                data_frame=df,
                x="year",
                y="convicts",
                labels={"convicts":"Convicts in Maharashtra",
                        "gender":"Gender"},           # map the labels of the figure
                height=400,
                title='Indian Prison Statistics', # figure title
                template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        )
    elif input == 'Quick Ratio':
        fig = px.line(
                data_frame=df,
                x="year",
                y="convicts",
                labels={"convicts":"Convicts in Maharashtra",
                        "gender":"Gender"},           # map the labels of the figure
                height=400,
                title='Indian Prison Statistics', # figure title
                template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        )
    elif input == 'Debt to Equity Ratio':
        fig = ''
    elif input == 'Debt to Assets Ratio':
        fig = ''
    else:
        fig = ''
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
    df = pd.read_csv("docs/Caste.csv")
    df = df[df['state_name']=='Maharashtra']
    df = df.groupby(['year','gender',], as_index=False)[['detenues','under_trial','convicts','others']].sum()

    if input_1 == 'QoQ' and input_2 == 'Revenue':
        fig = px.line(
                data_frame=df,
                x="year",
                y="convicts",
                labels={"convicts":"Convicts in Maharashtra",
                        "gender":"Gender"},           # map the labels of the figure
                title='Indian Prison Statistics', # figure title
                template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        )
    elif input_1 == 'QoQ' and input_2 == 'Revenue Growth':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'Gross Profit Growth':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'Income from Operations Growth':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'Net Income Growth':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'Adj EBITDA Growth':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'EPS Growth':
        fig = ''
    elif input_1 == 'QoQ' and input_2 == 'FcF Growth':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'Revenue Growth':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'Gross Profit Growth':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'Income from Operations Growth':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'Net Income Growth':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'Adj EBITDA Growth':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'EPS Growth':
        fig = ''
    else:
        fig = ''
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
    if input_1 == 'YoY' and input_2 == 'Invested Capital':
        fig = px.line(
                data_frame=df,
                x="year",
                y="convicts",
                labels={"convicts":"Convicts in Maharashtra",
                        "gender":"Gender"},           # map the labels of the figure
                title='Indian Prison Statistics', # figure title
                template='gridon'            # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
        )
    elif input_1 == 'YoY' and input_2 == 'Total Assets':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'ROE':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'ROA':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'Operating ROIC':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'FcF ROIC':
        fig = ''
    elif input_1 == 'YoY' and input_2 == 'WACC':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Invested Capital':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Total Assets':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'ROE':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'ROA':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'Operating ROIC':
        fig = ''
    elif input_1 == 'TTM' and input_2 == 'FcF ROIC':
        fig = ''
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
        fig = ''
    else:
        fig = ''
    return fig

@callback(
    Output('forecast-bargraph', 'figure'),
    Input('forecast-timescale', 'value')
)
def update_forecast_bottom_graph(input):
    if input == 'QoQ':
        fig = ''
    else:
        fig = ''
    return fig