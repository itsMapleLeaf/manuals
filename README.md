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

✅ Fully refactored

### [100% Orange Juice](./manuals/orange-juice/)

⚠️ Has its own build script which should be used instead of the new one. It should be run as a module, **_without_** uv:

```sh
cd manuals/orange-juice
python -m scripts.build
```

### [Sound Voltex](./manuals/sound-voltex/)

⚠️ Has its own build script, similarly to OJ.

It also has a script `fetch_songs.py` to fetch the full list of songs in the game. You shouldn't have to run this; the song list is committed (see [`data/songs.json`](./manuals/sound-voltex/src/data/songs.json)), and they don't update often.

### Setup

1. Install the following:

   - [Python](https://python.org)
   - [uv](https://docs.astral.sh/uv/#installation)

1. Run `uv sync`

1. Install Archipelago dependencies:

   ```sh
   cd Archipelago
   uv run setup.py
   ```

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
export OUTPUT_FOLDER="$HOME/archipelago/custom_worlds"
uv -m scripts.mkworld distance
```

```ps1
# powershell
$env:OUTPUT_FOLDER="/home/maple/archipelago/custom_worlds"
uv -m scripts.mkworld distance
```

#### `preview`

Prints out the generated data for the given manual.

```sh
# print the data for the distance manual
uv -m scripts.preview distance

# print only the items
uv -m scripts.preview distance items
```

### Manual Kit

The [manual kit](./manual_kit/) contains shared code used by each manual to generate its world data.

Archipelago requires using relative imports within worlds, so any code used by the manual source needs to be moved to the `src` folder; that's what the [`mkworld`](#mkworld) script does before generating an .apworld.

For running the code outside of world generation, a stub file is used, which re-exports from the manual_kit folder:

```py
# manuals/distance/src/manual_kit/__init__.py
from manual_kit import *
```

This stub is replaced with the real code during world generation, and the `PYTHONPATH` is configured such that this is accessible through an absolute import before generation.

> This is slightly gross, but it's the best way I could think of to accomplish code sharing ¯\\\_(ツ)\_/¯

### Testing

¯\\\_(ツ)\_/¯
