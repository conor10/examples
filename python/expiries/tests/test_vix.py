import datetime as dt
import unittest

from expiries import vix


class VixTests(unittest.TestCase):
    def test_get_expiry_date_for_month(self):
        self.assertEqual(
            dt.date(2014, 12, 17),
            vix.get_expiry_date_for_month(dt.date(2014, 12, 1)))
        self.assertEqual(
            dt.date(2015, 1, 21),
            vix.get_expiry_date_for_month(dt.date(2015, 1, 1)))
        self.assertEqual(
            dt.date(2015, 2, 18),
            vix.get_expiry_date_for_month(dt.date(2015, 2, 1)))


if __name__ == '__main__':
    unittest.main()
