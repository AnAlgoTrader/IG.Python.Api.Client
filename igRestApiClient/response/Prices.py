from dataclasses import dataclass
from igRestApiClient.helper.TypeConverter import *
from igRestApiClient.model.Price import Price


@dataclass
class Prices:
    prices: List[Price]
    instrument_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'Prices':
        assert isinstance(obj, dict)
        prices = from_list(Price.from_dict, obj.get("prices"))
        instrument_type = from_str(obj.get("instrumentType"))
        return Prices(prices, instrument_type)

    def to_dict(self) -> dict:
        result: dict = {"prices": from_list(lambda x: to_class(Price, x), self.prices),
                        "instrumentType": from_str(self.instrument_type)}
        return result


def prices_from_dict(s: Any) -> Prices:
    return Prices.from_dict(s)


def prices_to_dict(x: Prices) -> Any:
    return to_class(Prices, x)
