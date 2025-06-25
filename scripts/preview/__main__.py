import json
import sys

from ..lib.manuals import MANUALS


manual_arg = sys.argv[1]

manual = MANUALS[manual_arg]
manual_data = manual.load_data()

displayed_keys = {"item_table", "location_table", "option_table", "category_table"}
filtered_data = {k: manual_data[k] for k in displayed_keys}
print(json.dumps(filtered_data, indent="\t"))
