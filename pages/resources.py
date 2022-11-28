from gettext import textdomain
from pydoc import classname
from struct import pack
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

# GLOBAL CONSTANTS
TITLE_FONT_SIZE = 18

# GLOBAL METHODS
def get_title_component(title_text: str, icon: str) -> object:
    title = html.Div([
        html.I(className= icon, style={'font-size': '1rem', 'margin-right':'10px'}),
        html.P(title_text, style={'color': 'white', 'fontSize': TITLE_FONT_SIZE, 'font-weight': 'bold', 'margin-top': '18px'}, className="lead")
    ], style={'margin-left': '25px', 'margin-bottom': '-10px', 'margin-top': '3px'}, className='hstack')
    return title

def get_item_component(items_title: list, items_links: dict) -> object:
    item_list = dbc.Row([
        dbc.Col(html.Ul([html.Li(item, style={'margin-bottom': '5px'}) for item in items_title]), xs=dict(size=12), sm= dict(size=12), md= dict(size=5), lg= dict(size=4), xl= dict(size=4), xxl= dict(size=4)),
        dbc.Col([dbc.NavLink(key, href= value, active='exact', style={'margin-top': '-6.1px', 'margin-bottom': '-10.9px', 'margin-left': '-45px'}) for key, value in items_links.items()])
    ], style={'font-style': 'italic', 'margin-left': '25px'})    
    return item_list

resources_layout = dbc.Card([
    get_title_component('Websites financieras', 'fa fa-columns'),
    get_item_component(['Investopedia:', 'Yahoo Finance:', 'AlphaQuery', 'Autocharts', 'Clicktrade', 'Ark Invest', 'Vanguard Group'], {'Más en Investopedia site': 'https://www.investopedia.com/', 'Más en Yahoo site': 'https://es.finance.yahoo.com/', 'Más en AlphaQuery site': 'https://www.alphaquery.com/', 'Más en Autocharts site': 'https://www.autocharts.info/quarterly?group=By%20Model', 'Más en iBrokers site': 'https://www.clicktrade.es/', 'Ark Invest site': 'https://ark-invest.com/', 'Vanguard site': 'https://investor.vanguard.com/corporate-portal/'}),
    get_title_component('Personalidades interesantes', 'fa fa-users'),
    get_item_component(['Nic Carter:', 'Lyn Alden:', 'Gary Black:', 'Galileo Russell:', 'Cathie Wood:', 'Balaji S.:', 'Naval:', 'Doomberg:', 'Mayur Thaker:', 'Ray Dalio:', '10-k Diver:', 'Preston Pysch:', 'Ben Felix:', 'Cazadividendos:'], {'Nic Carter personal blog': 'https://niccarter.info/', 'Lyn Alden personal website': 'https://www.lynalden.com/', 'Gary Black twitter account': 'https://twitter.com/garyblack00', 'Hyperchange YouTube channel': 'https://www.youtube.com/@HyperChangeTV','Cathie Wood twitter account': 'https://twitter.com/CathieDWood', 'Balaji S. twitter account': 'https://twitter.com/balajis', 'Naval YouTube channel': 'https://www.youtube.com/@NavalR', 'Doomberg website': 'https://doomberg.substack.com/', 'Mayur Thaker twitter account': 'https://twitter.com/freshjiva', 'Ray Dalio linkedIn': 'https://www.linkedin.com/in/raydalio/', '10-k Diver twitter account': 'https://twitter.com/10kdiver', 'Preston Pysch twitter account': 'https://twitter.com/PrestonPysh', 'Ben Felix Youtube Channel': 'https://www.youtube.com/@BenFelixCSI', 'Cazadividendos website': 'https://www.cazadividendos.com/'}),
    get_title_component('Libros', 'fa fa-book'),
    get_item_component(['The Intelligent Investor:', 'The Sovereign Individual:', 'Layered Money:', 'The Bitcoin Standard:', 'Big Debt Crises:', 'Man, Economy and State:', 'The Next 100 Years:', 'Monetary nationalism:', 'The Wealth of Nations:'], {'Compra The Intelligent Investor en Amazon': 'https://www.amazon.es/Intelligent-Investor-Collins-Business-Essentials/dp/0060555661/ref=sr_1_1?keywords=the+intelligent+investor&qid=1669648518&qu=eyJxc2MiOiIxLjQwIiwicXNhIjoiMC44NCIsInFzcCI6IjEuMDcifQ%3D%3D&sprefix=the+intelli%2Caps%2C100&sr=8-1', 'Compra The Sovereign Individual en Amazon': 'https://www.amazon.es/Sovereign-Individual-Mastering-Transition-Information/dp/0684832720/ref=sr_1_1?keywords=the+sovereign+individual&qid=1669648547&qu=eyJxc2MiOiIxLjU1IiwicXNhIjoiMC42MCIsInFzcCI6IjAuODYifQ%3D%3D&sprefix=the+sovere%2Caps%2C93&sr=8-1', 'Compra Layered Money en Amazon': 'https://www.amazon.es/Layered-Money-Dollars-Bitcoin-Currencies/dp/1736110519/ref=sr_1_1?keywords=layered+money&qid=1669648570&qu=eyJxc2MiOiIwLjMzIiwicXNhIjoiMC4xNCIsInFzcCI6IjAuMzQifQ%3D%3D&sprefix=layered+mo%2Caps%2C102&sr=8-1', 'Compra The Bitcoin Standard en Amazon': 'https://www.amazon.es/Bitcoin-Standard-Decentralized-Alternative-Central/dp/1119473861/ref=sr_1_1?keywords=the+bitcoin+standard&qid=1669648637&qu=eyJxc2MiOiIxLjAxIiwicXNhIjoiMC40NiIsInFzcCI6IjAuNDYifQ%3D%3D&sprefix=the+bit%2Caps%2C97&sr=8-1', 'Compra Big Debt Crisis en Amazon': 'https://www.amazon.es/Principles-Navigating-Big-Debt-Crises/dp/1668009293/ref=sr_1_1?keywords=big+debt+crises+ray+dalio&qid=1669648656&qu=eyJxc2MiOiItMC4wMSIsInFzYSI6IjAuMDAiLCJxc3AiOiIwLjAwIn0%3D&sprefix=big+deb%2Caps%2C99&sr=8-1', 'Compra Man, Economy and State en Amazon': 'https://www.amazon.es/Man-Economy-State-Power-Market-ebook/dp/B0022NHOSE/ref=sr_1_1?keywords=man+economy+and+state&qid=1669648680&qu=eyJxc2MiOiIyLjE4IiwicXNhIjoiMC43MiIsInFzcCI6IjAuMDAifQ%3D%3D&sprefix=man%2C+econo%2Caps%2C97&sr=8-1', 'Compra The Next 100 Years en Amazon': 'https://www.amazon.es/Next-100-Years-Forecast-Century-ebook/dp/B006WB7QKS/ref=sr_1_1?keywords=the+next+100+years&qid=1669648696&qu=eyJxc2MiOiIxLjEyIiwicXNhIjoiMS4wMCIsInFzcCI6IjAuNjUifQ%3D%3D&sprefix=the+next+100%2Caps%2C111&sr=8-1', 'Compra Monetary nationalism en Amazon': 'https://www.amazon.es/Monetary-Nationalism-International-Stability-Friedrich/dp/1614273413/ref=sr_1_1?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=10JISXTYQ3Z37&keywords=monetary+nationalism&qid=1669648718&qu=eyJxc2MiOiIwLjAwIiwicXNhIjoiMC4wMCIsInFzcCI6IjAuMDAifQ%3D%3D&sprefix=monetary+nationalism%2Caps%2C87&sr=8-1', 'Compra The Wealth of Nations en Amazon': 'https://www.amazon.es/Wealth-Nations-Books-I-III-Bks-1-3/dp/0140432086/ref=sr_1_1?keywords=the+wealth+of+nations&qid=1669648735&qu=eyJxc2MiOiIyLjc1IiwicXNhIjoiMi4zMSIsInFzcCI6IjIuMDUifQ%3D%3D&sprefix=the+wea%2Caps%2C97&sr=8-1'}),
    get_title_component('Herramientas', 'fa fa-wrench'),
    get_item_component(['Compound Calculator:', 'StockDelver by Lyn Alden:'], {'Calculator website': 'http://www.moneychimp.com/calculator/compound_interest_calculator.htm', 'Stock Delver purchase link': 'https://www.lynalden.com/stockdelver-book/'}),
    get_title_component('Mis stocks favoritos', 'fa fa-line-chart'),
    get_item_component(['Tesla:', 'Square:', 'Block Inc:', 'Unity Software Inc:', 'Roblox Corp:'], {'Tesla investor relations site': 'https://ir.tesla.com/#quarterly-disclosure', 'Square website': 'https://squareinc2020ir.q4web.com/overview/default.aspx', 'Block Inc website': 'https://investors.block.xyz/overview/default.aspx', 'Unity website': 'https://investors.unity.com/overview/default.aspx', 'Roblox website': 'https://ir.roblox.com/overview/default.aspx'}),
    get_title_component('Tesla community', 'fa fa-car'),
    get_item_component(['Rob Mauer:', 'TheLimitingFactor:', 'Now You Know:', 'Stephen M. Ryan:', 'Troy Teslike:', 'James Stephenson:', 'TESLARATI:'], {'Tesla Daily YouTube channel': 'https://www.youtube.com/@TeslaDaily', 'The Limiting Factor YouTube channel': 'https://www.youtube.com/@thelimitingfactor', 'Now You Know YouTube channel': 'https://www.youtube.com/@NowYouKnowChannel', 'Solving The Money Problem YouTube channel': 'https://www.youtube.com/@SolvingTheMoneyProblem', 'Troy Teslike twitter account': 'https://twitter.com/TroyTeslike', 'James Stephenson twitter account': 'https://twitter.com/ICannot_Enough', 'TESLARATI website': 'https://www.teslarati.com/?utm_campaign=gs-2020-11-23&utm_source=google&utm_medium=smart_campaign&gclid=Cj0KCQiA1ZGcBhCoARIsAGQ0kkpgB15_I5paGQ4T15cbjrAJ5d4SIEUANl9Wgw2Viv4h6i_koiPlYx4aAnjnEALw_wcB'}),
], class_name= "card", style={'width': 'auto', 'height': 'auto', 'text-align': 'left'})

layout = dbc.Container(
    [
        resources_layout
    ]
, class_name='centered mb-5', style={'width': '800px'})

