"""Contains functions for running a 100 level challenge."""
from classes.features import FightBoss, Adventure, Augmentation, GoldDiggers
from classes.features import Wandoos, TimeMachine, BloodMagic, Rebirth
from classes.inputs   import Inputs

import coordinates as coords
import time

class Blind:
    """Contains functions for running a blind challenge.
    """
    advanced_training_locked = True
    bm_locked = True
    tm_locked = True

    @staticmethod
    def run(duration):
        """Procedure for Blind Challenge RBs."""
        Blind.advanced_training_locked = True
        Blind.bm_locked = True
        Blind.tm_locked = True

        tm_assigned = False
        bm_assigned = False

        end = time.time() + duration * 60 + 10
        FightBoss.nuke()
        time.sleep(2)
        FightBoss.fight()
        diggers = [2, 3, 11, 12]
        Adventure.adventure(highest=True)
        Augmentation.augments({"SS": 1}, 1e12)
        GoldDiggers.gold_diggers(diggers)
        while time.time() < end:
            Augmentation.augments({"EB": 0.66, "CS": 0.34}, 1e13)
            Wandoos.wandoos(True)
            FightBoss.nuke()
            FightBoss.fight()
            GoldDiggers.gold_diggers(diggers)
            Blind.update_gamestate()
            if not Blind.tm_locked and not tm_assigned:
                TimeMachine.time_machine(1e13, m=1e13)
                tm_assigned = True
            if not Blind.bm_locked and not bm_assigned:
                BloodMagic.blood_magic(8)
                bm_assigned = True
            if not Rebirth.check_challenge() and end - time.time() > 180:
                return
        if not Rebirth.check_challenge():
            return
        Rebirth.do_rebirth()
        return

    @staticmethod
    def update_gamestate():
        """Update relevant state information."""
        if Blind.advanced_training_locked:
            Blind.advanced_training_locked = Inputs.check_pixel_color(*coords.COLOR_ADV_TRAINING_LOCKED)
        if Blind.bm_locked:
            Blind.bm_locked = Inputs.check_pixel_color(*coords.COLOR_BM_LOCKED)
        if Blind.tm_locked:
            Blind.tm_locked = Inputs.check_pixel_color(*coords.COLOR_TM_LOCKED)

    @staticmethod
    def start():
        """Handle Blind Challenge run."""
        for x in range(8):
            Blind.run(3)
            if not Rebirth.check_challenge():
                return
        for x in range(5):
            Blind.run(7)
            if not Rebirth.check_challenge():
                return
        for x in range(5):
            Blind.run(12)
            if not Rebirth.check_challenge():
                return
        for x in range(5):
            Blind.run(60)
            if not Rebirth.check_challenge():
                return
