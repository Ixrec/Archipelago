from dataclasses import dataclass

from schema import Schema, And

from Options import Choice, DefaultOnToggle, OptionDict, PerGameCommonOptions, Range, StartInventoryPool, Toggle


class Goal(Choice):
    """The victory condition for your Archipelago run.
    Song of Five: Reach the Eye
    Song of Six: Reach the Eye after meeting Solanum"""
    display_name = "Goal"
    option_song_of_five = 0
    option_song_of_six = 1


class RandomizeCoordinates(DefaultOnToggle):
    """Randomize the Eye of the Universe coordinates needed to reach the end of the game."""
    display_name = "Randomize Coordinates"


class TrapChance(Range):
    """The probability for each filler item (including unique filler) to be replaced with a trap item.
    The exact number of trap items will still be somewhat random, so you can't know
    if you've seen the 'last trap' in your world without checking the spoiler log.
    If you don't want any traps, set this to 0."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 15


class TrapTypeWeights(OptionDict):
    """When a filler item is replaced with a trap, these weights determine the
    odds for each trap type to be selected.
    If you don't want a specific trap type, set its weight to 0.
    Setting all weights to 0 is the same as setting trap_chance to 0."""
    schema = Schema({
        "Ship Damage Trap": And(int, lambda n: n >= 0),
        "Nap Trap": And(int, lambda n: n >= 0),
        "Audio Trap": And(int, lambda n: n >= 0),
    })
    display_name = "Trap Type Weights"
    default = {
        "Ship Damage Trap": 2,
        "Nap Trap": 2,
        "Audio Trap": 1,
    }


class DeathLink(Choice):
    """When you die, everyone dies. Of course the reverse is true too.
    The "default" option will not include deaths to meditation, the supernova or the time loop ending.
    Be aware that the game mod provides a 'Death Link Override' setting, in case you change your mind later."""
    display_name = "Death Link"
    option_off = 0
    option_default = 1
    option_all_deaths = 2


# DLC + logsanity is another 71 checks. "rumor sanity" would be another 103 (+22 with DLC).
class Logsanity(Toggle):
    """Adds 176 locations for all the (non-DLC, non-rumor, non-missable) ship log facts in the game."""
    display_name = "Logsanity"


class ShuffleSpacesuit(Toggle):
    """Puts the spacesuit into the Archipelago item pool, forcing you to play suitless until it's found.
    This is a HIGHLY EXPERIMENTAL setting. Expect logic bugs. Feedback encouraged."""
    display_name = "Shuffle Spacesuit"


@dataclass
class OuterWildsGameOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    randomize_coordinates: RandomizeCoordinates
    trap_chance: TrapChance
    trap_type_weights: TrapTypeWeights
    death_link: DeathLink
    logsanity: Logsanity
    shuffle_spacesuit: ShuffleSpacesuit
