from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin

from .paths import manual_data_path


@dataclass
class Song(DataClassJsonMixin):
    identifier: str
    title: str
    artist: str
    groups: list[str]
    charts: dict[str, int]


songs_path = manual_data_path("songs.json")

ALL_SONGS: list[Song]
with open(songs_path, "r", encoding="utf-8") as file:
    ALL_SONGS = Song.schema().loads(file.read(), many=True)
