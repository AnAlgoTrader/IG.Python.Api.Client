from dataclasses import dataclass
from igRestApiClient.helper.TypeConverter import *


@dataclass
class AccountInfo:
    balance: float
    deposit: float
    profit_loss: float
    available: float

    @staticmethod
    def from_dict(obj: Any) -> 'AccountInfo':
        assert isinstance(obj, dict)
        balance = from_float(obj.get("balance"))
        deposit = from_float(obj.get("deposit"))
        profit_loss = from_float(obj.get("profitLoss"))
        available = from_float(obj.get("available"))
        return AccountInfo(balance, deposit, profit_loss, available)

    def to_dict(self) -> dict:
        result: dict = {"balance": to_float(self.balance), "deposit": to_float(self.deposit),
                        "profitLoss": to_float(self.profit_loss), "available": to_float(self.available)}
        return result
