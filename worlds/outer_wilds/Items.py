import os
import pkgutil
from typing import Dict, List, NamedTuple, Optional
from random import Random

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
    },
    "Tornado": {"Tornado Aerodynamic Adjustments"}
}


def create_item(player: int, name: str) -> OuterWildsItem:
    return OuterWildsItem(name, item_data_table[name].type, item_data_table[name].code, player)


repeatable_filler_weights = {
    "Nothing": 0,  # no longer used, here for backwards compatibility
    "Oxygen Refill": 10,
    "Jetpack Fuel Refill": 10,
    "Marshmallow": 8,
    "Perfect Marshmallow": 1,
    "Burnt Marshmallow": 1,
}


def create_items(random: Random, multiworld: MultiWorld, options: OuterWildsGameOptions, player: int) -> None:
    prog_and_useful_items: List[OuterWildsItem] = []
    unique_filler: List[OuterWildsItem] = []
    for name, item in item_data_table.items():
        if item.type != ItemClassification.filler:
            # todo: come up with a better way to exclude locked / pre-placed items from the itempool
            if item.code and name != "Launch Codes":
                prog_and_useful_items.append(create_item(player, name))
        else:
            if name not in repeatable_filler_weights:
                unique_filler.append(create_item(player, name))

    item_pool = prog_and_useful_items + unique_filler

    # add enough "repeatable"/non-unique filler items to make item count equal location count
    repeatable_filler_needed = len(multiworld.get_unfilled_locations(player)) - len(item_pool)
    repeatable_filler = random.choices(
        population=list(repeatable_filler_weights.keys()),
        weights=list(repeatable_filler_weights.values()),
        k=repeatable_filler_needed
    )
    item_pool += (create_item(player, name) for name in repeatable_filler)

    multiworld.itempool += item_pool
