import json
from pathlib import Path
from manual_kit.standalone import Requires, WorldSpec


def create_world_spec() -> WorldSpec:
    spec = WorldSpec(
        game="Distance",
        creator="MapleLeaf",
        filler_item_name="If you see this, there's a bug!",
        starting_items=[{"item_categories": ["Arcade"], "random": 7}],
    )

    arcade_levels = {
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
        # TODO: add challenge levels, probably
    }

    campaign_levels = {
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

    arcade_level_count = sum(len(level_list) for level_list in arcade_levels.values())
    keys_per_campaign: int = arcade_level_count // len(campaign_levels) // 2

    for arcade_set_name, arcade_level_names in arcade_levels.items():
        for arcade_level_name in arcade_level_names:
            arcade_level_item = spec.define_item(
                f"{arcade_set_name} - {arcade_level_name}",
                category="Arcade",
                progression=True,
            )

            for sector_index in range(2):
                spec.define_location(
                    f"{arcade_level_item['name']} - Sector {sector_index}",
                    category=[f"Arcade - {arcade_level_item['name']}"],
                    requires=Requires.item(arcade_level_item),
                )

    campaign_key_category = "Decryption"

    campaign_completion_item = spec.define_item(
        f"Campaign Completion",
        category="Campaign Completion",
        count=len(campaign_levels),
        progression=True,
    )

    for campaign_name, campaign_level_names in campaign_levels.items():
        campaign_key_item = spec.define_item(
            f"Decryption - {campaign_name}",
            category=campaign_key_category,
            count=keys_per_campaign,
            progression=True,
        )

        for level_index, level_name in enumerate(campaign_level_names):
            campaign_level_location = spec.define_location(
                f"{campaign_name} - {level_name}",
                category=f"Campaign - {campaign_name}",
                requires=Requires.item(campaign_key_item, "50%"),
            )

            if level_index == len(campaign_level_names) - 1:
                campaign_level_location["place_item"] = [
                    campaign_completion_item["name"]
                ]
            else:
                campaign_level_location["dont_place_item_category"] = [
                    campaign_key_category
                ]

    spec.define_location(
        "Campaign Completion Goal",
        category="(Victory)",
        requires=Requires.item(campaign_completion_item, "1"),
        victory=True,
    )

    for filler_item_name in filler_item_names:
        spec.define_item(
            filler_item_name,
            category="Filler",
            filler=True,
            trap=True,
        )

    # most cursed shit I've ever seen
    with open(Path(__file__).parent / "src/hooks/World.py.txt") as world_hooks_file:
        spec.files["hooks/World.py"] = world_hooks_file.read().replace(
            "%%filler_item_names%%", json.dumps(filler_item_names)
        )

    return spec
