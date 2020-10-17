from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable


T = TypeVar("T")


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Balance:
    balance: float
    deposit: float
    profit_loss: float
    available: float

    @staticmethod
    def from_dict(obj: Any) -> 'Balance':
        assert isinstance(obj, dict)
        balance = from_float(obj.get("balance"))
        deposit = from_float(obj.get("deposit"))
        profit_loss = from_float(obj.get("profitLoss"))
        available = from_float(obj.get("available"))
        return Balance(balance, deposit, profit_loss, available)

    def to_dict(self) -> dict:
        result: dict = {"balance": to_float(self.balance), "deposit": to_float(self.deposit),
                        "profitLoss": to_float(self.profit_loss), "available": to_float(self.available)}
        return result


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


@dataclass
class Accounts:
    accounts: List[Account]

    @staticmethod
    def from_dict(obj: Any) -> 'Accounts':
        assert isinstance(obj, dict)
        accounts = from_list(Account.from_dict, obj.get("accounts"))
        return Accounts(accounts)

    def to_dict(self) -> dict:
        result: dict = {"accounts": from_list(lambda x: to_class(Account, x), self.accounts)}
        return result


def accounts_from_dict(s: Any) -> Accounts:
    return Accounts.from_dict(s)


def accounts_to_dict(x: Accounts) -> Any:
    return to_class(Accounts, x)
