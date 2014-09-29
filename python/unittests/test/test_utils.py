import datetime as dt
import unittest

import numpy as np
from numpy.testing import utils as np_utils

import utils


class TestUtils(unittest.TestCase):
    def test_day_count(self):
        start = dt.datetime(2014, 7, 10)
        end = dt.datetime(2014, 8, 10)
        self.assertEqual(31, utils.day_count(start, end))

    def test_ffill(self):
        data = np.array([0, np.nan, 1, np.nan, np.nan, -1, np.nan])
        np_utils.assert_array_equal(
            np.array([0, 0, 1, 1, 1, -1, -1]),
            utils.ffill(data))


if __name__ == '__main__':
    unittest.main()

