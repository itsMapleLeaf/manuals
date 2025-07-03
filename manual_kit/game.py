from dataclasses import dataclass
from typing import NotRequired, TypedDict


class GameData(TypedDict):
    game: str
    """The name of your game, compatible with capital letters."""

    creator: str
    """Your Username."""

    filler_item_name: str
    """Name of the filler items that get placed when there's no more real items to place."""

    starting_items: NotRequired[list["StartingItemData"]]
    """(Optional) Starting inventory"""

    death_link: NotRequired[bool]
    """(Optional) Does your game support Deathlink?"""

    starting_index: NotRequired[int]
    """(Optional) (Advanced) Choose the starting index for your locations and items."""


@dataclass
class GameSpec:
    data: GameData

    @property
    def name(self):
        return self.data["game"]

    @property
    def creator(self):
        return self.data["creator"]


class StartingItemData(TypedDict):
    items: NotRequired[list[str]]
    """(Optional) List of item to pick from. If not included will pick from 'item_categories' if present or from the entire item pool if absent"""

    item_categories: NotRequired[list[str]]
    """(Optional) List of category of items to pick from. If not included will pick from 'items' if present or from the entire item pool if absent"""

    random: NotRequired[int]
    """(Optional) how many items of this block will be randomly added to inventory. Will add every item in the block if not included"""

    if_previous_item: NotRequired[list[str]]
    """(Optional) Causes the starting item block to only occur when any of the matching items have already been added to starting inventory by any previous starting item blocks"""

    yaml_option: NotRequired[list[str]]
    """(Optional) Array of Options that will decide if this block is rolled"""


@dataclass
class StartingItemSpec:
    data: StartingItemData
