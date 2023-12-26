from dataclasses import dataclass

from Options import Choice, Toggle, PerGameCommonOptions


class Goal(Choice):
    """The victory condition for your Archipelago run.
    Song of Five: Reach the Eye and gather the 5 Hearthian travelers
    Song of Six: Reach the Eye and gather 6 travelers (5 Hearthians and Solanum)."""
    display_name = "Goal"
    option_song_of_five = 0
    option_song_of_six = 1


class DeathLink(Toggle):
    """When you die, everyone dies. Of course the reverse is true too."""
    display_name = "Death Link"


@dataclass
class OuterWildsGameOptions(PerGameCommonOptions):
    goal: Goal
    death_link: DeathLink
