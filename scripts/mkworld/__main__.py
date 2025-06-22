from dataclasses import dataclass
import os
from pathlib import Path
import shutil
from dataclasses_json import DataClassJsonMixin
from tap import Tap

from ..lib.manuals import MANUALS
from ..lib.paths import MANUAL_LIB_FOLDER, PROJECT_ROOT


@dataclass
class GameInfo(DataClassJsonMixin):
    game: str
    creator: str


class ArgumentParser(Tap):
    manual: str

    def configure(self) -> None:
        self.add_argument("manual", choices=MANUALS.keys())


def copytree_print(source: str | Path, destination: str | Path, *args, **kwargs):
    relative_source = Path(source).relative_to(PROJECT_ROOT)
    relative_destination = Path(destination).relative_to(PROJECT_ROOT)
    print(f"[copytree] {relative_source} -> {relative_destination}")
    shutil.copytree(source, destination, *args, **kwargs)


parser = ArgumentParser(prog="mkworld", description="Generates a manual .apworld file")
args = parser.parse_args()
manual = MANUALS[args.manual]

apworld_output_folder = Path(
    os.getenv("OUTPUT_FOLDER") or "C:/ProgramData/Archipelago/custom_worlds"
)

game_info = GameInfo.from_json((manual.data_folder / "game.json").read_text("utf-8"))
world_name = f"manual_{game_info.game}_{game_info.creator}"

apworld_temp_contents_folder = manual.dist / world_name

if apworld_temp_contents_folder.exists():
    shutil.rmtree(apworld_temp_contents_folder)

copytree_print(manual.src, apworld_temp_contents_folder)

for entry in os.listdir(MANUAL_LIB_FOLDER):
    copytree_print(
        MANUAL_LIB_FOLDER / entry,
        apworld_temp_contents_folder / entry,
        dirs_exist_ok=True,
    )

output_zip = shutil.make_archive(world_name, "zip", root_dir=manual.dist, base_dir=".")
apworld_final_destination_fox_only_no_items = (
    apworld_output_folder / f"{world_name}.apworld"
)
shutil.move(output_zip, apworld_final_destination_fox_only_no_items)
print(f"saved world to {apworld_final_destination_fox_only_no_items}")
