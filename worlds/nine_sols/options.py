from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, StartInventoryPool, Toggle


class ShuffleSolSeals(DefaultOnToggle):
    """Allows the Sol Seal items to be placed on any location in the multiworld, instead of their vanilla locations."""
    display_name = "Shuffle Sol Seals"


class SkipSoulscapePlatforming(Toggle):
    """When you unlock Lady Ethereal by collecting 4 Sol Seals, if this option is enabled, Cortex Center will skip ahead
    to the state where you can enter her boss fight, instead of the long platforming sequence you normally do first."""
    display_name = "Skip Soulscape Platforming"


class LogicDifficulty(Choice):
    """
    `vanilla` is exactly what it sounds like: You will only be expected to do what the vanilla game required.

    `easy` adds tricks that are no harder to execute than what the vanilla game requires,
    once you've been told these tricks exist. Specifically:
    - Using a Cloud Piercer S (or X) arrow to break Charged Strike barriers without Charged Strike
    - Using a Thunder Buster arrow (any level) to break one-way barriers from the "wrong" side
    - "Bow hover": Press and hold jump, shoot the bow immediately (during the first half of Yi's upward movement) with
    any arrow equipped, and then simply never let go of the jump button until you're done hovering.
    - "Pseudo Air Dashes" using either talismans or Charged Strike

    Although these are as "easy" as vanilla, they may be more frustrating than vanilla, since missing a talisman dash
    or bow hover may involve significant backtracking to make another attempt.

    Bow and talisman logic will assume you only have the initial 2 arrows and 1 qi to spend in between root nodes and
    parryable enemies. Any route that requires more arrows or more qi (e.g. breaking one-way barriers with 3 Cloud
    Piercer arrows, traversing the bottom of AF (Depths) with only talisman dashes) will simply be out of logic.

    `oops_all_ledge_storage`: TODO
    """
    display_name = "Logic Difficulty"
    option_vanilla = 0
    option_easy = 1
    option_oops_all_ledge_storage = 2
    default = 0


@dataclass
class NineSolsGameOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    shuffle_sol_seals: ShuffleSolSeals
    skip_soulscape_platforming: SkipSoulscapePlatforming
    logic_difficulty: LogicDifficulty

