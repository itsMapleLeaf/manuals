from typing import Optional, Unpack

from .location import LocationArgs, LocationData, Requirement, Requires
from .item import ItemArgs, ItemData
from .category import CategoryArgs, CategoryData

requires = Requires()


class WorldSpec:
    items: list[ItemData] = []
    locations: list[LocationData] = []
    categories: dict[str, CategoryData] = {}

    @property
    def item_count(self) -> int:
        return sum(item.get("count", 0) for item in self.items)

    def item(self, name: str, **kwargs: Unpack[ItemArgs]) -> ItemData:
        item = ItemData(name=name, **kwargs)
        self.items += [item]
        return item

    def location(
        self,
        name: str,
        requires: Optional[str | Requirement] = None,
        **kwargs: Unpack[LocationArgs],
    ) -> LocationData:
        location = LocationData(name=name, **kwargs)

        if requires != None:
            location["requires"] = str(requires)

        self.locations += [location]
        return location

    def category(self, name: str, **kwargs: Unpack[CategoryArgs]) -> CategoryData:
        category = CategoryData(name=name, **kwargs)
        self.categories[name] = category
        return category
