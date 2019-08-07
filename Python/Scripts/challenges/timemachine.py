"""Contains functions for running a no time machine challenge."""
from classes.features import Features
from classes.inputs import Inputs
import coordinates as coords
import time


class Timemachine(Features, Inputs):
    """Contains functions for running a no time machine challenge.

    This script requires you to have a number high enough to do a normal
    3 minute rebirth.
    """
    buster_assigned = False
    final_aug = False

    def first_rebirth(self, duration):
        """Procedure for first rebirth."""
        ss_assigned = False
        adventure_pushed = False
        self.nuke()
        self.adventure(highest=True)
        while self.check_pixel_color(*coords.COLOR_TM_LOCKED):
            if not ss_assigned:
                time.sleep(1)
                self.augments({"SS": 1}, self.get_idle_cap(1))
                ss_assigned = True
            self.wandoos(True)
            if self.check_wandoos_bb_status():
                self.augments({"SS": 1}, self.get_idle_cap(1))
            self.nuke()
            time.sleep(2)
            self.fight()
        if ss_assigned:
            self.reclaim_aug()
        self.augments({"EB": 1}, self.get_idle_cap(1))

        while self.check_pixel_color(*coords.COLOR_BM_LOCKED):
            self.wandoos(True)
            if self.check_wandoos_bb_status():
                self.augments({"EB": 1}, self.get_idle_cap(1))
            self.nuke()
            self.fight()
        self.toggle_auto_spells(drop=False, gold=False)
        self.blood_magic(8)
        rb_time = self.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < duration:
            self.wandoos(True)
            self.nuke()
            self.fight()
            time.sleep(2)
            try:
                current_boss = int(self.get_current_boss())
                if current_boss > 28 and current_boss < 49:
                    if not self.buster_assigned:
                        self.reclaim_aug()
                        self.buster_assigned = True
                    self.augments({"EB": 1}, self.get_idle_cap(1))

                elif current_boss >= 49:
                    if not self.final_aug:
                        self.reclaim_aug()
                        self.final_aug = True
                        time.sleep(1)
                    self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap(1))
                if current_boss > 58 and not adventure_pushed:
                    self.adventure(highest=True)
                    adventure_pushed = True
            except ValueError:
                print("couldn't get current boss")
            rb_time = self.get_rebirth_time()

    def speedrun(self, duration):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        self.do_rebirth()
        self.nuke()
        time.sleep(2)
        self.adventure(highest=True)

        try:
            current_boss = int(self.get_current_boss())
            if current_boss > 28 and current_boss < 49:
                self.augments({"EB": 1}, self.get_idle_cap(1))
            elif current_boss >= 49:
                self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap(1))
        except ValueError:
            print("couldn't get current boss")

        while self.check_pixel_color(*coords.COLOR_TM_LOCKED):
            self.nuke()
            self.fight()
            self.wandoos(True)

        while self.check_pixel_color(*coords.COLOR_BM_LOCKED):
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()

        self.blood_magic(8)
        self.wandoos(True)
        rb_time = self.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < duration:
            self.nuke()
            self.fight()
            self.adventure(highest=True)
            self.wandoos(True)
            if self.check_wandoos_bb_status():
                self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap(1))
            """If current rebirth is scheduled for more than 3 minutes and
            we already finished the rebirth, we will return here, instead
            of waiting for the duration. Since we cannot start a new
            challenge if less than 3 minutes have passed, we must always
            wait at least 3 minutes."""
            rb_time = self.get_rebirth_time()
            if duration > 3:
                if not self.check_challenge():
                    while int(rb_time.timestamp.tm_min) < 3:
                        rb_time = self.get_rebirth_time()
                        time.sleep(1)
                    self.pit()
                    self.spin()
                    return

        self.pit()
        self.spin()
        return

    def start(self):
        """Defeat target boss."""
        self.set_wandoos(0)
        self.first_rebirth(3)
        if not self.check_challenge():
            return
        for x in range(8):
            self.speedrun(3)
            if not self.check_challenge():
                return
        for x in range(5):
            self.speedrun(7)
            if not self.check_challenge():
                return
        for x in range(5):
            self.speedrun(12)
            if not self.check_challenge():
                return
        for x in range(5):
            self.speedrun(60)
            if not self.check_challenge():
                return
        return