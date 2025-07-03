from dataclasses import dataclass
from typing import Optional, Unpack

from .requires import Requirement
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
    def __post_init__(self) -> None:
        self.__items: dict[str, ItemSpec] = {}
        self.__locations: dict[str, LocationSpec] = {}
        self.__categories: dict[str, CategorySpec] = {}
        self.user_options: dict[str, OptionData] = {}

    @property
    def items(self) -> list[ItemData]:
        return [item.data for item in self.__items.values()]

    @property
    def locations(self) -> list[LocationData]:
        return [location.data for location in self.__locations.values()]

    @property
    def categories(self) -> dict[str, CategoryData]:
        return {name: category.data for name, category in self.__categories.items()}

    @property
    def item_count(self) -> int:
        return sum(item.count for item in self.__items.values())

    def item(self, name: str, **kwargs: Unpack[ItemArgs]) -> ItemSpec:
        return self.__set_unique(self.__items, name, ItemSpec({**kwargs, "name": name}))

    def location(
        self,
        name: str,
        requires: Optional[str | Requirement] = None,
        **kwargs: Unpack[LocationArgs],
    ) -> LocationSpec:
        location = self.__set_unique(
            self.__locations, name, LocationSpec({**kwargs, "name": name})
        )
        if requires != None:
            location.data["requires"] = str(requires)
        return location

    def category(self, name: str, **kwargs: Unpack[CategoryArgs]) -> CategorySpec:
        return self.__set_unique(self.__categories, name, CategorySpec(name, kwargs))

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

    @staticmethod
    def __set_unique[T](items: dict[str, T], key: str, value: T) -> T:
        if key in items:
            raise Exception(f"{key} already exists")

        items[key] = value
        return value
