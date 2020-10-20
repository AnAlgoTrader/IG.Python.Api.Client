from dataclasses import dataclass
from igRestApiClient.helper.TypeConverter import *


@dataclass
class IGApiError:
    error_code: str

    @staticmethod
    def from_dict(obj: Any) -> 'IGApiError':
        assert isinstance(obj, dict)
        error_code = from_str(obj.get("errorCode"))
        return IGApiError(error_code)

    def to_dict(self) -> dict:
        result: dict = {"errorCode": from_str(self.error_code)}
        return result


def error_from_dict(s: Any) -> IGApiError:
    return IGApiError.from_dict(s)


def error_to_dict(x: IGApiError) -> Any:
    return to_class(IGApiError, x)
