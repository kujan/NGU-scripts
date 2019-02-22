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
        tm_unlocked = False
        bm_unlocked = False
        ci_assigned = False
        diggers = [2, 3, 8]
        self.loadout(1)
        self.nuke()
        time.sleep(2)
        self.fight()
        self.adventure(highest=True)
        while self.check_pixel_color(*coords.COLOR_TM_LOCKED):
            if not ci_assigned:
                time.sleep(1)
                self.augments({"CI": 1}, 1e9)
                ci_assigned = True
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()

        self.time_machine(1e9, magic=True)
        self.loadout(2)

        time.sleep(15)
        self.augments({"CI": 1}, 1e8)
        self.gold_diggers(diggers)
        self.adventure(highest=True)
        time.sleep(4)
        self.adventure(itopod=True, itopodauto=True)
        while self.check_pixel_color(*coords.COLOR_BM_LOCKED) or self.check_pixel_color(*coords.COLOR_BM_LOCKED_ALT):
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(5)

        self.menu("bloodmagic")
        time.sleep(0.2)
        self.blood_magic(8)
        bm_unlocked = True
        self.augments({"SS": 0.7, "DS": 0.3}, 5e8)
        final_aug = False

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
