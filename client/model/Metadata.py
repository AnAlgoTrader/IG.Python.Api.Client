from dataclasses import dataclass

from client.model.PageData import PageData
from client.helper.TypeConverter import *


@dataclass
class Metadata:
    size: int
    page_data: PageData

    @staticmethod
    def from_dict(obj: Any) -> 'Metadata':
        assert isinstance(obj, dict)
        size = from_int(obj.get("size"))
        page_data = PageData.from_dict(obj.get("pageData"))
        return Metadata(size, page_data)

    def to_dict(self) -> dict:
        result: dict = {"size": from_int(self.size), "pageData": to_class(PageData, self.page_data)}
        return result
