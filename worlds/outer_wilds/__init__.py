from typing import List

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import OuterWildsItem, item_data_table, item_table, item_name_groups
from .Locations import OuterWildsLocation, location_data_table, location_table, locked_locations, location_name_groups
from .Options import OuterWildsGameOptions
from .Regions import region_data_table
from .Rules import set_rules


class OuterWildsWebWorld(WebWorld):
    theme = "dirt"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to playing Outer Wilds.",
            language="English",
            file_name="guide_en.md",
            link="guide/en",
            authors=["Ixrec"]
        )
    ]


class OuterWildsWorld(World):
    game = "Outer Wilds"
    data_version = 1
    web = OuterWildsWebWorld()
    options_dataclass = OuterWildsGameOptions
    options: OuterWildsGameOptions
    location_name_to_id = location_table
    item_name_to_id = item_table

    def create_item(self, name: str) -> OuterWildsItem:
        return OuterWildsItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[OuterWildsItem] = []
        for name, item in item_data_table.items():
            if item.code and item.can_create(self.multiworld, self.player):
                item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.multiworld.get_region(region_name, self.player)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self.multiworld, self.player)
            }, OuterWildsLocation)
            region.add_exits(region_data_table[region_name].connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self.multiworld, self.player):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.multiworld.get_location(location_name, self.player).place_locked_item(locked_item)

    def get_filler_item_name(self) -> str:
        return "Nothing"

    set_rules = set_rules

    def fill_slot_data(self):
        return {}

    item_name_groups = item_name_groups

    location_name_groups = location_name_groups
