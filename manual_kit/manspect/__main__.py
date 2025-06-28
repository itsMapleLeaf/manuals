from argparse import ArgumentParser
from dataclasses import dataclass
import json
from pathlib import Path
import sys


from . import ManspectEnvironment, inspect_manual


@dataclass(init=False)
class AppArguments:
    world: str
    archipelago_repo: str | None = None
    file: str | None = None


def log(*msg: str):
    print(*msg, file=sys.stderr)


def main():
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

    environment = ManspectEnvironment(log=log)
    environment.bootstrap()

    output_json = inspect_manual(
        manual_world_path=args.world,
        python_bin_path=environment.python_bin_path,
        archipelago_repo_path=environment.archipelago_repo_path,
        log=log,
    )

    output_json = json.dumps(
        output_json,
        indent="\t",
        ensure_ascii=False,  # preserve special characters
    )

    if not args.file:
        print(output_json)
        return

    output_path = Path.cwd() / args.file

    with open(output_path, mode="w", encoding="utf-8") as output_file:
        output_file.write(output_json)

    print(f"Output saved to {output_path.relative_to(Path.cwd())}")


main()
