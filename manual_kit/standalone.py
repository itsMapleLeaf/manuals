import dataclasses
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from dataclasses import dataclass, field
from typing import Callable, Literal, Optional

from ._util import JsonObject, compact, list_names_or_none, omit


type RequireData = str | list[str]


@dataclass
class GameSpec:
    game: str
    """The name of your game, compatible with capital letters."""

    creator: str
    """Your Username."""

    filler_item_name: str
    """Name of the filler items that get placed when there's no more real items to place."""

    starting_items: list["StartingItem"] = field(default_factory=list)
    """(Optional) Starting inventory"""

    death_link = False
    """(Optional) Does your game support Deathlink?"""

    starting_index: Optional[int] = None
    """(Optional) (Advanced) Choose the starting index for your locations and items."""

    @property
    def data(self) -> JsonObject:
        return compact(
            {
                "game": self.game,
                "creator": self.creator,
                "filler_item_name": self.filler_item_name,
                "starting_items": (
                    [item.data for item in self.starting_items]
                    if self.starting_items
                    else None
                ),
                "death_link": self.death_link or None,
                "starting_index": self.starting_index,
            }
        )

    @dataclass
    class StartingItem:
        items: Optional[list["ItemSpec"]] = None
        """(Optional) List of item to pick from. If not included will pick from 'item_categories' if present or from the entire item pool if absent"""

        item_categories: Optional[list["CategorySpec"]] = None
        """(Optional) List of category of items to pick from. If not included will pick from 'items' if present or from the entire item pool if absent"""

        random: Optional[int] = None
        """(Optional) how many items of this block will be randomly added to inventory. Will add every item in the block if not included"""

        if_previous_item: Optional[list["ItemSpec"]] = None
        """(Optional) Causes the starting item block to only occur when any of the matching items have already been added to starting inventory by any previous starting item blocks"""

        yaml_option: Optional[list["ToggleOptionSpec"]] = None
        """(Optional) Array of Options that will decide if this block is rolled"""

        @property
        def data(self) -> JsonObject:
            return compact(
                {
                    "items": list_names_or_none(self.items),
                    "item_categories": list_names_or_none(self.item_categories),
                    "random": self.random,
                    "if_previous_item": list_names_or_none(self.if_previous_item),
                    "yaml_option": list_names_or_none(self.yaml_option),
                }
            )


@dataclass
class LocationSpec:
    name: str
    """The unique name of the location."""

    requires: str | None = None
    """(Optional) A boolean logic string that describes the required items, counts, etc. needed to reach this location."""

    category: list["CategorySpec"] = field(default_factory=list)
    """(Optional) A list of categories to be applied to this location."""

    region: "RegionSpec | None" = None
    """(Optional) The name of the region this location is part of."""

    place_item: list["ItemSpec"] = field(default_factory=list)
    """(Optional) Places an item that matches one of the item names listed in this setting at this location. Does not check logical access to the location."""

    dont_place_item: list["ItemSpec"] = field(default_factory=list)
    """(Optional) Configures what item names should not end up at this location during normal generation. Does not check logical access to the location."""

    place_item_category: list["CategorySpec"] = field(default_factory=list)
    """(Optional) Places an item that matches at least one of the categories listed in this setting at this location. Does not check logical access to the location."""

    dont_place_item_category: list["CategorySpec"] = field(default_factory=list)
    """(Optional) Configures what item categories should not end up at this location during normal generation. Does not check logical access to the location."""

    victory = False
    """(Optional) Is this location one of the possible goals of this Manual APWorld?"""

    prehint = False
    """(Optional) Should this location be hinted at the start?"""

    hint_entrance = ""
    """(Optional) Adds additional text to this location's hints to convey useful information. Typically used for entrance randomization."""

    id: int | None = None
    """(Optional) Skips the item ID forward to the given value.
    This can be used to provide buffer space for future items."""

    @property
    def data(self) -> JsonObject:
        return compact(
            {
                "name": self.name,
                "requires": self.requires,
                "category": list_names_or_none(self.category),
                "region": self.region.name if self.region else None,
                "place_item": list_names_or_none(self.place_item),
                "dont_place_item": list_names_or_none(self.dont_place_item),
                "place_item_category": list_names_or_none(self.place_item_category),
                "dont_place_item_category": list_names_or_none(
                    self.dont_place_item_category
                ),
                "victory": self.victory or None,
                "prehint": self.prehint or None,
                "hint_entrance": self.hint_entrance or None,
                "id": self.id,
            }
        )


@dataclass
class ItemSpec:
    name: str
    """The unique name of the item. Do not use (), :, or | in the name"""

    category: list["CategorySpec"] = field(default_factory=list)
    """(Optional) A list of categories to be applied to this item."""

    count: int = field(default=1)
    """(Optional) Total number of this item that will be in the itempool for randomization."""

    value: dict[str, int] = field(default_factory=dict)
    """(Optional) A dictionary of values this item has in the format {"name": int,"otherName": int}
    Used with the {ItemValue(Name: int)} in location requires eg. "value": {"coins":10} mean this item is worth 10 coins"""

    progression = False
    """(Optional) Is this item needed to unlock locations? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    progression_skip_balancing = False
    """(Optional) Should this item not get included in progression balance swaps? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    useful = False
    """(Optional) Is this item useful to have but not required to complete the game? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    trap = False
    """(Optional) Is this item something the player doesn't want to get? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    filler = False
    """(Optional) Is this item mostly useless and okay to skip placing sometimes? For more information on item classifications, see: https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#items"""

    early: int | bool = False
    """(Optional) How many copies of this item are required to be placed somewhere accessible from the start (Sphere 1)
    Choosing 'True' mark all of them to be early"""

    local = False
    """(Optional) Are all copies of this item supposed to be only in your locations (true), or can they be anywhere (false)?"""

    local_early = False
    """(Optional) How many copies of this item (or 'true' if all copies) are supposed to be early and only in your locations.
    Can be used to mark some of the copies of an item to be early and local since 'local' is a toggle between none or all of them."""

    id: int | None = None
    """(Optional) Skips the item ID forward to the given value.
    This can be used to provide buffer space for future items."""

    def __post_init__(self):
        if self.count < 1:
            raise Exception(f'Error in item "{self.name}": count must be at least 1')

    @property
    def data(self) -> JsonObject:
        return compact(
            {
                "name": self.name,
                "category": list_names_or_none(self.category),
                "count": self.count if self.count != 1 else None,
                "value": self.value or None,
                "progression": self.progression or None,
                "progression_skip_balancing": self.progression_skip_balancing or None,
                "useful": self.useful or None,
                "trap": self.trap or None,
                "filler": self.filler or None,
                "early": self.early or None,
                "local": self.local or None,
                "local_early": self.local_early or None,
                "id": self.id,
            }
        )


@dataclass
class RegionSpec:
    name: str
    requires: str | None = None
    connects_to: list[str] = field(default_factory=list)
    starting: bool = False
    exit_requires: dict[str, str] = field(default_factory=dict)
    entrance_requires: dict[str, str] = field(default_factory=dict)

    @property
    def data(self) -> JsonObject:
        return compact(
            {
                "name": self.name,
                "requires": self.requires,
                "connects_to": self.connects_to or None,
                "starting": self.starting or None,
                "exit_requires": self.exit_requires or None,
                "entrance_requires": self.entrance_requires or None,
            }
        )


@dataclass
class CategorySpec:
    name: str

    hidden: Optional[bool] = None
    """(Optional) Should this category be Hidden in the client?"""

    yaml_option: Optional[list["OptionSpec"]] = None
    """(Optional) Array of Options that will decide if the items & locations in this category are enabled"""

    @property
    def data(self) -> JsonObject:
        return compact(omit(dataclasses.asdict(self), "name"))


@dataclass(kw_only=True)
class OptionSpec:
    name: str = field(kw_only=False)
    description: str | list[str] | None = None
    """Description text explaining what this option does"""
    display_name: str | None = None
    """The display name shown to users for this option"""
    rich_text_doc: bool | None = None
    """Whether the description should be rendered as rich text"""
    group: str | None = None
    """The group this option belongs to in the UI"""
    hidden: bool | None = None
    """Whether this option should be hidden from the UI"""
    visibility: str | list[str] | int | None = None
    """Controls when this option is visible to users"""

    @property
    def data(self) -> JsonObject:
        return compact(omit(dataclasses.asdict(self), "name"))


@dataclass
class ToggleOptionSpec(OptionSpec):
    default: bool
    """The default value for this toggle option"""


@dataclass
class ChoiceOptionSpec(OptionSpec):
    ## TODO: nicer API for this
    values: dict[str, int]
    """Mapping of choice names to their corresponding values"""
    default: int
    """The default value for this choice option"""
    aliases: dict[str, int | str] | None = None
    """Alternative names that map to the same choices"""
    allow_custom_value: bool | None = None
    """Whether users can input custom values not in the predefined choices"""


@dataclass
class RangeOptionSpec(OptionSpec):
    name: str
    range_start: int
    """The minimum value allowed for this range"""
    range_end: int
    """The maximum value allowed for this range"""
    default: int
    """The default value for this range option"""
    values: dict[str, int] | None = None
    """Optional mapping of named values within the range"""


@dataclass
class MetaSpec:
    docs: "Docs | None" = None
    enable_region_diagram: bool | None = None

    @property
    def data(self) -> JsonObject:
        return compact(omit(dataclasses.asdict(self), "name"))

    @dataclass
    class Docs:
        apworld_description: list[str] | None = None
        web: "Web | None" = None

        @property
        def data(self) -> JsonObject:
            return compact(omit(dataclasses.asdict(self), "name"))

        @dataclass
        class Web:
            type Theme = Literal[
                "dirt",
                "grass",
                "grassFlowers",
                "ice",
                "jungle",
                "ocean",
                "partyTime",
                "stone",
            ]

            options_page: bool | str | None = None
            game_info_languages: list[str] | None = None
            theme: Theme | None = None
            bug_report_page: str | None = None
            tutorials: list[dict] | None = None
            options_presets: list[dict] | None = None

            @property
            def data(self) -> JsonObject:
                return compact(omit(dataclasses.asdict(self), "name"))


@dataclass
class WorldSpec(GameSpec):

    @dataclass(frozen=True)
    class DataFile:
        filename: str
        data_factory: Callable[[], JsonObject]

        @property
        def data(self) -> JsonObject:
            return self.data_factory()

    def __post_init__(self) -> None:
        self.categories: dict[str, CategorySpec] = {}
        self.items: dict[str, "ItemSpec"] = {}
        self.locations: dict[str, LocationSpec] = {}
        self.regions: dict[str, RegionSpec] = {}
        self.core_options: dict[str, OptionSpec] = {}
        self.user_options: dict[str, OptionSpec] = {}
        self.meta = MetaSpec()

        # these internal classes allow reusing the exact signature of the corresponding item classes
        # for factory methods which add the spec objects to the corresponding collection
        #
        # the alternative is writing methods which copy each field, their types, their doc comments, etc.
        # which is significantly more gross and bad and error-prone than this
        #
        # just give me typescript's `Parameters<>` and I'll be happy :)

        parent_self = self

        class BoundCategorySpec(CategorySpec):
            def __post_init__(self):
                set_unique(parent_self.categories, self.name, self)

        class BoundItemSpec(ItemSpec):
            def __post_init__(self):
                set_unique(parent_self.items, self.name, self)

        class BoundLocationSpec(LocationSpec):
            def __post_init__(self):
                set_unique(parent_self.locations, self.name, self)

        class BoundRegionSpec(RegionSpec):
            def __post_init__(self):
                set_unique(parent_self.regions, self.name, self)

        class BoundUserOptionSpec(OptionSpec):
            def __post_init__(self):
                set_unique(parent_self.user_options, self.name, self)

        class BoundCoreOptionSpec(OptionSpec):
            def __post_init__(self):
                set_unique(parent_self.core_options, self.name, self)

        self.category = BoundCategorySpec
        self.item = BoundItemSpec
        self.location = BoundLocationSpec
        self.region = BoundRegionSpec
        self.user_option = BoundUserOptionSpec
        self.core_option = BoundCoreOptionSpec

        def set_unique[T](items: dict[str, T], key: str, value: T) -> T:
            if key in items:
                raise Exception(f"{key} already exists")

            items[key] = value
            return value

    @property
    def item_count(self) -> int:
        return sum(item.count for item in self.items.values())

    @property
    def game_data(self) -> DataFile:
        self_super = super()
        return self.DataFile("game.json", lambda: self_super.data)

    @property
    def categories_data(self) -> DataFile:
        return self.DataFile(
            "categories.json",
            lambda: {name: spec.data for name, spec in self.categories.items()},
        )

    @property
    def items_data(self) -> DataFile:
        return self.DataFile(
            "items.json",
            lambda: {"data": [spec.data for spec in self.items.values()]},
        )

    @property
    def locations_data(self) -> DataFile:
        return self.DataFile(
            "locations.json",
            lambda: {"data": [spec.data for spec in self.locations.values()]},
        )

    @property
    def regions_data(self) -> DataFile:
        return self.DataFile(
            "regions.json",
            lambda: {name: spec.data for name, spec in self.regions.items()},
        )

    @property
    def options_data(self) -> DataFile:
        return self.DataFile(
            "options.json",
            lambda: {
                "core": {name: opt.data for name, opt in self.core_options.items()},
                "user": {name: opt.data for name, opt in self.user_options.items()},
            },
        )

    @property
    def meta_data(self) -> DataFile:
        return self.DataFile("meta.json", lambda: self.meta.data)

    def create_apworld_file(
        self,
        output_dir=Path("C:/ProgramData/Archipelago/custom_worlds"),
        manual_src_dir=Path(__file__).parent / "Manual/src",
        files: dict[str, str] | None = None,
    ) -> Path:
        files = (files or {}).copy()

        if not manual_src_dir.exists():
            raise FileNotFoundError(
                f"Manual source directory not found: {manual_src_dir}"
            )

        with TemporaryDirectory(prefix="manual_kit_standalone") as temp_root_dir:
            temp_root_dir = Path(temp_root_dir)
            temp_src_dir = temp_root_dir / "src"

            shutil.copytree(manual_src_dir, temp_src_dir)

            data_dir = temp_src_dir / "data"
            data_dir.mkdir(parents=True, exist_ok=True)

            import json

            all_data_files = [
                self.game_data,
                self.categories_data,
                self.items_data,
                self.locations_data,
                self.regions_data,
                self.options_data,
                self.meta_data,
            ]

            for data_file in all_data_files:
                (data_dir / data_file.filename).write_text(
                    json.dumps(data_file.data, indent=2, ensure_ascii=False)
                )

            for local_file_path, file_content in files.items():
                file_path = Path(temp_src_dir / local_file_path)
                os.makedirs(file_path.parent, exist_ok=True)
                file_path.write_text(file_content)

            from dataclasses_json import DataClassJsonMixin

            class JsonGameSpec(GameSpec, DataClassJsonMixin):
                pass

            # while in most cases it would work to use `self.game` and `self.creator`,
            # the filename of the apworld **has** to match what's in the game.json file,
            # and the game.json file can be overridden by the `files` arg
            # or changed through other means,
            # so it effectively becomes the best source of truth
            game_spec = JsonGameSpec.from_json(
                (data_dir / self.game_data.filename).read_text()
            )

            world_identifier = f"manual_{game_spec.game}_{game_spec.creator}"
            apworld_file = output_dir / f"{world_identifier}.apworld"

            shutil.move(temp_src_dir, temp_root_dir / world_identifier)

            world_zip = shutil.make_archive(
                str(output_dir / world_identifier),
                format="zip",
                root_dir=temp_root_dir,
                base_dir=".",
            )

        return Path(shutil.move(world_zip, apworld_file))
