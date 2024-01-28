import os
import pkgutil
from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification, MultiWorld

from . import jsonc


class OuterWildsItem(Item):
    game = "Outer Wilds"


class OuterWildsItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler


jsonc_data = pkgutil.get_data(__name__, 'shared_static_logic/items.jsonc')
items_data = jsonc.loads(jsonc_data.decode('utf-8'))

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

all_non_event_items_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

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
