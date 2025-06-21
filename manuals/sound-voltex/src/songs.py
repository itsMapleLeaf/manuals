from dataclasses import dataclass
from typing import cast
from typing import cast
from BaseClasses import MultiWorld
from worlds.AutoWorld import World

from .Helpers import get_option_value, load_data_file


@dataclass
class Song:
    identifier: str
    title: str
    artist: str
    groups: list[str]
    charts: dict[str, int]


ALL_SONGS = [Song(**item) for item in load_data_file("songs.json")]

song_names_by_navigator: dict[str, list[str]] = load_data_file("navigators.json")

song_groups_by_category_option = {
    "enable_category_sdvx_original": "SDVX Original",
    "enable_category_floor": "FLOOR",
    "enable_category_bemani": "BEMANI",
    "enable_category_other": "Other",
    "enable_category_touhou_arrange": "Touhou Arrange",
    "enable_category_vocaloid": "Vocaloid",
    "enable_category_pops_anime": "Pops & Anime",
    "enable_category_hinabitter_bandmeshi": "Hinabitter♪/BandMeshi♪",
}


class SongLibrary:
    PLAYABLE_SONGS: list[Song] = []
    BOSS_SONGS: list[Song] = []

    for song in ALL_SONGS:
        is_boss = any(level >= 20 for level in song.charts.values())
        if is_boss:
            BOSS_SONGS += [song]
        else:
            PLAYABLE_SONGS += [song]

    allowed_songs: list[Song] = []
    allowed_navigator_songs: dict[str, list[Song]] = {}
    chosen_songs: list[Song] = []

    def __init__(
        self,
        multiworld: MultiWorld,
        world: World,
        player: int,
        chosen_song_count: int,
        min_difficulty: int,
        max_difficulty: int,
    ) -> None:
        for navigator in song_names_by_navigator:
            self.allowed_navigator_songs[navigator] = []

        for song in SongLibrary.PLAYABLE_SONGS:
            has_valid_difficulty = False
            for chart in song.charts:
                difficulty = song.charts[chart]
                if min_difficulty <= difficulty <= max_difficulty:
                    has_valid_difficulty = True
                    break

            has_valid_category = False
            for category_option_name in song_groups_by_category_option:
                is_category_enabled = cast(
                    bool, get_option_value(multiworld, player, category_option_name)
                )
                if not is_category_enabled:
                    continue

                group_name = song_groups_by_category_option[category_option_name]
                if group_name in song.groups:
                    has_valid_category = True
                    break

            is_valid = has_valid_difficulty and has_valid_category
            if not is_valid:
                continue

            is_navigator_song = False
            for navigator in song_names_by_navigator:
                if song.title in song_names_by_navigator[navigator]:
                    self.allowed_navigator_songs[navigator].append(song)
                    is_navigator_song = True
                    break

            if not is_navigator_song:
                self.allowed_songs.append(song)

        for navigator_songs in self.allowed_navigator_songs.values():
            # print("chosen_navigator_songs:")
            # print("\n".join(chosen_navigator_songs), len(chosen_navigator_songs))
            world.random.shuffle(navigator_songs)
            self.chosen_songs.extend(
                navigator_songs.pop() for _ in range(min(5, len(navigator_songs)))
            )

        # chosen_allowed_songs = world.random.sample(
        #     [*self.allowed_songs],
        #     k=min(chosen_song_count, len(self.allowed_songs)),
        # )
        world.random.shuffle(self.allowed_songs)
        # print("chosen_allowed_songs:")
        # print("\n".join(chosen_allowed_songs), len(chosen_allowed_songs))
        self.chosen_songs.extend(
            self.allowed_songs.pop()
            for _ in range(min(chosen_song_count, len(self.allowed_songs)))
        )

        chosen_boss_songs = world.random.sample(
            SongLibrary.BOSS_SONGS, k=min(3, len(SongLibrary.BOSS_SONGS))
        )
        # print("chosen_boss_songs:")
        # print("\n".join(chosen_boss_songs), len(chosen_boss_songs))
        self.chosen_songs.extend(chosen_boss_songs)
