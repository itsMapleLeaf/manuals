from dataclasses import dataclass

from .category import CategoryData
from .location import LocationData
from .item import ItemData


@dataclass
class ManualData:
    game: dict[str, object]
    items: list[ItemData]
    locations: list[LocationData]
    regions: dict[str, object]
    categories: dict[str, CategoryData]
    options: dict[str, object]
    meta: dict[str, object]
