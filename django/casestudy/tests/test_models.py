from decimal import Decimal

from django.test import TestCase
from casestudy.models import Security
from django.contrib.auth.models import User
import json

class TestModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")


    def test_add_securities(self):
        data = {
            "ABC": "ABC Company",
            "XYZ": "XYZ Company",
        }
        Security.add_tickers(data)
        security = Security.objects.get(ticker="XYZ")
        self.assertEqual(security.name, "XYZ Company")

    def test_update_prices(self):
        data = {
            "ABC": "ABC Company",
            "XYZ": "XYZ Company",
        }
        Security.add_tickers(data)
        securities = dict((m.ticker, m) for m in Security.objects.all())
        updates = {
            'XYZ': 2.0
        }
        Security.update_prices(securities, updates)
        security = Security.objects.get(ticker="XYZ")
        self.assertEqual(security.last_price, Decimal("2.0"))

        updates['XYZ'] = 2.1
        Security.update_prices(securities, updates)
        security = Security.objects.get(ticker="XYZ")
        self.assertEqual(security.last_price, Decimal("2.1"))
