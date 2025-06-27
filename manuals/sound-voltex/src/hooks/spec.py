from ..manual_kit import WorldSpec

from .songs import SongLoader


class SoundVoltexWorldSpec(WorldSpec):
    def __init__(self) -> None:
        super().__init__()

        songs = SongLoader.load_all_songs()

        song_title_counts: dict[str, int] = {}
        for song in songs:
            song_title_counts[song.title] = song_title_counts.get(song.title, 0) + 1

        for song in songs:
            song_category_name = f"Song ID {song.id}"
            self.category(song_category_name, hidden=True)

            item_name = song.title
            if song_title_counts[song.title] > 1:
                item_name += f" by {song.artist}"

            self.item(
                item_name,
                useful=True,
                category=["Songs", song_category_name],
            )

        for bracket_index in range(10):
            bracket_start = bracket_index * 100 + 10
            bracket_end = (bracket_index + 1) * 100

            for score in range(bracket_start, bracket_end + 10, 10):
                score_location = self.location(
                    f"Reach {score} VOLFORCE",
                    category=[f"Score ({bracket_start}-{bracket_end})"],
                )

                if score == 1000:
                    score_location["victory"] = True
