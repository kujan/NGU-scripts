"""Guffin startup script."""
from scripts.guffin import GuffinRun
from classes.helper import Helper
from typing import NamedTuple, List
import constants as const


class Settings(NamedTuple):
    # Duration in seconds to run before rebirthing
    max_rb_duration: int = 1800
    # Name of the zone you wish to quest in when you're out of majors.
    # See QUEST_ZONE_MAP in constants.py for valid options.
    zone: str = "sewers"
    # Name of the zone you wish to go to at the start of the rebirth.
    # See ZONE_MAP in constants.py for valid options.
    gold_zone: str = "the rad-lands"
    # Which hack(s) to use.
    hacks: List[int] = [2]
    # Which digger(s) to use.
    diggers: List[int] = const.DEFAULT_DIGGER_ORDER
    # Use butter for major quests?
    butter: bool = True
    # Which augments to use, see classes.features.Augments.augments() for naming convention.
    aug: List[str] = ["SS", "DS"]
    # Assign resources to wishes?
    allocate_wishes: bool = False
    # Which wandoos version to use (0-2).
    wandoos_version: int = 0
    # Your minimum wish time.
    wish_min_time: int = 180
    # Your amount of wish slots.
    wish_slots: int = 4


Helper.init(True)
Helper.requirements()
GuffinRun.init(Settings())
while True:
    GuffinRun.run()
