from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Range, StartInventoryPool, Toggle


class ShuffleSolSeals(DefaultOnToggle):
    """Allows the Sol Seal items to be placed on any location in the multiworld, instead of their vanilla locations."""
    display_name = "Shuffle Sol Seals"


class SealsForEigong(Range):
    """The number of Sol Seals needed to open the door in Central Hall to New Kunlun Control Hub, fight Eigong,
    and complete the goal.
    Unlike the vanilla game, you don't need to visit Tiandao Research Center or trigger the "point of no return"."""
    display_name = "Seals For Eigong"
    range_start = 0
    range_end = 8
    default = 8


class SealsForPrison(Range):
    """The number of Sol Seals needed for Jiequan to appear in Factory (Great Hall), allowing you to "fight" him,
    do the whole Prison escape sequence, and check most of the locations in Factory (Machine Room).
    Note that you also need Mystic Nymph: Scout Mode before Jiequan will appear,
    since you can't do the Prison escape sequence without it.
    Unlike the vanilla game, the real Jiequan fight may be done before or after Prison, and it does not matter
    which Sol Seals you've collected, only the total number."""
    display_name = "Seals For Prison"
    range_start = 0
    range_end = 8
    default = 3


class SealsForEthereal(Range):
    """The number of Sol Seals needed for the entrance to Lady Ethereal's soulscape to appear in Cortex Center.
    See also the skip_soulscape_platforming option.
    Unlike the vanilla game, it does not matter which Sol Seals you've collected, only the total number."""
    display_name = "Seals For Ethereal"
    range_start = 0
    range_end = 8
    default = 4


class SkipSoulscapePlatforming(Toggle):
    """After you collect enough Sol Seals to unlock Lady Ethereal's soulscape (see seals_for_ethereal),
    if this option is enabled, Cortex Center will skip ahead to the state where you can enter her boss fight,
    instead of the long platforming sequence you normally do first.

    This is a .yaml/generation option because it has a small effect on logic: The platforming sequence logically
    requires Tai-Chi Kick, so skipping it allows the Lady Ethereal fight to be in-logic with only Air Dash."""
    display_name = "Skip Soulscape Platforming"


class RandomizeJadeCosts(Toggle):
    """Edit the cost of every jade in this slot to a randomly chosen number between jade_cost_min and jade_cost_max.

    This includes jades which are not Archipelago items.

    As a reminder: you start the game with 2 units of computing power, and there are 8 Computing Unit items to find,
    for a maximum power of 10."""
    display_name = "Randomize Jade Costs"


class JadeCostMin(Range):
    """The minimum possible jade cost. Has no effect if randomize_jade_costs is false."""
    display_name = "Jade Cost Minimum"
    range_start = 0
    range_end = 10
    default = 1


class JadeCostMax(Range):
    """The maximum possible jade cost. Has no effect if randomize_jade_costs is false."""
    display_name = "Jade Cost Maximum"
    range_start = 0
    range_end = 10
    default = 3


class LogicDifficulty(Choice):
    """
    `vanilla` is exactly what it sounds like: You will only be expected to do what the vanilla game required.

    `easy` adds tricks that are no harder to execute than what the vanilla game requires, once you've been told these
    tricks exist. Specifically:
    - "Pseudo Air Dashes" using either a talisman ("T-PAD") or Charged Strike ("CS-PAD")
    - Using a Cloud Piercer S (or X) arrow to break Charged Strike barriers without Charged Strike
    - Using a Thunder Buster arrow (any level) to break one-way barriers from the "wrong" side
    - "Bow Hover": Press and hold jump, shoot the bow immediately (during the first half of Yi's upward movement) with
    any arrow equipped, and then simply never let go of the jump button until you're done hovering.
    - Using the Swift Runner skill to jump with extra horizontal momentum

    `ledge_storage`: TODO
    ledge storage - cling to a ledge, slash, then interrupt the slash with either cloud leap, air dash or a talisman
        do we want talisman ledge storage in logic???
        I like the idea that CL or AD is required to do this stuff
        could we also make ledge cling itself an item?
        need to test doing this with skull kick
    ledge storage getup - after LS: jump, slash and hold up
        this can be done anytime during the jump, so slashing before the peak lets you getup at the peak
        e.g. the jump to the top of Daybreak Tower can be done with AD LS
        LS getup also *resets cloud leap*, which is how CL LS lets you do a "triple jump"
    ledge storage hover - after LS: press and hold jump, then press parry.
        Like bow hover, the parry has to be done early. I think during the first half of upward movement???
    ledge storage vault - after LS: press and hold jump, then press parry and hold up.
        you have to do this below min jump height, so it only helps after a bow hover like in elevator skip
    wall slide -

    To keep entrance randomization feasible, no logic level will expect you to carry a transient resource like
    azure sand, qi charges or ledge storage from one area to another.
    Bow and talisman logic will assume you only have the initial 2 arrows and 1 qi to spend in between root nodes and
    parryable enemies. Any route that requires more arrows or more qi (e.g. breaking one-way barriers with 3 Cloud
    Piercer arrows, traversing the bottom of AF (Depths) with multiple talisman dashes) will simply be out of logic.

    Other glitches like low gravity, rope storage, and respawn manip are simply out of logic.
    """
    display_name = "Logic Difficulty"
    option_vanilla = 0
    option_easy = 1
    option_ledge_storage = 2
    default = 0


@dataclass
class NineSolsGameOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    shuffle_sol_seals: ShuffleSolSeals
    seals_for_eigong: SealsForEigong
    seals_for_prison: SealsForPrison
    seals_for_ethereal: SealsForEthereal
    skip_soulscape_platforming: SkipSoulscapePlatforming
    randomize_jade_costs: RandomizeJadeCosts
    jade_cost_min: JadeCostMin
    jade_cost_max: JadeCostMax
    logic_difficulty: LogicDifficulty

