from . import OuterWildsTestBase


class TestDLC(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": 1
    }

    def test_eote_dlc(self):
        self.assertEqual(self.getLocationCount(), 123)  # 90 base game + 33 DLC locations

        self.assertNotReachableWith("EotE: River Lowlands Workshop", [])
        self.assertReachableWith("EotE: River Lowlands Workshop", [
            "Ghost Matter Wavelength"
        ])


class TestDLCWithLogsanity(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": 1,
        "logsanity": 1
    }

    def test_eote_dlc(self):
        # 90 base game default locations + 176 base game logsanity locations +
        # 33 DLC default locations + 72 DLC logsanity locations
        self.assertEqual(self.getLocationCount(), 371)

        # the obvious route: use the RL artifact on the RL flame
        self.assertReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [
            "Ghost Matter Wavelength", "River Lowlands Painting Code",
        ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Ghost Matter Wavelength" ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "River Lowlands Painting Code" ])

        # get the lab artifact, return to main hangar, use it on RL flame
        self.assertReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [
            "Breach Override Codes", "River Lowlands Painting Code",
        ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Breach Override Codes" ])

        # take a raft to HG, use its artifact on HG flame, use totems to reach HG dock, take dream raft to SW dock
        self.assertReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [
            "Stranger Light Modulator", "Hidden Gorge Painting Code", "Dream Totem Patch", "Raft Docks Patch"
        ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Dream Totem Patch", "Raft Docks Patch" ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Stranger Light Modulator", "Hidden Gorge Painting Code" ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Stranger Light Modulator", "Hidden Gorge Painting Code", "Raft Docks Patch" ])
