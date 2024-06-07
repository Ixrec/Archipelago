from . import OuterWildsTestBase
from ..Options import EarlyKeyItem, Spawn


class TestRandomWarp(OuterWildsTestBase):
    options = {
        "randomize_warp_platforms": True,
    }


class TestHGTSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_hourglass_twins,
    }


class TestHGTSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_hourglass_twins,
        "randomize_warp_platforms": True,
    }


class TestTHSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_timber_hearth,
    }


class TestTHSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_timber_hearth,
        "randomize_warp_platforms": True,
    }


class TestBHSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
    }


class TestBHSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_brittle_hollow,
        "randomize_warp_platforms": True,
    }


class TestGDSpawn(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_giants_deep,
    }


class TestGDSpawnRandomWarp(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_giants_deep,
        "randomize_warp_platforms": True,
    }


class TestHGTSpawnRandomWarpEKI(OuterWildsTestBase):
    options = {
        "spawn": Spawn.option_hourglass_twins,
        "randomize_warp_platforms": True,
        "early_key_item": EarlyKeyItem.option_global,
    }

