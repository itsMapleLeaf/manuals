from typing import NotRequired, TypedDict


class CategoryArgs(TypedDict):
    yaml_option: NotRequired[list[str]]
    """(Optional) Array of Options that will decide if the items & locations in this category are enabled"""

    hidden: NotRequired[bool]
    """(Optional) Should this category be Hidden in the client?"""


class CategoryData(CategoryArgs):
    name: str
    """Name of the category"""
