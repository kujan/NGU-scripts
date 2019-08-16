"""Contains functions for running a no rebirth challenge."""
from classes.features import Features
import coordinates as coords
import usersettings as userset
import time


class Rebirth(Features):
    """Contains functions for running a no rebirth challenge."""

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
        self.toggle_auto_spells(drop=False, number=False)
        while time.time() < end - 90:
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            try:
                current_boss = int(self.get_current_boss())
                if current_boss > 36:
                    self.augments({"SS": 0.67, "DS": 0.33}, self.get_idle_cap(1))
            except ValueError:
                print("couldn't get current boss")
            self.gold_diggers(diggers)

        while True:
            self.wandoos(True)
            self.nuke()
            time.sleep(1)
            try:
                current_boss = int(self.get_current_boss())
                if current_boss > 45:
                    if not self.final_aug:
                        self.reclaim_aug()
                        self.final_aug = True
                    self.augments({"SM": 0.67, "AA": 0.33}, self.get_idle_cap(1))
            except ValueError:
                print("couldn't get current boss")
            self.fight()
            self.gold_diggers(diggers)

            if time.time() > end and not self.check_challenge():
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
