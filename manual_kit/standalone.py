import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from dataclasses import dataclass
from typing import (
    Literal,
    NotRequired,
    TypedDict,
    Unpack,
)

from .manspect import StrPath


type RequirementData = str | list[str]
type RequirementSubject = ItemData | CategoryData


class GameData(TypedDict):
    game: str
    """The name of your game, compatible with capital letters."""

    creator: str
    """Your Username."""

    filler_item_name: str
    """Name of the filler items that get placed when there's no more real items to place."""

    starting_items: list["StartingItemData"] | None
    """(Optional) Starting inventory"""

    death_link: NotRequired[bool]
    """(Optional) Does your game support Deathlink?"""

    starting_index: NotRequired[int]
    """(Optional) (Advanced) Choose the starting index for your locations and items."""


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


class LocationArgs(TypedDict):
    requires: NotRequired[str]
    """(Optional) A boolean logic string that describes the required items, counts, etc. needed to reach this location."""

    category: NotRequired[str | list[str]]
    """(Optional) A list of categories to be applied to this location."""

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

    hint_entrance: NotRequired[bool]
    """(Optional) Adds additional text to this location's hints to convey useful information. Typically used for entrance randomization."""

    id: NotRequired[int]
    """(Optional) Skips the item ID forward to the given value.
    This can be used to provide buffer space for future items."""


class LocationData(LocationArgs):
    name: str
    """The unique name of the location."""


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


class RegionData(TypedDict):
    requires: NotRequired[str]
    connects_to: NotRequired[list[str]]
    starting: NotRequired[bool]
    exit_requires: NotRequired[dict[str, str]]
    entrance_requires: NotRequired[dict[str, str]]


class CategoryData(TypedDict):
    hidden: NotRequired[bool]
    """(Optional) Should this category be Hidden in the client?"""

    yaml_option: NotRequired[list[str]]
    """(Optional) Array of Options that will decide if the items & locations in this category are enabled"""


class OptionData(TypedDict):
    description: NotRequired[str | list[str]]
    """Description text explaining what this option does"""
    display_name: NotRequired[str]
    """The display name shown to users for this option"""
    rich_text_doc: NotRequired[bool]
    """Whether the description should be rendered as rich text"""
    group: NotRequired[str]
    """The group this option belongs to in the UI"""
    hidden: NotRequired[bool]
    """Whether this option should be hidden from the UI"""
    visibility: NotRequired[str | list[str] | int]
    """Controls when this option is visible to users"""


class ToggleOptionData(OptionData):
    default: bool
    """The default value for this toggle option"""


class ChoiceOptionData(OptionData):
    values: dict[str, int]
    """Mapping of choice names to their corresponding values"""
    default: int
    """The default value for this choice option"""
    aliases: NotRequired[dict[str, int | str]]
    """Alternative names that map to the same choices"""
    allow_custom_value: NotRequired[bool]
    """Whether users can input custom values not in the predefined choices"""


class RangeOptionData(OptionData):
    range_start: int
    """The minimum value allowed for this range"""
    range_end: int
    """The maximum value allowed for this range"""
    default: int
    """The default value for this range option"""
    values: NotRequired[dict[str, int]]
    """Optional mapping of named values within the range"""


class MetaData(TypedDict):
    docs: NotRequired["MetaDocsConfig"]
    enable_region_diagram: NotRequired[bool]


class MetaDocsConfig(TypedDict):
    apworld_description: NotRequired[list[str] | None]
    web: NotRequired["MetaDocsWebConfig | None"]


type MetaDocsWebTheme = Literal[
    "dirt",
    "grass",
    "grassFlowers",
    "ice",
    "jungle",
    "ocean",
    "partyTime",
    "stone",
]


class MetaDocsWebConfig(TypedDict):
    options_page: NotRequired[bool | str]
    game_info_languages: NotRequired[list[str]]
    theme: NotRequired[MetaDocsWebTheme]
    bug_report_page: NotRequired[str]
    tutorials: NotRequired[list[dict]]
    options_presets: NotRequired[list[dict]]


class Requires:
    type ItemInput = str | ItemData

    @staticmethod
    def item(
        item: ItemInput, amount: str | int | Literal["all", "half"] | None = None
    ) -> str:
        result = Requires.__as_item_name(item)

        if amount != None:
            result = f"{result}:{amount}"

        return f"|{result}|"

    @staticmethod
    def category(
        name: str, amount: str | int | Literal["all", "half"] | None = None
    ) -> str:
        result = name

        if amount != None:
            result = f"{result}:{amount}"

        return f"|@{result}|"

    @staticmethod
    def any_of(*inputs: str) -> str:
        exp = " or ".join(inputs)
        return f"({exp})"

    @staticmethod
    def all_of(*inputs: str) -> str:
        exp = " and ".join(inputs)
        return f"({exp})"

    @staticmethod
    def func(name: str, args: str) -> str:
        result = f"{name}({args})"
        return "{%s}" % result  # avoiding format string here for clarity

    @staticmethod
    def item_value(key: str, count: int) -> str:
        return Requires.func("ItemValue", f"{key}:{count}")

    @staticmethod
    def existing(item: ItemInput) -> str:
        return Requires.func("OptOne", Requires.__as_item_name(item))

    @staticmethod
    def all_existing(input: str) -> str:
        return Requires.func("OptAll", input)

    @staticmethod
    def enabled_option(name: str) -> str:
        return Requires.func("YamlEnabled", name)

    @staticmethod
    def disabled_option(name: str) -> str:
        return Requires.func("YamlDisabled", name)

    @staticmethod
    def option_expression(
        option_name: str,
        operator: Literal["==", "!=", ">=", "<=", ">", "<"],
        value: str | int | bool,
    ) -> str:
        return Requires.func("YamlCompare", f"{option_name} {operator} {value}")

    @staticmethod
    def __as_item_name(item_input: ItemInput) -> str:
        return item_input if isinstance(item_input, str) else item_input["name"]


class WorldSpec:
    def __init__(self, **kwargs: Unpack[GameData]) -> None:
        self.game: GameData = kwargs
        self.items: list[ItemData] = []
        self.locations: list[LocationData] = []
        self.categories: dict[str, CategoryData] = {}
        self.regions: dict[str, RegionData] = {}
        self.core_options: dict[str, OptionData] = {}
        self.user_options: dict[str, OptionData] = {}
        self.meta = MetaData()
        self.files: dict[str, str] = {}

    @property
    def item_count(self) -> int:
        return sum(item.get("count", 1) for item in self.items)

    def define_item(self, name: str, **args: Unpack[ItemArgs]) -> ItemData:
        if any(item["name"] == name for item in self.items):
            raise Exception(f"Item {name} defined twice")

        data = ItemData(name=name, **args)
        self.items += [data]
        return data

    def define_location(self, name: str, **args: Unpack[LocationArgs]) -> LocationData:
        if any(location["name"] == name for location in self.locations):
            raise Exception(f"Location {name} defined twice")

        data = LocationData(name=name, **args)
        self.locations += [data]
        return data

    def define_category(
        self, name: str, **data: Unpack[CategoryData]
    ) -> tuple[CategoryData, str]:
        return self.__set_unique("Category", self.categories, name, data), name

    def define_region(
        self, name: str, **data: Unpack[RegionData]
    ) -> tuple[RegionData, str]:
        return self.__set_unique("Region", self.regions, name, data), name

    def define_user_option(
        self, name: str, **data: Unpack[OptionData]
    ) -> tuple[OptionData, str]:
        return self.__set_unique("User option", self.user_options, name, data), name

    def define_core_option(
        self, name: str, **data: Unpack[OptionData]
    ) -> tuple[OptionData, str]:
        return self.__set_unique("Core option", self.core_options, name, data), name

    @staticmethod
    def __set_unique[T](
        item_type_name: str, items: dict[str, T], key: str, value: T
    ) -> T:
        if key in items:
            raise Exception(f'{item_type_name} "{key}" defined twice')

        items[key] = value
        return value

    @dataclass(frozen=True)
    class DataFileInfo:
        name: str
        data: object

    def game_file(self):
        return self.DataFileInfo("game.json", self.game)

    def categories_file(self):
        return self.DataFileInfo("categories.json", self.categories)

    def items_file(self):
        return self.DataFileInfo("items.json", {"data": self.items})

    def locations_file(self):
        return self.DataFileInfo("locations.json", {"data": self.locations})

    def regions_file(self):
        return self.DataFileInfo("regions.json", self.regions)

    def options_file(self):
        return self.DataFileInfo(
            "options.json",
            {"user": self.user_options, "core": self.core_options},
        )

    def meta_file(self):
        return self.DataFileInfo("meta.json", self.meta)

    def data_files(self):
        return [
            self.game_file(),
            self.categories_file(),
            self.items_file(),
            self.locations_file(),
            self.regions_file(),
            self.options_file(),
            self.meta_file(),
        ]

    def create_apworld_file(
        self,
        manual_src_dir=Path(__file__).parent / "Manual/src",
        apworld_contents_temp_dir: StrPath | None = None,
        apworld_output_dir: StrPath = Path("C:/ProgramData/Archipelago/custom_worlds"),
        preserve_apworld_contents_temp_dir=False,
    ) -> Path:
        def ensure_dir(input: StrPath) -> Path:
            path = Path(input)
            path.mkdir(parents=True, exist_ok=True)
            return path

        manual_src_dir = ensure_dir(manual_src_dir)
        apworld_output_dir = ensure_dir(apworld_output_dir)

        if apworld_contents_temp_dir != None:
            apworld_contents_temp_dir = ensure_dir(apworld_contents_temp_dir)

        with TemporaryDirectory(
            dir=apworld_contents_temp_dir,
            prefix="manual_kit_",
            delete=not preserve_apworld_contents_temp_dir,
        ) as temp_root_dir:
            temp_root_dir = Path(temp_root_dir)
            temp_src_dir = temp_root_dir / "src"

            shutil.copytree(manual_src_dir, temp_src_dir)

            data_dir = temp_src_dir / "data"
            data_dir.mkdir(parents=True, exist_ok=True)

            import json

            for data_file_info in self.data_files():
                with open(data_dir / data_file_info.name, "w") as data_file:
                    json.dump(
                        data_file_info.data, data_file, indent=2, ensure_ascii=False
                    )

            for local_file_path, file_content in self.files.items():
                file_path = Path(temp_src_dir / local_file_path)
                os.makedirs(file_path.parent, exist_ok=True)
                file_path.write_text(file_content)

            # while in most cases it would work to use `self.game` and `self.creator`,
            # the filename of the apworld **has** to match what's in the game.json file,
            # and the game.json file can be overridden by the `files` arg
            # or changed through other means,
            # so it effectively becomes the best source of truth
            with open(data_dir / self.game_file().name, "r") as game_file:
                game_data = GameData(json.load(game_file))

            world_identifier = f"manual_{game_data['game']}_{game_data['creator']}"
            apworld_file = Path(apworld_output_dir) / f"{world_identifier}.apworld"

            shutil.move(temp_src_dir, temp_root_dir / world_identifier)

            world_zip = shutil.make_archive(
                str(Path(apworld_output_dir) / world_identifier),
                format="zip",
                root_dir=temp_root_dir,
                base_dir=".",
            )

        return Path(shutil.move(world_zip, apworld_file))
