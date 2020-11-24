import os

import dateutil
import requests
import datetime
import json

from igRestApiClient.model.Resolution import Resolution
from igRestApiClient.model.enum.OrderType import OrderType
from igRestApiClient.model.enum.Currency import Currency
from igRestApiClient.model.enum.Expiry import Expiry
from igRestApiClient.request.OpenMarketPositionRequest import OpenMarketPositionRequest
from igRestApiClient.response.Accounts import accounts_from_dict
from igRestApiClient.response.Positions import positions_from_dict
from igRestApiClient.response.Transactions import transactions_from_dict
from igRestApiClient.response.Activities import activities_from_dict
from igRestApiClient.response.Prices import prices_from_dict
from igRestApiClient.response.Authentication import authentication_from_dict
from igRestApiClient.response.Authentication import authentication_to_dict
from igRestApiClient.response.IGApiError import error_from_dict


class IgRestClient:
    def __init__(self, creds, auth_response_file):
        self.__set_uris__()
        self.__set_base_uri__(creds)
        self.auth_response_file = auth_response_file
        self.__authenticate__(creds)

    def __authenticate__(self, creds):
        auth_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.auth_response_file)
        if os.path.isfile(auth_path):
            with open(auth_path) as json_file:
                auth = authentication_from_dict(json.loads(json_file.read()))
            diff_seconds = (datetime.datetime.now() - dateutil.parser.parse(auth.date)).seconds
            if diff_seconds > (5 * 3600):  # token expires in 5 hours (6 hours are given by the server)
                self.__auth__(creds)
            else:
                self.authentication = auth
        else:
            self.__auth__(creds)

    def __auth__(self, creds):
        username = creds['ig.username']
        password = creds['ig.password']
        key = creds['ig.key']
        headers = {"X-IG-API-KEY": key, "VERSION": "2"}
        data = {"identifier": username, "password": password}
        response = requests.post(self.base_uri + self.SESSION_URI, json=data, headers=headers)
        if response.status_code != 200:
            self.authentication.token = 'not authenticated'
        else:
            self.authentication = authentication_from_dict(json.loads(response.text))
            self.authentication.token = response.headers['X-SECURITY-TOKEN']
            self.authentication.api_key = key
            self.authentication.cst = response.headers['CST']
            self.authentication.date = datetime.datetime.now()
            auth_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.auth_response_file)
            with open(auth_path, 'w') as file_to_write:
                file_to_write.write(json.dumps(authentication_to_dict(self.authentication)))

    def __set_base_uri__(self, data):
        self.environment = data['ig.environment']
        if self.environment == "live":
            self.base_uri = 'https://liveapi.ig.com'
        elif self.environment == "demo":
            self.base_uri = 'https://demo-api.ig.com'
        else:
            self.base_uri = 'not set'

    def __set_uris__(self):
        self.SESSION_URI = '/gateway/deal/session'
        self.ACCOUNTS_URI = '/gateway/deal/accounts'
        self.TRANSACTIONS_URI = '/gateway/deal/history/transactions'
        self.ACTIVITIES_URI = '/gateway/deal/history/activity'
        self.PRICES_URI = '/gateway/deal/prices'
        self.POSITIONS_OTC_URI = '/gateway/deal/positions/otc'
        self.POSITIONS_URI = '/gateway/deal/positions'
        self.WORKING_ORDERS_URI = '/gateway/deal/workingorders/otc'
        self.TRADE_CONFIRM_URI = "/gateway/deal/confirms"

    def __get_response__(self, url, version):
        headers = {"X-IG-API-KEY": self.authentication.api_key,
                   "VERSION": version,
                   "CST": self.authentication.cst,
                   "X-SECURITY-TOKEN": self.authentication.token}
        response = requests.get(self.base_uri + url, headers=headers)
        if response.status_code != 200:
            self.error = error_from_dict(json.loads(response.text))
            return None
        else:
            return response.text

    def __post_response__(self, url, request, method, version):
        if method is None:
            headers = {'Content-type': 'application/json',
                       "X-IG-API-KEY": self.authentication.api_key,
                       "VERSION": version, "CST": self.authentication.cst,
                       "X-SECURITY-TOKEN": self.authentication.token}
        else:
            headers = {'Content-type': 'application/json',
                       "X-IG-API-KEY": self.authentication.api_key,
                       "VERSION": version,
                       "CST": self.authentication.cst,
                       "X-SECURITY-TOKEN": self.authentication.token,
                       "_method": method}
        json_content = json.dumps(request.__dict__)
        response = requests.post(self.base_uri + url, headers=headers, data=json_content)
        if response.status_code != 200:
            message = ''.join(['invalid response calling ', self.base_uri + url, response.text])
            raise Exception(message)
        else:
            return json.loads(response.text)

    def get_positions(self):
        response = self.__get_response__(self.POSITIONS_URI, "2")
        return positions_from_dict(json.loads(response))

    def get_accounts(self):
        response = self.__get_response__(self.ACCOUNTS_URI, "1")
        return accounts_from_dict(json.loads(response))

    def get_transactions(self, from_date: datetime):
        url = [self.TRANSACTIONS_URI, '?from=', from_date.strftime("%Y-%m-%d")]
        response = self.__get_response__(''.join(url), "2")
        return transactions_from_dict(json.loads(response))

    def get_activities(self, from_date: datetime):
        url = [self.ACTIVITIES_URI, '?from=', from_date.strftime("%Y-%m-%d")]
        response = self.__get_response__(''.join(url), "3")
        return activities_from_dict(json.loads(response))

    def get_historical_prices(self, epic, resolution: Resolution, from_date: datetime, to_date: datetime):
        from_date_formatted = from_date.strftime("%Y-%m-%d") + 'T00%3A00%3A00'
        to_date_formatted = to_date.strftime("%Y-%m-%d") + 'T00%3A00%3A00'
        url = [self.PRICES_URI, '/', epic, '?resolution=', resolution.name,
               '&from=', from_date_formatted, '&to=', to_date_formatted]
        response = self.__get_response__(''.join(url), "3")
        if response is None:
            return self.error
        else:
            return prices_from_dict(json.loads(response))

    def open_market_position(self, epic, side, size):
        request = OpenMarketPositionRequest()
        request.epic = epic
        request.direction = side
        request.size = size
        request.expiry = Expiry.DFB
        request.orderType = OrderType.Market
        request.guaranteedStop = False
        request.trailingStop = False
        request.forceOpen = True
        request.currencyCode = Currency.GBP
        return self.__post_response__(self.POSITIONS_OTC_URI, request, None, "2")

    def create_working_order(self, request):
        return self.__post_response__(self.WORKING_ORDERS_URI, request, None, "2")

    def get_trade_confirm(self, deal_reference):
        url = self.TRADE_CONFIRM_URI + "/" + deal_reference
        return self.__get_response__(url, "1")
