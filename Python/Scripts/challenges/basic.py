"""Contains functions for running a basic challenge."""
from classes.challenge import Challenge
from classes.features import Features
import ngucon as ncon
import time


class Basic(Challenge, Features):
    """Contains functions for running a basic challenge."""

    def first_rebirth(self):
        """Procedure for first rebirth after number reset."""
        end = time.time() + 3 * 60
        tm_unlocked = False
        bm_unlocked = False
        ci_assigned = False
        diggers = [2, 3, 8]
        self.loadout(1)
        self.fight()
        self.adventure(highest=True)
        while not tm_unlocked:
            if not ci_assigned:
                time.sleep(1)
                self.augments({"CI": 1}, 1e6)
                ci_assigned = True
            self.wandoos(True)
            self.fight()

            tm_color = self.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
            if tm_color != ncon.TMLOCKEDCOLOR:
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
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(5)

            bm_color = self.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
            if bm_color != ncon.BMLOCKEDCOLOR:
                self.menu("bloodmagic")
                time.sleep(0.2)
                self.send_string("t")
                self.send_string("r")
                self.blood_magic(5)
                bm_unlocked = True
                self.augments({"SS": 0.7, "DS": 0.3}, 5e8)

        while time.time() < end:
            self.wandoos(True)
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
        magic_assigned = False
        do_tm = True
        augments_assigned = False
        self.fight()
        self.loadout(1)  # Gold drop equipment
        self.adventure(0, True, False, False)
        time.sleep(3)
        self.loadout(2)  # Bar/power equimpent
        self.adventure(zone=0, highest=False, itopod=True, itopodauto=True)
        while time.time() < end - 15:
            bm_color = self.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
            tm_color = self.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
            # Do TM while waiting for magic cap
            if not magic_assigned and tm_color != ncon.TMLOCKEDCOLOR:
                self.time_machine(True)
            # If magic is assigned, continue adding energy to TM
            elif do_tm and tm_color != ncon.TMLOCKEDCOLOR:
                self.time_machine()
            else:
                self.wandoos(True)
            # Assign augments when energy caps
            if time.time() > end - (duration * 0.75 * 60):
                if do_tm and not augments_assigned:
                    self.send_string("r")
                    self.augments({"SM": 0.7, "AA": 0.3}, 8e8)
                    self.gold_diggers([2, 8, 9], True)
                    do_tm = False
                    augments_assigned = True
                    self.send_string("t")
                    self.wandoos(True)
                    self.boost_equipment()
            # Reassign magic from TM into BM after half the duration
            if (bm_color != ncon.BMLOCKEDCOLOR and not magic_assigned and
               time.time() > end - (duration * 0.75 * 60)):
                self.menu("bloodmagic")
                time.sleep(0.2)
                self.send_string("t")
                self.blood_magic(7)
                magic_assigned = True
                self.wandoos(True)
            # Assign leftovers into wandoos
            if augments_assigned:
                self.wandoos(True)
                self.gold_diggers([2, 8, 9])
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

        self.gold_diggers([3], True)
        self.fight()
        self.pit()
        self.spin()
        time.sleep(7)
        self.speedrun_bloodpill()
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
