from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Song:
    id: str
    title: str
    artist: str
    groups: list[str]
    charts: dict[str, int]


class SongLoader:
    loaded_songs: ClassVar[list[Song] | None] = []

    @classmethod
    def load_all_songs(cls) -> list[Song]:
        if not cls.loaded_songs:
            from ..Helpers import load_data_file

            cls.loaded_songs = [Song(**item) for item in load_data_file("songs.json")]

        return cls.loaded_songs
