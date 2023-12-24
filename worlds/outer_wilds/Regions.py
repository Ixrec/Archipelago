from typing import Dict, List, NamedTuple


class OuterWildsRegionData(NamedTuple):
    connecting_regions: List[str] = []


region_data_table: Dict[str, OuterWildsRegionData] = {
    "Menu": OuterWildsRegionData(["Timber Hearth Village"]),
    "Timber Hearth Village": OuterWildsRegionData(["Timber Hearth Surface"]),  # requires ship + codes | alt spawn
    "Timber Hearth Surface": OuterWildsRegionData(),
}
