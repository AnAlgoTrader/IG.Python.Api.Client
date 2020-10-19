from dataclasses import dataclass
from helper.TypeConverter import *
from model.enum.Period import Period
from model.enum.Status import Status


@dataclass
class Activity:
    date: datetime
    epic: str
    period: Period
    deal_id: str
    channel: str
    activity_type: str
    status: Status
    description: str
    details: None

    @staticmethod
    def from_dict(obj: Any) -> 'Activity':
        assert isinstance(obj, dict)
        date = from_datetime(obj.get("date"))
        epic = from_str(obj.get("epic"))
        period = Period(obj.get("period"))
        deal_id = from_str(obj.get("dealId"))
        channel = from_str(obj.get("channel"))
        activity_type = from_str(obj.get("type"))
        status = Status(obj.get("status"))
        description = from_str(obj.get("description"))
        details = from_none(obj.get("details"))
        return Activity(date, epic, period, deal_id, channel, activity_type, status, description, details)

    def to_dict(self) -> dict:
        result: dict = {"date": self.date.isoformat(), "epic": self.epic,
                        "period": to_enum(Period, self.period), "dealId": from_str(self.deal_id),
                        "channel": self.channel, "type": self.activity_type,
                        "status": to_enum(Status, self.status), "description": from_str(self.description),
                        "details": from_none(self.details)}
        return result
