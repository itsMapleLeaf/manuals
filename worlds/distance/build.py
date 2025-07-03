import os
from pathlib import Path

from manual_kit.standalone import create_apworld_file
from scripts.lib.paths import PROJECT_ROOT


def __main():
    files: dict[str, str] = {}
    manual_src_dir = PROJECT_ROOT / "manuals/distance/src"

    for dir_path, dir_names, file_names in os.walk(manual_src_dir):
        if "__pycache__" in dir_path:
            continue

        for file_name in file_names:
            file_path = Path(dir_path) / file_name
            files[file_path.relative_to(manual_src_dir).as_posix()] = (
                file_path.read_text()
            )

    create_apworld_file(files)


if __name__ != "__main__":
    raise Exception("This file can only be run as a script.")

__main()
