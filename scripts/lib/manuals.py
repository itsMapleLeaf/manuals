from dataclasses import dataclass
import os
from pathlib import Path
from typing import TypedDict
from manual_kit import CategoryData, LocationData, ItemData

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
        import tempfile
        import json
        import subprocess
        import textwrap

        with open(Path(__file__).parent / "data_loader.py") as data_loader_file:
            data_loader_script = data_loader_file.read()

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            dir=self.src,
            delete_on_close=False,
        ) as temp_file:
            temp_file.write(data_loader_script)
            temp_file.close()
            (temp_module, _) = os.path.splitext(os.path.basename(temp_file.name))

            python_paths = [
                PROJECT_ROOT,
                ARCHIPELAGO_FOLDER,
            ]

            data_json = subprocess.check_output(
                ["uv", "run", "-m", f"src.{temp_module}"],
                cwd=self.root,
                env={
                    **os.environ.copy(),
                    "PYTHONPATH": ";".join(map(str, python_paths)),
                },
            )

        return ManualData(**json.loads(data_json))


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
