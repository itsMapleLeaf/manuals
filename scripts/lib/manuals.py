from dataclasses import dataclass
import os
from pathlib import Path
from ...manual_kit.manspect import Manspect

from .paths import ARCHIPELAGO_FOLDER, PROJECT_ROOT


@dataclass
class ProjectManual:
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
        return (
            Manspect(archipelago=ARCHIPELAGO_FOLDER)
            .ensure_environment()
            .inspect_from_source(self.src)
        )


MANUALS_FOLDER = PROJECT_ROOT / "manuals"
MANUALS = {name: ProjectManual(name) for name in os.listdir(MANUALS_FOLDER)}
