import subprocess

from ..lib.manuals import MANUALS
from ..lib.paths import PROJECT_ROOT


print("Updating Archipelago...")
subprocess.run(
    "git pull --tags --autostash origin main",
    cwd=PROJECT_ROOT / "Archipelago",
)

# update manuals
for manual in MANUALS.values():
    print(f"Updating {manual.name}...")
    subprocess.run(f"git subtree pull --prefix {manual.root} manual main")

print("Done")
