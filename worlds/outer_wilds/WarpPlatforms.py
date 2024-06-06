from random import Random
from typing import List, Tuple


warp_platforms = [
    "SS",  # Sun Station
    "ST",  # Sun Tower on Ash Twin
    "ET",  # Ember Twin
    "ETT",  # Ember Twin Tower
    "ATP",  # inside Ash Twin Project
    "ATT",  # Ash Twin Tower on Ash Twin's surface
    "TH",  # Timber Hearth
    "THT",  # Timber Hearth Tower on Ash Twin
    "BHNG",  # Brittle Hollow Northern Glacier
    "WHS",  # White Hole Station
    "BHF",  # the pad on the Hanging City ceiling used to access Black Hole Forge
    "BHT",  # Brittle Hollow Tower on Ash Twin
    "GD",  # Giant's Deep
    "GDT",  # Giant's Deep Tower on Ash Twin
]


# The vanilla warp mapping is:
# [("SS", "ST"), ("ET", "ETT"), ("ATP", "ATT"), ("TH", "THT"), ("BHNG", "WHS"), ("BHF", "BHT"), ("GD", "GDT")]
def generate_random_warp_platform_mapping(random: Random) -> List[Tuple[str, str]]:
    platforms = warp_platforms.copy()
    random.shuffle(platforms)
    it = iter(platforms)
    return list(zip(it, it))


warp_platform_to_logical_region = {
    "SS": "Sun Station",
    "ST": "Hourglass Twins",
    "ET": "Hourglass Twins",
    "ETT": "Hourglass Twins",
    "ATP": "Ash Twin Interior",
    "ATT": "Hourglass Twins",
    "TH": "Timber Hearth",
    "THT": "Hourglass Twins",
    "BHNG": "Brittle Hollow",
    "WHS": "White Hole Station",
    "BHF": "Hanging City Ceiling",
    "BHT": "Hourglass Twins",
    "GD": "Giant's Deep",
    "GDT": "Hourglass Twins",
}

warp_platform_required_items = {
    "SS": ["Spacesuit"]
}
