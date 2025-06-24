import dataclasses
import json
import sys

from ..lib.manuals import MANUALS


manual_arg = sys.argv[1]

manual = MANUALS[manual_arg]
manual_data = manual.load_data()

print(
    json.dumps(
        {
            k: v
            for k, v in dataclasses.asdict(manual_data).items()
            if k in {"item_table", "location_table"}
        },
        indent=2,
    )
)
