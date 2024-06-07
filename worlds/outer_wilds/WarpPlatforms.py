from random import Random
from typing import List, Tuple


warp_platforms = {
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
}

# These are the warp platforms which (logically) can only be reached via another warp platform
dead_end_platforms = {
    "SS",
    "ATP",
    "BHF",
}

platforms_reachable_by_ship = warp_platforms.difference(dead_end_platforms)


# The vanilla warp mapping is:
# [("SS", "ST"), ("ET", "ETT"), ("ATP", "ATT"), ("TH", "THT"), ("BHNG", "WHS"), ("BHF", "BHT"), ("GD", "GDT")]
def generate_random_warp_platform_mapping(random: Random) -> List[Tuple[str, str]]:
    unmapped_platforms = warp_platforms.copy()
    mappings = []

    # Handle dead ends first to avoid pairing dead ends with other dead ends (e.g. Sun Station <-> ATP)
    for dead_end_platform in dead_end_platforms:
        destination = random.choice(list(unmapped_platforms.intersection(platforms_reachable_by_ship)))
        mappings.append((dead_end_platform, destination))
        unmapped_platforms.remove(dead_end_platform)
        unmapped_platforms.remove(destination)

    unmapped_platforms = list(unmapped_platforms)
    random.shuffle(unmapped_platforms)
    it = iter(unmapped_platforms)
    mappings.extend(list(zip(it, it)))

    return mappings


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
