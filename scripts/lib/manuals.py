from dataclasses import dataclass
import os
from pathlib import Path
from typing import TypedDict
from manual_kit import CategoryData, LocationData, ItemData, manspect

from .paths import ARCHIPELAGO_FOLDER, PROJECT_ROOT


@dataclass
class ManualDefinition:
    name: str

    @property
    def root(self) -> Path:
        return MANUALS_FOLDER / self.name

    @property
    def src(self) -> Path:
        return self.root / "src"

    @property
    def data_folder(self) -> Path:
        return self.src / "data"

    @property
    def dist(self) -> Path:
        return self.root / "dist"

    def load_data(self):
        return manspect.inspect_from_source(
            self.src,
            archipelago_repo_path=ARCHIPELAGO_FOLDER,
        )


class ManualData(TypedDict):
    game_table: dict[str, object]
    item_table: list[ItemData]
    location_table: list[LocationData]
    region_table: dict[str, object]
    category_table: dict[str, CategoryData]
    option_table: dict[str, object]
    meta_table: dict[str, object]


MANUALS_FOLDER = PROJECT_ROOT / "manuals"
MANUALS = {name: ManualDefinition(name) for name in os.listdir(MANUALS_FOLDER)}
