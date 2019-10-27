"""Contains functions for running a no augments challenge."""
from classes.features import FightBoss, Adventure, Wandoos, BloodMagic
from classes.features import GoldDiggers, TimeMachine, Misc, Rebirth
from classes.inputs   import Inputs

import coordinates as coords
import time


class Augment:
    """Contains functions for running a no augments challenge."""
    
    @staticmethod
    def normal_rebirth(duration):
        """Procedure for first rebirth."""
        diggers = [2, 3, 11, 12]  # Wandoos, stat, blood, exp
        FightBoss.nuke()
        time.sleep(2)
        FightBoss.fight()
        Adventure.adventure(highest=True)
        Wandoos.set_wandoos(1)  # wandoos Meh, use 0 for 98
        BloodMagic.toggle_auto_spells(drop=False)
        GoldDiggers.gold_diggers(diggers)
        while Inputs.check_pixel_color(*coords.COLOR_TM_LOCKED):
            Wandoos.wandoos(True)
            FightBoss.nuke()
            time.sleep(2)
            FightBoss.fight()

        TimeMachine.time_machine(Misc.get_idle_cap(1) * 0.1, magic=True)
        Adventure.adventure(itopod=True, itopodauto=True)

        while Inputs.check_pixel_color(*coords.COLOR_BM_LOCKED):
            Wandoos.wandoos(True)
            FightBoss.nuke()
            time.sleep(2)
            FightBoss.fight()
            GoldDiggers.gold_diggers(diggers)
        BloodMagic.blood_magic(8)
        rb_time = Rebirth.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < duration:
            Wandoos.wandoos(True)
            FightBoss.nuke()
            FightBoss.fight()
            time.sleep(2)
            GoldDiggers.gold_diggers(diggers)
            rb_time = Rebirth.get_rebirth_time()
            # return if challenge is completed and rebirth time is above 3 minutes
            if int(rb_time.timestamp.tm_min) >= 3 and not Rebirth.check_challenge():
                return

        Rebirth.do_rebirth()
    
    @staticmethod
    def start():
        """Challenge rebirth sequence.

        If you wish to edit the length or sequence of the rebirths; change the for-loop values
        and durations in the Augment.normal_rebirth(duration) calls."""

        for x in range(8):  # runs 3-minute rebirth 8 times, if we still aren't done move to 7 min
            Augment.normal_rebirth(3)  # start a run with a 3 minute duration
            if not Rebirth.check_challenge(): return
        for x in range(5):
            Augment.normal_rebirth(7)
            if not Rebirth.check_challenge(): return
        for x in range(5):
            Augment.normal_rebirth(12)
            if not Rebirth.check_challenge(): return
        for x in range(5):
            Augment.normal_rebirth(60)
            if not Rebirth.check_challenge(): return
        return
