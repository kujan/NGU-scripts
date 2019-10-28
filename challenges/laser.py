"""Contains functions for running a basic challenge."""
from classes.features import FightBoss, Wandoos, Adventure, TimeMachine, Misc
from classes.features import GoldDiggers, BloodMagic, Augmentation, Rebirth

import time


class Laser:
    """Contains functions for running a basic challenge.

    This script requires you to have a number high enough to do a normal
    3 minute rebirth.
    """

    @staticmethod
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
        Wandoos.wandoos(True)
        BloodMagic.blood_magic(8)
        while Rebirth.check_challenge():
            FightBoss.nuke()
            Augmentation.augments({"LS": 0.92, "QSL": 0.08}, Misc.get_idle_cap(1))
            GoldDiggers.gold_diggers(diggers)

        rb_time = Rebirth.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < 3:
            rb_time = Rebirth.get_rebirth_time()
            time.sleep(1)
    
    @staticmethod
    def start():
        """Defeat target boss."""
        Laser.speedrun()
