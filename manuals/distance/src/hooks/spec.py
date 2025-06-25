from dataclasses import dataclass
import json

from ..manual_kit import WorldSpec, requires


@dataclass
class ArcadeLevel:
    name: str
    set_name: str

    @property
    def item_name(self):
        return f"{self.name} [{self.set_name}]"

    @property
    def location_category_name(self):
        return f"Arcade - {self.name} [{self.set_name}]"

    @property
    def location_names(self):
        # just gives every level multiple checks for fun,
        # and to fit all the items
        return {
            f"{self.item_name} - Sector {sector_index}" for sector_index in range(2)
        }


arcade_item_category_name = "Arcade"
arcade_location_category_name = "Arcade Location"

arcade_levels = [
    ArcadeLevel(name=level_name, set_name=set_name)
    for set_name, levels in {
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
    }.items()
    for level_name in levels
]

campaigns = {
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
    # "Lost to Echoes": [
    #     "Long Ago",
    #     "Forgotten Utopia",
    #     "A Deeper Void",
    #     "Eye of the Storm",
    #     "The Sentinel Still Watches",
    #     "Shadow of the Beast",
    #     "Pulse of a Violent Heart",
    #     "It Was Supposed To Be Perfect",
    #     "Echoes",
    # ],
    # "Nexus": [
    #     "Mobilization",
    #     "Resonance",
    #     "Deterrence",
    #     "Terminus",
    #     "Collapse",
    # ],
    # this is run via Arcade and doesn't actually have a campaign,
    # but I'm treating it as a campaign because it's more fun to run in order
    # "Legacy": [
    #     "Broken Symmetry",
    #     "Lost Society",
    #     "Negative Space",
    #     "Departure",
    #     "Ground Zero",
    #     "The Observer Effect",
    #     "Aftermath",
    #     "Friction",
    #     "The Thing About Machines",
    #     "Corruption",
    #     "Dissolution",
    #     "Falling Through",
    #     "Monolith",
    #     "Destination Unknown",
    #     "Rooftops",
    #     "Factory",
    #     "Stronghold",
    #     "Approach",
    #     "Continuum",
    #     "Escape",
    # ],
}

# keys_per_campaign = sum(
#     arcade_levels
# ) // len(campaigns)
keys_per_campaign = 10

filler_item_names = [
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


def get_campaign_key_name(campaign_name: str):
    return f"Decryption - {campaign_name}"


class DistanceWorldSpec(WorldSpec):
    def __init__(self) -> None:
        for level in arcade_levels:
            level_item = self.item(
                name=level.item_name,
                category=arcade_item_category_name,
                progression=True,
            )

            # just gives every level multiple checks for fun,
            # and to fit all the items
            for location_name in level.location_names:
                self.location(
                    name=location_name,
                    category=[
                        arcade_location_category_name,
                        level.location_category_name,
                    ],
                    requires=requires.item(level_item),
                )

        campaign_completion_item = self.item(
            name=f"Campaign Completion",
            category="Campaign Completion",
            count=len(campaigns),
            progression=True,
        )

        for campaign_name, levels in campaigns.items():
            campaign_key_item = self.item(
                name=get_campaign_key_name(campaign_name),
                category="Decryption",
                count=keys_per_campaign,
                progression=True,
            )

            *progressive_levels, completion_level = levels

            for level_name in progressive_levels:
                self.location(
                    name=f"{level_name} [{campaign_name}]",
                    category=f"Campaign - {campaign_name}",
                    requires=requires.item(campaign_key_item, "50%"),
                    dont_place_item=[campaign_key_item["name"]],
                )

            self.location(
                name=f"{completion_level} [{campaign_name}]",
                category=f"Campaign - {campaign_name}",
                requires=requires.item(campaign_key_item, "50%"),
                place_item=[campaign_completion_item["name"]],
            )

        self.location(
            name="Campaign Completion Goal",
            category="(Victory)",
            requires=requires.item(campaign_completion_item, "1"),
            victory=True,
        )

        for filler_item_name in filler_item_names:
            self.item(
                filler_item_name,
                category="Filler",
                filler=True,
                trap=True,
            )


if __name__ == "__main__":
    spec = DistanceWorldSpec()

    print(json.dumps(spec.items, indent=2))
    print(json.dumps(spec.locations, indent=2))
    print(json.dumps(spec.categories, indent=2))

    print(f"{spec.item_count} items")
    print(f"{len(spec.locations)} locations")
    print(f"{len(spec.categories)} configured categories")
