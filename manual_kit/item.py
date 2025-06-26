from typing import Final, NotRequired, TypedDict


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


class ItemSpec:
    def __init__(self, data: ItemData) -> None:
        self.name: Final = data["name"]
        self.data: Final = data
