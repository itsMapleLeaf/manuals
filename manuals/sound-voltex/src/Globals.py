from typing import TYPE_CHECKING


# fixes circular import
if TYPE_CHECKING:
    from .songs import SongLibrary

PLAYER_SONG_LIBRARIES: dict[int, "SongLibrary"] = {}
