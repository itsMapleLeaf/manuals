from dataclasses import dataclass
import re
from dataclasses_json import DataClassJsonMixin
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from .builder import WorldBuilder, Category


@dataclass
class CampaignData:
    episodes: Optional[int] = None
    dlc: Optional[str] = None


@dataclass
class CardData:
    count: int


@dataclass
class CharacterData:
    goal: Optional[str] = None
    dlc: Optional[str] = None


@dataclass
class ContentData(DataClassJsonMixin):
    campaigns: dict[str, CampaignData]
    characters: dict[str, CharacterData]
    card_packs: dict[str, dict[str, CardData]]
    victory_campaign: str


class OrangeJuiceWorldBuilder(WorldBuilder):
    dlc_categories: dict[str, Category] = {}

    def resolve_dlc_category(self, name: str | None) -> list[Category]:
        if not name:
            return []

        if name in self.dlc_categories:
            return [self.dlc_categories[name]]

        dlc_category = self.category(
            f"{name} DLC",
            hidden=True,
            yaml_option=self.toggle_option(
                f"enable_{to_snake_case(name)}_dlc",
                description=f"Enables the {name} DLC.",
                default=True,
            ),
        )

        self.dlc_categories[name] = dlc_category

        return [dlc_category]

    def build(self):
        content = ContentData.from_json(
            Path("src/data/content.json").read_text(encoding="utf-8")
        )

        for character_name, character_info in content.characters.items():
            character_item = self.item(
                character_name,
                progression=True,
                category=[
                    "Characters",
                ],
            )

            for level in range(4):
                self.location(
                    f"{character_name} - Reach Level {level+2}",
                    category=[f"Characters - {character_name}"],
                    requires=character_item,
                )

            self.location(
                f"{character_name} - Complete a Game",
                category=[f"Characters - {character_name}"],
                requires=character_item,
            )

        orange_amounts = [
            # (orange_count, item_count)
            (100, 1),
            (50, 2),
            (25, 4),
            (10, 10),
            (5, 20),
        ]

        for orange_count, item_count in orange_amounts:
            self.item(
                f"{orange_count} Oranges",
                progression=True,
                filler=True,
                count=item_count,
                value={"oranges": orange_count},
                category=["Oranges"],
            )

        total_oranges = sum(
            orange_count * item_count for orange_count, item_count in orange_amounts
        )

        self.location(
            f"Complete {content.victory_campaign}",
            victory=True,
            requires=f"{{ItemValue(oranges:{int(round(total_oranges * 0.8))})}}",
            category=["Victory"],
        )

        self.generate_data().build_world()


def to_snake_case(text: str):
    words = re.findall(r"[A-Z0-9]?[a-z0-9]+", text)
    return "_".join(words).lower()


if __name__ == "__main__":
    load_dotenv()
    OrangeJuiceWorldBuilder().build()
