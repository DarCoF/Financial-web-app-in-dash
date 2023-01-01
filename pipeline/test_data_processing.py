# GLOBAL IMPORTS
import sys
import unittest
import pymongo
from pymongo import MongoClient
import pandas as pd

# LOCAL IMPORTS
sys.path.insert(0, "C:\\Users\\dario\\pet_projects\\tmts-oracle-app")
from data_processing import TeslaFinancials
from db.db_interface import CompanyDbInterface

# REVENUE
# TODO: test class TeslaFinancials. Fix bugs. After cleaning it up, couple front-end to back-end and populate graphs.
# - Test and debbug class
# - Couple front-end to back-end

class TestTeslaFinancials(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print('Start Testing')
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        print('Finish Testing')
        return super().tearDownClass()

    def setUp(self) -> None:
        self.tesla_financial = TeslaFinancials()
        return super().setUp()

    def tearDown(self) -> None:
        print('teardown \n')
        return super().tearDown()

    def test_get_revenue(self):
        self.assertEqual(type(self.tesla_financial.get_revenue()), dict)
        self.assertEqual(len(self.tesla_financial.get_revenue()['TotalRevenues']), 15)
        self.assertEqual(self.tesla_financial.get_revenue()['TotalRevenues'], [21454, 16934, 18756, 17719, 13757, 11958, 10389, 10744, 8771, 6036, 5985, 7384, 6303, 6350, 4541]
        )
        self.assertEqual(self.tesla_financial.get_revenue()['date'], ['3Q22', '2Q22', '1Q22', '4Q21', '3Q21', '2Q21', '1Q21', '4Q20', '3Q20', '2Q20', '1Q20', '4Q19', '3Q19', '2Q19', '1Q19']
        )
        self.assertDictEqual(self.tesla_financial.get_revenue(), {'TotalRevenues': [21454, 16934, 18756, 17719, 13757, 11958, 10389, 10744, 8771, 6036, 5985, 7384, 6303, 6350, 4541], 'date': ['3Q22', '2Q22', '1Q22', '4Q21', '3Q21', '2Q21', '1Q21', '4Q20', '3Q20', '2Q20', '1Q20', '4Q19', '3Q19', '2Q19', '1Q19']}
        )

if __name__ == '__main__':
    unittest.main()