from dataclasses import dataclass
from typing import cast
from BaseClasses import MultiWorld

from . import ItemData, LocationData


@dataclass
class Sampler:
    item_category: str
    items: set[str]
    location_category: str
    locations: set[str]

    def before_is_item_enabled(self, multiworld: "MultiWorld", item):
        # here to ensure this works with universal tracker logic figure-outer
        if hasattr(multiworld, "generation_is_fake"):
            return None

        item_dict = cast("ItemData", item)
        item_categories = item_dict.get("category") or []

        if self.item_category in item_categories:
            return item_dict["name"] in self.items

        return None

    def before_is_location_enabled(self, multiworld: "MultiWorld", location):
        # here to ensure this works with universal tracker logic figure-outer
        if hasattr(multiworld, "generation_is_fake"):
            return None

        location_dict = cast("LocationData", location)
        location_categories = location_dict.get("category") or []

        if self.location_category in location_categories:
            return location_dict["name"] in self.locations

        return None
