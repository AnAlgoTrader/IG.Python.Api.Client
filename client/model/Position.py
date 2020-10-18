from dataclasses import dataclass

from client.helper.TypeConverter import *
from client.model.enum.Currency import Currency
from client.model.enum.Direction import Direction


@dataclass
class Position:
    contract_size: float
    created_date: str
    created_date_utc: datetime
    deal_id: str
    deal_reference: str
    size: float
    direction: Direction
    limit_level: None
    level: float
    currency: Currency
    controlled_risk: bool
    stop_level: None
    trailing_step: None
    trailing_stop_distance: None
    limited_risk_premium: None

    @staticmethod
    def from_dict(obj: Any) -> 'Position':
        assert isinstance(obj, dict)
        contract_size = from_float(obj.get("contractSize"))
        created_date = from_str(obj.get("createdDate"))
        created_date_utc = from_datetime(obj.get("createdDateUTC"))
        deal_id = from_str(obj.get("dealId"))
        deal_reference = from_str(obj.get("dealReference"))
        size = from_float(obj.get("size"))
        direction = Direction(obj.get("direction"))
        limit_level = from_none(obj.get("limitLevel"))
        level = from_float(obj.get("level"))
        currency = Currency(obj.get("currency"))
        controlled_risk = from_bool(obj.get("controlledRisk"))
        stop_level = from_none(obj.get("stopLevel"))
        trailing_step = from_none(obj.get("trailingStep"))
        trailing_stop_distance = from_none(obj.get("trailingStopDistance"))
        limited_risk_premium = from_none(obj.get("limitedRiskPremium"))
        return Position(contract_size, created_date, created_date_utc, deal_id, deal_reference, size, direction,
                        limit_level, level, currency, controlled_risk, stop_level, trailing_step,
                        trailing_stop_distance, limited_risk_premium)

    def to_dict(self) -> dict:
        result: dict = {"contractSize": from_float(self.contract_size), "createdDate": from_str(self.created_date),
                        "createdDateUTC": self.created_date_utc.isoformat(), "dealId": from_str(self.deal_id),
                        "dealReference": from_str(self.deal_reference), "size": to_float(self.size),
                        "direction": to_enum(Direction, self.direction), "limitLevel": from_none(self.limit_level),
                        "level": to_float(self.level), "currency": to_enum(Currency, self.currency),
                        "controlledRisk": from_bool(self.controlled_risk), "stopLevel": from_none(self.stop_level),
                        "trailingStep": from_none(self.trailing_step),
                        "trailingStopDistance": from_none(self.trailing_stop_distance),
                        "limitedRiskPremium": from_none(self.limited_risk_premium)}
        return result
