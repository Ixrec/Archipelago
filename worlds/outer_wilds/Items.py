import os
from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification, MultiWorld

from . import jsonc


class OuterWildsItem(Item):
    game = "Outer Wilds"


class OuterWildsItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


filename = os.path.join(os.path.dirname(__file__), 'shared_static_logic/items.jsonc')
with open(filename) as jsonc_data:
    items_data = jsonc.load(jsonc_data)

item_types_map = {
    "progression": ItemClassification.progression,
    "useful": ItemClassification.useful,
    "filler": ItemClassification.filler
}

item_data_table: Dict[str, OuterWildsItemData] = {}
for item in items_data:
    item_data_table[item["name"]] = OuterWildsItemData(
        code=(item["code"] if "code" in item else None),
        type=item_types_map[item["type"]]
    )

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

item_name_groups = {
    "Frequencies": {
        "Distress Beacon Frequency",
        "Quantum Fluctuations Frequency",
        "Hide & Seek Frequency"
    },
    "Signals": {
        "Chert's Signal",
        "Esker's Signal",
        "Riebeck's Signal",
        "Gabbro's Signal",
        "Feldspar's Signal",
        "Museum Shard Signal",
        "Grove Shard Signal",
        "Cave Shard Signal",
        "Tower Shard Signal",
        "Island Shard Signal",
        "Quantum Moon Signal",
        "Escape Pod 1 Signal",
        "Escape Pod 2 Signal",
        "Escape Pod 3 Signal",
        "Galena's Radio Signal",
        "Tephra's Radio Signal"
    }
}
