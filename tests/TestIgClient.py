import datetime
import inspect
import json
import unittest

from client.IgClient import IgClient
from client.model.Resolution import Resolution


def print_test_result(caller, result):
    print("-------------------------", end="\n")
    print("test: " + caller, end="\n")
    print("-------------------------", end="\n")
    print("result:" + result, end="\n\n")


class TestIgClient(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestIgClient, self).__init__(*args, **kwargs)
        self.client = IgClient()
        self.assertEqual(self.client.environment, "demo", "Client not connected to the demo environment")

    def test_token(self):
        self.assertNotEqual(self.client.token, "not authenticated", "Authentication error")
        print_test_result(inspect.stack()[0][0].f_code.co_name, self.client.token)

    def test_account(self):
        data = self.client.get_accounts()
        self.assertNotEqual(bool(data), False, "No account retrieved")
        print_test_result(inspect.stack()[0][0].f_code.co_name,
                          json.dumps(data['accounts'], indent=4, sort_keys=True))

    def test_transactions(self):
        data = self.client.get_transactions(datetime.datetime(2020, 7, 1))
        self.assertNotEqual(bool(data), False, "No transactions retrieved")
        print_test_result(inspect.stack()[0][0].f_code.co_name,
                          json.dumps(data['transactions'], indent=4, sort_keys=True))

    def test_activities(self):
        data = self.client.get_activities(datetime.datetime(2020, 7, 1))
        self.assertNotEqual(bool(data), False, "No activities retrieved")
        print_test_result(inspect.stack()[0][0].f_code.co_name,
                          json.dumps(data['activities'], indent=4, sort_keys=True))

    def test_prices(self):
        data = self.client.get_prices('IX.D.FTSE.DAILY.IP', Resolution.DAY, datetime.datetime(2020, 7, 20), datetime.datetime(2020, 7, 21))
        self.assertNotEqual(bool(data), False, "No prices retrieved")
        print_test_result(inspect.stack()[0][0].f_code.co_name,
                          json.dumps(data['prices'], indent=4, sort_keys=True))

    def test_positions(self):
        data = self.client.get_positions()
        self.assertNotEqual(bool(data), False, "No positions retrieved")
        print_test_result(inspect.stack()[0][0].f_code.co_name,
                          json.dumps(data['positions'], indent=4, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
