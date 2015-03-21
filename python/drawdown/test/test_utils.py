import unittest

import numpy as np
from numpy.testing import utils as np_utils


import drawdown.utils as utils


class TestUtils(unittest.TestCase):

    def test_lag(self):
        np_utils.assert_array_equal(
            np.array([0, 1, 2, 3, 4]),
            utils.lag(np.array([1, 2, 3, 4, 5])))

    def test_calculate_max_drawdown(self):
        returns = np.array(
            [0.1, 0.2, -0.1, -0.2, 0.1, -0.2, 0.1, 0.1, 0.1, 0.1, 0.3])
        compound_returns = (1. + returns).cumprod() - 1.
        max_dd, max_duration, dd_offset, duration_offset = \
            utils.calculate_max_drawdown(compound_returns)
        self.assertAlmostEqual(-0.3664, max_dd)
        self.assertEqual(8, max_duration)
        self.assertEqual(5, dd_offset)
        self.assertEqual(9, duration_offset)