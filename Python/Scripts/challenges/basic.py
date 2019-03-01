"""Contains functions for running a basic challenge."""
from classes.features import Features
import coordinates as coords
import usersettings as userset
import time

class Basic(Features):
    """Contains functions for running a basic challenge."""
    final_aug = False
    def first_rebirth(self):
        """Procedure for first rebirth."""
        end = time.time() + 3 * 60
        ss_assigned = False
        diggers = [x for x in range(1, 13)]
        self.nuke()
        time.sleep(2)
        self.fight()
        self.adventure(highest=True)
        while self.check_pixel_color(*coords.COLOR_TM_LOCKED):
            if not ss_assigned:
                time.sleep(1)
                self.augments({"SS": 1}, 3e12)
                ss_assigned = True
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()

        self.time_machine(1e9, magic=True)
        self.augments({"DS": 1}, 1e12)
        self.gold_diggers(diggers)
        self.adventure(itopod=True, itopodauto=True)

        while self.check_pixel_color(*coords.COLOR_BM_LOCKED) or self.check_pixel_color(*coords.COLOR_BM_LOCKED_ALT):
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()
            self.gold_diggers(diggers)
        self.blood_magic(8)
        while self.check_challenge():
            self.wandoos(True)
            self.nuke()
            self.fight()
            time.sleep(2)
            try:
                current_boss = int(self.get_current_boss())
                if current_boss > 36 and current_boss <= 45:
                    self.augments({"SS": 0.66, "DS": 0.33}, self.get_idle_cap())
                elif current_boss > 45:
                    if not self.final_aug:
                        self.reclaim_aug()
                        self.final_aug = True
                        time.sleep(1)
                    self.augments({"SM": 0.66, "AA": 0.33}, self.get_idle_cap())
            except ValueError:
                print("couldn't get current boss")
            self.gold_diggers(diggers)

    def speedrun(self, duration, target):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        self.do_rebirth()
        diggers = [x for x in range(1, 13)]
        start = time.time()
        end = time.time() + (duration * 60)
        self.nuke()
        time.sleep(2)
        self.adventure(highest=True)
        time.sleep(4)
        self.adventure(itopod=True, itopodauto=True)
        self.augments({"SS": 0.7, "DS": 0.3}, self.get_idle_cap())
        self.blood_magic(8)
        self.wandoos(True)
        self.gold_diggers(diggers)

        while time.time() < end - 10:
            self.wandoos(True)
            self.gold_diggers(diggers)
            self.nuke()

        self.pit()
        self.spin()
        #tracker.adjustxp()
        while self.check_challenge():
            self.nuke()
            self.fight()
            try:
                """If current rebirth is scheduled for more than 3 minutes and
                we already finished the rebirth, we will return here, instead
                of waiting for the duration. Since we cannot start a new
                challenge if less than 3 minutes have passed, we must always
                wait at least 3 minutes."""

                current_boss = int(self.get_current_boss())
                if duration > 3 and current_boss > target:
                    if not self.check_challenge():
                        while time.time() < start + 180:
                            time.sleep(1)
                        return
                if current_boss < 101:
                    self.fight()

            except ValueError:
                print("OCR couldn't find current boss")
        return

    def basic(self, target):
        """Defeat target boss."""
        self.first_rebirth()
        """
        for x in range(8):
            self.speedrun(3, target)
            if not self.check_challenge():
                return
        for x in range(5):
            self.speedrun(7, target)
            if not self.check_challenge():
                return
        for x in range(5):
            self.speedrun(12, target)
            if not self.check_challenge():
                return
        for x in range(5):
            self.speedrun(60, target)
            if not self.check_challenge():
                return
        return
        """