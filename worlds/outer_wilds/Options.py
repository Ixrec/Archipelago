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


@dataclass
class OuterWildsGameOptions(PerGameCommonOptions):
    goal: Goal
    death_link: DeathLink
