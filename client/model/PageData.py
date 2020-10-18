from dataclasses import dataclass
from client.helper.TypeConverter import *


@dataclass
class PageData:
    page_size: int
    page_number: int
    total_pages: int

    @staticmethod
    def from_dict(obj: Any) -> 'PageData':
        assert isinstance(obj, dict)
        page_size = from_int(obj.get("pageSize"))
        page_number = from_int(obj.get("pageNumber"))
        total_pages = from_int(obj.get("totalPages"))
        return PageData(page_size, page_number, total_pages)

    def to_dict(self) -> dict:
        result: dict = {"pageSize": from_int(self.page_size), "pageNumber": from_int(self.page_number),
                        "totalPages": from_int(self.total_pages)}
        return result
