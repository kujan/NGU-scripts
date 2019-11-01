"""Contains functions for running a 100 level challenge."""
from classes.features import FightBoss, Adventure, Augmentation, GoldDiggers, Rebirth, Misc

import coordinates as coords
import time

class Level:
    """Contains functions for running a 100 level challenge.

    IMPORTANT

    Set target level for energy buster to 67 and charge shot to 33.
    Disable "Advance Energy" in augments
    Disable beards if you cap ultra fast.

    """

    @staticmethod
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

    @staticmethod
    def start():
        """Handle LC run."""
        for x in range(8):
            Level.speedrun(3)
            if not Rebirth.check_challenge():
                return
        for x in range(5):
            Level.speedrun(7)
            if not Rebirth.check_challenge():
                return
        for x in range(5):
            Level.speedrun(12)
            if not Rebirth.check_challenge():
                return
        for x in range(5):
            Level.speedrun(60)
            if not Rebirth.check_challenge():
                return
