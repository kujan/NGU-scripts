"""Contains functions for running a basic challenge."""
from classes.features import Features
import coordinates as ncon
import usersettings as userset
import time

class Basic(Features):
    """Contains functions for running a basic challenge."""

    def __init__(self, tracker):
        self.tracker = tracker

    def first_rebirth(self):
        """Procedure for first rebirth after number reset."""
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
        while not tm_unlocked:
            if not ci_assigned:
                time.sleep(1)
                self.augments({"CI": 1}, 1e6)
                ci_assigned = True
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()

            if not self.check_pixel_color(*ncon.COLOR_TM_LOCKED):
                self.send_string("r")
                self.send_string("t")
                self.time_machine(True)
                self.loadout(2)
                tm_unlocked = True

        time.sleep(15)
        self.augments({"CI": 1}, 1e8)
        self.gold_diggers(diggers, True)
        self.adventure(highest=True)
        time.sleep(4)
        self.adventure(itopod=True, itopodauto=True)
        while not bm_unlocked:
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(5)

            if not check_pixel_color(*ncon.COLOR_BM_LOCKED):
                self.menu("bloodmagic")
                time.sleep(0.2)
                self.send_string("t")
                self.send_string("r")
                self.blood_magic(5)
                bm_unlocked = True
                self.augments({"SS": 0.7, "DS": 0.3}, 5e8)

        while time.time() < end:
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(5)

    def speedrun(self, duration, target):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        self.do_rebirth()
        start = time.time()
        end = time.time() + (duration * 60)
        blood_digger_active = False
        self.nuke(125)
        time.sleep(2)
        self.loadout(1)  # Gold drop equipment
        self.adventure(highest=True)
        time.sleep(7)
        self.loadout(2)  # Bar/power equimpent
        self.adventure(itopod=True, itopodauto=True)
        self.time_machine(True)
        self.augments({"EB": 0.7, "CS": 0.3}, 4.5e9)

        self.blood_magic(8)
        self.boost_equipment()
        self.wandoos(True)
        self.gold_diggers([2, 5, 8, 9], True)

        while time.time() < end - 20:
            self.wandoos(True)
            self.gold_diggers([2, 5, 8, 9, 11])
            if time.time() > start + 60 and not blood_digger_active:
                blood_digger_active = True
                self.gold_diggers([11], True)
            if time.time() > start + 90:
                try:
                    NGU_energy = self.ocr_number(*ncon.OCR_ENERGY)
                    self.assign_ngu(NGU_energy, [1, 2, 4, 5, 6])
                    NGU_magic = self.ocr_number(*ncon.OCR_MAGIC)
                    self.assign_ngu(NGU_magic, [2], magic=True)
                except ValueError:
                    print("couldn't assign e/m to NGUs")
                time.sleep(0.5)
        self.gold_diggers([2, 3, 5, 9, 12], True)
        self.nuke()
        time.sleep(2)
        self.fight()
        self.pit()
        self.spin()
        self.tracker.progress()
        #tracker.adjustxp()
        while time.time() < end:
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
