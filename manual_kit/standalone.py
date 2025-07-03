import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from dataclasses_json import DataClassJsonMixin

from .game import GameData


class GameDataJson(GameData, DataClassJsonMixin):
    pass


def create_apworld_file(files: dict[str, str]) -> Path:
    manual_src_dir = Path(__file__).parent / "Manual/src"
    output_dir = Path.cwd()

    with TemporaryDirectory(prefix="manual_kit_standalone") as temp_root_dir:
        temp_root_dir = Path(temp_root_dir)
        temp_src_dir = temp_root_dir / "src"

        shutil.copytree(manual_src_dir, temp_src_dir)

        for local_file_path, file_content in files.items():
            file_path = Path(temp_src_dir / local_file_path)
            os.makedirs(file_path.parent, exist_ok=True)
            file_path.write_text(file_content)

        game_data = GameDataJson.from_json(
            Path(temp_src_dir / "data/game.json").read_bytes(),
        )

        world_identifier = f"manual_{game_data.game}_{game_data.creator}"
        world_zip_base = output_dir / world_identifier
        apworld_file = output_dir / f"{world_identifier}.apworld"

        shutil.move(temp_src_dir, temp_root_dir / world_identifier)

        world_zip = shutil.make_archive(
            str(world_zip_base),
            format="zip",
            root_dir=temp_root_dir,
            base_dir=".",
        )

        shutil.move(world_zip, apworld_file)

    return apworld_file
