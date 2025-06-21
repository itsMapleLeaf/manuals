i made a monorepo for all my AP manuals because i make too many, they all require scripting[^scripting-required], and i'm tired of rewriting basic shit

[^scripting-required]: I _could_ use the online manual builder or write the JSON files myself, but all of these are complicated enough that that would be torture! 😃

> [!important]
>
> **This module uses submodules; clone with `git clone --recursive`!**

## Development (⚠️ Here Be Demons ⚠️)

Some of the manuals use their own old ad-hoc generation code written before I pulled them together into this repo, and still need to be updated to use the same consistent approach for world generation. You can see the refactoring status of each manual below.

### [Distance](./manuals/distance/)

✅ Fully refactored

### [Super Monkey Ball 2](./manuals/super-monkey-ball-2/)

⚙️ Can be built with [`mkworld`](#mkworld), but the source does not use the new APIs

### [100% Orange Juice](./manuals/orange-juice/)

⚠️ Has its own build script which should be used instead of the new one. It should be run as a module, **_without_** uv:

```sh
cd manuals/orange-juice
python -m scripts.build
```

### [Sound Voltex](./manuals/sound-voltex/)

⚠️ Has its own build script, similarly to OJ.

It also has a script `fetch_songs.py` to fetch the full list of songs in the game. You shouldn't have to run this; the song list is committed (see [`data/songs.json`](./manuals/sound-voltex/src/data/songs.json)), and they don't update often.

### Requirements

- [Python](https://python.org)
- [uv](https://docs.astral.sh/uv/#installation)

You may need to install additional dependencies through uv or pip to run the legacy manual-specific scripts.

### Scripts

Scripts reside in the `scripts` folder as `__main__.py` files in their own folder. `scripts/lib` is shared script-specific code.

**Each script should be run through uv as a module**, e.g. `uv -m scripts.pull` to run the `pull` script.

#### `pull`

Pulls changes from upstream repos. Specifically:

1. Updates the [Archipelago](https://github.com/ArchipelagoMW/Archipelago) submodule
1. Patches updates from the [Manual](https://github.com/ManualForArchipelago/Manual) main branch into each manual via `git subtree pull [...]`

#### `mkworld`

Creates an .apworld file from a given manual. Running `uv -m scripts.mkworld distance` will generate an .apworld file for [the Distance manual](./manuals/distance/).

By default, this saves the world file to the worlds folder in the default Archipelago install path for Windows (`C:\ProgramData\Archipelago\custom_worlds`). You can change this by setting the `OUTPUT_FOLDER` environment variable:

```sh
# bash
export OUTPUT_FOLDER=/home/maple/archipelago/custom_worlds
uv -m scripts.mkworld distance
```

```powershell
# powershell
$env:OUTPUT_FOLDER="/home/maple/archipelago/custom_worlds"
uv -m scripts.mkworld distance
```

### Manual Structure

> TODO

### Sharing Code

The [`mkworld`](#mkworld) script copies files inside the `lib` folder into the world's source folder before generating its .apworld. If you have a file at `lib/util.py`, that will get copied to the root folder in the .apworld, e.g. at `manual_Distance_MapleLeaf/util.py`.

Archipelago requires using relative imports within worlds. For type checking, you can add a `.pyi` file that re-exports from the lib folder, which will get overwritten on build:

```py
# manuals/distance/src/world_spec/__init__.pyi
from .....lib.world_spec import *
```

```py
# alternatively, if you have the top-level lib folder configured in python paths
# (ℹ️ this repo configures this in .vscode/settings.json)
from lib.world_spec import *
```

### Testing

¯\\\_(ツ)\_/¯
