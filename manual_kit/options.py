from dataclasses import dataclass
from typing import Literal, TypedDict, NotRequired


type OptionData = ToggleOptionData | ChoiceOptionData | RangeOptionData
type OptionSpec = ToggleOptionSpec | ChoiceOptionSpec | RangeOptionSpec


class BaseOptionData(TypedDict):
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


class ToggleOptionArgs(BaseOptionData):
    default: bool
    """The default value for this toggle option"""


class ToggleOptionData(ToggleOptionArgs):
    type: Literal["Toggle"]


@dataclass
class ToggleOptionSpec:
    name: str
    args: ToggleOptionArgs


class ChoiceOptionArgs(BaseOptionData):
    values: dict[str, int]
    """Mapping of choice names to their corresponding values"""
    default: int
    """The default value for this choice option"""
    aliases: NotRequired[dict[str, int | str]]
    """Alternative names that map to the same choices"""
    allow_custom_value: NotRequired[bool]
    """Whether users can input custom values not in the predefined choices"""


class ChoiceOptionData(ChoiceOptionArgs):
    type: Literal["Choice"]


@dataclass
class ChoiceOptionSpec:
    name: str
    args: ChoiceOptionArgs


class RangeOptionArgs(BaseOptionData):
    range_start: int
    """The minimum value allowed for this range"""
    range_end: int
    """The maximum value allowed for this range"""
    default: int
    """The default value for this range option"""
    values: NotRequired[dict[str, int]]
    """Optional mapping of named values within the range"""


class RangeOptionData(RangeOptionArgs):
    type: Literal["Range"]


@dataclass
class RangeOptionSpec:
    name: str
    args: RangeOptionArgs
