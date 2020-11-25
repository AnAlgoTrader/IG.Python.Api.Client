from dataclasses import dataclass
from typing import Optional, Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class ClosePositionResponse:
    deal_reference: Optional[str] = None
    error_code: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ClosePositionResponse':
        assert isinstance(obj, dict)
        deal_reference = from_union([from_str, from_none], obj.get("dealReference"))
        error_code = from_union([from_str, from_none], obj.get("errorCode"))
        return ClosePositionResponse(deal_reference, error_code)

    def to_dict(self) -> dict:
        result: dict = {"dealReference": from_union([from_str, from_none], self.deal_reference),
                        "errorCode": from_union([from_str, from_none], self.error_code)}
        return result


def close_position_response_from_dict(s: Any) -> ClosePositionResponse:
    return ClosePositionResponse.from_dict(s)


def close_position_response_to_dict(x: ClosePositionResponse) -> Any:
    return to_class(ClosePositionResponse, x)
