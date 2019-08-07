"""Contains functions for running a basic challenge."""
from classes.features import Features
from classes.inputs import Inputs
import coordinates as coords
import time


class Laser(Features, Inputs):
    """Contains functions for running a basic challenge.

    This script requires you to have a number high enough to do a normal
    3 minute rebirth.
    """

    def speedrun(self):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        diggers = [2, 3, 11, 12]
        self.nuke()
        self.set_wandoos(0)
        self.adventure(highest=True)
        self.time_machine(self.get_idle_cap(1) * 0.01, magic=True)
        self.gold_diggers(diggers)
        self.wandoos(True)
        self.blood_magic(8)
        while self.check_challenge():
            self.nuke()
            self.augments({"LS": 0.92, "QSL": 0.08}, self.get_idle_cap(1))
            self.gold_diggers(diggers)

        rb_time = self.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < 3:
            rb_time = self.get_rebirth_time()
            time.sleep(1)

    def start(self):
        """Defeat target boss."""
        self.speedrun()
