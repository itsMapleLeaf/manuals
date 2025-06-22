import json
from dataclasses import dataclass

from .manual_kit import WorldSpec, requires

@dataclass
class LevelWorld:
    name: str
    levels: list[str]

class SuperMonkeyBall2WorldSpec(WorldSpec):
    worlds = [
        LevelWorld(
            name="Jungle Island",
            levels=[
                "Simple", "Hollow", "Bumpy", "Switches", "Conveyers",
                "Floaters", "Slopes", "Sliders", "Spinning Top", "Curve Bridge",
            ],
        ),
        LevelWorld(
            name="Volcanic Magma",
            levels=[
                "Banks", "Eaten Floor", "Hoppers", "Coaster", "Bumpy Check",
                "Swell", "Gravity Slider", "Inchworms", "Totalitarianism", "Alternative",
            ],
        ),
        LevelWorld(
            name="Under the Ocean",
            levels=[
                "Organic Form", "Reversible Gear", "Stepping Stones", "Dribbles", "U.R.L.",
                "Mad Rings", "Curvy Options", "Twister", "Downhill", "Junction",
            ],
        ),
        LevelWorld(
            name="Inside a Whale",
            levels=[
                "Pro Skaters", "Giant Comb", "Beehive", "Dynamic Maze", "Triangle Holes",
                "Launchers", "Randomizer", "Coin Slots", "Seesaw Bridges", "Arthropod",
            ],
        ),
        LevelWorld(
            name="Amusement Park",
            levels=[
                "Wormhole", "Free Fall", "Melting Pot", "Mad Shuffle", "Bead Screen",
                "Jump Machine", "Zigzag Slope", "Tower", "Toggle", "Fluctuation",
            ],
        ),
        LevelWorld(
            name="Boiling Pot",
            levels=[
                "Combination", "Punched Seesaws", "Opera", "Brandished", "Tiers",
                "Cliffs", "Narrow Peaks", "Detour", "Switch Inferno", "Folders",
            ],
        ),
        LevelWorld(
            name="Bubbly Washing Machine",
            levels=[
                "Spiral Bridge", "Wavy Option", "Obstacle", "Domino", "Sieve",
                "Flock", "Double Spiral", "Hierarchy", "8 Bracelets", "Quick Turn",
            ],
        ),
        LevelWorld(
            name="Clock Tower Factory",
            levels=[
                "Pistons", "Soft Cream", "Momentum", "Entangled Path", "Totters",
                "Vortex", "Warp", "Trampolines", "Swing Shaft", "Linear Seesaws",
            ],
        ),
        LevelWorld(
            name="Space Colony",
            levels=[
                "Serial Jump", "Cross Floors", "Spinning Saw", "Chipped Pipes", "Flat Maze",
                "Guillotine", "Cork Screw", "Orbiters", "Twin Basin", "Air Hockey",
            ],
        ),
    ]

    victory_world = LevelWorld(
        name="Dr. Bad-Boon's Base",
        levels=[
            "Training", "Gimmick", "Mountain", "Disorder", "3D Maze",
            "Labyrinth", "Postmodern", "Revolution", "Invisible", "Created By",
        ],
    )

    victory_level_required_banana_count = 5

    def __init__(self) -> None:
        for world_index, world in enumerate(self.worlds):
            world_item = self.item(
                name=f"{world.name} (World {world_index + 1})",
                category="Worlds",
                progression=True,
            )

            for level_index, level in enumerate(world.levels):
                self.location(
                    name=f"{level_index + 1}. {level} (World {world_index + 1})",
                    category=f"World {world_index + 1}",
                    requires=requires.item(world_item),
                )

        banana_item = self.item(
            name="Banana",
            category="Bananas",
            count=int(
                self.victory_level_required_banana_count
                * len(self.victory_world.levels)
                * 1.5
            ),
            progression=True,
        )

        for level_index, level in enumerate(self.victory_world.levels):
            self.location(
                name=f"{level_index + 1}. {level} ({self.victory_world.name})",
                category=self.victory_world.name,
                requires=requires.item(
                    banana_item,
                    self.victory_level_required_banana_count * (level_index + 1),
                ),
                victory=level_index == len(self.victory_world.levels) - 1,
            )


if __name__ == "__main__":
    spec = SuperMonkeyBall2WorldSpec()

    print(json.dumps(spec.items, indent=2))
    print(json.dumps(spec.locations, indent=2))
    print(json.dumps(spec.categories, indent=2))

    print(f"{spec.item_count} items")
    print(f"{len(spec.locations)} locations")
    print(f"{len(spec.categories)} configured categories")
