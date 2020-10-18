from dataclasses import dataclass

from client.helper.TypeConverter import *
from client.model.enum.Expiry import Expiry
from client.model.enum.InstrumentType import InstrumentType
from client.model.enum.MarketStatus import MarketStatus


@dataclass
class Market:
    instrument_name: str
    expiry: Expiry
    epic: str
    instrument_type: InstrumentType
    lot_size: float
    high: float
    low: float
    percentage_change: float
    net_change: float
    bid: float
    offer: float
    update_time: datetime
    update_time_utc: datetime
    delay_time: int
    streaming_prices_available: bool
    market_status: MarketStatus
    scaling_factor: int

    @staticmethod
    def from_dict(obj: Any) -> 'Market':
        assert isinstance(obj, dict)
        instrument_name = from_str(obj.get("instrumentName"))
        expiry = Expiry(obj.get("expiry"))
        epic = from_str(obj.get("epic"))
        instrument_type = InstrumentType(obj.get("instrumentType"))
        lot_size = from_float(obj.get("lotSize"))
        high = from_float(obj.get("high"))
        low = from_float(obj.get("low"))
        percentage_change = from_float(obj.get("percentageChange"))
        net_change = from_float(obj.get("netChange"))
        bid = from_float(obj.get("bid"))
        offer = from_float(obj.get("offer"))
        update_time = from_datetime(obj.get("updateTime"))
        update_time_utc = from_datetime(obj.get("updateTimeUTC"))
        delay_time = from_int(obj.get("delayTime"))
        streaming_prices_available = from_bool(obj.get("streamingPricesAvailable"))
        market_status = MarketStatus(obj.get("marketStatus"))
        scaling_factor = from_int(obj.get("scalingFactor"))
        return Market(instrument_name, expiry, epic, instrument_type, lot_size, high, low, percentage_change,
                      net_change, bid, offer, update_time, update_time_utc, delay_time, streaming_prices_available,
                      market_status, scaling_factor)

    def to_dict(self) -> dict:
        result: dict = {"instrumentName": from_str(self.instrument_name), "expiry": to_enum(Expiry, self.expiry),
                        "epic": from_str(self.epic), "instrumentType": to_enum(InstrumentType, self.instrument_type),
                        "lotSize": from_int(self.lot_size), "high": to_float(self.high), "low": to_float(self.low),
                        "percentageChange": from_int(self.percentage_change), "netChange": from_int(self.net_change),
                        "bid": to_float(self.bid), "offer": to_float(self.offer),
                        "updateTime": self.update_time.isoformat(), "updateTimeUTC": self.update_time_utc.isoformat(),
                        "delayTime": from_int(self.delay_time),
                        "streamingPricesAvailable": from_bool(self.streaming_prices_available),
                        "marketStatus": to_enum(MarketStatus, self.market_status),
                        "scalingFactor": from_int(self.scaling_factor)}
        return result
