from dataclasses import dataclass

from igRestApiClient.helper.TypeConverter import *
from igRestApiClient.model.Market import Market
from igRestApiClient.model.Position import Position


@dataclass
class PositionElement:
    position: Position
    market: Market

    @staticmethod
    def from_dict(obj: Any) -> 'PositionElement':
        assert isinstance(obj, dict)
        position = Position.from_dict(obj.get("position"))
        market = Market.from_dict(obj.get("market"))
        return PositionElement(position, market)

    def to_dict(self) -> dict:
        result: dict = {"position": to_class(Position, self.position), "market": to_class(Market, self.market)}
        return result


@dataclass
class Positions:
    positions: List[PositionElement]

    @staticmethod
    def from_dict(obj: Any) -> 'Positions':
        assert isinstance(obj, dict)
        positions = from_list(PositionElement.from_dict, obj.get("positions"))
        return Positions(positions)

    def to_dict(self) -> dict:
        result: dict = {"positions": from_list(lambda x: to_class(PositionElement, x), self.positions)}
        return result


def positions_from_dict(s: Any) -> Positions:
    return Positions.from_dict(s)


def positions_to_dict(x: Positions) -> Any:
    return to_class(Positions, x)
