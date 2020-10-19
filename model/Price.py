from dataclasses import dataclass
from helper.TypeConverter import *


@dataclass
class PriceValue:
    bid: float
    ask: float
    last_traded: None

    @staticmethod
    def from_dict(obj: Any) -> 'PriceValue':
        assert isinstance(obj, dict)
        bid = from_float(obj.get("bid"))
        ask = from_float(obj.get("ask"))
        last_traded = from_none(obj.get("lastTraded"))
        return PriceValue(bid, ask, last_traded)

    def to_dict(self) -> dict:
        result: dict = {"bid": to_float(self.bid), "ask": to_float(self.ask), "lastTraded": from_none(self.last_traded)}
        return result


@dataclass
class Price:
    snapshot_time: str
    snapshot_time_utc: datetime
    open_price: PriceValue
    close_price: PriceValue
    high_price: PriceValue
    low_price: PriceValue
    last_traded_volume: int

    @staticmethod
    def from_dict(obj: Any) -> 'Price':
        assert isinstance(obj, dict)
        snapshot_time = from_str(obj.get("snapshotTime"))
        snapshot_time_utc = from_datetime(obj.get("snapshotTimeUTC"))
        open_price = PriceValue.from_dict(obj.get("openPrice"))
        close_price = PriceValue.from_dict(obj.get("closePrice"))
        high_price = PriceValue.from_dict(obj.get("highPrice"))
        low_price = PriceValue.from_dict(obj.get("lowPrice"))
        last_traded_volume = from_int(obj.get("lastTradedVolume"))
        return Price(snapshot_time, snapshot_time_utc, open_price, close_price, high_price, low_price,
                     last_traded_volume)

    def to_dict(self) -> dict:
        result: dict = {"snapshotTime": from_str(self.snapshot_time),
                        "snapshotTimeUTC": self.snapshot_time_utc.isoformat(),
                        "openPrice": to_class(PriceValue, self.open_price),
                        "closePrice": to_class(PriceValue, self.close_price),
                        "highPrice": to_class(PriceValue, self.high_price),
                        "lowPrice": to_class(PriceValue, self.low_price),
                        "lastTradedVolume": from_int(self.last_traded_volume)}
        return result
