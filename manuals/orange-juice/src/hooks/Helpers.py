from typing import Optional, TYPE_CHECKING, cast
from BaseClasses import MultiWorld

if TYPE_CHECKING:
    from ..Items import ManualItem
    from ..Locations import ManualLocation
    from ..manual_kit import ItemData


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(
    multiworld: MultiWorld, player: int, category_name: str
) -> Optional[bool]:
    from ..pool import OrangeJuiceWorldGenPool

    pool = OrangeJuiceWorldGenPool.player_pools[player]

    if category_name.startswith("Characters"):
        return any(
            category_name == f"Characters - {character}"
            for character in pool.characters
        )

    if category_name.startswith("Boards"):
        return any(category_name == f"Boards - {board}" for board in pool.boards)

    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(
    multiworld: MultiWorld, player: int, item_arg: "ManualItem"
) -> Optional[bool]:
    from ..pool import OrangeJuiceWorldGenPool

    item = cast("ItemData", item_arg)
    categories = item.get("category") or []
    pool = OrangeJuiceWorldGenPool.player_pools[player]

    if "Characters" in categories:
        return item["name"] in pool.characters

    if "Boards" in categories:
        return item["name"] in pool.boards

    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(
    multiworld: MultiWorld, player: int, location: "ManualLocation"
) -> Optional[bool]:
    return None
