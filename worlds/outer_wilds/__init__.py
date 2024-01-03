from typing import List

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World

from .Items import OuterWildsItem, item_data_table, item_table, item_name_groups
from .LocationsAndRegions import location_table, location_name_groups, create_regions
from .Options import OuterWildsGameOptions


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
    web = OuterWildsWebWorld()

    # because we use options_dataclass, this is the minimum AP version we support
    required_client_version = (0, 4, 4)
    required_server_version = (0, 4, 4)

    # members and methods implemented by Items.py and items.jsonc

    item_name_to_id = item_table
    item_name_groups = item_name_groups

    def create_item(self, name: str) -> OuterWildsItem:
        return OuterWildsItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[OuterWildsItem] = []
        for name, item in item_data_table.items():
            # todo: come up with a better way to exclude locked / pre-placed items from the itempool
            if item.code and name != "Launch Codes":
                item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

        # add enough "Nothing"s to make item count equal location count
        filler_needed = len(self.location_name_to_id) - len(self.item_name_to_id)
        self.multiworld.itempool += [self.create_item("Nothing") for _ in range(filler_needed)]

    def get_filler_item_name(self) -> str:
        # todo: after we have more interesting filler items, see if we can make
        # this rotate between fillers to evenly fill remaining locations
        return "Nothing"

    # members and methods implemented by LocationsAndRegions.py, locations.jsonc and connections.jsonc

    location_name_to_id = location_table
    location_name_groups = location_name_groups

    def create_regions(self) -> None:
        create_regions(self.multiworld, self.player, self.create_item)

    # members and methods related to Options.py

    options_dataclass = OuterWildsGameOptions
    options: OuterWildsGameOptions

    def set_rules(self) -> None:
        # here we only set the completion condition; all the location and region rules were set earlier
        option_key_to_item_name = {
            'song_of_five': "Victory - Song of Five",
            'song_of_six': "Victory - Song of Six",
        }

        goal = getattr(self.multiworld, "goal")[self.player]
        goal_item = option_key_to_item_name[goal.current_key]
        self.multiworld.completion_condition[self.player] = lambda state: state.has(goal_item, self.player)

    def fill_slot_data(self):
        slot_data = self.options.as_dict("goal", "death_link")
        # Archipelago does not yet have apworld versions (data_version is deprecated),
        # so we have to roll our own with slot_data for the time being
        slot_data["apworld_version"] = "0.1.0"
        return slot_data
