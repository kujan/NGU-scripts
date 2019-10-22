"""Guffin startup script."""
import scripts.guffin
from classes.helper import Helper
from typing import NamedTuple, List
import constants as const

class Settings(NamedTuple):
    max_rb_duration: int = 1800
    zone: str = "sewers"
    gold_zone: str = "the rad-lands"
    hacks: List[int] = [2]
    diggers: List[int] = const.DEFAULT_DIGGER_ORDER
    butter: bool = False
    aug: List[str] = ["SS", "DS"]
    allocate_wishes: bool = False
    wandoos_version: int = 0
    wish_min_time: int = 180
    wish_slots: int = 4

Helper.init(True)
Helper.requirements()
scripts.guffin.GuffinRun.init(Settings())
while True: scripts.guffin.GuffinRun.run()
