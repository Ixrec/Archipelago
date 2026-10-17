from .bases import OuterWildsTestBase


default_precollected_equipment = {
    "Ship Medkit",
    "Ship Jetpack Refueler",
    "Velocity Indicator",
    "Distance Indicator",
    "Ship Lights",
}


class TestShuffleSpacesuitTrue(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": True,
    }

    def test_shuffle_spacesuit_true(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        self.assertSetEqual(precollected_item_names, default_precollected_equipment)
        self.assertIn("Spacesuit", itempool_names)


class TestShuffleSpacesuitFalse(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": False,
    }

    def test_shuffle_spacesuit_false(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        self.assertSetEqual(precollected_item_names, default_precollected_equipment.union({"Spacesuit"}))
        self.assertNotIn("Spacesuit", itempool_names)

