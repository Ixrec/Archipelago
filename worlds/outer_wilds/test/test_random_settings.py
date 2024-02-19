import unittest
from argparse import Namespace

from worlds.AutoWorld import call_all
from test.general import gen_steps, setup_solo_multiworld
from Options import NumericOption

from .. import OuterWildsWorld
from . import OuterWildsTestBase


class TestRandomWorlds(unittest.TestCase):
    def test_random_worlds(self):
        for s in range(0, 1000):
            with self.subTest(f"random world seed={s}"):
                mw = setup_solo_multiworld(OuterWildsWorld, ())
                mw.set_seed(s)

                test_options = {
                    "goal": "random"
                }

                ns_options = Namespace()
                for name, option in OuterWildsWorld.options_dataclass.type_hints.items():
                    # if option.name == "trap_type_weights"
                    value = option(test_options[name]) if name in test_options else option.from_any(option.default)
                    if isinstance(option, NumericOption):
                        if callable(getattr(option, "from_text", None)):
                            value = option.from_text("random")
                    setattr(ns_options, name, {1: value})

                mw.set_options(ns_options)

                for step in gen_steps:
                    call_all(mw, step)


class TestRandomWorld(OuterWildsTestBase):
    options = {
        "goal": "random",
        "randomize_coordinates": "random",
        "trap_chance": "random",
        # "trap_type_weights" can't support "random" since it's an OptionDict
        "death_link": "random",
        "logsanity": "random",
    }
