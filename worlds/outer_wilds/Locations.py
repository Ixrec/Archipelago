from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Location, MultiWorld


class OuterWildsLocation(Location):
    game = "Outer Wilds"


class OuterWildsLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    locked_item: Optional[str] = None


# per AP docs, randomly chosen from the range of positive 32-bit integers
# to avoid conflicts with any other AP game's ids
min_location_id = 1085038250

location_data_table: Dict[str, OuterWildsLocationData] = {
    "Enter Your Spaceship": OuterWildsLocationData(
        region="Timber Hearth Village",  # for now, later will depend on spaceship spawn settings
        address=None,
        locked_item="Spaceship",
    ),

    "TH: Ghost Matter Plaque": OuterWildsLocationData(
        region="Timber Hearth Village",
        address=min_location_id + 1,
    ),
    "TH: Zero-G Repairs": OuterWildsLocationData(
        region="Timber Hearth Village",
        address=min_location_id + 2,
    ),
    "TH: Get the Translator from Hal": OuterWildsLocationData(
        region="Timber Hearth Village",
        address=min_location_id + 3,
    ),
    "TH: Talk to Hornfels": OuterWildsLocationData(
        region="Timber Hearth Village",
        address=min_location_id + 4,
        locked_item="Launch Codes",
    ),

    "TH: Bramble Seed Crater": OuterWildsLocationData(
        region="Timber Hearth Surface",
        address=min_location_id + 5,
    ),
    "TH: Mines (Text Wall)": OuterWildsLocationData(
        region="Timber Hearth Surface",
        address=min_location_id + 6,
    ),

    # "Distress Beacon Frequency"
    "Quantum Fluctuations Frequency": OuterWildsLocationData(
        region="Timber Hearth Village",
        address=min_location_id + 100,
    ),
    "Hide & Seek Frequency": OuterWildsLocationData(
        region="Timber Hearth Village",
        address=min_location_id + 101,
    ),

    "TH: Museum Shard Signal": OuterWildsLocationData(
        region="Timber Hearth Village",
        address=min_location_id + 102,
    ),
    "TH: Grove Shard Signal": OuterWildsLocationData(
        region="Timber Hearth Surface",
        address=min_location_id + 103,
    ),

    # for now, this is only here to help test settings
    "TH_Museum_EyeSymbol line 1": OuterWildsLocationData(
        region="Timber Hearth Village",
        address=min_location_id+1001,
        can_create=lambda multiworld, player: bool(getattr(multiworld, "textsanity")[player]),
    ),
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}

location_name_groups = {
    "Frequencies": {
        # "Distress Beacon Frequency"
        "Quantum Fluctuations Frequency",
        "Hide & Seek Frequency",
    },
    "Signals": {},
    "Hourglass Twins": {},
    "Timber Hearth": {
        "TH: Ghost Matter Plaque",
        "TH: Zero-G Repairs",
        "TH: Get the Translator from Hal",
        "TH: Talk to Hornfels",
        "TH: Bramble Seed Crater",
        "TH: Mines (Text Wall)",
        "Hide & Seek Frequency",
        "TH: Museum Shard Signal",
        "TH: Grove Shard Signal",
    },
    "Brittle Hollow": {},
    "Giant's Deep": {},
    "Dark Bramble": {},
}
