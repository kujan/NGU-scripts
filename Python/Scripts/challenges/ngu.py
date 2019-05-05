"""Contains functions for running a no time machine challenge."""
from classes.features import Features
from classes.inputs import Inputs
import coordinates as coords
import time


class Ngu(Features, Inputs):
    """Contains functions for running a no NGU challenge."""
    def first_rebirth(self, duration):
        """Procedure for first rebirth."""
        adv_training_assigned = False
        self.current_boss = 1
        self.minutes_elapsed = 0
        self.advanced_training_locked = True
        self.bm_locked = True
        self.tm_locked = True
        while self.current_boss < 18 and self.minutes_elapsed < duration:
            self.wandoos(True)
            self.fight()
            self.update_gamestate()
            if not self.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                self.advanced_training(4e11)
        self.adventure(highest=True)
        while self.minutes_elapsed < duration:
            self.wandoos(True)
            self.augments({"SS": 1}, self.get_idle_cap())
            self.update_gamestate()


    def speedrun(self, duration):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        diggers = [2, 3, 11, 12]
        adv_training_assigned = False
        self.do_rebirth()
        self.wandoos(True)
        self.nuke()
        time.sleep(2)
        self.fight()
        self.adventure(highest=True)
        self.current_boss = 1
        self.minutes_elapsed = 0
        self.advanced_training_locked = True
        self.bm_locked = True
        self.tm_locked = True
        self.update_gamestate()

        while self.current_boss < 18 and self.minutes_elapsed < duration:  # augs unlocks after 17
            self.wandoos(True)
            self.augments({"SS": 1}, self.get_idle_cap())
            self.nuke()
            self.fight()
            if not self.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                self.reclaim_aug()
                self.advanced_training(4e11)
                self.augments({"SS": 1}, self.get_idle_cap())
                adv_training_assigned = True
            self.update_gamestate()
        self.adventure(highest=True)

        while self.current_boss < 29 and self.minutes_elapsed < duration:  # buster unlocks after 28
            self.wandoos(True)
            self.nuke()
            self.fight()
            if not self.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                self.reclaim_aug()
                self.advanced_training(4e11)
                self.augments({"SS": 1}, self.get_idle_cap())
                adv_training_assigned = True
            self.update_gamestate()

        if self.minutes_elapsed < duration:  # only reclaim if we're not out of time
            self.reclaim_aug()

        while self.current_boss < 31 and self.minutes_elapsed < duration:  # TM unlocks after 31
            self.augments({"EB": 1}, self.get_idle_cap())
            self.wandoos(True)
            self.nuke()
            self.fight()
            if not self.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                self.reclaim_aug()
                self.advanced_training(4e11)
                self.augments({"EB": 1}, self.get_idle_cap())
                adv_training_assigned = True
            self.update_gamestate()

        if self.minutes_elapsed < duration:  # only reclaim if we're not out of time
            self.reclaim_aug()  # get some energy back for TM
            self.send_string("t")  # get all magic back from wandoos
            self.time_machine(self.get_idle_cap() * 0.05, m=self.get_idle_cap(True) * 0.05)

        while self.current_boss < 38 and self.minutes_elapsed < duration:  # BM unlocks after 37
            self.gold_diggers(diggers)
            self.augments({"EB": 1}, self.get_idle_cap())
            self.wandoos(True)
            self.nuke()
            self.fight()
            if not self.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                self.reclaim_aug()
                self.advanced_training(4e11)
                self.augments({"EB": 1}, self.get_idle_cap())
                adv_training_assigned = True
            self.update_gamestate()

        if self.minutes_elapsed < duration:
            self.blood_magic(8)
            self.toggle_auto_spells(drop=False)
            time.sleep(10)
            print("waiting 10 seconds for gold ritual")
            self.toggle_auto_spells(drop=False, gold=False)

        while self.current_boss < 49 and self.minutes_elapsed < duration:
            self.gold_diggers(diggers)
            self.wandoos(True)
            self.augments({"EB": 1}, self.get_idle_cap())
            self.nuke()
            self.fight()
            if not self.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                self.reclaim_aug()
                self.advanced_training(4e11)
                self.augments({"EB": 1}, self.get_idle_cap())
                adv_training_assigned = True
            self.update_gamestate()
        if self.minutes_elapsed < duration:  # only reclaim if we're not out of time
            self.reclaim_aug()

        while self.minutes_elapsed < duration:
            self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap())
            self.gold_diggers(diggers)
            self.wandoos(True)
            self.nuke()
            self.fight()
            if not self.advanced_training_locked and not adv_training_assigned:
                print("assigning adv")
                self.reclaim_aug()
                self.advanced_training(4e11)
                self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap())
                adv_training_assigned = True
            self.update_gamestate()
            if not self.check_challenge() and self.minutes_elapsed >= 3:
                return
 
        return

    def update_gamestate(self):
        """Update relevant state information."""
        rb_time = self.get_rebirth_time()
        self.minutes_elapsed = int(rb_time.timestamp.tm_min)
        try:
            self.current_boss = int(self.get_current_boss())
        except ValueError:
            self.current_boss = 1
            print("couldn't get current boss")

        if self.advanced_training_locked:
            self.advanced_training_locked = self.check_pixel_color(*coords.COLOR_ADV_TRAINING_LOCKED)
        if self.bm_locked:
            self.bm_locked = self.check_pixel_color(*coords.COLOR_BM_LOCKED)
        if self.tm_locked:
            self.tm_locked = self.check_pixel_color(*coords.COLOR_TM_LOCKED)

    def start(self):
        """Defeat target boss."""
        self.set_wandoos(0)
        self.first_rebirth(15)
        if not self.check_challenge():
            return
        for x in range(8):
            self.speedrun(30)
            if not self.check_challenge():
                return
        while True:
            self.speedrun(60)
            if not self.check_challenge():
                return
        return