from dataclasses import dataclass
import os
from pathlib import Path
import shutil
from dataclasses_json import DataClassJsonMixin
from tap import Tap

from ..lib.constants import MANUALS, PROJECT_ROOT


@dataclass
class GameInfo(DataClassJsonMixin):
    game: str
    creator: str


class ArgumentParser(Tap):
    manual: str

    def configure(self) -> None:
        self.add_argument("manual", choices=MANUALS)


parser = ArgumentParser(prog="mkworld", description="Generates a manual .apworld file")
args = parser.parse_args()

manual_folder = PROJECT_ROOT / args.manual
manual_src_folder = manual_folder / Path("src")
manual_dist_folder = manual_folder / Path("dist")

apworld_output_folder = Path(
    os.getenv("OUTPUT_FOLDER") or "C:/ProgramData/Archipelago/custom_worlds"
)

game_info = GameInfo.from_json(
    (manual_src_folder / "data/game.json").read_text("utf-8")
)
world_name = f"manual_{game_info.game}_{game_info.creator}"

apworld_temp_contents_folder = manual_dist_folder / world_name

if apworld_temp_contents_folder.exists():
    shutil.rmtree(apworld_temp_contents_folder)

shutil.copytree(manual_src_folder, apworld_temp_contents_folder)

output_zip = shutil.make_archive(
    world_name, "zip", root_dir=manual_dist_folder, base_dir="."
)
apworld_final_destination_fox_only_no_items = (
    apworld_output_folder / f"{world_name}.apworld"
)
shutil.move(output_zip, apworld_final_destination_fox_only_no_items)
print(f"saved world to {apworld_final_destination_fox_only_no_items}")
