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
    "filler": ItemClassification.filler,
    "trap": ItemClassification.trap
}

item_data_table: Dict[str, OuterWildsItemData] = {}
for items_data_entry in items_data:
    item_data_table[items_data_entry["name"]] = OuterWildsItemData(
        code=(items_data_entry["code"] if "code" in items_data_entry else None),
        type=item_types_map[items_data_entry["type"]]
    )

all_non_event_items_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

item_names: set[str] = set(entry["name"] for entry in items_data)
item_name_groups = {
    # Auto-generated groups
    # We don't need an "Everything" group because AP makes that for us

    "progression": set(entry["name"] for entry in items_data if entry["type"] == "progression"),
    "useful": set(entry["name"] for entry in items_data if entry["type"] == "useful"),
    "filler": set(entry["name"] for entry in items_data if entry["type"] == "filler"),
    "trap": set(entry["name"] for entry in items_data if entry["type"] == "trap"),

    "Frequencies": set(n for n in item_names if n.endswith(" Frequency")),
    "Signals": set(n for n in item_names if n.endswith(" Signal")),

    # Manually curated groups
    "Ship Upgrades": {
        "Tornado Aerodynamic Adjustments",
        "Silent Running Mode",
        "Autopilot",
        "Landing Camera",
    },
    "Tools": {
        "Translator",
        "Signalscope",
        "Scout",
        "Ghost Matter Wavelength",
        "Imaging Rule",
    },

    # Aliases
    "Little Scout": {"Scout"},
    "Probe": {"Scout"},
    "Anglerfish": {"Silent Running Mode"},
    "Tornado": {"Tornado Aerodynamic Adjustments"},
    "Insulation": {"Electrical Insulation"},
    "Jellyfish": {"Electrical Insulation"},
    "Quantum Wavelength": {"Imaging Rule"},
    "Quantum Camera": {"Imaging Rule"},
    "GM": {"Ghost Matter Wavelength"},
    "Ghost Matter": {"Ghost Matter Wavelength"},
    "GM Wavelength": {"Ghost Matter Wavelength"},
    "Advanced Warp Core": {"Warp Core Installation Manual"},
    "Eye Coordinates": {"Coordinates"},
    "EotU Coordinates": {"Coordinates"},
    "Eye of the Universe Coordinates": {"Coordinates"},
    "DBF": {"Distress Beacon Frequency"},
    "DB Frequency": {"Distress Beacon Frequency"},
    "QFF": {"Quantum Fluctuations Frequency"},
    "QF Frequency": {"Quantum Fluctuations Frequency"},
    "HSF": {"Hide & Seek Frequency"},
    "HS Frequency": {"Hide & Seek Frequency"},
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
        if item.type == ItemClassification.filler:
            if name not in repeatable_filler_weights:
                unique_filler.append(create_item(player, name))
        else:
            if item.type != ItemClassification.trap:
                # todo: come up with a better way to exclude locked / pre-placed items from the itempool
                if item.code and name != "Launch Codes":
                    prog_and_useful_items.append(create_item(player, name))

    unique_filler_with_traps = unique_filler

    # replace some unique filler items with trap items, depending on trap settings
    trap_weights = options.trap_type_weights
    trap_chance = (options.trap_chance / 100)
    filler_chance = 1 - trap_chance
    apply_trap_items = options.trap_chance > 0 and any(v > 0 for v in options.trap_type_weights.values())
    if apply_trap_items:
        trap_overwrites = random.choices(
            population=[None] + list(trap_weights.keys()),
            weights=[filler_chance] + list(v * trap_chance for v in trap_weights.values()),
            k=len(unique_filler)
        )
        for i in range(0, len(unique_filler)):
            trap_overwrite = trap_overwrites[i]
            if trap_overwrite is not None:
                unique_filler_with_traps[i] = create_item(player, trap_overwrite)

    # add enough "repeatable"/non-unique filler items (and/or traps) to make item count equal location count
    unique_item_count = len(prog_and_useful_items) + len(unique_filler)
    repeatable_filler_needed = len(multiworld.get_unfilled_locations(player)) - unique_item_count
    junk_names = list(repeatable_filler_weights.keys())
    junk_values = list(repeatable_filler_weights.values())
    if apply_trap_items:
        junk_names += list(trap_weights.keys())
        junk_values = list(v * filler_chance for v in junk_values)
        junk_values += list(v * trap_chance for v in trap_weights.values())
    repeatable_filler_names_with_traps = random.choices(
        population=junk_names,
        weights=junk_values,
        k=repeatable_filler_needed
    )
    repeatable_filler_with_traps = list(create_item(player, name) for name in repeatable_filler_names_with_traps)

    itempool = prog_and_useful_items + unique_filler_with_traps + repeatable_filler_with_traps
    multiworld.itempool += itempool
