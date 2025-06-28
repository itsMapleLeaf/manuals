from . import Data
import json
import sys

json.dump(
    {
        "game": Data.game_table,
        "items": Data.item_table,
        "locations": Data.location_table,
        "regions": Data.region_table,
        "categories": Data.category_table,
        "options": Data.option_table,
        "meta": Data.meta_table,
    },
    sys.stdout,
)
