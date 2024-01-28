from dataclasses import dataclass

from Options import Choice, Toggle, PerGameCommonOptions


class Goal(Choice):
    """The victory condition for your Archipelago run.
    Song of Five: Reach the Eye
    Song of Six: Reach the Eye after meeting Solanum"""
    display_name = "Goal"
    option_song_of_five = 0
    option_song_of_six = 1


class DeathLink(Choice):
    """When you die, everyone dies. Of course the reverse is true too.
    The "default" option will not include deaths to meditation, the supernova or the time loop ending."""
    display_name = "Death Link"
    option_off = 0
    option_default = 1
    option_all_deaths = 2


# DLC + logsanity is another 71 checks. "rumor sanity" would be another 103 (+22 with DLC).
class Logsanity(Toggle):
    """Adds a location for every (non-DLC, non-rumor) ship log fact in the game, which totals 178 new checks."""
    display_name = "Logsanity"


@dataclass
class OuterWildsGameOptions(PerGameCommonOptions):
    goal: Goal
    death_link: DeathLink
    logsanity: Logsanity
