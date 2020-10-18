from dataclasses import dataclass
from client.helper.TypeConverter import *
from client.model.Balance import Balance


@dataclass
class Account:
    account_id: str
    account_name: str
    account_alias: None
    status: str
    account_type: str
    preferred: bool
    balance: Balance
    currency: str
    can_transfer_from: bool
    can_transfer_to: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Account':
        assert isinstance(obj, dict)
        account_id = from_str(obj.get("accountId"))
        account_name = from_str(obj.get("accountName"))
        account_alias = from_none(obj.get("accountAlias"))
        status = from_str(obj.get("status"))
        account_type = from_str(obj.get("accountType"))
        preferred = from_bool(obj.get("preferred"))
        balance = Balance.from_dict(obj.get("balance"))
        currency = from_str(obj.get("currency"))
        can_transfer_from = from_bool(obj.get("canTransferFrom"))
        can_transfer_to = from_bool(obj.get("canTransferTo"))
        return Account(account_id, account_name, account_alias, status,
                       account_type, preferred, balance, currency, can_transfer_from, can_transfer_to)

    def to_dict(self) -> dict:
        result: dict = {"accountId": from_str(self.account_id), "accountName": from_str(self.account_name),
                        "accountAlias": from_none(self.account_alias), "status": from_str(self.status),
                        "accountType": from_str(self.account_type), "preferred": from_bool(self.preferred),
                        "balance": to_class(Balance, self.balance), "currency": from_str(self.currency),
                        "canTransferFrom": from_bool(self.can_transfer_from),
                        "canTransferTo": from_bool(self.can_transfer_to)}
        return result
