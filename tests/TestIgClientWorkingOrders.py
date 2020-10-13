import unittest
import inspect
from client.IgClient import IgClient
from client.model.CreateWorkingOrderRequest import CreateWorkingOrderRequest


def print_test_result(caller, result):
    print("-------------------------", end="\n")
    print("test: " + caller, end="\n")
    print("-------------------------", end="\n")
    print("result:" + result, end="\n\n")


class TestIgClientWorkingOrders(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIgClientWorkingOrders, self).__init__(*args, **kwargs)
        self.client = IgClient()
        self.assertEqual(self.client.environment, "demo", "Client not connected to the demo environment")

    def test_token(self):
        self.assertNotEqual(self.client.token, "not authenticated", "Authentication error")
        print_test_result(inspect.stack()[0][0].f_code.co_name, self.client.token)

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
