from . import OuterWildsTestBase


class TestHN1(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1
    }

    def test_hn1(self):
        self.assertEqual(self.getLocationCount(), 109)  # 87(+2V) base game + 20 HN1 locations


class TestHN1Logsanity(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1,
        "logsanity": 1
    }

    def test_hn1_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 20 HN1 default locations + 41 HN1 logsanity locations
        self.assertEqual(self.getLocationCount(), 326)


class TestOutsider(OuterWildsTestBase):
    options = {
        "enable_outsider_mod": 1
    }

    def test_outsider(self):
        pass #self.assertEqual(self.getLocationCount(), 109)  # 87(+2V) base game + ? TO locations


class TestOutsiderLogsanity(OuterWildsTestBase):
    options = {
        "enable_outsider_mod": 1,
        "logsanity": 1
    }

    def test_outsider_logsanity(self):
        pass # 87(+2V) base game default locations + 176 base game logsanity locations +
        #self.assertEqual(self.getLocationCount(), 326)


class TestAC(OuterWildsTestBase):
    options = {
        "enable_ac_mod": 1
    }

    def test_ac(self):
        pass #self.assertEqual(self.getLocationCount(), 109)  # 87(+2V) base game + ? AC locations


class TestACLogsanity(OuterWildsTestBase):
    options = {
        "enable_ac_mod": 1,
        "logsanity": 1
    }

    def test_ac_logsanity(self):
        pass # 87(+2V) base game default locations + 176 base game logsanity locations +
        #self.assertEqual(self.getLocationCount(), 326)


class TestAllMods(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1,
        "enable_outsider_mod": 1,
        "enable_ac_mod": 1
    }

    def test_all_mods(self):
        # 87(+2V) base game default locations +
        # 20 HN1 default locations +
        pass#self.assertEqual(self.getLocationCount(), 109)


class TestAllModsLogsanity(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1,
        "enable_to_mod": 1,
        "enable_ac_mod": 1,
        "logsanity": 1
    }

    def test_all_mods_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 20 HN1 default locations + 41 HN1 logsanity locations
        pass#self.assertEqual(self.getLocationCount(), 326)


# this is just to get an assertion on the maximum possible location count
class TestAllModsAndDLCLogsanity(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": 1,
        "enable_hn1_mod": 1,
        "enable_to_mod": 1,
        "enable_ac_mod": 1,
        "logsanity": 1
    }

    def test_all_mods_and_dlc_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 34(+4V) DLC default locations + 72 DLC logsanity locations +
        # 20 HN1 default locations + 41 HN1 logsanity locations
        pass#self.assertEqual(self.getLocationCount(), 436)
