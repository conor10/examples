import unittest

import numpy.testing as ntest
import pandas as pd

import model_validation.volatility as volatility


FILENAME = 'data/AAPL_std_dev.xlsx'


class TestVolatility(unittest.TestCase):
    def setUp(self):
        self.xls_file = pd.ExcelFile(FILENAME)
        self.data = self.xls_file.parse('AAPL Std Dev',
                                   header=0, index_col=0, parse_cols='A:J')
        # We want to reverse our series so the first index is the oldest
        # entry not newest
        self.data.sort_index(inplace=True)

    def test_population_std_dev(self):
        vol30 = volatility.population_std_dev(self.data['Adj Close'], 30)
        ntest.assert_array_almost_equal(self.data['30 Day Vol'], vol30)

        vol60 = volatility.population_std_dev(self.data['Adj Close'], 60)
        ntest.assert_array_almost_equal(self.data['60 Day Vol'], vol60)

    def test_pandas_std_dev(self):
        vol = volatility.pandas_std_dev(self.data['Adj Close'], 30)
        ntest.assert_array_almost_equal(self.data['30 Day Vol'], vol)

        vol = volatility.pandas_std_dev(self.data['Adj Close'], 60)
        ntest.assert_array_almost_equal(self.data['60 Day Vol'], vol)

if __name__ == '__main__':
    unittest.main()
