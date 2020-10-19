import os

import requests
import datetime
import json

from client.model.Resolution import Resolution
from client.response.Accounts import accounts_from_dict
from client.response.Positions import positions_from_dict
from client.response.Transactions import transactions_from_dict
from client.response.Activities import activities_from_dict
from client.response.Prices import prices_from_dict
from client.response.Authentication import authentication_from_dict


class IgRestClient:
    def __init__(self, creds):
        self.__set_uris__()
        self.__set_base_uri__(creds)
        self.__authenticate__(creds)

    def __authenticate__(self, creds):
        auth_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'auth.response.json')
        if os.path.isfile(auth_path):
            pass
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
            self.token = 'not authenticated'
        else:
            self.authentication = authentication_from_dict(json.loads(response.text))
            self.authentication.token = response.headers['X-SECURITY-TOKEN']
            self.authentication.api_key = key
            self.authentication.cst = response.headers['CST']

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
                   "X-SECURITY-TOKEN": self.token}
        response = requests.get(self.base_uri + url, headers=headers)
        if response.status_code != 200:
            raise Exception("invalid response calling " + self.base_uri + url)
        else:
            return response.text

    def __post_response__(self, url, request, method, version):
        if method is None:
            headers = {'Content-type': 'application/json',
                       "X-IG-API-KEY": self.authentication.api_key,
                       "VERSION": version, "CST": self.authentication.cst,
                       "X-SECURITY-TOKEN": self.token}
        else:
            headers = {'Content-type': 'application/json',
                       "X-IG-API-KEY": self.authentication.api_key,
                       "VERSION": version,
                       "CST": self.authentication.cst,
                       "X-SECURITY-TOKEN": self.token,
                       "_method": method}
        json_content = json.dumps(request.__dict__)
        response = requests.post(self.base_uri + url, headers=headers, data=json_content)
        if response.status_code != 200:
            raise Exception("invalid response calling " + self.base_uri + url)
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
        return prices_from_dict(json.loads(response))

    def create_working_order(self, request):
        return self.__post_response__(self.WORKING_ORDERS_URI, request, None, "2")

    def get_trade_confirm(self, deal_reference):
        url = self.TRADE_CONFIRM_URI + "/" + deal_reference
        return self.__get_response__(url, "1")
