import json
import unittest

from services import price_service


class ServicesTest(unittest.TestCase):
    def setUp(self):
        self.app = price_service.app.test_client()

    def test_gbm(self):
        data = {
            'periods': 100,
            'startPrice': 70.0,
            'mu': 0.05,
            'sigma': 0.30,
            'delta': 1.0
        }

        response = self.app.get('/gbm', query_string=data)
        self.assertEqual(200, response.status_code)
        data = json.loads(response.get_data().decode('utf-8'))
        self.assertEqual(100, len(data['result']))
