from dataclasses import dataclass

from client.helper.TypeConverter import *
from client.model.enum.Currency import Currency
from client.model.enum.Period import Period
from client.model.enum.TransactionType import TransactionType


@dataclass
class Transaction:
    date: datetime
    date_utc: datetime
    open_date_utc: datetime
    instrument_name: str
    period: Period
    profit_and_loss: str
    transaction_type: TransactionType
    reference: str
    open_level: str
    close_level: str
    size: str
    currency: Currency
    cash_transaction: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Transaction':
        assert isinstance(obj, dict)
        date = from_datetime(obj.get("date"))
        date_utc = from_datetime(obj.get("dateUtc"))
        open_date_utc = from_datetime(obj.get("openDateUtc"))
        instrument_name = from_str(obj.get("instrumentName"))
        period = Period(obj.get("period"))
        profit_and_loss = from_str(obj.get("profitAndLoss"))
        transaction_type = TransactionType(obj.get("transactionType"))
        reference = from_str(obj.get("reference"))
        open_level = from_str(obj.get("openLevel"))
        close_level = from_str(obj.get("closeLevel"))
        size = obj.get("size")
        currency = Currency(obj.get("currency"))
        cash_transaction = from_bool(obj.get("cashTransaction"))
        return Transaction(date, date_utc, open_date_utc, instrument_name, period,
                           profit_and_loss, transaction_type, reference, open_level,
                           close_level, size, currency, cash_transaction)

    def to_dict(self) -> dict:
        result: dict = {"date": self.date.isoformat(), "dateUtc": self.date_utc.isoformat(),
                        "openDateUtc": self.open_date_utc.isoformat(), "instrumentName": from_str(self.instrument_name),
                        "period": to_enum(Period, self.period), "profitAndLoss": from_str(self.profit_and_loss),
                        "transactionType": to_enum(TransactionType, self.transaction_type),
                        "reference": from_str(self.reference), "openLevel": from_str(self.open_level),
                        "closeLevel": from_str(self.close_level), "size": self.size,
                        "currency": to_enum(Currency, self.currency),
                        "cashTransaction": from_bool(self.cash_transaction)}
        return result
