from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Item, ItemClassification, MultiWorld


class OuterWildsItem(Item):
    game = "Outer Wilds"


class OuterWildsItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True


# per AP docs, randomly chosen from the range of positive 32-bit integers
# to avoid conflicts with any other AP game's ids
min_item_id = 1734473680

item_data_table: Dict[str, OuterWildsItemData] = {
    "Nothing": OuterWildsItemData(
        code=min_item_id + 0,
        type=ItemClassification.filler,
    ),

    "Launch Codes": OuterWildsItemData(
        code=min_item_id + 1,
        type=ItemClassification.progression,
    ),
    "Spaceship": OuterWildsItemData(
        code=None,
        type=ItemClassification.progression,
    ),
    "Translator": OuterWildsItemData(
        code=min_item_id + 2,
        type=ItemClassification.progression,
    ),
    "Signalscope": OuterWildsItemData(
        code=min_item_id + 3,
        type=ItemClassification.progression,
    ),
    "Scout": OuterWildsItemData(
        code=min_item_id + 4,
        type=ItemClassification.progression,
    ),

    # "Distress Beacon Frequency"
    "Quantum Fluctuations Frequency": OuterWildsItemData(
        code=min_item_id + 100,
        type=ItemClassification.progression,  # just for testing
    ),
    "Hide & Seek Frequency": OuterWildsItemData(
        code=min_item_id + 101,
        type=ItemClassification.filler,
    ),

    "Museum Shard Signal": OuterWildsItemData(
        code=min_item_id + 102,
        type=ItemClassification.filler,
    ),
    "Grove Shard Signal": OuterWildsItemData(
        code=min_item_id + 103,
        type=ItemClassification.filler,
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

item_name_groups = {
    "Frequencies": {
        "Quantum Fluctuations Frequency",
        "Hide & Seek Frequency"
    },
    "Signals": {
        "Museum Shard Signal",
        "Grove Shard Signal",
    },
}
