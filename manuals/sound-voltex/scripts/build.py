from dataclasses import dataclass
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

        @dataclass
        class ChainItemSpec:
            value: int
            count: int

        chain_item_specs = [
            ChainItemSpec(value=100, count=1),
            ChainItemSpec(value=50, count=2),
            ChainItemSpec(value=20, count=5),
            ChainItemSpec(value=10, count=10),
            ChainItemSpec(value=5, count=16),
            ChainItemSpec(value=1, count=20),
        ]
        chain_amount_total = sum(item.value * item.count for item in chain_item_specs)
        chain_amount_required = int(chain_amount_total * 0.7)

        self.items += [
            Item(
                name=f"CHAIN {"%03d" % item.value}",
                category=[
                    f"CHAIN ({chain_amount_required}/{chain_amount_total} required)"
                ],
                progression=True,
                count=item.count,
                value={"chain": item.value},
            )
            for item in chain_item_specs
        ]

        # adds an amount to a score to reach a goal
        self.items += [
            Item(
                name=f"Score +{bonus}",
                count=count,
                useful=True,
                category=["Helpers"],
            )
            for count, bonus in [
                (25, "5.0000"),
                (10, "10.0000"),
            ]
        ]

        # adds a percentage to a score to make it a pass
        self.items += [
            Item(
                name=f"Score Gauge +5%",
                count=10,
                useful=True,
                category=["Helpers"],
            )
        ]

        # allows playing a lower difficulty
        self.items += [
            Item(
                name="Downlevel",
                count=10,
                useful=True,
                category=["Helpers"],
            ),
        ]

        self.categories["Goals"] = {"hidden": True}

        for navigator in navigators:
            self.items += [
                Item(name=navigator, progression=True, category=["Navigators"])
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

            top_diff = max(song.charts.values())
            is_boss = top_diff >= 20

            def goals():
                match top_diff:
                    case 20:
                        return ["Track Clear"]
                    case 19:
                        return ["Track Clear", "A Rank", "AA Rank"]
                    case 18:
                        return ["Track Clear", "AA Rank", "AAA Rank"]
                    case _:
                        return ["AAA Rank", "S Rank"]

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
                        requires=f"{{ItemValue(chain:{chain_amount_required})}} and |@{song_number_category_for(song_number)}|",
                        category=[
                            "Goals",
                            song.identifier,
                            f"(Boss) {song.identifier}",
                        ],
                        place_item=[f"{song.identifier} (Completion)"],
                    )
                ]
            elif song_navigators:
                for goal in goals():
                    self.locations += [
                        Location(
                            name=f"{song.identifier} ({goal})",
                            requires=" or ".join(
                                f"|{navigator}|" for navigator in song_navigators
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
                for goal in goals():
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
        os.environ.get("APWORLD_OUTPUT_FOLDER")
        or "C:/ProgramData/Archipelago/custom_worlds"
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
