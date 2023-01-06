# -*- coding: utf-8 -*-

# GLOBAL IMPORTS
from os import times
import sys
import abc
from time import time
from xml.dom.minidom import Element
import pandas as pd
import numpy as np

# LOCAL IMPORTS
sys.path.insert(0, "C:\\Users\\dario\\pet_projects\\tmts-oracle-app")
from dataclasses import make_dataclass
import json
from db.db_interface import CompanyDbInterface
from utils.utils import *


class CompanyFinancials(metaclass=abc.ABCMeta):
    """ 
    Metaclass that serves as a template for company financial data. It contains 6 distinct categories to reflect financial health of the instantiated
    subclass:
    1- Fundamental metrics (two timescales: QoQ and TTM): revenue, gross profit, income from operations, net income, adjusted EBITDA and FcF. As well as margin values for gross profit, 
    net income, income from operations and adjusted EBITDA.
    2- Liquidity and solvency ratios (single timescale: QoQ): current ratio, quick ratio, debt to equity ratio, debt to assets ratio and equity to assets ratio.
    3- Growth metrics (two timescales: QoQ and YoY): revenue growth, gross profit growth, income from operations growth, net income growth, adjusted ebitda growth, fcf growth
    4- Performance metrics (two timescales: QoQ and TTM): invested capital, total assets, ROA, ROE, NOPAT ROIC, FcF ROIC, WACC.
    5- Equity structure: outstanding shares QoQ, investors table, investors weight per category (retail, insiders, institutional)
    6- Price Forecast: simple model that projects expected FcF per quarter for next 10 years. Based on 4qtr FcF ROIC rate and 4 qtr Invested Capital rate. 
    Maximum FcF ROIC allowed = 40%; Maximum Invested Capital Increased QoQ = 10%.

    Args:
        metaclass (_type_, optional): _description_. Defaults to abc.ABCMeta.

    Raises:
        NotImplementedError: _description_
        NotImplementedError: _description_
        NotImplementedError: _description_
        NotImplementedError: _description_
        TypeError: _description_
        TypeError: _description_
        NotImplementedError: _description_
        NotImplementedError: _description_
        NotImplementedError: _description_

    Returns:
        _type_: _description_
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_fcf') and 
                callable(subclass.get_fcf) and
                hasattr(subclass, 'get_quick_ratio') and 
                callable(subclass.get_quick_ratio) and
                hasattr(subclass, 'get_debt_to_equity_ratio') and 
                callable(subclass.get_debt_to_equity_ratio) and
                hasattr(subclass, 'get_debt_to_assets_ratio') and 
                callable(subclass.get_debt_to_assets_ratio) and
                hasattr(subclass, 'get_fcf_growth') and 
                callable(subclass.get_fcf_growth) and
                hasattr(subclass, 'get_invested_capital') and 
                callable(subclass.get_invested_capital) and
                hasattr(subclass, 'get_fcf_roic') and 
                callable(subclass.get_fcf_roic) and
                hasattr(subclass, 'get_nopat_roic') and 
                callable(subclass.get_nopat_roic) and
                hasattr(subclass, 'get_wacc') and 
                callable(subclass.get_wacc) or 
                NotImplemented)

    def __init__(self, company_name: str, host: str, database: str):
        self.company_name = company_name
        self._db_interface= CompanyDbInterface(host, database)

    @property
    def hostname(self) -> str:
        """ The hostname 

        Returns:
            str: _description_
        """
        return self._db_interface._host

    @property
    def database_name(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return self._db_interface._db
    
    @property
    def collections(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """
        return self._db_interface._db_collections

    @property
    def financials_in_json(self) -> json:
        pass

    def _parse_to_timescaled_dict(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ A method that parses input data from database into a dictionary with keys and values. Values are returned in different timescales
        depending of the timescale flag argument value.

        Args:
            collection (str): database collection target.
            key (list): List of keys to be searched in collection. Defaults to ['TotalRevenues', 'date'].
            timescale (str): Frequency of returned data. Defaults to 'QoQ. Any of three values: QoQ, YoY or TTM.

        Returns:
            _type_: dictionary with keys equal to input key names and values equal to lists.
        """
        packed_data = self._db_interface._find_values_for_multiple_keys(collection, keys)
        unpacked_data = unpack_cursor_object_multiple(packed_data, keys)
        if timescale == 'QoQ':            
            return unpacked_data
        elif timescale == 'YoY':
            # TODO: Add Year column directly to database
            df_data = pd.DataFrame.from_dict(unpacked_data)
            try:
                df_data['Year'] = df_data['date'].apply(lambda x: int('20' + x[2:]))
            except ValueError as e:
                print(['Wrong date value format in database collection {}'.format(collection)], e)
            df_data.drop('date', axis = 1, inplace= True)
            df_data = df_data.groupby('Year').sum().reset_index().sort_index(ascending=False)
            dict_data = df_data.to_dict()
            return dict_values_to_list_values_in_dict(dict_data)
        elif timescale == 'TTM':
            df_data = pd.DataFrame.from_dict(unpacked_data)
            i = 0
            for k in keys:
                if [type(element) for element in unpacked_data[k]] == [type(element) for element in range(len(unpacked_data[k]))]:
                    df_data.insert(loc = i, column= 'TTM' + k, value = compute_rolling_window(df_data[k].to_list(), 4))                   
                    df_data.drop(k, axis = 1)
                    i+=1
            return dict_values_to_list_values_in_dict(df_data.to_dict()) 

    def _add_ratio_metric_to_dict(self, keys: list = [], input_dict: dict = {}) -> dict:
        """ A method that divides a list over another list and append the results in a newly created key to the input dict.

        Args:
            keys (list): List of keys in input dictionary. Defaults to [].
            input_dict (dict): A dictionary containing lists of integers. Defaults to {}.

        Returns:
            dict: return dictionary with newly created key based on ratio of two input keys (1 and 0).
        """
        input_dict['Ratio' + keys[0] + '/' + keys[1]] = [x / y for x, y in zip(input_dict[keys[0]], input_dict[keys[1]])]
        return input_dict

    # FUNDAMENTALS: revenue, gross profit, income from operations, net income, adj EBITDA, FcF. Gross profit margin, income form ops margin,
    # net income margin, adj EBITDA margin.
    def get_revenue(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting revenue per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve revenue. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for revenue.
        """
        return self._parse_to_timescaled_dict(collection, keys, timescale)

    def get_gross_profit(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting gross profit per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve gross profit. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for gross profit.
        """
        return self._parse_to_timescaled_dict(collection, keys, timescale)

    def get_income_ops(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting income from operations per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve income from operations. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for income from operations.
        """
        return self._parse_to_timescaled_dict(collection, keys, timescale)

    def get_net_income(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting net income per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve net income. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for net income.
        """
        return self._parse_to_timescaled_dict(collection, keys, timescale)

    def get_adj_ebitda(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting adjusted EBITDA per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve adjusted EBITDA. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for adjusted EBITDA.
        """
        return self._parse_to_timescaled_dict(collection, keys, timescale)

    @abc.abstractmethod
    def get_fcf(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting free cash flow per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve free cash flow Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for free cash flow.
        """
        raise NotImplementedError

    def get_gross_profit_margin(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting gross profit margin per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve gross profit margin. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for gross profit margin.
        """
        gross_profit_marign_dict = self.get_gross_profit(collection, keys, timescale)
        return self._add_ratio_metric_to_dict(get_list(gross_profit_marign_dict), gross_profit_marign_dict)

    def get_income_ops_margin(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting income operations margin per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve income from operations margin. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for income from operations margin.
        """
        income_ops_margin_dict = self.get_income_ops(collection, keys, timescale)
        return self._add_ratio_metric_to_dict(get_list(income_ops_margin_dict), income_ops_margin_dict)

    def get_net_income_margin(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting net income margin per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve net income margin. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for net income margin.
        """
        net_income_margin_dict = self.get_net_income(collection, keys, timescale)
        return self._add_ratio_metric_to_dict(get_list(net_income_margin_dict), net_income_margin_dict)

    def get_adj_ebitda_margin(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting adjusted EBITDA margin per quarter or TTM.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve adjusted EBITDA margin margin. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for adjusted EBITDA margin margin.
        """
        adj_ebitda_dict = self._parse_to_timescaled_dict(collection[0], [keys[0], keys[2]], timescale)
        total_revenues_dict = self.get_total_assets(collection[1], [keys[1], keys[2]], timescale)
        if timescale == 'YoY':
            adj_ebitda_dict.pop('Year')
            adj_ebitda_margin_dict = adj_ebitda_dict | total_revenues_dict
            return self._add_ratio_metric_to_dict([keys[0], keys[1]], adj_ebitda_margin_dict)
        elif timescale == 'TTM' or 'QoQ':
            adj_ebitda_dict.pop(keys[2])
            adj_ebitda_margin_dict = adj_ebitda_dict | total_revenues_dict
            keys = get_list(adj_ebitda_margin_dict)
            if timescale == 'TTM':
                return self._add_ratio_metric_to_dict([keys[0], keys[2]], adj_ebitda_margin_dict)
            else:
                return self._add_ratio_metric_to_dict([keys[0], keys[1]], adj_ebitda_margin_dict)
        else:
            raise TypeError('Timescale specified is not contemplated. Please enter "YoY" or "TTM"')
    
    # LIQUIDITY AND SOLVENCY: current ratio, quick ratio, debt to equity ratio, debt to assets ratio and equity ratio
    def get_current_ratio(self, collection: str, keys: list = []) -> dict:
        """ Wrapper method for getting current ratio based on input data.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to calculate current ratio. It should contain at least "Total Current Assets" and "Total 
            current liabililities". Defaults to [].

        Returns:
            dict: dict containing input keys with corresponding values and extended key relating to current ratio values over time.
        """
        current_ratio_dict = self._parse_to_timescaled_dict(collection, keys)
        return self._add_ratio_metric_to_dict(keys, current_ratio_dict)

    @abc.abstractmethod
    def get_quick_ratio(self, collection: str, keys: list = []) -> dict:
        """ Wrapper method for getting quick ratio based on input data.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to calculate quick ratio. Defaults to [].

        Raises:
            NotImplementedError

        Returns:
            dict: dict containing input keys with corresponding values and extended key relating to quick ratio values over time.
        """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_debt_to_equity_ratio(self, collection: str, keys: list = []) -> dict:
        """ Wrapper method for getting debt to equity ratio based on input data.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to calculate debt to equity ratio. Defaults to [].

        Raises:
            NotImplementedError

        Returns:
            dict: dict containing input keys with corresponding values and extended key relating to debt to equity ratio values over time.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_debt_to_assets_ratio(self, collection: str, keys: list = []) -> dict:
        """ Wrapper method for getting debt to assets ratio based on input data.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to calculate debt to assets ratio. Defaults to [].

        Raises:
            NotImplementedError

        Returns:
            dict: dict containing input keys with corresponding values and extended key relating to debt to assets ratio values over time.
        """
        raise NotImplementedError
        
    def get_equity_ratio(self, collection: str, keys: list = []) -> dict:
        """ Wrapper method for getting equity ratio based on input data.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to calculate equity ratio. It should contain at least "Total stockholders equity" and "Total 
            assets". Defaults to [].

        Returns:
            dict: dict containing input keys with corresponding values and extended key relating to equity ratio values over time.
        """
        equity_ratio_dict = self._parse_to_timescaled_dict(collection, keys)
        return self._add_ratio_metric_to_dict(keys, equity_ratio_dict)


    # GROWTH METRICS: revenue growth, gross profit growth, income from operations growth, net income growth, adj ebitda growth, eps growth and fcf growth
    def _get_growth_metric_dict(self, data: dict = {}, keys: list = []) -> dict:
        """ Get current ratio based on input data.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to calculate current ratio. It should contain at least "Total Current Assets" and "Total 
            current liabililities". Defaults to [].
            timescale (str): a flag determining timescale frequency.

        Returns:
            dict: dict containing input keys with corresponding values and extended key relating to current ratio values over time.
        """
        #growth_ratio_dict = self._parse_to_timescaled_dict(collection, keys, timescale)
        growth_ratio_dict = data
        growth_ratio_df = pd.DataFrame.from_dict(growth_ratio_dict)
        growth_ratio_df['GrowthRatio'] = (growth_ratio_df[keys[0]] - growth_ratio_df[keys[0]].shift(-1)) / np.abs(growth_ratio_df[keys[0]].shift(-1)) * 100
        return dict_values_to_list_values_in_dict(growth_ratio_df.to_dict()) 

    def get_revenue_growth(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting revenue growth QoQ or YoY.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve revenue. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for revenue.
        """
        return self._get_growth_metric_dict(self.get_revenue(collection, keys, timescale), keys)

    def get_gross_profit_growth(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting gross profit growth QoQ or YoY.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve gross profit. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for gross profit.
        """
        return self._get_growth_metric_dict(self.get_gross_profit(collection, keys, timescale), keys)

    def get_income_ops_growth(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting income from operations growth QoQ or YoY.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve income from operations. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for income from operations.
        """
        return self._get_growth_metric_dict(self.get_income_ops(collection, keys, timescale), keys)

    def get_net_income_growth(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting net income growth QoQ or YoY.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve net income. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for net income.
        """
        return self._get_growth_metric_dict(self.get_net_income(collection, keys, timescale), keys)

    def get_adj_ebitda_growth(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting adjusted EBITDA growth QoQ or YoY.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve adjusted EBITDA. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for adjusted EBITDA.
        """
        return self._get_growth_metric_dict(self.get_adj_ebitda(collection, keys, timescale), keys)

    def get_fcf_growth(self, collection: str, keys: list = [], timescale: str = 'QoQ') -> dict:
        """ Wrapper method for getting FcF growth QoQ or YoY.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve revenue. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'QoQ'.

        Returns:
            dict: dict containing input keys with corresponding values for revenue.
        """
        fcf_dict = self.get_fcf(collection, keys, timescale)
        keys = get_list(fcf_dict)
        return self._get_growth_metric_dict(fcf_dict, keys)

    # PERFORMANCE METRICS: invested capital, total assets, roa, roe, nopat roic, fcf roic  
    @abc.abstractmethod
    def get_invested_capital(self, collection: str, keys: list = [], timescale: str = 'YoY') -> dict:
        """ Get invested capital per year.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to retrieve invested capital. Defaults to [].

        Raises:
            NotImplementedError

        Returns:
            dict: dict containing input keys with corresponding values. First key of the dictionary is the resulting value of invested capital.
        """
        raise NotImplementedError 

    def get_total_assets(self, collection: str, keys: list = [], timescale: str = 'YoY') -> dict:
        """ Get total assets from balance sheet.

        Args:
            collection (str): database collection target.
            keys (list): A list of keys to be searched in database in order to retrieve total assets. Defaults to [].
            timescale (str): flag determining timescale frequency. Defaults to 'YoY'.

        Returns:
            dict: dict containing input keys with corresponding values for total assets.
        """
        total_assets_dict = self._parse_to_timescaled_dict(collection, keys, timescale)
        keys = get_list(total_assets_dict)
        if timescale == 'YoY':
            total_assets_dict[keys[0]] = [value / 4 for value in total_assets_dict[keys[0]]]
        return  total_assets_dict

    def get_return_on_assets(self, collection: list = [], keys: list = [], timescale: str = 'YoY') -> dict:
        """ Get return on assets ratio based on input data.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to calculate return on assets ratio. Defaults to [].

        Returns:
            dict: dict containing input keys with corresponding values and extended key relating to return on assets ratio values over time.
        """
        net_income_dict = self._parse_to_timescaled_dict(collection[0], [keys[0], keys[2]], timescale)
        total_assets_dict = self.get_total_assets(collection[1], [keys[1], keys[2]], timescale)
        if timescale == 'YoY':
            net_income_dict.pop('Year')
            return_on_assets_dict = net_income_dict | total_assets_dict
            return self._add_ratio_metric_to_dict([keys[0], keys[1]], return_on_assets_dict)
        elif timescale == 'TTM' or 'QoQ':
            net_income_dict.pop(keys[2])
            return_on_assets_dict = net_income_dict | total_assets_dict
            keys = get_list(return_on_assets_dict)
            if timescale == 'TTM':
                return self._add_ratio_metric_to_dict([keys[0], keys[2]], return_on_assets_dict)
            else:
                return self._add_ratio_metric_to_dict([keys[0], keys[1]], return_on_assets_dict)
        else:
            raise TypeError('Timescale specified is not contemplated. Please enter "YoY" or "TTM"')

    def get_return_on_equity(self, collection: list = [], keys: list = [], timescale: str = 'YoY') -> dict:
        """ Get return on equity ratio based on input data.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to calculate return on equity ratio. Defaults to [].

        Returns:
            dict: dict containing input keys with corresponding values and extended key relating to return on equity ratio values over time.
        """
        net_income_dict = self._parse_to_timescaled_dict(collection[0], [keys[0], keys[2]], timescale)
        total_stockholders_dict = self._parse_to_timescaled_dict(collection[1], [keys[1], keys[2]], timescale)
        if timescale == 'YoY':
            net_income_dict.pop('Year')
            total_stockholders_dict[keys[1]] = [value / 4 for value in total_stockholders_dict[keys[1]]]
            return_on_equity_dict = net_income_dict | total_stockholders_dict
            return self._add_ratio_metric_to_dict([keys[0], keys[1]], return_on_equity_dict)
        elif timescale == 'TTM' or 'QoQ':
            net_income_dict.pop(keys[2])
            return_on_equity_dict = net_income_dict | total_stockholders_dict
            keys = get_list(return_on_equity_dict)
            if timescale == 'TTM':
                return self._add_ratio_metric_to_dict([keys[0], keys[2]], return_on_equity_dict)
            else:
                return self._add_ratio_metric_to_dict([keys[0], keys[1]], return_on_equity_dict)
        else:
            raise TypeError('Timescale specified is not contemplated. Please enter "YoY" or "TTM"')

    @abc.abstractmethod
    def get_fcf_roic(self, timescale: str = 'YoY') -> dict:
        """ Get fcf roic per year or TTM.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to retrieve fcf roic. Defaults to [].

        Raises:
            NotImplementedError

        Returns:
            dict: dict containing input keys with corresponding values of terms in fcf roic equation and fcf roic ratio over time.
        """
        raise NotImplementedError 
    
    @abc.abstractmethod
    def get_nopat_roic(self, collection: str, keys: list = [], timescale: str = 'YoY') -> dict:
        """ Get NOPAT roic per year or TTM.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to retrieve NOPAT roic. Defaults to [].

        Raises:
            NotImplementedError

        Returns:
            dict: dict containing input keys with corresponding values of terms in NOPAT roic equation and NOPAT roic ratio over time.
        """
        raise NotImplementedError 

    @abc.abstractmethod
    def get_wacc(self, collection, keys: list = [], timescale: str = 'YoY') -> dict:
        """ Get WACC per year or TTM.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to retrieve WACC. Defaults to [].

        Raises:
            NotImplementedError

        Returns:
            dict: dict containing input keys with corresponding values of terms in WACC equation and WACC value over time.
        """
        raise NotImplementedError


    # EQUITY STRUCTURE: investors, outstanding shares
    def get_investor_table(self, collection: str, keys: list = []) -> dict:
        pass
    
    def get_investor_classification(self, list_investors: list = []) -> dict:
        pass

    def get_outstanding_shares(self, collection: str, keys: list = []) -> dict:
        """ Get basic or diluted outstanding shares.

        Args:
            collection (_type_): database collection target.
            keys (list): A list of keys to be searched in database to retrieve outstanding shares. Defaults to [].

        Raises:
            NotImplementedError

        Returns:
            dict: dict containing input keys with corresponding share values.
        """
        return self._parse_to_timescaled_dict(collection, keys)

    # PRICE FORECAST: 4qtr fcf roic rate, 4qtr invested capital rate, project fcf
    # TODO: abstract method to compute derivative: _get_rate_of_change(self, input_dict (two columns: metric and date), keys:list = ['Rate', 'TTMRate'])
    def _get_rate_fcf_roic(self, timescale: str = 'QoQ') -> dict:
        """ Calculate free cash flow ROIC rate of change in a trailing twelve month basis.

        Args:
            timescale (str): Frequency of returned data from which TTM will be computed. Defaults to 'QoQ.

        Returns:
            dict: dictionary with keys equal: RateTTM, FcFRoic, Date, Rate
        """
        fcf_roic_dict = self.get_fcf_roic(timescale = timescale) # fcf roic QoQ and date
        fcf_roic_df = pd.DataFrame.from_dict(fcf_roic_dict) # dataframe columns: fcfroic, date
        keys = get_list(fcf_roic_dict)
        fcf_roic_df['Rate'] = (fcf_roic_df[keys[1]] - fcf_roic_df[keys[1]].shift(-1)) / fcf_roic_df[keys[1]].shift(-1) * 100 # df columns: fcfroic, date, rate
        fcf_roic_df.insert(loc = 0, column= 'RateTTM', value = compute_rolling_window(fcf_roic_df['Rate'].to_list(), 4)) # df columns: ratettm, fcfroic, date, rate
        return dict_values_to_list_values_in_dict(fcf_roic_df.to_dict())
    
    def _get_rate_invested_capital(self, timescale: str = 'QoQ') -> dict:
        """ Calculate invested capital rate of change in a trailing twelve month basis.

         Args:
            imescale (str): Frequency of returned data from which TTM will be computed. Defaults to 'QoQ.

        Returns:
            dict: dictionary with keys equal: RateTTM, CapitalInvested, Date, Rate
        """
        invested_capital_dict = self.get_invested_capital(timescale = timescale) # investedCapital QoQ and date
        invested_capital_df = pd.DataFrame.from_dict(invested_capital_dict) # dataframe columns: investedCapital, date
        keys = get_list(invested_capital_dict)
        invested_capital_df['Rate'] = (invested_capital_df[keys[0]] - invested_capital_df[keys[0]].shift(-1)) / invested_capital_df[keys[0]].shift(-1) * 100 # df columns: investedCapital, date, rate
        invested_capital_df.insert(loc = 0, column= 'RateTTM', value = compute_rolling_window(invested_capital_df['Rate'].to_list(), 4)) # df columns: ratettm, investedCapital, date, rate
        return dict_values_to_list_values_in_dict(invested_capital_df.to_dict())
    
    def projected_fcf(self, timescale: str = 'QoQ') -> dict:
        # TODO: Create method that automates creation of sequence of quarters: get_sequence_of_quarter(start_quarter, start_year, number_of_years)
        """_summary_

        Args:
            keys (list, optional): _description_. Defaults to [].

        Returns:
            dict: _description_
        """
        # Local variables
        # Create vector of future/projected quarters. Next 40 quarters (10 yrs of projected cash flows).
        array_proj_qoq = ['4Q22', '1Q23', '2Q23', '3Q23', '4Q23', '1Q24', '2Q24', '3Q24', '4Q24', '1Q25', '2Q25', '3Q25', '4Q25', '1Q26', '2Q26', '3Q26', 
                            '4Q26', '1Q27', '2Q27', '3Q27', '4Q27', '1Q28','2Q28', '3Q28', '4Q28', '1Q29', '2Q29', '3Q29', '4Q29', '1Q30', '2Q30',
                            '3Q30', '4Q30', '1Q31', '2Q31', '3Q31', '4Q31', '1Q32', '2Q32', '3Q32', '4Q32']

        # Get FcF ROIC rate of change in a TTM basis and starting 4qtr average FcF ROIC (last 4 quarters of public financial data)
        fcf_dict = self._get_rate_fcf_roic(timescale = timescale) 
        keys = get_list(fcf_dict)
        fcf_roic_rate_ttm, fcf_roic_start = average_of_dict_keys_n_values(fcf_dict, [keys[0], keys[2]], [1, 4]) 
        # Get Invested capital rate of change in a TTM basis and starting 4qtr average Invested Capital (last 4 quarters of public financial data)
        invested_capital_dict = self._get_rate_invested_capital(timescale = timescale)
        keys = get_list(invested_capital_dict)
        invested_capital_rate_ttm, invested_capital_start = average_of_dict_keys_n_values(invested_capital_dict, [keys[0], keys[1]], [1, 4])
        # Calculate projected FcF per quarter
        fcf_projected_qoq = []
        for i in range(len(array_proj_qoq)):
            fcf_i = (invested_capital_start * (1 + invested_capital_rate_ttm/100)**i) * min((fcf_roic_start * (1 + fcf_roic_rate_ttm/100)**i), 0.4)
            fcf_projected_qoq.append(fcf_i)
        
        # Cast list of projected cash flow to dict and return
        dict_fcf_project = {'FcFProjected': fcf_projected_qoq, 'Quarter': array_proj_qoq}
        return dict_fcf_project




class TeslaFinancials(CompanyFinancials):
    

    def __init__(self, name = 'Tesla', host = "mongodb://localhost:27017", database = "tesla_db"):     
        return super().__init__(name, host, database)

    # TODO: implement abstract methods:
    # Debt to assets ratio (ST debt & LT debt), debt to equity ratio (ST debt & LT debt), WACC
    # Table of investors

    # FUNDAMENTALS
    def get_revenue(self, collection = 'statement_operations', keys: list = ['TotalRevenues', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_revenue(collection, keys, timescale)

    def get_gross_profit(self, collection = 'statement_operations', keys: list = ['GrossProfit', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_gross_profit(collection, keys, timescale)

    def get_income_ops(self, collection = 'statement_operations', keys: list = ['IncomeFromOperations', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_income_ops(collection, keys, timescale)

    def get_net_income(self, collection = 'statement_operations', keys: list = ['NetIncome', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_net_income(collection, keys, timescale)
    
    def get_adj_ebitda(self, collection = 'gaap_non_gaap', keys: list = ['AdjustedEBITDA', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_adj_ebitda(collection, keys, timescale)
    
    def get_fcf(self, collection = 'cash_flow', keys: list = ['NetCashOperatingActivities', 'Capex', 'date'], timescale: str = 'QoQ') -> dict:
        fcf_dict= self._parse_to_timescaled_dict(collection, keys, timescale)
        keys = get_list(fcf_dict)
        fcf_df = pd.DataFrame.from_dict(fcf_dict)
        if timescale == 'QoQ' or 'YoY':
            fcf_df.insert(loc = 0, column= 'FcF', value = fcf_df[keys[0]] + fcf_df[keys[1]])
        if timescale == 'TTM':
            fcf_df.insert(loc = 0, column= 'TTMFcF', value = fcf_df[keys[0]] + fcf_df[keys[1]])        
        return dict_values_to_list_values_in_dict(fcf_df.to_dict())
    
    def get_gross_profit_margin(self, collection = 'statement_operations', keys: list = ['GrossProfit', 'TotalRevenues', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_gross_profit_margin(collection, keys, timescale)
    
    def get_income_ops_margin(self, collection = 'statement_operations', keys: list = ['IncomeFromOperations', 'TotalRevenues', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_income_ops_margin(collection, keys, timescale)
    
    def get_net_income_margin(self, collection = 'statement_operations', keys: list = ['NetIncome', 'TotalRevenues', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_net_income_margin(collection, keys, timescale)
    
    def get_adj_ebitda_margin(self, collection = ['gaap_non_gaap', 'statement_operations'], keys: list = ['AdjustedEBITDA', 'TotalRevenues', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_adj_ebitda_margin(collection, keys, timescale)
        

    # LIQUIDITY & SOLVENCY
    def get_current_ratio(self, collection = 'balance_sheet', keys: list = ['TotalCurrentAssets', 'TotalCurrentLiabilities', 'date']) -> dict:
        return super().get_current_ratio(collection, keys)
    
    def get_quick_ratio(self, collection = 'balance_sheet', keys: list = ['TotalCurrentAssets', 'Inventory', 'TotalCurrentLiabilities', 'date']) -> dict:
        # Get dictionary with key-pair values from database
        quick_ratio_dict= self._parse_to_timescaled_dict(collection, keys)
        # Cast dict to dataframe and compute quick ratio in new column
        quick_ratio_df = pd.DataFrame.from_dict(quick_ratio_dict)
        quick_ratio_df.insert(loc = 0, column= 'QuickRatio', value= (quick_ratio_df[keys[0]] - quick_ratio_df[keys[1]]) / quick_ratio_df[keys[2]])
        # Drop TotalCurrentAssets, Inventory and TotalCurrentLiabiliites from dataframe
        quick_ratio_df.drop([keys[0], keys[1], keys[2]], axis = 1)
        # Convert back to dictionary and return.        
        return dict_values_to_list_values_in_dict(quick_ratio_df.to_dict())
    
    # TODO: override method.
    def get_debt_to_assets_ratio(self, collection = 'balance_sheet', keys: list = []) -> dict:
        return super().get_debt_to_assets_ratio(collection, keys)
    
    # TODO: override method.
    def get_debt_to_equity_ratio(self, collection = 'balance_sheet', keys: list = []) -> dict:
        return super().get_debt_to_equity_ratio(collection, keys)
    
    def get_equity_ratio(self, collection = 'balance_sheet', keys: list = ['TotalStockholdersEquity', 'TotalAssets', 'date']) -> dict:
        return super().get_equity_ratio(collection, keys)
    
    
    # GROWTH METRICS
    def get_revenue_growth(self, collection = 'statement_operations', keys: list = ['TotalRevenues', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_revenue_growth(collection, keys, timescale)
    
    def get_gross_profit_growth(self, collection = 'statement_operations', keys: list = ['GrossProfit', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_gross_profit_growth(collection, keys, timescale)
    
    def get_income_ops_growth(self, collection = 'statement_operations', keys: list = ['IncomeFromOperations', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_income_ops_growth(collection, keys, timescale)
    
    def get_net_income_growth(self, collection = 'statement_operations', keys: list = ['NetIncome', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_net_income_growth(collection, keys, timescale)
    
    def get_adj_ebitda_growth(self, collection = 'gaap_non_gaap', keys: list = ['AdjustedEBITDA', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_adj_ebitda_growth(collection, keys, timescale)
    
    def get_fcf_growth(self, collection = 'cash_flow', keys: list = ['NetCashOperatingActivities', 'Capex', 'date'], timescale: str = 'QoQ') -> dict:
        return super().get_fcf_growth(collection, keys, timescale)
    

    # PERFORMANCE METRICS
    def get_invested_capital(self, collection = 'balance_sheet', keys: list = ['TotalAssets', 'AccountsPayable', 'AccruedLiabilitiesAndOther', 'CashAndCashEquivalents', 'TotalCurrentAssets', 'TotalCurrentLiabilities', 'date'], timescale: str = 'YoY') -> dict:
        invested_capital_dict = self._parse_to_timescaled_dict(collection, keys, timescale)
        keys = get_list(invested_capital_dict)
        if timescale == 'YoY':
            invested_capital_dict['TotalAssets'] = [value / 4 for value in invested_capital_dict['TotalAssets']]
            invested_capital_dict['AccountsPayable'] = [value / 4 for value in invested_capital_dict['AccountsPayable']]
            invested_capital_dict['AccruedLiabilitiesAndOther'] = [value / 4 for value in invested_capital_dict['AccruedLiabilitiesAndOther']]
            invested_capital_dict['CashAndCashEquivalents'] = [value / 4 for value in invested_capital_dict['CashAndCashEquivalents']]
            invested_capital_dict['TotalCurrentAssets'] = [value / 4 for value in invested_capital_dict['TotalCurrentAssets']]
            invested_capital_dict['TotalCurrentLiabilities'] = [value / 4 for value in invested_capital_dict['TotalCurrentLiabilities']]
        invested_capital_df = pd.DataFrame.from_dict(invested_capital_dict)
        invested_capital_df.insert(loc= 0, column= 'InvestedCapital', value= invested_capital_df[keys[0]] - invested_capital_df[keys[1]] - invested_capital_df[keys[2]] - invested_capital_df[keys[3]] - [np.max([0, i]) for i in invested_capital_df[keys[5]] - invested_capital_df[keys[4]] + invested_capital_df[keys[3]]])
        return dict_values_to_list_values_in_dict(invested_capital_df.to_dict())
    
    def get_total_assets(self, collection = 'balance_sheet', keys: list = ['TotalAssets', 'date'], timescale: str = 'YoY') -> dict:
        return super().get_total_assets(collection, keys, timescale)
    
    def get_return_on_assets(self, collection: list = ['statement_operations', 'balance_sheet'], keys: list = ['NetIncome', 'TotalAssets', 'date'], timescale: str = 'YoY') -> dict:
        return super().get_return_on_assets(collection, keys, timescale)
    
    def get_return_on_equity(self, collection: list = ['statement_operations', 'balance_sheet'], keys: list = ['NetIncome', 'TotalStockholdersEquity', 'date'], timescale: str = 'YoY') -> dict:
        return super().get_return_on_equity(collection, keys, timescale)
    
    def get_fcf_roic(self, timescale = 'YoY') -> dict:
        # Get FcF and Invested capital dictionaries.
        fcf_dict = self.get_fcf(timescale = timescale)
        invested_capital_dict = self.get_invested_capital(timescale = timescale)
        #Join into single ROIC dict.
        if timescale == 'YoY':
            fcf_dict.pop('Year')
        elif timescale == 'TTM' or 'QoQ':
            fcf_dict.pop('date')
        else:
            raise TypeError('Timescale specified is not contemplated. Please enter "YoY" or "TTM"')
        fcf_invested_capital_dict = fcf_dict | invested_capital_dict
        # Create Ratio (FcF/InvestedCapital) key and return.
        roic_dict = self._add_ratio_metric_to_dict(['FcF', 'InvestedCapital'], fcf_invested_capital_dict)
        return roic_dict
    
    def _get_nopat(self, collection = 'statement_operations', keys: list = ['IncomeFromOperations', 'IncomeBeforeIncomeTaxes', 'ProvisionForIncomeTaxes', 'date'], timescale: str = 'YoY') -> dict:
        """ Private getter method for NOPAT dictionary.

        Args:
            collection (str, optional): _description_. Defaults to 'statement_operations'.
            keys (dict, optional): _description_. Defaults to {'IncomeFromOperations', 'IncomeBeforeIncomeTaxes', 'ProvisionForIncomeTaxes', 'date'}.
            timescale (str, optional): _description_. Defaults to 'YoY'.

        Returns:
            dict: _description_
        """
        nopact_dict = self._parse_to_timescaled_dict(collection, keys, timescale)
        nopat_df = pd.DataFrame.from_dict(nopact_dict)
        nopat_df.insert(loc = 0, column= 'NOPAT', value= nopat_df[keys[0]] * (1 - (nopat_df[keys[2]] / nopat_df[keys[1]])))
        nopat_df.drop([keys[0], keys[1], keys[2]], axis= 1, inplace=True)
        return dict_values_to_list_values_in_dict(nopat_df.to_dict())

    def get_nopat_roic(self, timescale: str = 'YoY') -> dict:
        nopat_dict = self._get_nopat(timescale = timescale) # NOPAT; date
        invested_capital_dict = self.get_invested_capital(timescale = timescale) # invested capital; date
        #Join into single ROIC dict.
        if timescale == 'YoY':
            nopat_dict.pop('Year')
        elif timescale == 'TTM' or 'QoQ':
            nopat_dict.pop('date')
        else:
            raise TypeError('Timescale specified is not contemplated. Please enter "YoY" or "TTM"')
        nopat_roic_dict = nopat_dict | invested_capital_dict
        return self._add_ratio_metric_to_dict(['NOPAT', 'InvestedCapital'], nopat_roic_dict)

    # TODO: override method.
    def get_wacc(self, collection, keys: list = [], timescale: str = 'YoY') -> dict:
        return super().get_wacc(collection, keys, timescale)


    # EQUITY STRUCTURE
    def get_outstanding_shares(self, collection = 'statement_operations', keys: list = ['WeightedAverageSharesDiluted', 'WeightedAverageSharesBasic', 'date']) -> dict:
        return super().get_outstanding_shares(collection, keys)

    # PRICE FORECAST
    def projected_fcf(self, timescale = 'QoQ') -> dict:
        return super().projected_fcf(timescale)

tesla = TeslaFinancials()
data = tesla._get_rate_invested_capital(timescale='QoQ')
print(data)