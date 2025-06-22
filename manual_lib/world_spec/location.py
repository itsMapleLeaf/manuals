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

    def function(self, name: str, input: str):
        return FunctionRequirement(name, input)

    def all_of(self, *items: Requirement):
        return BooleanRequirement("and", items)

    def any_of(self, *items: Requirement):
        return BooleanRequirement("or", items)


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
