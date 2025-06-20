import json
from logging import warning
import os
import zipfile
from pathlib import Path
from typing import Dict, List, NotRequired, Union, TypedDict

from .lib.songs import ALL_SONGS
from .lib.navigators import navigators
from .lib.paths import manual_data_path


class Item(TypedDict):
    name: str
    category: NotRequired[List[str]]
    count: NotRequired[int]
    value: NotRequired[Dict[str, Union[str, int]]]
    progression: NotRequired[bool]
    progression_skip_balancing: NotRequired[bool]
    useful: NotRequired[bool]
    trap: NotRequired[bool]


class Location(TypedDict):
    name: str
    category: NotRequired[List[str]]
    requires: NotRequired[str]
    place_item: NotRequired[List[str]]
    place_item_category: NotRequired[List[str]]
    victory: NotRequired[bool]


class Category(TypedDict):
    hidden: NotRequired[bool]
    yaml_option: NotRequired[List[str]]


class StartingItemInfo(TypedDict):
    items: NotRequired[list[str]]
    item_categories: NotRequired[list[str]]
    random: NotRequired[int]


class GameInfo(TypedDict):
    game: str
    creator: str
    filler_item_name: str
    death_link: bool
    starting_items: list[StartingItemInfo]


def song_number_category_for(song_number: int) -> str:
    return f"Song Number {song_number}"


def navigator_key_category_for(navigator: str) -> str:
    return f"Navigator Access for {navigator}"


class SoundVoltexWorld:
    locations: list[Location] = []
    items: list[Item] = []
    categories: dict[str, Category] = {}

    @property
    def item_count(self):
        return sum(item.get("count") or 1 for item in self.items)

    def __init__(self) -> None:
        self.locations += [
            Location(
                name="PERFECT ULTIMATE CHAIN",
                requires="|@Boss Clear|",
                victory=True,
                category=["(((Victory)))"],
            )
        ]

        self.items += [
            Item(
                name=f"CHAIN {"%03d" % amount}",
                category=["CHAIN"],
                progression=True,
                count=count,
                value={"chain": amount},
            )
            for amount, count in [
                (100, 1),
                (50, 2),
                (20, 3),
                (10, 5),
                (5, 10),
                (1, 20),
            ]
        ]

        self.categories["Goals"] = {"hidden": True}

        for navigator in navigators:
            self.categories[navigator_key_category_for(navigator)] = Category(
                hidden=True
            )
            self.items += [
                Item(
                    name=navigator,
                    progression=True,
                    category=["Navigator Keys", navigator_key_category_for(navigator)],
                )
            ]

        for song_number, song in enumerate(ALL_SONGS):
            self.categories[song.identifier] = Category(hidden=True)
            self.categories[song_number_category_for(song_number)] = Category(
                hidden=True
            )

            song_navigators = [
                navigator
                for navigator, navigator_songs in navigators.items()
                if song.title in navigator_songs
            ]

            goals = ["Track Clear", "AA Rank", "AAA Rank"]
            is_boss = any(level >= 20 for level in song.charts.values())

            if is_boss:
                self.items += [
                    Item(
                        name=song.identifier,
                        progression=True,
                        category=[
                            "Goals",
                            song.identifier,
                            song_number_category_for(song_number),
                            "Boss Access",
                        ],
                    ),
                    Item(
                        name=f"{song.identifier} (Completion)",
                        progression=True,
                        category=["Goals", song.identifier, "Boss Clear"],
                    ),
                ]
                self.locations += [
                    Location(
                        name=song.identifier,
                        requires=f"{{ItemValue(chain:300)}} and |@{song_number_category_for(song_number)}|",
                        category=[
                            "Goals",
                            song.identifier,
                            f"(Boss) {song.identifier}",
                        ],
                        place_item=[f"{song.identifier} (Completion)"],
                    )
                ]
            elif song_navigators:
                for goal in goals:
                    self.locations += [
                        Location(
                            name=f"{song.identifier} ({goal})",
                            requires=" or ".join(
                                f"|@{navigator_key_category_for(navigator)}|"
                                for navigator in song_navigators
                            ),
                            category=[
                                "Goals",
                                song.identifier,
                                *[
                                    f"(Song) ({navigator}) {song.identifier}"
                                    for navigator in song_navigators
                                ],
                            ],
                        )
                    ]
            else:
                self.items += [
                    Item(
                        name=song.identifier,
                        progression=True,
                        category=[
                            "Songs",
                            song.identifier,
                            song_number_category_for(song_number),
                        ],
                    )
                ]
                for goal in goals:
                    self.locations += [
                        Location(
                            name=f"{song.identifier} ({goal})",
                            requires=f"|@{song_number_category_for(song_number)}|",
                            category=[
                                "Goals",
                                song.identifier,
                                f"(Song) {song.identifier}",
                                f"(Goal) {goal}",
                            ],
                        )
                    ]

        # set the current lazer color, which ever came latest
        # they're all traps because any of them could give you awkward combinations,
        # like reversed colors, same colors,
        # or non-normal colors that are reversed from the previous non-normal colors
        # that you got used to (lol)
        # self.items += [
        #     Item(
        #         name=f"{side} Lazer: {color}",
        #         count=2,
        #         trap=True,
        #         category=["(Traps) Lazer Color"],
        #     )
        #     for side in ["Left", "Right"]
        #     for color in ["Red", "Yellow", "Green", "Blue"]
        # ]

        # alter speed (1.0x === CMod/MMod 100)
        # set base speed at the start of the game
        # current speed is the sum of all
        # all are traps; slow or fast are both bad, but they can balance out!
        # self.items += [
        #     Item(name="Speed +0.2", count=8, trap=True, category=["(Traps) Speed"]),
        #     Item(name="Speed -0.2", count=8, trap=True, category=["(Traps) Speed"]),
        # ]

        # set the random mod, whichever came latest
        # self.items += [
        #     Item(name="Random On", count=3, trap=True, category=["(Traps) Random"]),
        #     Item(name="Random Off", count=3, useful=True, category=["(Traps) Random"]),
        # ]

        # progressive hidden/sudden, current is sum of all
        # self.items += [
        #     Item(name="Hidden +5%", count=8, trap=True, category=["(Traps) Hidden"]),
        #     Item(name="Hidden -5%", count=8, useful=True, category=["(Traps) Hidden"]),
        #     Item(name="Sudden +5%", count=8, trap=True, category=["(Traps) Sudden"]),
        #     Item(name="Sudden -5%", count=8, useful=True, category=["(Traps) Sudden"]),
        # ]

        # adds an amount to a score to reach a goal
        self.items += [
            Item(
                name=f"Score +{bonus}",
                count=count,
                useful=True,
                category=["Score"],
            )
            for count, bonus in [
                (50, "5.0000"),
                (20, "10.0000"),
                # (1, "100.0000"),
                # (3, "50.0000"),
                # (6, "20.0000"),
                # (12, "10.0000"),
                # (20, "5.0000"),
            ]
        ]

        # adds a percentage to a score to make it a pass
        self.items += [
            Item(
                name=f"Score Gauge +{bonus}%",
                count=count,
                useful=True,
                category=["Score Gauge"],
            )
            for count, bonus in [
                (20, "5"),
                # (3, "25"),
                # (5, "10"),
                # (8, "5"),
                # (15, "1"),
            ]
        ]

        self.items += [
            # Item(name="Cancel Trap", count=10, useful=True, category=["Helpers"]),
            Item(name="Downlevel", count=10, useful=True, category=["Helpers"]),
        ]

        # start with hard timing window, and this "upgrades" to normal
        normal_timing_window_item = Item(
            name="Normal Timing Window", progression=True, category=["Helpers"]
        )
        self.items += [
            normal_timing_window_item,
        ]
        self.locations += [
            Location(
                name=normal_timing_window_item["name"],
                category=["(Helpers) Normal Timing Window"],
                requires=f"|{normal_timing_window_item["name"]}|",
            ),
        ]

        gauge_levels = [
            # start at Blastive 2.5
            "Blastive 2.0",
            "Blastive 1.5",
            "Blastive 1.0",
            "Blastive 0.5",
            "Effective",
        ]

        self.items += [
            Item(
                name="Progressive Gauge",
                count=len(gauge_levels) + 3,
                progression=True,
                category=["Progressive Gauge"],
            )
        ]

        for index, rate in enumerate(gauge_levels):
            self.locations += [
                Location(
                    name=f"Progressive Gauge ({rate})",
                    requires=f"|Progressive Gauge:{index + 1}|",
                    category=["((Helpers)) Progressive Gauge"],
                )
            ]


if __name__ == "__main__":
    is_dev = True
    if os.getenv("DEV") == False:
        is_dev = False

    if is_dev:
        warning("Building a development world suffixed with '_dev'")
        warning("Set the envionment variable DEV=false to generate without _dev suffix")

    game_info = GameInfo(
        game="SDVX" + ("_dev" if is_dev else ""),
        creator="MapleLeaf",
        filler_item_name="you tried (Score +1.0000)",
        death_link=False,
        starting_items=[{"item_categories": ["Songs"], "random": 5}],
    )

    world = SoundVoltexWorld()

    world_file_name = f"manual_{game_info['game']}_{game_info['creator']}"
    script_dir = Path(__file__).parent

    apworld_folder = Path(
        os.environ.get("APWORLD_OUTPUT_FOLDER") or script_dir.parent.parent / "dist"
    )
    apworld_folder.mkdir(exist_ok=True)

    zip_path = apworld_folder / f"{world_file_name}.apworld"

    class JsonDumpArgs(TypedDict):
        ensure_ascii: NotRequired[bool]
        indent: NotRequired[str | int]

    json_dump_args = JsonDumpArgs(ensure_ascii=False)
    if is_dev:
        json_dump_args["indent"] = "\t"

    print(f"Game: {game_info['game']}")
    print(f"Creator: {game_info['creator']}")

    print(f"Generated {world.item_count} items")
    print(f"Generated {len(world.locations)} locations")
    print(f"Configured {len(world.categories)} categories")
    print(f"World path: {zip_path}")

    print("Saving game info...")
    with open(manual_data_path("game.json"), "w", encoding="utf-8") as file:
        json.dump(game_info, file, **json_dump_args)

    print("Saving items...")
    with open(manual_data_path("items.json"), "w", encoding="utf-8") as file:
        json.dump(world.items, file, **json_dump_args)

    print("Saving locations...")
    with open(manual_data_path("locations.json"), "w", encoding="utf-8") as file:
        json.dump(world.locations, file, **json_dump_args)

    print("Saving categories...")
    with open(manual_data_path("categories.json"), "w", encoding="utf-8") as file:
        json.dump(world.categories, file, **json_dump_args)

    print("Saving apworld...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        manual_src = script_dir.parent / "src"
        for root, dirs, files in os.walk(manual_src):
            for file in files:
                file_path = Path(root) / file
                arcname = Path(world_file_name) / file_path.relative_to(manual_src)
                zip_file.write(file_path, arcname)

    print("Done!")
