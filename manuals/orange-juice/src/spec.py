from typing import Optional
from dataclasses import dataclass

from .manual_kit import WorldSpec, requires, RangeOptionSpec
from .util import plural


@dataclass
class CharacterSpec:
    name: str
    goal: Optional[str] = None


@dataclass
class BoardSpec:
    name: str


@dataclass
class OrangeItemSpec:
    value: int
    count: int


class OrangeJuiceWorldSpec(WorldSpec):
    characters: dict[str, CharacterSpec] = {
        item.name: item
        for item in [
            CharacterSpec("QP"),
            CharacterSpec("Yuki"),
            CharacterSpec("Aru"),
            CharacterSpec("Suguri"),
            CharacterSpec("Hime"),
            CharacterSpec("Sora"),
            CharacterSpec("Marc"),
            CharacterSpec("Fernet"),
            CharacterSpec("Peat"),
            CharacterSpec("Kai"),
            CharacterSpec("Marie Poppo"),
            CharacterSpec("Tomomo"),
            CharacterSpec("Chicken"),
            CharacterSpec("Robo Ball"),
            CharacterSpec("Seagull"),
            CharacterSpec("Store Manager"),
            CharacterSpec("Shifu Robot"),
            CharacterSpec("Flying Castle"),
            CharacterSpec("Syura"),
            CharacterSpec("Nanako"),
            CharacterSpec("QP (Dangerous)"),
            CharacterSpec("Saki"),
            CharacterSpec("Kyousuke"),
            CharacterSpec("Krilalaris"),
            CharacterSpec("Kae"),
            CharacterSpec("Alte"),
            CharacterSpec("Kyoko"),
            CharacterSpec("Marie Poppo (Mixed)"),
            CharacterSpec("Sham"),
            CharacterSpec("Sherry"),
            CharacterSpec("Sora (Military)"),
            CharacterSpec("Star Breaker"),
            CharacterSpec("Sweet Breaker"),
            CharacterSpec("Aru (Scramble)"),
            CharacterSpec("Nath", goal="Play 20 battle cards"),
            CharacterSpec("Mimyuu"),
            CharacterSpec("Tomato"),
            CharacterSpec("Kiriko"),
            CharacterSpec("NoName"),
            CharacterSpec("Ceoreparque"),
            CharacterSpec("Miusaki"),
            CharacterSpec("Yuki (Dangerous)"),
            CharacterSpec("Tomomo (Casual)"),
            CharacterSpec("Suguri (Ver.2)"),
            CharacterSpec("Tsih"),
            CharacterSpec("Tequila"),
            CharacterSpec("Mei"),
            CharacterSpec("Natsumi"),
            CharacterSpec("Nico"),
            CharacterSpec("Arthur"),
            CharacterSpec("Iru"),
            CharacterSpec("Mira"),
            CharacterSpec("Cuties"),
            CharacterSpec("Yuuki"),
            CharacterSpec("Islay"),
            CharacterSpec("Mio"),
            CharacterSpec("Suguri (46 Billion Years)"),
            CharacterSpec("Sumika"),
            CharacterSpec("Ellie"),
            CharacterSpec("Lulu"),
            CharacterSpec("Marc (Pilot)"),
            CharacterSpec("Alicianrone"),
            CharacterSpec("Teotoratta"),
            CharacterSpec("Arnelle"),
            CharacterSpec("Maynie"),
            CharacterSpec("Kyupita"),
            CharacterSpec("Chris"),
            CharacterSpec("Halena"),
            CharacterSpec("Cook"),
            CharacterSpec("Lone Rider"),
            CharacterSpec("Merchant"),
            CharacterSpec("Hime (Moonlight)"),
            CharacterSpec("Fernet (Noble)"),
            CharacterSpec("Malt"),
            CharacterSpec("Mescal"),
            CharacterSpec("Shifu"),
            CharacterSpec("Hoshino Reika"),
            CharacterSpec("Watty"),
            CharacterSpec("Pomeranius"),
            CharacterSpec("Sweet Creator"),
            CharacterSpec("Saki (Sweet Maker)"),
            CharacterSpec("Natsumi (Sweet Blogger)"),
            CharacterSpec("Mio (Festive)"),
            CharacterSpec("Krilalaris (Pajamas)"),
            CharacterSpec("Mimyuu (Jailbird)"),
            CharacterSpec("Mother Poppo"),
            CharacterSpec("Dark Lulu"),
            CharacterSpec("Hyper Ellie"),
            CharacterSpec("Kai (Hero)"),
            CharacterSpec("Bourbon"),
            CharacterSpec("Grain"),
            CharacterSpec("Poyo"),
            CharacterSpec("Chuu"),
            CharacterSpec("Haruka", goal="Revive 10 players with Hype Bringer"),
            CharacterSpec("Kanata"),
        ]
    }

    boards: dict[str, BoardSpec] = {
        item.name: item
        for item in [
            BoardSpec("Practice Field"),
            BoardSpec("Space Wanderer"),
            BoardSpec("Pudding Chase"),
            BoardSpec("Christmas Miracle"),
            BoardSpec("Planet Earth"),
            BoardSpec("Lagoon Flight"),
            BoardSpec("Warfare"),
            BoardSpec("Highway Heist"),
            BoardSpec("Sealed Archive"),
            BoardSpec("Sunset"),
            BoardSpec("Tomomo's Abyss"),
            BoardSpec("White Winter"),
            BoardSpec("Night Flight"),
            BoardSpec("Clover"),
            BoardSpec("Farm"),
            BoardSpec("Star Circuit"),
            BoardSpec("Training Program"),
            BoardSpec("Vortex"),
            BoardSpec("Sweet Heaven"),
            BoardSpec("Starship"),
            BoardSpec("Frost Cave"),
            BoardSpec("Shipyard"),
            BoardSpec("Treasure Island"),
            BoardSpec("Treasure Island (Night)"),
            BoardSpec("Witch Forest"),
            BoardSpec("Icy Hideout"),
            BoardSpec("Sakura Smackdown"),
            BoardSpec("Santa's Workshop"),
            BoardSpec("Ocean Dive"),
            BoardSpec("Over the Sea"),
            BoardSpec("Dark Citadel"),
            BoardSpec("Beginner Town"),
            BoardSpec("Scarred Land"),
            BoardSpec("Fungus Cave"),
            BoardSpec("Beginner Town (Winter)"),
            BoardSpec("Lonely Railway"),
            BoardSpec("Circus"),
            BoardSpec("The Void"),
        ]
    }

    orange_item_specs = [
        OrangeItemSpec(100, 1),
        OrangeItemSpec(50, 2),
        OrangeItemSpec(20, 3),
        OrangeItemSpec(10, 6),
        OrangeItemSpec(5, 12),
        OrangeItemSpec(1, 20),
    ]

    total_oranges = sum(item.count * item.value for item in orange_item_specs)
    required_oranges_for_victory = int(total_oranges / 2)

    character_count_option: RangeOptionSpec
    board_count_option: RangeOptionSpec

    def __init__(self) -> None:
        super().__init__()
        self.define_characters()
        self.define_boards()
        self.define_oranges()
        self.define_victory_location()
        # self.define_achievements()

    def define_characters(self):
        self.character_count_option = self.range_option(
            "character_count",
            display_name="Character Count",
            description="The number of randomly selected characters added to the pool",
            range_start=5,
            range_end=len(self.characters),
            default=20,
        )

        for character in self.characters.values():
            item = self.item(
                character.name,
                category="Characters",
                progression=True,
            )

            character_category = f"Characters - {character.name}"

            if character.goal:
                self.location(
                    f"{character.name} - {character.goal}",
                    category=character_category,
                    requires=requires.item(item),
                )

            for game_count in [1, 2]:
                self.location(
                    f"Play {game_count} {"game" if game_count == 1 else "games"} as {character.name}",
                    category=character_category,
                    requires=requires.opt_all(requires.item(item)),
                )

    def define_boards(self):
        self.board_count_option = self.range_option(
            "board_count",
            display_name="Board Count",
            description="The number of randomly selected boards added to the pool",
            range_start=3,
            range_end=len(self.boards),
            default=20,
        )

        for board in self.boards.values():
            board_item = self.item(
                board.name,
                category="Boards",
                progression=True,
            )

            for game_count in [1, 2]:
                self.location(
                    f"Play {game_count} game{"" if game_count == 1 else "s"} on {board.name}",
                    category=f"Boards - {board.name}",
                    requires=requires.opt_all(requires.item(board_item)),
                )

    def define_oranges(self):
        for item in self.orange_item_specs:
            self.item(
                plural(item.value, "Orange"),
                progression=True,
                category="Oranges",
                count=item.count,
                value={"oranges": item.value},
            )

    def define_achievements(self):
        for achievement in [
            "Win 10 games",
            "Complete 50 normas",
            "Complete 20 win normas",
            "Complete 20 star normas",
            "Collect 10,000 stars",
            "Gain 100 wins",
            "Defeat the field boss",
            "Play 50 mushrooms",
            "Bounty Hunt - Slay 50 monsters",
            "Bounty Hunt - Acquire 120 fame",
        ]:
            self.location(achievement, category="Achievements")

    def define_victory_location(self):
        self.location(
            "Complete Mio's Dark Citadel",
            victory=True,
            category="(Victory)",
            requires=requires.item_value("oranges", self.required_oranges_for_victory),
        )


spec = OrangeJuiceWorldSpec()
