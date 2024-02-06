import os
import pkgutil
from typing import Dict, List, NamedTuple, Optional

from BaseClasses import Item, ItemClassification, MultiWorld

from . import jsonc
from .Options import OuterWildsGameOptions


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
for items_data_entry in items_data:
    item_data_table[items_data_entry["name"]] = OuterWildsItemData(
        code=(items_data_entry["code"] if "code" in items_data_entry else None),
        type=item_types_map[items_data_entry["type"]]
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


def create_item(player: int, name: str) -> OuterWildsItem:
    return OuterWildsItem(name, item_data_table[name].type, item_data_table[name].code, player)


def create_items(multiworld: MultiWorld, options: OuterWildsGameOptions, player: int) -> None:
    item_pool: List[OuterWildsItem] = []
    for name, item in item_data_table.items():
        # todo: come up with a better way to exclude locked / pre-placed items from the itempool
        if item.code and name != "Launch Codes":
            item_pool.append(create_item(player, name))

    multiworld.itempool += item_pool

    # add enough "Nothing"s to make item count equal location count
    filler_needed = len(multiworld.get_unfilled_locations(player)) - len(item_pool)
    multiworld.itempool += [create_item(player, "Nothing") for _ in range(filler_needed)]
