"""Contains functions for running a laser sword challenge."""
from classes.features import FightBoss, Wandoos, Adventure, TimeMachine, Misc
from classes.features import GoldDiggers, BloodMagic, Augmentation, Rebirth

import time


def speedrun():
    """Start a speedrun.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    diggers = [2, 3, 11, 12]
    FightBoss.nuke()
    Wandoos.set_wandoos(0)
    Adventure.adventure(highest=True)
    TimeMachine.time_machine(Misc.get_idle_cap(1) * 0.01, magic=True)
    GoldDiggers.gold_diggers(diggers)
    Wandoos.wandoos(True, True)
    BloodMagic.blood_magic(8)
    while Rebirth.check_challenge():
        FightBoss.nuke()
        Augmentation.augments({"LS": 0.92, "QSL": 0.08}, Misc.get_idle_cap(1))
        GoldDiggers.gold_diggers(diggers)

    rb_time = Rebirth.get_rebirth_time()
    while int(rb_time.timestamp.tm_min) < 3:
        rb_time = Rebirth.get_rebirth_time()
        time.sleep(1)

def laser():
    """Run laser sword challenge."""
    speedrun()
