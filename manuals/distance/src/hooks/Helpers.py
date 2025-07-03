from typing import Optional, TYPE_CHECKING, cast
from BaseClasses import MultiWorld

if TYPE_CHECKING:
    from ..Items import ManualItem
    from ..Locations import ManualLocation

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    return None


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item: "ManualItem") -> Optional[bool]:
    if hasattr(multiworld, "generation_is_fake"):
        return None

    from .state import player_excluded_items

    if cast(dict, item)["name"] in player_excluded_items[player]:
        return False

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location: "ManualLocation") -> Optional[bool]:
    if hasattr(multiworld, "generation_is_fake"):
        return None

    from .state import player_excluded_locations

    if cast(dict, location)["name"] in player_excluded_locations[player]:
        return False

    return None
