import unittest

import numpy as np
from numpy.testing import utils as np_utils

import prices.bm as bm


class GBMTests(unittest.TestCase):
    def test_geometric_models(self):
        np.random.seed(10)

        periods = 1000
        price = 70.0
        mu = 0.05
        sigma = 0.3
        period_duration = 1.0

        np.random.seed(10)
        iterative_ret = bm.generate_gbm_prices(
            periods, price, mu, sigma, period_duration)
        np.random.seed(10)
        vectorised_ret = bm.generate_gbm_prices_vec(
            periods, price, mu, sigma, period_duration)

        # Equal to 6 decimal places
        np_utils.assert_array_almost_equal(iterative_ret, vectorised_ret)


if __name__ == '__main__':
    unittest.main()
