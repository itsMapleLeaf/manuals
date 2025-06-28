from dataclasses import dataclass

from ..Helpers import load_data_file
from ..manual_kit import WorldSpec, requires


@dataclass
class SongData:
    id: str
    title: str
    artist: str
    groups: list[str]
    charts: dict[str, int]


class SongLoader:
    songs = [SongData(**item) for item in load_data_file("songs.json")]

    song_title_counts: dict[str, int] = {}
    for song in songs:
        song_title_counts[song.title] = song_title_counts.get(song.title, 0) + 1


class SongSpec:
    def __init__(self, data: SongData, world_spec: "SoundVoltexWorldSpec") -> None:
        item_name = data.title
        if SongLoader.song_title_counts[data.title] > 1:
            item_name += f" by {data.artist}"

        chart_levels = [*data.charts.values()]
        chart_levels.sort()

        self.data = data

        self.category = world_spec.category(f"Song ID {data.id}", hidden=True)

        self.item = world_spec.item(
            item_name,
            progression=True,
            category=["Songs", self.category["name"]],
        )

        self.location = world_spec.location(
            f"{item_name} ({"/".join(map(str, chart_levels))}) - Track Clear",
            requires=requires.category(self.category),
            category=["Songs"],
        )


class SoundVoltexWorldSpec(WorldSpec):
    def __init__(self) -> None:
        super().__init__()

        self.songs = [SongSpec(song, self) for song in SongLoader.songs]

        for score in range(100, 1000 + 1, 100):
            score_location = self.location(
                f"Reach {score} VOLFORCE",
                category=["VOLFORCE"],
            )

            if score == 1000:
                score_location["victory"] = True


world_spec = SoundVoltexWorldSpec()
