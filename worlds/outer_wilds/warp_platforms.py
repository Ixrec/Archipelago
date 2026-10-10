from random import Random
from .options import OuterWildsGameOptions, Spawn


# we use lists instead of sets here to ensure determinism
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

# These are the warp platforms which (logically) can only be reached via another warp platform
dead_end_platforms = [
    "SS",
    "ATP",
    "BHF",
]

platforms_reachable_by_ship = [p for p in warp_platforms if p not in dead_end_platforms]
vanilla_warp_mapping = [("SS", "ST"), ("ET", "ETT"), ("ATP", "ATT"), ("TH", "THT"), ("BHNG", "WHS"), ("BHF", "BHT"), ("GD", "GDT")]


def generate_random_warp_platform_mapping(random: Random, options: OuterWildsGameOptions) -> list[tuple[str, str]]:
    unmapped_platforms = warp_platforms.copy()
    mappings = []

    # Astral Codec requires a shipless warp path from the Hourglass Twins to Timber Hearth.
    # For simplicity, we connect HGT to TH directly, only randomizing which HGT pad gets used.
    if options.enable_ac_mod:
        available_hgt_platforms = ["ST", "ETT", "ATT", "THT", "BHT", "GDT", "ET"]  # all the towers plus Ember Twin
        hgt_platform = random.choice(available_hgt_platforms)
        mappings.append(("TH", hgt_platform))
        unmapped_platforms.remove("TH")
        unmapped_platforms.remove(hgt_platform)

    # Handle dead ends first to avoid pairing dead ends with other dead ends (e.g. Sun Station <-> ATP)
    for dead_end_platform in dead_end_platforms:
        available_platforms = [p for p in unmapped_platforms if p in platforms_reachable_by_ship]

        # Sun Station is the only warp platform that disappears about halfway through the loop.
        # Technically every other platform is exposed by then, but for some the margin is just too small.
        if dead_end_platform == 'SS':  # actually falls into the sun at 11:30 - 11:40
            available_platforms = [p for p in available_platforms if p not in [
                'THT',  # exposed at ~10:30
                'BHT',  # exposed at ~10:30
                'GDT'   # exposed at ~11:00
            ]]
            # The above rules out a direct THT/BHT/GDT->SS warp, but we also need to rule out a longer
            # warp path through THT/BHT/GDT being the only way to SS. Such a path would have to go
            # through Brittle Hollow because it's the only planet besides HGT with multiple warp pads.
            if options.spawn != Spawn.option_brittle_hollow:
                available_platforms = [p for p in available_platforms if p not in ['BHNG', 'WHS']]

        destination = random.choice(available_platforms)
        mappings.append((dead_end_platform, destination))
        unmapped_platforms.remove(dead_end_platform)
        unmapped_platforms.remove(destination)

    random.shuffle(unmapped_platforms)
    it = iter(unmapped_platforms)
    mappings.extend(list(zip(it, it)))

    return mappings


def connection_exists(mappings: list[tuple[str, str]], from_region: str, to_region: str, two_way: bool = False, skip_regions: set[str]|None = None) -> bool:
    # Avoid infinite recursion by keeping list of what regions have been checked.
    if skip_regions == None:
        skip_regions = set()
    if from_region in skip_regions or from_region not in warp_platform_to_logical_region.values():
        return False
    # Check not only local warps but also ones we can walk to (ie. BH's multiple warps).
    reachable_regions = { from_region }
    if two_way:
        reachable_regions.update(*{r for r in connected_regions.get(from_region, set()) if from_region in connected_regions.get(r, set())})
    else:
        reachable_regions.update(*connected_regions.get(from_region, set()))
    reachable_regions.difference_update(skip_regions)
    from_warps = [warp for warp, region in warp_platform_to_logical_region.items() if region in reachable_regions]

    skip_regions.update(reachable_regions)
    
    while len(from_warps) > 0:
        warp = from_warps.pop(0)
        to_warp = get_connected_warp(mappings, warp)
        target_region = warp_platform_to_logical_region[to_warp]
        if target_region == to_region or connection_exists(mappings, target_region, to_region, two_way, skip_regions):
            return True
    return False


def get_connected_warp(mappings: list[tuple[str, str]], from_warp: str) -> str:
    return [*[w2 for (w1, w2) in mappings if w1 == from_warp], *[w1 for (w1, w2) in mappings if w2 == from_warp]][0]


connected_regions = {
    "Brittle Hollow": {"White Hole Station"},
    "Hanging City Ceiling": {"White Hole Station", "Brittle Hollow"},
}

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
