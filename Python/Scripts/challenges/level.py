"""Contains functions for running a 100 level challenge."""
from classes.features import Features
import coordinates as coords
import time

class Level(Features):
    """Contains functions for running a 100 level challenge.

    IMPORTANT

    Set target level for energy buster to 67 and charge shot to 33.
    Disable "Advance Energy" in augments
    Disable beards if you cap ultra fast.

    """
    def speedrun(self, duration):
        """Procedure for first rebirth in a 100LC."""
        self.nuke()
        time.sleep(2)
        self.fight()
        diggers = [2, 3, 11, 12]
        self.adventure(highest=True)
        current_boss = int(self.get_current_boss())
        if current_boss > 48:
            self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap())
        else:
            self.augments({"EB": 1}, coords.INPUT_MAX)
        self.gold_diggers(diggers)
        rb_time = self.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < duration:
            self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap())
            self.nuke()
            self.fight()
            self.gold_diggers(diggers)
            rb_time = self.get_rebirth_time()
        self.do_rebirth()
        return

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
