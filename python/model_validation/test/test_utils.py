import unittest

import numpy as np
from numpy.testing import utils as np_utils

import model_validation.utils as utils


class TestUtils(unittest.TestCase):
    def test_lag(self):
        np_utils.assert_array_equal(
            np.array([0, 1, 2, 3, 4]),
            utils.lag(np.array([1, 2, 3, 4, 5])))

    def test_lag_nan(self):
        np_utils.assert_array_equal(
            np.array([np.NAN, 1, 2, 3, 4]),
            utils.lag(np.array([1., 2., 3., 4., 5.]), np.NAN))


if __name__ == '__main__':
    unittest.main()
