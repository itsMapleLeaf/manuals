from dataclasses import dataclass
import os
from pathlib import Path
import shutil
from dataclasses_json import DataClassJsonMixin


@dataclass
class GameInfo(DataClassJsonMixin):
    game: str
    creator: str


if __name__ == "__main__":
    game_info = GameInfo.from_json(Path("src/data/game.json").read_text("utf-8"))
    world_name = f"manual_{game_info.game}_{game_info.creator}"

    source_dir = Path("src")
    dist_dir = Path("dist")
    temp_dir = dist_dir / world_name

    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    shutil.copytree(source_dir, temp_dir)

    output_zip = shutil.make_archive(world_name, "zip", root_dir=dist_dir, base_dir=".")
    output_folder = (
        os.getenv("OUTPUT_FOLDER") or "C:/ProgramData/Archipelago/custom_worlds"
    )
    output_path = Path(output_folder) / f"{world_name}.apworld"
    shutil.move(output_zip, output_path)
    print(f"saved world to {output_path}")
