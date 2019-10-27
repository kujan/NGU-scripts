"""Contains functions for running a no time machine challenge."""
from classes.features import FightBoss, Adventure, MoneyPit
from classes.features import Wandoos, Augmentation, Rebirth, Misc, BloodMagic
from classes.inputs   import Inputs

import coordinates as coords
import time


class Timemachine:
    """Contains functions for running a no time machine challenge.

    This script requires you to have a number high enough to do a normal
    3 minute rebirth.
    """
    buster_assigned = False
    final_aug = False

    @staticmethod
    def first_rebirth(duration):
        """Procedure for first rebirth."""
        ss_assigned = False
        adventure_pushed = False

        FightBoss.nuke()
        Adventure.adventure(highest=True)
        while Inputs.check_pixel_color(*coords.COLOR_TM_LOCKED):
            if not ss_assigned:
                time.sleep(1)
                Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
                ss_assigned = True
            Wandoos.wandoos(True)
            if Wandoos.check_wandoos_bb_status():
                Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
            FightBoss.nuke()
            time.sleep(2)
            FightBoss.fight()
        if ss_assigned:
            Misc.reclaim_aug()
        Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))

        while Inputs.check_pixel_color(*coords.COLOR_BM_LOCKED):
            Wandoos.wandoos(True)
            if Wandoos.check_wandoos_bb_status():
                Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
            FightBoss.nuke()
            FightBoss.fight()
        BloodMagic.toggle_auto_spells(drop=False, gold=False)
        BloodMagic.blood_magic(8)
        rb_time = Rebirth.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < duration:
            Wandoos.wandoos(True)
            FightBoss.nuke()
            FightBoss.fight()
            time.sleep(2)
            try:
                current_boss = int(FightBoss.get_current_boss())
                if current_boss > 28 and current_boss < 49:
                    if not Timemachine.buster_assigned:
                        Misc.reclaim_aug()
                        Timemachine.buster_assigned = True
                    Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))

                elif current_boss >= 49:
                    if not Timemachine.final_aug:
                        Misc.reclaim_aug()
                        Timemachine.final_aug = True
                        time.sleep(1)
                    Augmentation.augments({"EB": 0.66, "CS": 0.34}, Misc.get_idle_cap(1))
                if current_boss > 58 and not adventure_pushed:
                    Adventure.adventure(highest=True)
                    adventure_pushed = True
            except ValueError:
                print("couldn't get current boss")
            rb_time = Rebirth.get_rebirth_time()

    @staticmethod
    def speedrun(duration):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        Rebirth.do_rebirth()
        FightBoss.nuke()
        time.sleep(2)
        Adventure.adventure(highest=True)

        try:
            current_boss = int(FightBoss.get_current_boss())
            if current_boss > 28 and current_boss < 49:
                Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
            elif current_boss >= 49:
                Augmentation.augments({"EB": 0.66, "CS": 0.34}, Misc.get_idle_cap(1))
        except ValueError:
            print("couldn't get current boss")

        while Inputs.check_pixel_color(*coords.COLOR_TM_LOCKED):
            FightBoss.nuke()
            FightBoss.fight()
            Wandoos.wandoos(True)

        while Inputs.check_pixel_color(*coords.COLOR_BM_LOCKED):
            Wandoos.wandoos(True)
            FightBoss.nuke()
            time.sleep(2)
            FightBoss.fight()

        BloodMagic.blood_magic(8)
        Wandoos.wandoos(True)
        rb_time = Rebirth.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < duration:
            FightBoss.nuke()
            FightBoss.fight()
            Adventure.adventure(highest=True)
            Wandoos.wandoos(True)
            if Wandoos.check_wandoos_bb_status():
                Augmentation.augments({"EB": 0.66, "CS": 0.34}, Misc.get_idle_cap(1))
            """If current rebirth is scheduled for more than 3 minutes and
            we already finished the rebirth, we will return here, instead
            of waiting for the duration. Since we cannot start a new
            challenge if less than 3 minutes have passed, we must always
            wait at least 3 minutes."""
            rb_time = Rebirth.get_rebirth_time()
            if duration > 3:
                if not Rebirth.check_challenge():
                    while int(rb_time.timestamp.tm_min) < 3:
                        rb_time = Rebirth.get_rebirth_time()
                        time.sleep(1)
                    MoneyPit.pit()
                    MoneyPit.spin()
                    return

        MoneyPit.pit()
        MoneyPit.spin()
        return

    @staticmethod
    def start():
        """Defeat target boss."""
        Wandoos.set_wandoos(0)
        Timemachine.first_rebirth(3)
        if not Rebirth.check_challenge():
            return
        for x in range(8):
            Timemachine.speedrun(3)
            if not Rebirth.check_challenge():
                return
        for x in range(5):
            Timemachine.speedrun(7)
            if not Rebirth.check_challenge():
                return
        for x in range(5):
            Timemachine.speedrun(12)
            if not Rebirth.check_challenge():
                return
        for x in range(5):
            Timemachine.speedrun(60)
            if not Rebirth.check_challenge():
                return
        return
