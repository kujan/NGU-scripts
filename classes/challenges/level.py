"""Contains functions for running a 100 level challenge."""
from classes.features import FightBoss, Adventure, Augmentation, GoldDiggers, Rebirth, Misc

import coordinates as coords
import time


def speedrun(duration):
    """Procedure for first rebirth in a 100LC."""
    FightBoss.nuke()
    time.sleep(2)
    FightBoss.fight()
    diggers = [2, 3, 11, 12]
    Adventure.adventure(highest=True)
    current_boss = int(FightBoss.get_current_boss())
    if current_boss > 48:
        Augmentation.augments({"EB": 0.66, "CS": 0.34}, Misc.get_idle_cap(1))
    else:
        Augmentation.augments({"EB": 1}, coords.INPUT_MAX)
    GoldDiggers.gold_diggers(diggers)
    rb_time = Rebirth.get_rebirth_time()
    while int(rb_time.timestamp.tm_min) < duration:
        Augmentation.augments({"EB": 0.66, "CS": 0.34}, Misc.get_idle_cap(1))
        FightBoss.nuke()
        FightBoss.fight()
        GoldDiggers.gold_diggers(diggers)
        rb_time = Rebirth.get_rebirth_time()
    if not Rebirth.check_challenge() and rb_time.timestamp.tm_min >= 3:
        return
    Rebirth.do_rebirth()
    return

def level():
    """Run 100 level challenge."""
    for x in range(8):
        speedrun(3)
        if not Rebirth.check_challenge():
            return
    for x in range(5):
        speedrun(7)
        if not Rebirth.check_challenge():
            return
    for x in range(5):
        speedrun(12)
        if not Rebirth.check_challenge():
            return
    for x in range(5):
        speedrun(60)
        if not Rebirth.check_challenge():
            return
