from dataclasses import dataclass
from typing import Optional, Unpack

from .requires import Requirement
from .tables import WorldSpecDict, WorldSpecList
from .options import (
    ChoiceOptionArgs,
    ChoiceOptionData,
    ChoiceOptionSpec,
    OptionData,
    RangeOptionArgs,
    RangeOptionData,
    RangeOptionSpec,
    ToggleOptionArgs,
    ToggleOptionData,
    ToggleOptionSpec,
)
from .location import LocationArgs, LocationData, LocationSpec
from .item import ItemArgs, ItemData, ItemSpec
from .category import CategoryArgs, CategoryData, CategorySpec


@dataclass
class WorldSpec:
    name: str
    creator: str

    def __post_init__(self) -> None:
        self.item_table = WorldSpecList[ItemData, ItemSpec](
            "items", lambda _, data: ItemSpec(data)
        )
        self.location_table = WorldSpecDict[LocationData, LocationSpec](
            "locations", lambda _, data: LocationSpec(data)
        )
        self.category_table = WorldSpecDict[CategoryData, CategorySpec](
            "categories", CategorySpec
        )
        self.user_options: dict[str, OptionData] = {}

    @property
    def item_count(self) -> int:
        return sum(item.get("count", 1) for item in self.item_table.values)

    @property
    def items(self) -> list[ItemData]:
        return self.item_table.data

    def item(self, name: str, **kwargs: Unpack[ItemArgs]) -> ItemSpec:
        return self.item_table.add(name, ItemData(**kwargs, name=name))

    @property
    def locations(self) -> dict[str, LocationData]:
        return self.location_table.data

    def location(
        self,
        name: str,
        requires: Optional[str | Requirement] = None,
        **kwargs: Unpack[LocationArgs],
    ) -> LocationSpec:
        location = LocationData(name=name, **kwargs)

        if requires != None:
            location["requires"] = str(requires)

        return self.location_table.add(name, location)

    @property
    def categories(self) -> dict[str, CategoryData]:
        return self.category_table.data

    def category(self, name: str, **kwargs: Unpack[CategoryArgs]) -> CategorySpec:
        return self.category_table.add(name, CategoryData(**kwargs))

    def toggle_option(
        self, name: str, **kwargs: Unpack[ToggleOptionArgs]
    ) -> ToggleOptionSpec:
        self.user_options[name] = ToggleOptionData(**kwargs, type="Toggle")
        return ToggleOptionSpec(name, kwargs)

    def range_option(
        self, name: str, **kwargs: Unpack[RangeOptionArgs]
    ) -> RangeOptionSpec:
        self.user_options[name] = RangeOptionData(**kwargs, type="Range")
        return RangeOptionSpec(name, kwargs)

    def choice_option(
        self, name: str, **kwargs: Unpack[ChoiceOptionArgs]
    ) -> ChoiceOptionSpec:
        self.user_options[name] = ChoiceOptionData(**kwargs, type="Choice")
        return ChoiceOptionSpec(name, kwargs)
