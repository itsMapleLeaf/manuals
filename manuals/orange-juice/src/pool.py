from typing import ClassVar, cast
from BaseClasses import MultiWorld

from .spec import spec


class OrangeJuiceWorldGenPool:
    player_pools: ClassVar[dict[int, "OrangeJuiceWorldGenPool"]] = {}

    characters: set[str]
    boards: set[str]

    def __init__(self, multiworld: MultiWorld, player: int) -> None:
        from .Helpers import get_option_value

        self.characters = set(
            multiworld.random.sample(
                [*spec.characters.keys()],
                k=cast(
                    int,
                    get_option_value(
                        multiworld, player, spec.character_count_option.name
                    ),
                ),
            )
        )

        self.boards = set(
            multiworld.random.sample(
                [*spec.boards.keys()],
                k=cast(
                    int,
                    get_option_value(multiworld, player, spec.board_count_option.name),
                ),
            )
        )
