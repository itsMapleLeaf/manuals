from argparse import ArgumentParser
from dataclasses import dataclass
import json
import os
from pathlib import Path
import tempfile
import subprocess
from typing import ClassVar
from zipfile import ZipFile

import git


class AppInfo:
    name: ClassVar = "manspect"
    program_data_path: ClassVar = Path.home() / name


@dataclass(init=False)
class AppArguments:
    world: str
    archipelago_repo: str | None = None
    file: str | None = None


def confirm(message: str):
    answer = input(f"{message} (Y/n) ").strip()
    return answer == "" or answer.lower().startswith("y")


def main():
    arg_parser = ArgumentParser(
        prog=AppInfo.name,
        description="Inspect the data of an Archipelago Manual world.",
    )

    arg_parser.add_argument("world", help="The path to the manual .apworld file")

    arg_parser.add_argument(
        "--archipelago-repo",
        "-a",
        help="The path to the Archipelago repo.\n"
        "This must be provided if the repo is not already downloaded,"
        "and not running in an interactive terminal.",
    )

    arg_parser.add_argument(
        "--file",
        "-f",
        help="Writes the world data to a file. Otherwise, prints it out in the console.",
    )

    args = arg_parser.parse_args(namespace=AppArguments())

    world_path = Path(args.world)

    archipelago_repo_path = (
        Path(args.archipelago_repo)
        if args.archipelago_repo
        else AppInfo.program_data_path / "Archipelago"
    )

    if not archipelago_repo_path.is_dir():
        should_download_repo = confirm(
            f"{AppInfo.name} requires the Archipelago repo. Download the repo and continue?"
        )
        if not should_download_repo:
            print("Aborting.")
            exit()

        print("Cloning Archipelago...")
        git.Repo.clone_from(
            "https://github.com/ArchipelagoMW/Archipelago",
            to_path=archipelago_repo_path,
        )

        # TODO: run setup, ideally with a .venv
        # print("Running setup...")

        print("Done.")

    output_path = Path.cwd() / args.file if args.file else None

    world_path = Path(world_path)
    apworld_zip = ZipFile(world_path, mode="r")

    data_loader_source = """from . import Data
import json
import os

print(json.dumps({
    "game.json": Data.game_table,
    "items.json": Data.item_table,
    "locations.json": Data.location_table,
    "regions.json": Data.region_table,
    "categories.json": Data.category_table,
    "options.json": Data.option_table,
    "meta.json": Data.meta_table,
}))
"""

    with tempfile.TemporaryDirectory() as temp_world_folder:
        apworld_zip.extractall(temp_world_folder)
        apworld_name = os.listdir(temp_world_folder)[0]

        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=Path(temp_world_folder) / apworld_name,
            suffix=".py",
            delete_on_close=False,
        ) as data_loader_file:
            data_loader_file.write(data_loader_source)
            data_loader_file.close()

            (data_loader_module_name, _) = os.path.splitext(
                os.path.basename(data_loader_file.name)
            )

            subprocess_env = {
                **os.environ,
                "PYTHONPATH": str(archipelago_repo_path),
            }

            output_json = subprocess.check_output(
                ["python", "-m", f"{apworld_name}.{data_loader_module_name}"],
                cwd=temp_world_folder,
                env=subprocess_env,
            )

    # to preserve special characters instead of escaped characters,
    # re-stringify the JSON with ensure_ascii set to false
    output_json = json.dumps(
        json.loads(output_json),
        indent="\t",
        ensure_ascii=False,
    )

    if output_path:
        with open(output_path, mode="w", encoding="utf-8") as output_file:
            output_file.write(output_json)

        print(f"Output saved to {output_path.relative_to(Path.cwd())}")
    else:
        print(output_json)


main()
