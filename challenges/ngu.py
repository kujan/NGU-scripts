"""Contains functions for running a no time machine challenge."""
from classes.features import FightBoss, Wandoos, Misc, Adventure, GoldDiggers, TimeMachine
from classes.features import Augmentation, Rebirth, AdvancedTraining, BloodMagic
from classes.inputs   import Inputs

import coordinates as coords
import time


class NGU:
    """Contains functions for running a no NGU challenge."""
    current_boss = 1
    minutes_elapsed = 0
    advanced_training_locked = True
    bm_locked = True
    tm_locked = True

    @staticmethod
    def first_rebirth(duration):
        """Procedure for first rebirth."""
        adv_training_assigned = False
        NGU.current_boss = 1
        NGU.minutes_elapsed = 0
        NGU.advanced_training_locked = True
        NGU.bm_locked = True
        NGU.tm_locked = True

        while NGU.current_boss < 18 and NGU.minutes_elapsed < duration:
            Wandoos.wandoos(True)
            FightBoss.fight()
            NGU.update_gamestate()
            if not NGU.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                AdvancedTraining.advanced_training(4e11)
                adv_training_assigned = True
        Adventure.adventure(highest=True)
        while NGU.minutes_elapsed < duration:
            Wandoos.wandoos(True)
            Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
            NGU.update_gamestate()

    @staticmethod
    def speedrun(duration):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        diggers = [2, 3, 11, 12]
        adv_training_assigned = False
        Rebirth.do_rebirth()
        Wandoos.wandoos(True)
        FightBoss.nuke()
        time.sleep(2)
        FightBoss.fight()
        Adventure.adventure(highest=True)
        NGU.current_boss = 1
        NGU.minutes_elapsed = 0
        NGU.advanced_training_locked = True
        NGU.bm_locked = True
        NGU.tm_locked = True
        NGU.update_gamestate()

        while NGU.current_boss < 18 and NGU.minutes_elapsed < duration:  # augs unlocks after 17
            Wandoos.wandoos(True)
            Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
            FightBoss.nuke()
            FightBoss.fight()
            if not NGU.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                Misc.reclaim_aug()
                AdvancedTraining.advanced_training(4e11)
                Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
                adv_training_assigned = True
            NGU.update_gamestate()
        Adventure.adventure(highest=True)

        while NGU.current_boss < 29 and NGU.minutes_elapsed < duration:  # buster unlocks after 28
            Wandoos.wandoos(True)
            FightBoss.nuke()
            FightBoss.fight()
            if not NGU.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                Misc.reclaim_aug()
                AdvancedTraining.advanced_training(4e11)
                Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
                adv_training_assigned = True
            NGU.update_gamestate()

        if NGU.minutes_elapsed < duration:  # only reclaim if we're not out of time
            Misc.reclaim_aug()

        while NGU.current_boss < 31 and NGU.minutes_elapsed < duration:  # TM unlocks after 31
            Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
            Wandoos.wandoos(True)
            FightBoss.nuke()
            FightBoss.fight()
            if not NGU.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                Misc.reclaim_aug()
                AdvancedTraining.advanced_training(4e11)
                Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
                adv_training_assigned = True
            NGU.update_gamestate()

        if NGU.minutes_elapsed < duration:  # only reclaim if we're not out of time
            Misc.reclaim_aug()  # get some energy back for TM
            Misc.reclaim_res(magic=True)  # get all magic back from wandoos
            TimeMachine.time_machine(Misc.get_idle_cap(1) * 0.05, m=Misc.get_idle_cap(2) * 0.05)

        while NGU.current_boss < 38 and NGU.minutes_elapsed < duration:  # BM unlocks after 37
            GoldDiggers.gold_diggers(diggers)
            Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
            Wandoos.wandoos(True)
            FightBoss.nuke()
            FightBoss.fight()
            if not NGU.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                Misc.reclaim_aug()
                AdvancedTraining.advanced_training(4e11)
                Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
                adv_training_assigned = True
            NGU.update_gamestate()

        if NGU.minutes_elapsed < duration:
            BloodMagic.blood_magic(8)
            BloodMagic.toggle_auto_spells(drop=False)
            time.sleep(10)
            print("waiting 10 seconds for gold ritual")
            BloodMagic.toggle_auto_spells(drop=False, gold=False)

        while NGU.current_boss < 49 and NGU.minutes_elapsed < duration:
            GoldDiggers.gold_diggers(diggers)
            Wandoos.wandoos(True)
            Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
            FightBoss.nuke()
            FightBoss.fight()
            if not NGU.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                Misc.reclaim_aug()
                AdvancedTraining.advanced_training(4e11)
                Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
                adv_training_assigned = True
            NGU.update_gamestate()
        if NGU.minutes_elapsed < duration:  # only reclaim if we're not out of time
            Misc.reclaim_aug()

        while NGU.minutes_elapsed < duration:
            Augmentation.augments({"EB": 0.66, "CS": 0.34}, Misc.get_idle_cap(1))
            GoldDiggers.gold_diggers(diggers)
            Wandoos.wandoos(True)
            FightBoss.nuke()
            FightBoss.fight()
            if not NGU.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                Misc.reclaim_aug()
                AdvancedTraining.advanced_training(4e11)
                Augmentation.augments({"EB": 0.66, "CS": 0.34}, Misc.get_idle_cap(1))
                adv_training_assigned = True
            NGU.update_gamestate()
            if not Rebirth.check_challenge() and NGU.minutes_elapsed >= 3:
                return
 
        return

    @staticmethod
    def update_gamestate():
        """Update relevant state information."""
        rb_time = Rebirth.get_rebirth_time()
        NGU.minutes_elapsed = int(rb_time.timestamp.tm_min)
        try:
            NGU.current_boss = int(FightBoss.get_current_boss())
        except ValueError:
            NGU.current_boss = 1
            print("couldn't get current boss")

        if NGU.advanced_training_locked:
            NGU.advanced_training_locked = Inputs.check_pixel_color(*coords.COLOR_ADV_TRAINING_LOCKED)
        if NGU.bm_locked:
            NGU.bm_locked = Inputs.check_pixel_color(*coords.COLOR_BM_LOCKED)
        if NGU.tm_locked:
            NGU.tm_locked = Inputs.check_pixel_color(*coords.COLOR_TM_LOCKED)

    @staticmethod
    def start():
        """Defeat target boss."""
        Wandoos.set_wandoos(0)
        NGU.first_rebirth(15)
        if not Rebirth.check_challenge():
            return
        for x in range(8):
            NGU.speedrun(30)
            if not Rebirth.check_challenge():
                return
        while True:
            NGU.speedrun(60)
            if not Rebirth.check_challenge():
                return
        return