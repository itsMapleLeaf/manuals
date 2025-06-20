import enum
import json
from typing import NotRequired, TypedDict, Unpack


class ItemArgs(TypedDict):
    category: NotRequired[str | list[str]]
    """(Optional) A list of categories to be applied to this item."""

    count: NotRequired[int]
    """(Optional) Total number of this item that will be in the itempool for randomization."""

    value: NotRequired[dict[str, int]]
    """(Optional) A dictionary of values this item has in the format {"name": int,"otherName": int}
    Used with the {ItemValue(Name: int)} in location requires eg. "value": {"coins":10} mean this item is worth 10 coins"""

    progression: NotRequired[bool]
    """(Optional) Is this item needed to unlock locations? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    progression_skip_balancing: NotRequired[bool]
    """(Optional) Should this item not get included in progression balance swaps? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    useful: NotRequired[bool]
    """(Optional) Is this item useful to have but not required to complete the game? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    trap: NotRequired[bool]
    """(Optional) Is this item something the player doesn't want to get? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    filler: NotRequired[bool]
    """(Optional) Is this item mostly useless and okay to skip placing sometimes? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    early: NotRequired[int | bool]
    """(Optional) How many copies of this item are required to be placed somewhere accessible from the start (Sphere 1)
    Choosing 'True' mark all of them to be early"""

    local: NotRequired[bool]
    """(Optional) Are all copies of this item supposed to be only in your locations (true), or can they be anywhere (false)?"""

    local_early: NotRequired[bool]
    """(Optional) How many copies of this item (or 'true' if all copies) are supposed to be early and only in your locations.
    Can be used to mark some of the copies of an item to be early and local since 'local' is a toggle between none or all of them."""

    id: NotRequired[int]
    """(Optional) Skips the item ID forward to the given value.
    This can be used to provide buffer space for future items."""


class ItemData(ItemArgs):
    name: str
    """The unique name of the item. Do not use (), :, or | in the name"""


class LocationArgs(TypedDict):
    category: NotRequired[str | list[str]]
    """(Optional) A list of categories to be applied to this location."""

    requires: NotRequired[str]
    """(Optional) A boolean logic string that describes the required items, counts, etc. needed to reach this location."""

    region: NotRequired[str]
    """(Optional) The name of the region this location is part of."""

    place_item: NotRequired[list[str]]
    """(Optional) Places an item that matches one of the item names listed in this setting at this location. Does not check logical access to the location."""

    dont_place_item: NotRequired[list[str]]
    """(Optional) Configures what item names should not end up at this location during normal generation. Does not check logical access to the location."""

    place_item_category: NotRequired[list[str]]
    """(Optional) Places an item that matches at least one of the categories listed in this setting at this location. Does not check logical access to the location."""

    dont_place_item_category: NotRequired[list[str]]
    """(Optional) Configures what item categories should not end up at this location during normal generation. Does not check logical access to the location."""

    victory: NotRequired[bool]
    """(Optional) Is this location one of the possible goals of this Manual APWorld?"""

    prehint: NotRequired[bool]
    """(Optional) Should this location be hinted at the start?"""

    hint_entrance: NotRequired[str]
    """(Optional) Adds additional text to this location's hints to convey useful information. Typically used for entrance randomization."""

    id: NotRequired[int]
    """(Optional) Skips the item ID forward to the given value.
    This can be used to provide buffer space for future items."""


class LocationData(LocationArgs):
    name: str
    """The unique name of the location."""


class CategoryArgs(TypedDict):
    yaml_option: NotRequired[list[str]]
    """(Optional) Array of Options that will decide if the items & locations in this category are enabled"""

    hidden: NotRequired[bool]
    """(Optional) Should this category be Hidden in the client?"""


class CategoryData(CategoryArgs):
    name: str
    """Name of the category"""


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

    def location(self, name: str, **kwargs: Unpack[LocationArgs]) -> LocationData:
        location = LocationData(name=name, **kwargs)
        self.locations += [location]
        return location

    def category(self, name: str, **kwargs: Unpack[CategoryArgs]) -> CategoryData:
        category = CategoryData(name=name, **kwargs)
        self.categories[name] = category
        return category


class DistanceWorldSpec(WorldSpec):
    campaigns = {
        "Adventure": [
            "Instantiation",
            "Cataclysm",
            "Diversion",
            "Euphoria",
            "Entanglement",
            "Automation",
            "Abyss",
            "Embers",
            "Isolation",
            "Repulsion",
            "Compression",
            "Research",
            "Contagion",
            "Overload",
            "Ascension",
            "Enemy",
        ],
        "Lost to Echoes": [
            "Long Ago",
            "Forgotten Utopia",
            "A Deeper Void",
            "Eye of the Storm",
            "The Sentinel Still Watches",
            "Shadow of the Beast",
            "Pulse of a Violent Heart",
            "It Was Supposed To Be Perfect",
            "Echoes",
        ],
    }

    arcade_level_sets = {
        "Adventure": [
            "Cataclysm",
            "Diversion",
            "Euphoria",
            "Entanglement",
            "Automation",
            "Abyss",
            "Embers",
            "Isolation",
            "Repulsion",
            "Compression",
            "Research",
            "Contagion",
            "Overload",
            "Ascension",
        ],
        "Lost to Echoes": [
            "Forgotten Utopia",
            "A Deeper Void",
            "Eye of the Storm",
            "The Sentinel Still Watches",
            "Shadow of the Beast",
            "Pulse of a Violent Heart",
            "It Was Supposed To Be Perfect",
        ],
        "Legacy": [
            "Broken Symmetry",
            "Lost Society",
            "Negative Space",
            "Departure",
            "Ground Zero",
            "The Observer Effect",
            "Aftermath",
            "Friction",
            "The Thing About Machines",
            "Corruption",
            "Dissolution",
            "Falling Through",
            "Monolith",
            "Destination Unknown",
            "Rooftops",
            "Factory",
            "Stronghold",
            "Approach",
            "Continuum",
            "Escape",
        ],
    }

    filler_item_names = [
        # "corruption error",
        "out of memory",
        "access violation",
        "invalid sequence termination",
        "segmentation fault",
        "kernel failure",
        "version mismatch",
        "unknown protocol",
        "syntax error",
        "calibration failure",
        "permission denied",
        "resource limit exceeded",
    ]

    def __init__(self) -> None:
        for set_name, levels in self.arcade_level_sets.items():
            for level_name in levels:
                level_item = self.item(
                    name=f"{level_name} [{set_name}]",
                    category="Arcade",
                    progression=True,
                )

                for medal in ["Gold", "Diamond"]:
                    self.location(
                        name=f"{level_name} - {medal} Medal [{set_name}]",
                        category=f"(Arcade: {set_name}) {level_name}",
                        requires=f"|{level_item['name']}|",
                    )

        campaign_completion_item = self.item(
            name=f"Campaign Completion",
            category="Campaign Completion",
            count=len(self.campaigns),
            progression=True,
        )

        for campaign_name, levels in self.campaigns.items():
            campaign_item = self.item(
                name=f"{campaign_name} [Progressive Campaign]",
                category="Campaign",
                count=len(levels),
                progression=True,
            )

            for level_index, level_name in enumerate(levels):
                campaign_level_location = self.location(
                    name=f"{level_name} [{campaign_name}]",
                    category=f"(Campaign: {campaign_name}) {level_name}",
                    requires=f"|{campaign_item['name']}:{level_index + 1}|",
                )

                if level_index == len(levels) - 1:
                    campaign_level_location["place_item"] = [
                        campaign_completion_item["name"]
                    ]

        self.location(
            name="All Campaigns Completed",
            requires=f"|{campaign_completion_item['name']}:all|",
            victory=True,
        )

        for filler_item_name in self.filler_item_names:
            self.item(
                filler_item_name,
                category="fatal exception (Filler)",
                filler=True,
                trap=True,
            )


if __name__ == "__main__":
    spec = DistanceWorldSpec()

    print(json.dumps(spec.items, indent=2))
    print(json.dumps(spec.locations, indent=2))
    print(json.dumps(spec.categories, indent=2))

    print(f"{spec.item_count} items")
    print(f"{len(spec.locations)} locations")
    print(f"{len(spec.categories)} configured categories")
