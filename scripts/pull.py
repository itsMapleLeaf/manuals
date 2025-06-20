import subprocess

from .lib.constants import MANUALS, PROJECT_ROOT


# update Archipelago
subprocess.run(
    "git pull --tags --autostash origin main",
    cwd=PROJECT_ROOT / "Archipelago",
)

# update manuals
for folder in MANUALS:
    subprocess.run(
        f"git subtree pull --prefix {folder} manual main",
        cwd=PROJECT_ROOT,
    )
