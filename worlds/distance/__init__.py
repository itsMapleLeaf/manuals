from dataclasses import dataclass
from typing import Final


from manual_kit.standalone import ItemSpec, LocationSpec, WorldSpec


class GameContent:
    arcade: Final = {
        "Ignition": [
            "Chroma",
            "Vector Valley",
            "Static Fire Signal",
            "Shallow",
            "Incline",
            "Station",
            "Whisper",
            "Particular Journey",
            "Turbines",
            "COAT Speedway",
            "Tharsis Tholus",
        ],
        "High Impact": [
            "Virtual Rift",
            "Sea",
            "Beta Echoes",
            "Sender",
            "Absorption",
            "Fiber",
            "Homestead",
            "Salmon",
            "The Manor",
            "Uncanny Valley",
            "Sakura Skyway",
            "Le Teleputo",
            "Method",
            "Binary Construct",
            "Storm 2 - Neon Thunder",
            "Amusement",
            "Outrun",
            "Iris",
        ],
        "Brute Force": [
            "Volcanic Rush",
            "Ruin",
            "Moonlight",
            "Instability",
            "Shafty",
            "Precept",
            "Aeris",
            "Overdrive",
            "Floral",
            "Past",
            "Neo Seoul",
            "Event Horizon",
            "Yellow",
            "Sugar Rush",
            "Sword",
            "Forsaken Shrine",
            "Toy Time",
            "Noir",
            "Brink",
            "Projection",
            "Vibe",
            "Luminescence",
        ],
        "Overdrive": [
            "Paradise Lost",
            "Epicentre",
            "Neo Seoul II",
            "Serenity",
            "Red",
            "Table",
            "Knowledge",
            "Pacebreaker",
            "White",
            "Tetreal",
            "Mentality",
            "Wired",
            "Hardline",
            "Gravity",
            "Digital",
            "Monument",
            "Fulcrum",
            "SR Motorplex",
            "Hard Light Transfer",
            "Impulse",
            "Observatory",
            "Earth",
            "Eclipse",
            "Shrine",
            "Liminal",
            "White Lightning Returns",
        ],
        "Nightmare Fuel": [
            "Affect",
            "The Night Before",
            "Industrial Fury",
            "Fallback Protocol",
            "Cosmic Glitch",
            "Orthodox",
            "Zenith",
            "Micro",
            "Candles of Hekate",
            "Sector 0",
            "Macro",
            "Glide in the Hole",
            "Inferno",
        ],
        "Legacy": [
            "Broken Symmetry",
            "Lost Society",
            "Negative Space",
            "Departure",
            "Ground Zero",
            "The Observer Effect",
            "Aftermath",
            "Friction",
            "The Thing About Machines",
            "Corruption",
            "Dissolution",
            "Falling Through",
            "Monolith",
            "Destination Unknown",
            "Rooftops",
            "Factory",
            "Stronghold",
            "Approach",
            "Continuum",
            "Escape",
        ],
    }

    campaigns: Final = {
        "Adventure": [
            "Instantiation",
            "Cataclysm",
            "Diversion",
            "Euphoria",
            "Entanglement",
            "Automation",
            "Abyss",
            "Embers",
            "Isolation",
            "Repulsion",
            "Compression",
            "Research",
            "Contagion",
            "Overload",
            "Ascension",
            "Enemy",
        ],
        "Lost to Echoes": [
            "Long Ago",
            "Forgotten Utopia",
            "A Deeper Void",
            "Eye of the Storm",
            "The Sentinel Still Watches",
            "Shadow of the Beast",
            "Pulse of a Violent Heart",
            "It Was Supposed To Be Perfect",
            "Echoes",
        ],
        "Nexus": [
            "Mobilization",
            "Resonance",
            "Deterrence",
            "Terminus",
            "Collapse",
        ],
    }


@dataclass
class ArcadeLevelSpec:
    name: str
    set_name: str

    def __post_init__(self) -> None:
        self.item = ItemSpec(
            name=f"{self.set_name} - {self.name}",
            category="Arcade",
            progression=True,
        )

        self.locations = [
            LocationSpec(
                name=f"{self.item.name} - Sector {sector_index}",
                category=["Arcade"],
                requires=self.item,
            )
            for sector_index in range(2)
        ]


class DistanceWorldSpec(WorldSpec):
    arcade_level_count: Final = sum(
        len(level_list) for level_list in GameContent.arcade.values()
    )

    keys_per_campaign: Final[int] = (
        arcade_level_count // len(GameContent.campaigns) // 2
    )

    filler_item_names: Final = [
        "corruption error",
        "out of memory",
        "access violation",
        "invalid sequence termination",
        "segmentation fault",
        "kernel failure",
        "version mismatch",
        "unknown protocol",
        "syntax error",
        "calibration failure",
        "permission denied",
        "resource limit exceeded",
        "fatal exception",
    ]

    arcade_levels: Final = [
        ArcadeLevelSpec(name=level_name, set_name=set_name)
        for set_name, level_names in GameContent.arcade.items()
        for level_name in level_names
    ]

    @staticmethod
    def get_campaign_key_name(campaign_name: str):
        return f"Decryption - {campaign_name}"

    def __init__(self) -> None:
        super().__init__(
            game="Distance",
            creator="MapleLeaf",
            filler_item_name="If you see this, there's a bug!",
        )

        for arcade_level in self.arcade_levels:
            self.items[arcade_level.item.name] = arcade_level.item
            self.locations.update(
                {location.name: location for location in arcade_level.locations}
            )

        campaign_completion_item = self.item(
            name=f"Campaign Completion",
            category="Campaign Completion",
            count=len(GameContent.campaigns),
            progression=True,
        )

        campaign_key_category = "Decryption"

        for campaign_name, level_names in GameContent.campaigns.items():
            campaign_key_item = self.item(
                name=f"Decryption - {campaign_name}",
                category=campaign_key_category,
                count=self.keys_per_campaign,
                progression=True,
                local=True,
            )

            for level_index, level_name in enumerate(level_names):
                campaign_level_location = self.location(
                    name=f"{campaign_name} - {level_name}",
                    category=f"Campaign - {campaign_name}",
                    requires=(campaign_key_item, "50%"),
                )

                if level_index == len(level_names) - 1:
                    campaign_level_location.place_item = [campaign_completion_item.name]
                else:
                    campaign_level_location.dont_place_item_category = [
                        campaign_key_category
                    ]

        self.location(
            name="Campaign Completion Goal",
            category="(Victory)",
            requires=(campaign_completion_item, "1"),
            victory=True,
        )

        for filler_item_name in self.filler_item_names:
            self.item(
                filler_item_name,
                category="Filler",
                filler=True,
                trap=True,
            )


world_spec = DistanceWorldSpec()
