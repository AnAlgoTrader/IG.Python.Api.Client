from dataclasses import dataclass
from client.helper.TypeConverter import *
from client.model.Transaction import Transaction


@dataclass
class Transactions:
    transactions: List[Transaction]

    @staticmethod
    def from_dict(obj: Any) -> 'Transactions':
        assert isinstance(obj, dict)
        transactions = from_list(Transaction.from_dict, obj.get("transactions"))
        return Transactions(transactions)

    def to_dict(self) -> dict:
        result: dict = {"transactions": from_list(lambda x: to_class(Transaction, x), self.transactions)}
        return result


def transactions_from_dict(s: Any) -> Transactions:
    return Transactions.from_dict(s)


def transactions_to_dict(x: Transactions) -> Any:
    return to_class(Transactions, x)
