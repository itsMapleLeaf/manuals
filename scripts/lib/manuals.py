from dataclasses import dataclass
import dataclasses
import os
from pathlib import Path
from types import ModuleType
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

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            dir=self.src,
            delete_on_close=False,
        ) as temp_file:
            data_loader_script = textwrap.dedent(
                """
                from . import Data
                import json

                print(json.dumps({
                    "game_table": Data.game_table,
                    "item_table": Data.item_table,
                    "location_table": Data.location_table,
                    "region_table": Data.region_table,
                    "category_table": Data.category_table,
                    "option_table": Data.option_table,
                    "meta_table": Data.meta_table,
                }))
                """
            ).strip()

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


@dataclass
class ManualData:
    game_table: dict[str, object]
    item_table: list[ItemData]
    location_table: list[LocationData]
    region_table: dict[str, object]
    category_table: dict[str, CategoryData]
    option_table: dict[str, object]
    meta_table: dict[str, object]

    @classmethod
    def from_module(cls, module: ModuleType) -> "ManualData":
        class_fields = {f.name for f in dataclasses.fields(cls)}
        known_module_items = {
            k: v for k, v in module.__dict__.items() if k in class_fields
        }
        return ManualData(**known_module_items)


MANUALS_FOLDER = PROJECT_ROOT / "manuals"
MANUALS = {name: ManualDefinition(name) for name in os.listdir(MANUALS_FOLDER)}
