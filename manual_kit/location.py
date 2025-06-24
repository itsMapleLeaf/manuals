from dataclasses import dataclass
from typing import Iterable, Literal, NotRequired, Optional, TypedDict

from .item import ItemData
from .category import CategoryData


class Requirement:
    pass


@dataclass
class ItemRequirement(Requirement):
    subject: str
    amount: Optional[str] = None
    is_category: bool = False

    def __str__(self) -> str:
        output = "|"

        if self.is_category:
            output += "@"

        output += self.subject

        if self.amount:
            output += ":" + self.amount

        return output + "|"


@dataclass
class FunctionRequirement(Requirement):
    name: str
    input: str

    def __str__(self) -> str:
        return "%s(%s)" % (self.name, self.input)


@dataclass
class BooleanRequirement(Requirement):
    operator: Literal["or"] | Literal["and"]
    members: Iterable[Requirement]

    def __str__(self) -> str:
        return "(%s)" % f" {self.operator} ".join(map(str, self.members))


class Requires:
    def item(self, item: ItemData, amount: Optional[str | int] = None):
        return ItemRequirement(
            item["name"],
            str(amount) if amount != None else None,
        )

    def category(self, category: CategoryData, amount: Optional[str | int] = None):
        return ItemRequirement(
            category["name"],
            str(amount) if amount != None else None,
            is_category=True,
        )

    def all_of(self, *items: Requirement):
        return BooleanRequirement("and", items)

    def any_of(self, *items: Requirement):
        return BooleanRequirement("or", items)

    def function(self, name: str, input: str | Requirement):
        return FunctionRequirement(name, str(input))

    def item_value(self, key: str, amount: str | int):
        """
        Checks if you've collected the specificed value of a value-based item.

        For Example, `{ItemValue(Coins:12)}` will check if the player has collect at least 12 coins worth of items
        """

        return self.function("ItemValue", f"{key}:{amount}")

    def opt_one(self, input: Requirement):
        """
        Requires an item only if that item exists.  Useful if an item might have been disabled by a yaml option.
        """
        return self.function("OptOne", str(input))

    def opt_all(self, input: str | Requirement):
        """
        Takes an entire requires string, and applies the above check to each item inside it.

        For example, `requires: "{OptAll(|DisabledItem| and |@CategoryWithModifedCount:10|)} and |other items|"` will be transformed into `"|DisabledItem:0| and |@CategoryWithModifedCount:2| and |other items|"`
        """
        return self.function("OptAll", input)

    def yaml_enabled(self, option_name: str):
        """
        Allows you to check yaml options within your logic.

        You might use this to allow glitches

        ```json
        {
            "name": "Item on Cliff",
            "requires": "|Double Jump| or {YamlEnabled(allow_hard_glitches)}"
        }
        ```

        Or make key items optional

        ```json
        {
            "name": "Hidden Item in Pokemon",
            "requires": "|Itemfinder| or {YamlDisabled(require_itemfinder)}"
        }
        ```

        You can even combine the two in complex ways

        ```json
        {
            "name": "This is probably a region",
            "requires": "({YamlEnabled(easy_mode)} and |Gravity|) or ({YamlDisabled(easy_mode)} and |Jump| and |Blizzard| and |Water|)"
        }
        ```
        """
        return self.function("YamlEnabled", option_name)

    def yaml_disabled(self, option_name: str):
        """
        Allows you to check yaml options within your logic.

        You might use this to allow glitches

        ```json
        {
            "name": "Item on Cliff",
            "requires": "|Double Jump| or {YamlEnabled(allow_hard_glitches)}"
        }
        ```

        Or make key items optional

        ```json
        {
            "name": "Hidden Item in Pokemon",
            "requires": "|Itemfinder| or {YamlDisabled(require_itemfinder)}"
        }
        ```

        You can even combine the two in complex ways

        ```json
        {
            "name": "This is probably a region",
            "requires": "({YamlEnabled(easy_mode)} and |Gravity|) or ({YamlDisabled(easy_mode)} and |Jump| and |Blizzard| and |Water|)"
        }
        ```
        """
        return self.function("YamlEnabled", option_name)

    def yaml_compare(
        self,
        option_name: str,
        comparator: (
            Literal["=="]
            | Literal["="]
            | Literal["!="]
            | Literal[">="]
            | Literal["<="]
            | Literal["<"]
            | Literal[">"]
        ),
        value: str | int,
    ):
        """
        Verify that the result of the option called _option_name_'s value compared using the _comparator_symbol_ with the requested _value_

        The comparator symbol can be any of the following: `== or =, !=, >=, <=, <, >`

        The value can be of any type that your option supports

        - Range: integer aka number
        - Range with values aka NamedRange: integer or one of the value name in "values"
        - Choice: either numerical or string representation of a value in the option's "values"
        - Choice with allow_custom_value: either numerical or string representation of a value in the option's "values" or a custom string
        - Toggle: a boolean value represented by any of the following not case sensitive:
        - True: "true", "on", 1
        - False: "false", "off", 0

        The folowing example would check that the player.yaml value of the range option Example_Range is bigger than 5 or that the `Item A` item is present:

        ```json
        {
            "name": "Example Region",
            "requires": "|Item A| or {YamlCompare(Example_Range > 5)}"
        }
        ```
        """

        return self.function(
            "YamlCompare", " ".join([option_name, comparator, str(value)])
        )


class LocationArgs(TypedDict):
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

    hint_entrance: NotRequired[str]
    """(Optional) Adds additional text to this location's hints to convey useful information. Typically used for entrance randomization."""

    id: NotRequired[int]
    """(Optional) Skips the item ID forward to the given value.
    This can be used to provide buffer space for future items."""


class LocationData(LocationArgs):
    name: str
    """The unique name of the location."""

    requires: NotRequired[str]
    """(Optional) A boolean logic string that describes the required items, counts, etc. needed to reach this location."""
