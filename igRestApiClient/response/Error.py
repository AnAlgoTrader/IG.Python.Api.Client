from dataclasses import dataclass
from igRestApiClient.helper.TypeConverter import *


@dataclass
class Error:
    error_code: str

    @staticmethod
    def from_dict(obj: Any) -> 'Error':
        assert isinstance(obj, dict)
        error_code = from_str(obj.get("errorCode"))
        return Error(error_code)

    def to_dict(self) -> dict:
        result: dict = {"errorCode": from_str(self.error_code)}
        return result


def error_from_dict(s: Any) -> Error:
    return Error.from_dict(s)


def error_to_dict(x: Error) -> Any:
    return to_class(Error, x)
