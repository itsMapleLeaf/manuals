import subprocess
from git import Repo

from ..lib.manuals import MANUALS
from ..lib.paths import PROJECT_ROOT


print("\n🏝️  Updating Archipelago...")
subprocess.run(
    "git pull --tags --autostash origin main",
    cwd=PROJECT_ROOT / "Archipelago",
)

repo = Repo(PROJECT_ROOT)
has_changes = repo.index.diff(None) != []

# subtree calls fail if there are uncommitted changes, so ghetto auto-stash
if has_changes:
    print("\n⚠️  Found unsaved changes; stashing.")
    print(
        "⚠️  If you cancel the script before unstashing, run `git stash pop` yourself."
    )
    repo.git.stash("save")

# update manuals
for manual in MANUALS.values():
    print(f"\n⚙️  Updating {manual.name}...")
    subprocess.run(f"git subtree pull --prefix {manual.root} manual main")

if has_changes:
    print("\n🗄️  Restoring changes...")
    repo.git.stash("pop")

print("\n✅  Done")
