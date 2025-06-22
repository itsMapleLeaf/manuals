import json

from .manual_kit import WorldSpec, requires


class DistanceWorldSpec(WorldSpec):
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
    }

    arcade_level_sets = {
        "Adventure": [
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
        ],
        "Lost to Echoes": [
            "Forgotten Utopia",
            "A Deeper Void",
            "Eye of the Storm",
            "The Sentinel Still Watches",
            "Shadow of the Beast",
            "Pulse of a Violent Heart",
            "It Was Supposed To Be Perfect",
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

    @staticmethod
    def get_campaign_item_name(campaign_name: str):
        return f"{campaign_name} [Progressive Campaign]"

    def __init__(self) -> None:
        for set_name, levels in self.arcade_level_sets.items():
            for level_name in levels:
                level_item = self.item(
                    name=f"{level_name} [{set_name}]",
                    category="Arcade",
                    progression=True,
                )

                for medal in ["Gold", "Diamond"]:
                    self.location(
                        name=f"{level_name} - {medal} Medal [{set_name}]",
                        category=f"Arcade: {set_name}",
                        requires=requires.item(level_item),
                    )

        campaign_completion_item = self.item(
            name=f"Campaign Completion",
            category="Campaign Completion",
            count=len(self.campaigns),
            progression=True,
        )

        for campaign_name, levels in self.campaigns.items():
            campaign_item = self.item(
                name=self.get_campaign_item_name(campaign_name),
                category="Campaign",
                count=len(levels),
                progression=True,
            )

            for level_index, level_name in enumerate(levels):
                campaign_level_location = self.location(
                    name=f"{level_name} [{campaign_name}]",
                    category=f"Campaign: {campaign_name}",
                    requires=requires.item(campaign_item, level_index + 1),
                )

                if level_index == len(levels) - 1:
                    campaign_level_location["place_item"] = [
                        campaign_completion_item["name"]
                    ]

        self.location(
            name="All Campaigns Completed",
            requires=requires.item(campaign_completion_item, "all"),
            victory=True,
        )

        for filler_item_name in self.filler_item_names:
            self.item(
                filler_item_name,
                category="fatal exception (Filler)",
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
