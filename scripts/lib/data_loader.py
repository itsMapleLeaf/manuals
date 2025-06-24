from . import Data  # type: ignore
import json

print(
    json.dumps(
        {
            "game_table": Data.game_table,
            "item_table": Data.item_table,
            "location_table": Data.location_table,
            "region_table": Data.region_table,
            "category_table": Data.category_table,
            "option_table": Data.option_table,
            "meta_table": Data.meta_table,
        }
    )
)
