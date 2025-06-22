import sys
from typing import Callable
from tabulate import tabulate

from ..lib.manuals import MANUALS, ManualData

collections: dict[str, Callable[[ManualData], dict | list]] = {
    "items": lambda manual_data: manual_data.item_table,
    "locations": lambda manual_data: manual_data.location_table,
}

manual_arg = sys.argv[1]
collection_arg = [sys.argv[2]] if len(sys.argv) >= 3 else [*collections.keys()]

manual = MANUALS[manual_arg]
manual_data = manual.load_data()

for collection_name in collection_arg:
    print(collection_name.capitalize())
    print(
        tabulate(
            collections[collection_name](manual_data),
            headers="keys",
            tablefmt="rounded_grid",
        )
    )
