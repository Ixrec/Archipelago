from typing import Callable

from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import add_rule, set_rule, forbid_item, add_item_rule


def set_rules(world: "OuterWildsWorld") -> None:
    mw = world.multiworld
    p = world.player

    # figure out region rules when I rewrite regions
    # set_rule(mw.get_entrance("Boss Door", p), lambda state: state.has("Boss Key", p))

    # todo: only true for vanilla spawn
    add_rule(mw.get_location("Enter Your Spaceship", p), lambda state: state.has("Launch Codes", p))

    add_rule(mw.get_location("TH: Mines (Text Wall)", p), lambda state: state.has("Translator", p))

    if getattr(mw, "textsanity")[p]:
        add_rule(mw.get_location("TH_Museum_EyeSymbol line 1", p), lambda state: state.has("Translator", p))

    mw.completion_condition[p] = lambda state: (state.has("Spaceship", p) and
                                                state.has("Signalscope", p) and
                                                state.has("Quantum Fluctuations Frequency", p))
