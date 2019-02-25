"""Contains functions for running a no rebirth challenge."""
from classes.features import Features
import coordinates as coords
import usersettings as userset
import time


class Rebirth(Features):
    """Contains functions for running a no rebirth challenge."""

    def first_rebirth(self):
        """Procedure for first rebirth."""
        end = time.time() + 3 * 60
        ss_assigned = False
        final_aug = False
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
        while time.time() < end + 1:
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            try:
                current_boss = int(self.get_current_boss())
                if current_boss > 36:
                    self.augments({"SS": 0.7, "DS": 0.3}, self.get_idle_cap())
            except ValueError:
                print("couldn't get current boss")
            self.gold_diggers(diggers)

        while True:
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            try:
                current_boss = int(self.get_current_boss())
                if current_boss > 56 and not final_aug:
                    self.augments({"AE": 0.7, "ES": 0.3}, 1e11)
                    final_aug = True
            except ValueError:
                print("couldn't get current boss")
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(10)

            if not self.check_challenge() and time.time() > end:
                return

    def check_challenge(self):
        """Check if a challenge is active."""
        self.rebirth()
        self.click(*coords.CHALLENGE_BUTTON)
        time.sleep(userset.LONG_SLEEP)
        return True if self.check_pixel_color(*coords.COLOR_CHALLENGE_ACTIVE) else False

    def rebirth_challenge(self):
        """Defeat target boss."""
        self.first_rebirth()
        return
