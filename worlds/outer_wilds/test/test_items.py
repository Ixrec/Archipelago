from .bases import OuterWildsTestBase
from ..options import ShuffleEquipment


situational_equipment = {
    "Surface Integrity Scanner",
    "Eject Button",
    "Landing Camera",
}
useful_equipment = {
    "Autopilot",
    "Velocity Matcher",
}
essential_equipment = {
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

        self.assertSetEqual(precollected_item_names, essential_equipment)
        self.assertIn("Spacesuit", itempool_names)


class TestShuffleSpacesuitFalse(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": False,
    }

    def test_shuffle_spacesuit_false(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        self.assertSetEqual(precollected_item_names, essential_equipment.union({"Spacesuit"}))
        self.assertNotIn("Spacesuit", itempool_names)


class TestShuffleEquipmentSituational(OuterWildsTestBase):
    options = {
        "shuffle_equipment": ShuffleEquipment.option_situational,
    }

    def test_shuffle_equipment(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        for e in situational_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in useful_equipment:
            self.assertIn(e, precollected_item_names)
            self.assertNotIn(e, itempool_names)
        for e in essential_equipment:
            self.assertIn(e, precollected_item_names)
            self.assertNotIn(e, itempool_names)


class TestShuffleEquipmentUseful(OuterWildsTestBase):
    options = {
        "shuffle_equipment": ShuffleEquipment.option_useful,
    }

    def test_shuffle_equipment(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        for e in situational_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in useful_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in essential_equipment:
            self.assertIn(e, precollected_item_names)
            self.assertNotIn(e, itempool_names)


class TestShuffleEquipmentEssential(OuterWildsTestBase):
    options = {
        "shuffle_equipment": ShuffleEquipment.option_essential,
    }

    def test_shuffle_equipment(self):
        precollected_item_names = set(i.name for i in self.multiworld.precollected_items[self.player])
        itempool_names = list(i.name for i in self.multiworld.itempool)

        for e in situational_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in useful_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)
        for e in essential_equipment:
            self.assertNotIn(e, precollected_item_names)
            self.assertIn(e, itempool_names)

