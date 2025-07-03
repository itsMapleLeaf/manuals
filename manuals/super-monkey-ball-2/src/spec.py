from dataclasses import dataclass
from typing import ClassVar

from .manual_kit import WorldSpec, requires


@dataclass
class LevelWorld:
    name: str
    levels: list[str]


class SuperMonkeyBall2WorldSpec(WorldSpec):
    worlds: ClassVar = [
        LevelWorld(
            name="Jungle Island",
            levels=[
                "Simple",
                "Hollow",
                "Bumpy",
                "Switches",
                "Conveyers",
                "Floaters",
                "Slopes",
                "Sliders",
                "Spinning Top",
                "Curve Bridge",
            ],
        ),
        LevelWorld(
            name="Volcanic Magma",
            levels=[
                "Banks",
                "Eaten Floor",
                "Hoppers",
                "Coaster",
                "Bumpy Check",
                "Swell",
                "Gravity Slider",
                "Inchworms",
                "Totalitarianism",
                "Alternative",
            ],
        ),
        LevelWorld(
            name="Under the Ocean",
            levels=[
                "Organic Form",
                "Reversible Gear",
                "Stepping Stones",
                "Dribbles",
                "U.R.L.",
                "Mad Rings",
                "Curvy Options",
                "Twister",
                "Downhill",
                "Junction",
            ],
        ),
        LevelWorld(
            name="Inside a Whale",
            levels=[
                "Pro Skaters",
                "Giant Comb",
                "Beehive",
                "Dynamic Maze",
                "Triangle Holes",
                "Launchers",
                "Randomizer",
                "Coin Slots",
                "Seesaw Bridges",
                "Arthropod",
            ],
        ),
        LevelWorld(
            name="Amusement Park",
            levels=[
                "Wormhole",
                "Free Fall",
                "Melting Pot",
                "Mad Shuffle",
                "Bead Screen",
                "Jump Machine",
                "Zigzag Slope",
                "Tower",
                "Toggle",
                "Fluctuation",
            ],
        ),
        LevelWorld(
            name="Boiling Pot",
            levels=[
                "Combination",
                "Punched Seesaws",
                "Opera",
                "Brandished",
                "Tiers",
                "Cliffs",
                "Narrow Peaks",
                "Detour",
                "Switch Inferno",
                "Folders",
            ],
        ),
        LevelWorld(
            name="Bubbly Washing Machine",
            levels=[
                "Spiral Bridge",
                "Wavy Option",
                "Obstacle",
                "Domino",
                "Sieve",
                "Flock",
                "Double Spiral",
                "Hierarchy",
                "8 Bracelets",
                "Quick Turn",
            ],
        ),
        LevelWorld(
            name="Clock Tower Factory",
            levels=[
                "Pistons",
                "Soft Cream",
                "Momentum",
                "Entangled Path",
                "Totters",
                "Vortex",
                "Warp",
                "Trampolines",
                "Swing Shaft",
                "Linear Seesaws",
            ],
        ),
        LevelWorld(
            name="Space Colony",
            levels=[
                "Serial Jump",
                "Cross Floors",
                "Spinning Saw",
                "Chipped Pipes",
                "Flat Maze",
                "Guillotine",
                "Cork Screw",
                "Orbiters",
                "Twin Basin",
                "Air Hockey",
            ],
        ),
        LevelWorld(
            name="Dr. Bad-Boon's Base",
            levels=[
                "Training",
                "Gimmick",
                "Mountain",
                "Disorder",
                "3D Maze",
                "Labyrinth",
                "Postmodern",
                "Revolution",
                "Invisible",
                "Created By",
            ],
        ),
    ]

    def __init__(self) -> None:
        super().__init__()

        banana_item = self.item(
            name="Banana",
            category="Bananas",
            count=20,
            progression=True,
            local=True,
        )

        self.location(
            name="Find all bananas!",
            category="(Victory)",
            requires=requires.item(banana_item, "all"),
            victory=True,
        )

        for world_number, world in enumerate(self.worlds):
            world_number += 1

            for level_number, level_name in enumerate(world.levels):
                level_number += 1

                level_item = self.item(
                    name=f"{world_number}-{level_number} {level_name}",
                    category=["Levels", f"World {world_number}"],
                    progression=True,
                )

                # add an extra location to fit all the items, plus extra checks are fun
                for i in range(2):
                    self.location(
                        name=f"{level_item["name"]} - {i + 1}",
                        category=f"World {world_number}",
                        requires=requires.item(level_item),
                    )
