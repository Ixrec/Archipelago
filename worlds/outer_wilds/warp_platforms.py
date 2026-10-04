from random import Random
from .options import OuterWildsGameOptions, Spawn
from Options import OptionError


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


# The vanilla warp mapping is:
# [("SS", "ST"), ("ET", "ETT"), ("ATP", "ATT"), ("TH", "THT"), ("BHNG", "WHS"), ("BHF", "BHT"), ("GD", "GDT")]
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

    # Handle warp plando.
    for w1, w2 in options.warp_platform_plando.items():
        if (w1 in dead_end_platforms and w2 in dead_end_platforms):
            raise OptionError(f"Error while processing warp plando: Trying to connect 2 dead ends ({w1} - {w2})")
        if (w1 == w2):
            raise OptionError(f"Error while processing warp plando: Trying to connect {w1} to itself.")
        if (w1 not in unmapped_platforms):
            raise OptionError(f"Error while processing warp plando: {w1} is connected twice.")
        if (w2 not in unmapped_platforms):
            raise OptionError(f"Error while processing warp plando: {w2} is connected twice.")
        mappings.append((w1, w2))
        unmapped_platforms.remove(w1)
        unmapped_platforms.remove(w2)
    
    # Handle dead ends first to avoid pairing dead ends with other dead ends (e.g. Sun Station <-> ATP)
    for dead_end_platform in dead_end_platforms:
        if (dead_end_platform not in unmapped_platforms):
            continue # Warp has been connected via plando.
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
