from dataclasses import dataclass
import dataclasses
import os
from pathlib import Path
from types import ModuleType
from manual_lib.world_spec import CategoryData, LocationData, ItemData

from .paths import PROJECT_ROOT


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
        import importlib.util
        import sys

        data_module_path = self.src / "Data.py"
        spec = importlib.util.spec_from_file_location(
            f"{self.name}.src.Data", data_module_path
        )

        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module from {data_module_path}")

        data_module = importlib.util.module_from_spec(spec)

        old_path = sys.path[:]
        old_modules = sys.modules.copy()

        try:
            sys.path.insert(0, str(self.root.parent))
            sys.path.append(str(PROJECT_ROOT / "Archipelago"))

            src_module = ModuleType(f"{self.name}.src")
            src_module.__path__ = [str(self.src)]
            sys.modules[f"{self.name}.src"] = src_module

            spec.loader.exec_module(data_module)
        finally:
            sys.path[:] = old_path
            for module_name in list(sys.modules.keys()):
                if module_name.startswith(f"{self.name}.") or module_name == self.name:
                    if module_name not in old_modules:
                        del sys.modules[module_name]

        return ManualData.from_module(data_module)


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
