from dataclasses import dataclass
import importlib
import sys
from typing import Callable
import os
from pathlib import Path
import tempfile
import subprocess
import venv
from zipfile import ZipFile
import git
import platformdirs

from .. import CategoryData, LocationData, ItemData

type LogFn = Callable[[str], None]


class ManspectEnvironment:

    def __init__(
        self,
        root: str | Path = platformdirs.user_config_dir(
            "manspect", appauthor=False, ensure_exists=True
        ),
        archipelago_repo: str | Path | None = None,
        log: LogFn = lambda x: None,
    ) -> None:
        self.root = Path(root)
        self.virtual_environment_path = self.root / ".venv"
        self.python_bin_path = self.virtual_environment_path / "Scripts/python"
        self.archipelago_repo_path = Path(
            archipelago_repo or (self.root / "Archipelago")
        )
        self.log = log

    def bootstrap(self):
        if not self.virtual_environment_path.is_dir():
            self.log("Virtual environment not found.")
            self.log("Setting up virtual environment...")
            venv.create(self.virtual_environment_path, with_pip=True)

        if not self.archipelago_repo_path.is_dir():
            self.log("Archipelago repo not found.")
            self.log("Cloning Archipelago...")
            git.Repo.clone_from(
                "https://github.com/ArchipelagoMW/Archipelago",
                to_path=self.archipelago_repo_path,
            )

            self.log("Running setup...")
            subprocess.run(
                [self.python_bin_path, "setup.py"],
                cwd=self.archipelago_repo_path,
            )


def inspect_manual(
    manual_world_path: str | Path,
    archipelago_repo_path: str | Path,
):
    world_zip = ZipFile(manual_world_path, mode="r")

    with tempfile.TemporaryDirectory() as temp_world_folder:
        world_zip.extractall(temp_world_folder)
        world_name = os.listdir(temp_world_folder)[0]

        original_path = sys.path.copy()
        try:
            sys.path += [temp_world_folder, str(archipelago_repo_path)]
            data_module = importlib.import_module(".Data", world_name)
        finally:
            sys.path = original_path

        return ManualData(
            game=data_module.game_table,
            items=data_module.item_table,
            locations=data_module.location_table,
            regions=data_module.region_table,
            categories=data_module.category_table,
            options=data_module.option_table,
            meta=data_module.meta_table,
        )


@dataclass
class ManualData:
    game: dict[str, object]
    items: list[ItemData]
    locations: list[LocationData]
    regions: dict[str, object]
    categories: dict[str, CategoryData]
    options: dict[str, object]
    meta: dict[str, object]
