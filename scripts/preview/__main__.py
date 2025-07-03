import dataclasses
import json
import sys

from ..lib.manuals import MANUALS


manual_arg = sys.argv[1]

manual = MANUALS[manual_arg]
manual_data = manual.load_data()

json.dump(
    {
        "item_count": sum(item.get("count", 1) for item in manual_data.items),
        "location_count": len(manual_data.locations),
        **dataclasses.asdict(manual_data),
    },
    sys.stdout,
    indent="\t",
)
