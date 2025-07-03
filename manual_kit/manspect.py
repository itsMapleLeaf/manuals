from argparse import ArgumentParser
from dataclasses import dataclass
import dataclasses
import importlib
import importlib.util
import json
import random
import sys
from typing import Callable, Literal
import os
from pathlib import Path
import tempfile
import subprocess
import venv
from zipfile import ZipFile
import git
import platformdirs

from .manual_data import ManualData


type LogFn = Callable[..., None]

type StrPath = str | Path


class Manspect:

    def __init__(
        self,
        data_dir: StrPath | None = None,
        archipelago: StrPath | None = None,
        log: (
            Literal["stdout"] | Literal["stderr"] | LogFn | None | Literal[False]
        ) = "stderr",
    ) -> None:
        self.data_dir = Path(
            data_dir
            or platformdirs.user_config_dir(
                "manspect", appauthor=False, ensure_exists=True
            )
        )
        self.venv_dir = self.data_dir / ".venv"
        self.python_path = self.venv_dir / "Scripts/python"
        self.archipelago_repo_dir = Path(archipelago or (self.data_dir / "Archipelago"))

        self.__log: LogFn
        if log == "stdout":
            self.__log = self.__log_to_stdout
        elif log == "stderr":
            self.__log = self.__log_to_stderr
        elif isinstance(log, Callable):
            self.__log = log
        else:
            self.__log = lambda: None

    def __log_to_stdout(self, *values: object):
        print(*values)

    def __log_to_stderr(self, *values: object):
        print(*values, file=sys.stderr)

    def ensure_environment(self):
        if not self.venv_dir.is_dir():
            self.__log("Virtual environment not found.")
            self.__log("Setting up virtual environment...")
            venv.create(self.venv_dir, with_pip=True)

        if not self.archipelago_repo_dir.is_dir():
            self.__log("Archipelago repo not found.")
            self.__log("Cloning Archipelago...")
            git.Repo.clone_from(
                "https://github.com/ArchipelagoMW/Archipelago",
                to_path=self.archipelago_repo_dir,
            )

            self.__log("Running setup...")
            subprocess.run(
                [self.python_path, "setup.py"],
                cwd=self.archipelago_repo_dir,
            )

        return self

    def inspect_apworld(self, manual_world_path: StrPath):
        with tempfile.TemporaryDirectory() as temp_world_folder:
            with ZipFile(manual_world_path, mode="r") as world_zip:
                world_zip.extractall(temp_world_folder)

            world_name = os.listdir(temp_world_folder)[0]

            return self.inspect_from_source(
                source_dir=Path(temp_world_folder) / world_name,
            )

    def inspect_from_source(self, source_dir: StrPath) -> ManualData:
        source_dir = Path(source_dir)

        # create a random module name to avoid caching,
        # making sure we're always loading a fresh module
        module_name = f"manual_data_{random.randbytes(16).hex()}"

        spec = importlib.util.spec_from_file_location(
            name=module_name,
            location=source_dir / "Data.py",
            submodule_search_locations=[str(source_dir)],
        )

        if not spec or not spec.loader:
            raise Exception(
                f"Failed to create module spec for {source_dir / "Data.py"}"
            )

        data_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = data_module

        original_sys_path = sys.path.copy()
        try:
            sys.path.append(self.archipelago_repo_dir.as_posix())
            spec.loader.exec_module(data_module)
        finally:
            sys.path = original_sys_path

        manual_data = ManualData(
            game=data_module.game_table,
            items=data_module.item_table,
            locations=data_module.location_table,
            regions=data_module.region_table,
            categories=data_module.category_table,
            options=data_module.option_table,
            meta=data_module.meta_table,
        )

        del sys.modules[module_name]

        return manual_data


def __main():
    @dataclass(init=False)
    class AppArguments:
        world: str
        archipelago_repo: str | None = None
        file: str | None = None

    arg_parser = ArgumentParser(
        prog="manspect",
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

    manspect = Manspect(
        log="stderr", archipelago=args.archipelago_repo
    ).ensure_environment()

    manual_data = manspect.inspect_apworld(
        manual_world_path=args.world,
    )

    manual_data_json = json.dumps(
        dataclasses.asdict(manual_data),
        indent="\t",
        ensure_ascii=False,  # preserve special characters
    )

    if not args.file:
        print(manual_data_json)
        return

    output_path = Path.cwd() / args.file

    with open(output_path, mode="w", encoding="utf-8") as output_file:
        output_file.write(manual_data_json)

    print(f"Output saved to {output_path.relative_to(Path.cwd())}")


if __name__ == "__main__":
    __main()
