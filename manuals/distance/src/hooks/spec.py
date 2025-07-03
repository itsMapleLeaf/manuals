from dataclasses import InitVar, dataclass
from typing import Final


from ..manual_kit import WorldSpec, requires


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
    world_spec: InitVar["DistanceWorldSpec"]
    name: str
    set_name: str

    def __post_init__(self, world_spec: "DistanceWorldSpec") -> None:
        self.item = world_spec.item(
            name=f"{self.name} [{self.set_name}]",
            category="Arcade",
            progression=True,
        )

        self.locations = [
            world_spec.location(
                name=f"{self.item.name} - Sector {sector_index}",
                category=[f"Arcade - {self.name} [{self.set_name}]"],
                requires=requires.item(self.item),
            )
            for sector_index in range(2)
        ]


class DistanceWorldSpec(WorldSpec):
    default_included_level_count: Final = 30
    keys_per_campaign: Final = 10

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

    @staticmethod
    def get_campaign_key_name(campaign_name: str):
        return f"Decryption - {campaign_name}"

    def __init__(self) -> None:
        super().__init__()

        self.arcade_levels = [
            ArcadeLevelSpec(world_spec=self, name=level_name, set_name=set_name)
            for set_name, level_names in GameContent.arcade.items()
            for level_name in level_names
        ]

        campaign_completion_item = self.item(
            name=f"Campaign Completion",
            category="Campaign Completion",
            count=len(GameContent.campaigns),
            progression=True,
        )

        for campaign_name, level_names in GameContent.campaigns.items():
            campaign_key_item = self.item(
                name=f"Decryption - {campaign_name}",
                category="Decryption",
                count=self.keys_per_campaign,
                progression=True,
                local=True,
            )

            for level_index, level_name in enumerate(level_names):
                campaign_level_location = self.location(
                    name=f"{level_name} [{campaign_name}]",
                    category=f"Campaign - {campaign_name}",
                    requires=requires.item(campaign_key_item, "50%"),
                )

                if level_index == len(level_names) - 1:
                    campaign_level_location.data["place_item"] = [
                        campaign_completion_item.data["name"]
                    ]
                else:
                    campaign_level_location.data["dont_place_item"] = [
                        campaign_key_item.data["name"]
                    ]

        self.location(
            name="Campaign Completion Goal",
            category="(Victory)",
            requires=requires.item(campaign_completion_item, "1"),
            victory=True,
        )

        for filler_item_name in self.filler_item_names:
            self.item(
                filler_item_name,
                category="Filler",
                filler=True,
                trap=True,
            )
