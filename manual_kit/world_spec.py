from typing import Optional, Unpack

from .game import GameSpec
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


class WorldSpec:

    def __init__(self, game_spec: GameSpec | None = None) -> None:
        self.category_specs: dict[str, CategorySpec] = {}
        self.game_spec = game_spec
        self.item_specs: dict[str, ItemSpec] = {}
        self.location_specs: dict[str, LocationSpec] = {}
        self.user_option_specs: dict[str, OptionData] = {}

    @property
    def items(self) -> list[ItemData]:
        return [item.data for item in self.item_specs.values()]

    @property
    def locations(self) -> list[LocationData]:
        return [location.data for location in self.location_specs.values()]

    @property
    def categories(self) -> dict[str, CategoryData]:
        return {name: category.data for name, category in self.category_specs.items()}

    @property
    def item_count(self) -> int:
        return sum(item.count for item in self.item_specs.values())

    def item(self, name: str, **kwargs: Unpack[ItemArgs]) -> ItemSpec:
        return self.__set_unique(
            self.item_specs, name, ItemSpec({**kwargs, "name": name})
        )

    def location(
        self,
        name: str,
        requires: Optional[str | Requirement] = None,
        **kwargs: Unpack[LocationArgs],
    ) -> LocationSpec:
        location = self.__set_unique(
            self.location_specs, name, LocationSpec({**kwargs, "name": name})
        )
        if requires != None:
            location.data["requires"] = str(requires)
        return location

    def category(self, name: str, **kwargs: Unpack[CategoryArgs]) -> CategorySpec:
        return self.__set_unique(self.category_specs, name, CategorySpec(name, kwargs))

    def toggle_option(
        self, name: str, **kwargs: Unpack[ToggleOptionArgs]
    ) -> ToggleOptionSpec:
        self.user_option_specs[name] = ToggleOptionData(**kwargs, type="Toggle")
        return ToggleOptionSpec(name, kwargs)

    def range_option(
        self, name: str, **kwargs: Unpack[RangeOptionArgs]
    ) -> RangeOptionSpec:
        self.user_option_specs[name] = RangeOptionData(**kwargs, type="Range")
        return RangeOptionSpec(name, kwargs)

    def choice_option(
        self, name: str, **kwargs: Unpack[ChoiceOptionArgs]
    ) -> ChoiceOptionSpec:
        self.user_option_specs[name] = ChoiceOptionData(**kwargs, type="Choice")
        return ChoiceOptionSpec(name, kwargs)

    @staticmethod
    def __set_unique[T](items: dict[str, T], key: str, value: T) -> T:
        if key in items:
            raise Exception(f"{key} already exists")

        items[key] = value
        return value
