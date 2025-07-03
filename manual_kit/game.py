from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class GameData(DataClassJsonMixin):
    game: str
    creator: str
