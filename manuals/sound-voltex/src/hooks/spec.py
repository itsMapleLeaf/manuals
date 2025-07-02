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

        self.locations = [
            world_spec.location(
                f"{item_name} ({"/".join(map(str, chart_levels))}) - {i + 1}",
                requires=requires.category(self.category),
                category=[f"Songs - {item_name}"],
            )
            for i in range(2)
        ]


class SoundVoltexWorldSpec(WorldSpec):
    def __init__(self) -> None:
        super().__init__()

        score_values = range(100, 1000 + 1, 100)

        score_gate_item = self.item(
            f"Progressive VOLFORCE Gate",
            category="Progressive VOLFORCE Gate",
            count=len(score_values) * 2,
            progression=True,
        )

        for index, score in enumerate(score_values):
            score_location = self.location(
                f"Reach {score} VOLFORCE",
                category=["VOLFORCE"],
                requires=requires.item(score_gate_item, index + 1),
            )

            if score == 1000:
                score_location["victory"] = True

        self.songs = [SongSpec(song, self) for song in SongLoader.songs]


world_spec = SoundVoltexWorldSpec()
