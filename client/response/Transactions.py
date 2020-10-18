from dataclasses import dataclass
from client.helper.TypeConverter import *
from client.model.Metadata import Metadata
from client.model.Transaction import Transaction


@dataclass
class Transactions:
    transactions: List[Transaction]
    metadata: Metadata

    @staticmethod
    def from_dict(obj: Any) -> 'Transactions':
        assert isinstance(obj, dict)
        transactions = from_list(Transaction.from_dict, obj.get("transactions"))
        metadata = Metadata.from_dict(obj.get("metadata"))
        return Transactions(transactions, metadata)

    def to_dict(self) -> dict:
        result: dict = {"transactions": from_list(lambda x: to_class(Transaction, x), self.transactions),
                        "metadata": to_class(Metadata, self.metadata)}
        return result


def transactions_from_dict(s: Any) -> Transactions:
    return Transactions.from_dict(s)


def transactions_to_dict(x: Transactions) -> Any:
    return to_class(Transactions, x)
