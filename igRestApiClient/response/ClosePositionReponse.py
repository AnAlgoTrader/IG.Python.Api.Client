from dataclasses import dataclass
from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class ClosePositionResponse:
    deal_reference: str
    error_code: str

    @staticmethod
    def from_dict(obj: Any) -> 'ClosePositionResponse':
        assert isinstance(obj, dict)
        deal_reference = from_str(obj.get("dealReference"))
        error_code = from_str(obj.get("errorCode"))
        return ClosePositionResponse(deal_reference, error_code)

    def to_dict(self) -> dict:
        result: dict = {"dealReference": from_str(self.deal_reference), "errorCode": from_str(self.error_code)}
        return result


def close_position_response_from_dict(s: Any) -> ClosePositionResponse:
    return ClosePositionResponse.from_dict(s)


def close_position_response_to_dict(x: ClosePositionResponse) -> Any:
    return to_class(ClosePositionResponse, x)
