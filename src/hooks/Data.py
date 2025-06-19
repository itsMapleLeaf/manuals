from dataclasses import dataclass
from typing import Any, NotRequired, TypedDict


@dataclass
class StoryWorld:
    name: str
    levels: list[str]


worlds: list[StoryWorld] = [
    StoryWorld(
        "Jungle Island",
        [
            "Simple",
            "Hollow",
            "Bumpy",
            "Switches",
            "Conveyers",
            "Floaters",
            "Slopes",
            "Sliders",
            "Spinning Top",
            "Curve Bridge",
        ],
    ),
    StoryWorld(
        "Volcanic Magma",
        [
            "Banks",
            "Eaten Floor",
            "Hoppers",
            "Coaster",
            "Bumpy Check",
            "Swell",
            "Gravity Slider",
            "Inchworms",
            "Totalitarianism",
            "Alternative",
        ],
    ),
    StoryWorld(
        "Under the Ocean",
        [
            "Organic Form",
            "Reversible Gear",
            "Stepping Stones",
            "Dribbles",
            "U.R.L.",
            "Mad Rings",
            "Curvy Options",
            "Twister",
            "Downhill",
            "Junction",
        ],
    ),
    StoryWorld(
        "Inside a Whale",
        [
            "Pro Skaters",
            "Giant Comb",
            "Beehive",
            "Dynamic Maze",
            "Triangle Holes",
            "Launchers",
            "Randomizer",
            "Coin Slots",
            "Seesaw Bridges",
            "Arthropod",
        ],
    ),
    StoryWorld(
        "Amusement Park",
        [
            "Wormhole",
            "Free Fall",
            "Melting Pot",
            "Mad Shuffle",
            "Bead Screen",
            "Jump Machine",
            "Zigzag Slope",
            "Tower",
            "Toggle",
            "Fluctuation",
        ],
    ),
    StoryWorld(
        "Boiling Pot",
        [
            "Combination",
            "Punched Seesaws",
            "Opera",
            "Brandished",
            "Tiers",
            "Cliffs",
            "Narrow Peaks",
            "Detour",
            "Switch Inferno",
            "Folders",
        ],
    ),
    StoryWorld(
        "Bubbly Washing Machine",
        [
            "Spiral Bridge",
            "Wavy Option",
            "Obstacle",
            "Domino",
            "Sieve",
            "Flock",
            "Double Spiral",
            "Hierarchy",
            "8 Bracelets",
            "Quick Turn",
        ],
    ),
    StoryWorld(
        "Clock Tower Factory",
        [
            "Pistons",
            "Soft Cream",
            "Momentum",
            "Entangled Path",
            "Totters",
            "Vortex",
            "Warp",
            "Trampolines",
            "Swing Shaft",
            "Linear Seesaws",
        ],
    ),
    StoryWorld(
        "Space Colony",
        [
            "Serial Jump",
            "Cross Floors",
            "Spinning Saw",
            "Chipped Pipes",
            "Flat Maze",
            "Guillotine",
            "Cork Screw",
            "Orbiters",
            "Twin Basin",
            "Air Hockey",
        ],
    ),
]

victory_world = StoryWorld(
    "Dr. Bad-Boon's Base",
    [
        "Training",
        "Gimmick",
        "Mountain",
        "Disorder",
        "3D Maze",
        "Labyrinth",
        "Postmodern",
        "Revolution",
        "Invisible",
        "Created By",
    ],
)

victory_level_required_banana_count = 5


class Item(TypedDict):
    name: str
    category: NotRequired[str | list[str]]
    count: NotRequired[int]
    value: NotRequired[dict[str, int]]
    progression: NotRequired[bool]
    progression_skip_balancing: NotRequired[bool]
    useful: NotRequired[bool]
    trap: NotRequired[bool]
    filler: NotRequired[bool]
    early: NotRequired[int | bool]
    local: NotRequired[bool]
    local_early: NotRequired[bool]
    id: NotRequired[int]


class Location(TypedDict):
    name: str
    category: NotRequired[str | list[str]]
    requires: NotRequired[str]
    region: NotRequired[str]
    place_item: NotRequired[list[str]]
    dont_place_item: NotRequired[list[str]]
    place_item_category: NotRequired[list[str]]
    dont_place_item_category: NotRequired[list[str]]
    victory: NotRequired[bool]
    prehint: NotRequired[bool]
    hint_entrance: NotRequired[str]
    id: NotRequired[int]


# called after the game.json file has been loaded
def after_load_game_file(game_table: dict) -> dict:
    return game_table


# called after the items.json file has been loaded, before any item loading or processing has occurred
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def after_load_item_file(item_table: list) -> list:
    item_table += [
        Item(
            name=f"{world.name} (World {world_index + 1})",
            category="Worlds",
            progression=True,
        )
        for world_index, world in enumerate(worlds)
    ]

    item_table += [
        Item(
            name="Banana",
            category="Bananas",
            count=int(
                victory_level_required_banana_count * len(victory_world.levels) * 1.5
            ),
            progression=True,
        )
    ]

    return item_table


# NOTE: Progressive items are not currently supported in Manual. Once they are,
#       this hook will provide the ability to meaningfully change those.
def after_load_progressive_item_file(progressive_item_table: list) -> list:
    return progressive_item_table


# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_location_file(location_table: list) -> list:
    location_table += [
        Location(
            name=f"{level_index + 1}. {level} (World {world_index + 1})",
            category=f"World {world_index + 1}",
            requires=f"|{world.name} (World {world_index + 1})|",
        )
        for world_index, world in enumerate(worlds)
        for level_index, level in enumerate(world.levels)
    ]

    location_table += [
        Location(
            name=f"{level_index + 1}. {level} ({victory_world.name})",
            category=victory_world.name,
            requires=f"|Banana:{victory_level_required_banana_count * (level_index + 1)}|",
        )
        for level_index, level in enumerate(victory_world.levels)
    ]

    location_table += [
        Location(
            name="Defeat Dr. Bad-Boon",
            victory=True,
            category="Victory!",
            requires=f"|Banana:{victory_level_required_banana_count * len(victory_world.levels)}|",
        )
    ]

    return location_table


# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_region_file(region_table: dict) -> dict:
    return region_table


# called after the categories.json file has been loaded
def after_load_category_file(category_table: dict) -> dict:
    return category_table


# called after the categories.json file has been loaded
def after_load_option_file(option_table: dict) -> dict:
    # option_table["core"] is the dictionary of modification of existing options
    # option_table["user"] is the dictionary of custom options
    return option_table


# called after the meta.json file has been loaded and just before the properties of the apworld are defined. You can use this hook to change what is displayed on the webhost
# for more info check https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#webworld-class
def after_load_meta_file(meta_table: dict) -> dict:
    return meta_table


# called when an external tool (eg Universal Tracker) ask for slot data to be read
# use this if you want to restore more data
# return True if you want to trigger a regeneration if you changed anything
def hook_interpret_slot_data(
    world, player: int, slot_data: dict[str, Any]
) -> dict | bool:
    return False
