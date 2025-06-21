from pathlib import Path


def root_path(*segments: str | Path):
    return Path(__file__).parent.parent.parent / Path(*segments)


def manual_data_path(*segments: str | Path):
    return root_path("src", "data", *segments)
