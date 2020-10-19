from dataclasses import dataclass
from helper.TypeConverter import *
from model.Activity import Activity


@dataclass
class Activities:
    activities: List[Activity]

    @staticmethod
    def from_dict(obj: Any) -> 'Activities':
        assert isinstance(obj, dict)
        activities = from_list(Activity.from_dict, obj.get("activities"))
        return Activities(activities)

    def to_dict(self) -> dict:
        result: dict = {"activities": from_list(lambda x: to_class(Activity, x), self.activities)}
        return result


def activities_from_dict(s: Any) -> Activities:
    return Activities.from_dict(s)


def activities_to_dict(x: Activities) -> Any:
    return to_class(Activities, x)
