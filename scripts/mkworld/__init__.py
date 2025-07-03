import os
from pathlib import Path
import shutil
from manual_kit import GameData

from ..lib.manuals import ProjectManual
from ..lib.paths import MANUAL_KIT_FOLDER, MANUAL_KIT_NAME, PROJECT_ROOT


def generate_world(manual: ProjectManual):
    def copytree_print(source: str | Path, destination: str | Path, *args, **kwargs):
        relative_source = Path(source).relative_to(PROJECT_ROOT)
        relative_destination = Path(destination).relative_to(PROJECT_ROOT)
        print(f"[copytree] {relative_source} -> {relative_destination}")
        shutil.copytree(source, destination, *args, **kwargs)

    apworld_output_folder = Path(
        os.getenv("OUTPUT_FOLDER") or "C:/ProgramData/Archipelago/custom_worlds"
    )

    game_info = GameData.from_json(
        (manual.data_folder / "game.json").read_text("utf-8")
    )
    world_name = f"manual_{game_info.game}_{game_info.creator}"

    apworld_temp_contents_folder = manual.dist / world_name

    if manual.dist.exists():
        shutil.rmtree(manual.dist)

    copytree_print(manual.src, apworld_temp_contents_folder)

    copytree_print(
        MANUAL_KIT_FOLDER,
        apworld_temp_contents_folder / MANUAL_KIT_NAME,
        dirs_exist_ok=True,
    )

    output_zip = shutil.make_archive(
        world_name, "zip", root_dir=manual.dist, base_dir="."
    )
    apworld_final_destination_fox_only_no_items = (
        apworld_output_folder / f"{world_name}.apworld"
    )
    shutil.move(output_zip, apworld_final_destination_fox_only_no_items)
    print(f"saved world to {apworld_final_destination_fox_only_no_items}")
