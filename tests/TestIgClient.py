import os
import datetime
import inspect
import json
import unittest

from IgRestClient import IgRestClient
from model.Resolution import Resolution
from request.CreateWorkingOrderRequest import CreateWorkingOrderRequest
from pprint import pprint


def print_test_result(caller, result):
    print("-------------------------", end="\n")
    print("test: " + caller, end="\n")
    print("-------------------------", end="\n")
    print("result:" + result, end="\n\n")


def print_test_header(caller):
    print("-------------------------", end="\n")
    print("test: " + caller, end="\n")
    print("-------------------------", end="\n")


class TestIgClient(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestIgClient, self).__init__(*args, **kwargs)
        creds_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'auth.personal.json')
        with open(creds_path) as json_file:
            creds = json.load(json_file)
        self.client = IgRestClient(creds)
        self.assertEqual(self.client.environment, "demo", "Client not connected to the demo environment")

    def test_token(self):
        self.assertNotEqual(self.client.authentication.token, "not authenticated", "Authentication error")
        print_test_header(inspect.stack()[0][0].f_code.co_name)
        print(self.client.authentication.date)
        print("token:" + self.client.authentication.token)

    def test_get_positions(self):
        response = self.client.get_positions()
        print_test_header(inspect.stack()[0][0].f_code.co_name)
        for position in response.positions:
            pprint(vars(position))

    def test_get_accounts(self):
        response = self.client.get_accounts()
        print_test_header(inspect.stack()[0][0].f_code.co_name)
        for account in response.accounts:
            pprint(vars(account))

    def test_get_transactions(self):
        response = self.client.get_transactions(datetime.datetime(2020, 10, 1))
        print_test_header(inspect.stack()[0][0].f_code.co_name)
        for transaction in response.transactions:
            pprint(vars(transaction))

    def test_get_activities(self):
        response = self.client.get_activities(datetime.datetime(2020, 10, 1))
        print_test_header(inspect.stack()[0][0].f_code.co_name)
        for activity in response.activities:
            pprint(vars(activity))

    def test_get_historical_prices(self):
        response = self.client.get_historical_prices('IX.D.FTSE.DAILY.IP', Resolution.DAY,
                                                     datetime.datetime(2020, 10, 1), datetime.datetime(2020, 10, 15))
        print_test_header(inspect.stack()[0][0].f_code.co_name)
        for price in response.prices:
            pprint(vars(price))

    def test_create_order(self):
        create_working_order_request = CreateWorkingOrderRequest()
        create_working_order_request.epic = "CS.D.GBPUSD.TODAY.IP"
        create_working_order_request.direction = "BUY"
        create_working_order_request.expiry = "DFB"
        create_working_order_request.size = "1"
        create_working_order_request.timeInForce = "GOOD_TILL_CANCELLED"
        create_working_order_request.currencyCode = "GBP"
        create_working_order_request.guaranteedStop = False
        create_working_order_request.type = "LIMIT"
        create_working_order_request.level = "11450"
        data = self.client.create_working_order(create_working_order_request)
        self.assertNotEqual(bool(data), False, "No response retrieved")
        deal_reference = data['dealReference']
        data = self.client.get_trade_confirm(deal_reference)
        print_test_result(inspect.stack()[0][0].f_code.co_name, data['dealStatus'])

    def test_create_order_limit_stop(self):
        create_working_order_request = CreateWorkingOrderRequest()
        create_working_order_request.epic = "CS.D.GBPUSD.TODAY.IP"
        create_working_order_request.direction = "BUY"
        create_working_order_request.expiry = "DFB"
        create_working_order_request.size = "1"
        create_working_order_request.timeInForce = "GOOD_TILL_CANCELLED"
        create_working_order_request.currencyCode = "GBP"
        create_working_order_request.guaranteedStop = False
        create_working_order_request.type = "LIMIT"
        create_working_order_request.level = "11450"
        create_working_order_request.stopLevel = "11350"
        create_working_order_request.limitLevel = "11550"
        data = self.client.create_working_order(create_working_order_request)
        self.assertNotEqual(bool(data), False, "No response retrieved")
        deal_reference = data['dealReference']
        data = self.client.get_trade_confirm(deal_reference)
        print_test_result(inspect.stack()[0][0].f_code.co_name, data['dealStatus'])


if __name__ == '__main__':
    unittest.main()
