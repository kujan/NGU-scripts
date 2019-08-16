"""Contains functions for running a 100 level challenge."""
from classes.features import Features
import coordinates as coords
import time

class Blind(Features):
    """Contains functions for running a 100 level challenge.

    IMPORTANT

    Set target level for energy buster to 67 and charge shot to 33.
    Disable "Advance Energy" in augments
    Disable beards if you cap ultra fast.

    """
    def speedrun(self, duration):
        """Procedure for first rebirth in a 100LC."""
        self.advanced_training_locked = True
        self.bm_locked = True
        self.tm_locked = True
        tm_assigned = False
        bm_assigned = False
        end = time.time() + duration * 60 + 10
        self.nuke()
        time.sleep(2)
        self.fight()
        diggers = [2, 3, 11, 12]
        self.adventure(highest=True)
        self.augments({"SS": 1}, 1e12)
        self.gold_diggers(diggers)
        while time.time() < end:
            self.augments({"EB": 0.66, "CS": 0.34}, 1e13)
            self.wandoos(True)
            self.nuke()
            self.fight()
            self.gold_diggers(diggers)
            self.update_gamestate()
            if not self.tm_locked and not tm_assigned:
                self.time_machine(1e13, m=1e13)
                tm_assigned = True
            if not self.bm_locked and not bm_assigned:
                self.blood_magic(8)
                bm_assigned = True
            if not self.check_challenge() and end - time.time() > 180:
                return
        if not self.check_challenge():
            return
        self.do_rebirth()
        return

    def update_gamestate(self):
        """Update relevant state information."""

        if self.advanced_training_locked:
            self.advanced_training_locked = self.check_pixel_color(*coords.COLOR_ADV_TRAINING_LOCKED)
        if self.bm_locked:
            self.bm_locked = self.check_pixel_color(*coords.COLOR_BM_LOCKED)
        if self.tm_locked:
            self.tm_locked = self.check_pixel_color(*coords.COLOR_TM_LOCKED)

    def start(self):
        """Handle LC run."""
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
