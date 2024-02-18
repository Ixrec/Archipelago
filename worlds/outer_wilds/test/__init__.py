from test.bases import WorldTestBase, CollectionState


class OuterWildsTestBase(WorldTestBase):
    game = "Outer Wilds"
    player: int = 1

    def make_state_with(self, item_names: list[str]) -> CollectionState:
        state = CollectionState(self.multiworld)
        for i in self.get_items_by_name(item_names):
            state.collect(i)
        return state

    def get_location_count(self) -> int:
        return sum(1 for _ in self.multiworld.get_locations(1))

    def can_reach_location_with(self, location_name: str, item_names: list[str]) -> bool:
        state = self.make_state_with(item_names)
        return state.can_reach(location_name, "Location", 1)

    def location_requires_exactly(self, location_name: str, item_names: list[str]) -> bool:
        items = self.get_items_by_name(item_names)
        state = CollectionState(self.multiworld)

        # check that it can be reached with all the items
        for i in items:
            state.collect(i)
        if not state.can_reach(location_name, "Location", 1):
            return False

        # check that removing any one item makes it unreachable again
        for i in items:
            state.remove(i)
            if state.can_reach(location_name, "Location", 1):
                return False
            state.collect(i)

        return True

    def assert_all_locations_requiring_exactly(self, location_names: list[str], item_names: list[str]) -> None:
        for location in self.multiworld.get_locations():
            if location.name in location_names:
                self.assertTrue(
                    self.location_requires_exactly(location.name, item_names),
                    f"location '{location}' should require exactly {item_names} to reach, but it doesn't"
                )
            else:
                self.assertFalse(
                    self.location_requires_exactly(location.name, item_names),
                    f"location '{location}' was not one of the locations being asserted on, "
                    f"but it requires exactly {item_names} to reach, so it should be"
                )

    def test_all_worlds(self) -> None:
        self.assertAccessDependency(
            ["Victory - Song of Five", "Victory - Song of Six"],
            [["Coordinates"]]
        )

        # for now, we create the Victory events unconditionally, and the Goal
        # setting only changes which one is used in the completion_condition,
        # so these "go mode" tests pass regardless of the Goal setting
        self.assertTrue(self.make_state_with([
            "Launch Codes",
            "Nomai Warp Codes",
            "Warp Core Installation Manual",
            "Silent Running Mode",
            "Signalscope",
            "Distress Beacon Frequency",
            "Scout",
            "Coordinates"
        ]).can_reach("Victory - Song of Five", "Location", 1))

        self.assertFalse(self.make_state_with([
            "Launch Codes",
            "Nomai Warp Codes",
            "Warp Core Installation Manual",
            "Silent Running Mode",
            "Signalscope",
            "Distress Beacon Frequency",
            "Scout",
            "Coordinates"
        ]).can_reach("Victory - Song of Six", "Location", 1))

        self.assertTrue(self.make_state_with([
            "Launch Codes",
            "Nomai Warp Codes",
            "Warp Core Installation Manual",
            "Silent Running Mode",
            "Signalscope",
            "Distress Beacon Frequency",
            "Scout",
            "Coordinates",
            # added by Song of Six
            "Imaging Rule",
            "Shrine Door Codes",
            "Entanglement Rule"
        ]).can_reach("Victory - Song of Six", "Location", 1))


class TestDefaultWorld(OuterWildsTestBase):
    options = {}

    def test_default_world(self):
        self.assertEqual(self.get_location_count(), 86)  # default locations, including Victory events

        # with default locations, Insulation only blocks 2 checks
        self.assertAccessDependency(
            ["GD: Enter the Core", "GD: See the Coordinates"],
            [["Electrical Insulation"]]
        )

        self.assert_all_locations_requiring_exactly(
            ["Ruptured Core (Text Wheel)"],
            ["Launch Codes", "Scout", "Ghost Matter Wavelength", "Translator"]
        )

        # logsanity locations don't exist, so trying to access one raises
        self.assertRaises(KeyError, lambda: self.multiworld.get_location("Ship Log: Village 1 - Identify", 1))


class TestSongOfSixWorld(OuterWildsTestBase):
    options = {
        "goal": 1
    }

    def test_six_world(self):
        self.assertEqual(self.get_location_count(), 86)  # same as song of five

        # same as song of five
        self.assertAccessDependency(
            ["GD: Enter the Core", "GD: See the Coordinates"],
            [["Electrical Insulation"]]
        )


class TestLogsanityWorld(OuterWildsTestBase):
    options = {
        "logsanity": "true"
    }

    def test_logsanity_world(self):
        self.assertEqual(self.get_location_count(), 262)  # 86 default + 176 logsanity locations

        # make sure the logsanity locations exist; this one requires nothing to reach
        self.assertTrue(self.multiworld.state.can_reach("TH Ship Log: Village 1 - Identify", "Location", 1))

        # and some of those new locations are Insulation-gated
        self.assertAccessDependency(
            [
                "GD: Enter the Core", "GD: See the Coordinates",
                "GD Ship Log: Ocean Depths 2 - Coral Forest",
                "GD Ship Log: Probe Tracking Module 1 - Millions",
                "GD Ship Log: Probe Tracking Module 2 - Anomaly Located",
                "GD Ship Log: Probe Tracking Module 3 - Statue",
                "GD Ship Log: Probe Tracking Module 4 - Coordinates"
            ],
            [["Electrical Insulation"]]
        )
