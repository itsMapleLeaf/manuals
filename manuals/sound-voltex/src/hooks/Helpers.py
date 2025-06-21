from typing import Optional, TYPE_CHECKING, cast
from BaseClasses import MultiWorld, Item, Location
from .Globals import PLAYER_SONG_LISTS

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

    # this is actually a dict i have no fucking idea why it's typed as an instance because it's literaqlly fucking not
    item_dict = cast(dict, item)
    categories: list[str] = item_dict.get('category', [])

    if ('Songs' in categories) or ('Goals' in categories):
        song_identifier = categories[1]
        # if song_identifier in PLAYER_SONG_LISTS[player]:
        #     print("enabled item:", item_dict['name'])
        return song_identifier in PLAYER_SONG_LISTS[player]

    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location: "ManualLocation") -> Optional[bool]:
    if hasattr(multiworld, "generation_is_fake"):
        return None

    # this is actually a dict i have no fucking idea why it's typed as an instance because it's literaqlly fucking not
    location_dict = cast(dict, location)
    categories: list[str] = location_dict.get('category', [])

    if 'Goals' in categories:
        song_identifier = categories[1]
        # if song_identifier in PLAYER_SONG_LISTS[player]:
        #     print("enabled location:", location_dict['name'])
        return song_identifier in PLAYER_SONG_LISTS[player]

    return None
