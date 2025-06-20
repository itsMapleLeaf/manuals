from pathlib import Path
import subprocess


root_dir = Path(__file__).parent.parent

# update Archipelago
subprocess.run(
    "git pull --tags --autostash origin main",
    cwd=root_dir / "Archipelago",
)

# update manuals
manual_folders = [
    root_dir / folder
    for folder in [
        "distance",
        "orange-juice",
        "sound-voltex",
        "super-monkey-ball-2",
    ]
]

for folder in manual_folders:
    subprocess.run(f"git subtree pull --prefix {folder} manual main")
