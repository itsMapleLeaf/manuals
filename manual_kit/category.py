from typing import Final, NotRequired, TypedDict


class CategoryArgs(TypedDict):
    yaml_option: NotRequired[list[str]]
    """(Optional) Array of Options that will decide if the items & locations in this category are enabled"""

    hidden: NotRequired[bool]
    """(Optional) Should this category be Hidden in the client?"""


class CategoryData(CategoryArgs):
    pass


class CategorySpec:
    def __init__(self, name: str, data: CategoryData) -> None:
        self.name: Final = name
        self.data: Final = data
