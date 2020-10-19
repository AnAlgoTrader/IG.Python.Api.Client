from dataclasses import dataclass
from helper.TypeConverter import *


@dataclass
class AuthenticationAccount:
    account_id: str
    account_name: str
    preferred: bool
    account_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'AuthenticationAccount':
        assert isinstance(obj, dict)
        account_id = from_str(obj.get("accountId"))
        account_name = from_str(obj.get("accountName"))
        preferred = from_bool(obj.get("preferred"))
        account_type = from_str(obj.get("accountType"))
        return AuthenticationAccount(account_id, account_name, preferred, account_type)

    def to_dict(self) -> dict:
        result: dict = {"accountId": from_str(self.account_id), "accountName": from_str(self.account_name),
                        "preferred": from_bool(self.preferred), "accountType": from_str(self.account_type)}
        return result
