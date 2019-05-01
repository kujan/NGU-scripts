"""Contains functions for running a basic challenge."""
from classes.features import Features
import coordinates as coords
import usersettings as userset
import time

class Basic(Features):
    """Contains functions for running a basic challenge."""
    buster_assigned = False
    final_aug = False
    def first_rebirth(self, duration):
        """Procedure for first rebirth."""
        ss_assigned = False
        diggers = [2, 3, 11, 12]
        self.nuke()
        time.sleep(2)
        self.fight()
        self.adventure(highest=True)
        while self.check_pixel_color(*coords.COLOR_TM_LOCKED):
            if not ss_assigned:
                time.sleep(1)
                self.augments({"SS": 1}, self.get_idle_cap())
                ss_assigned = True
            self.wandoos(True)
            if self.check_wandoos_bb_status():
                self.augments({"SS": 1}, self.get_idle_cap())
            self.nuke()
            time.sleep(2)
            self.fight()

        self.time_machine(self.get_idle_cap() * 0.5, magic=True)
        self.reclaim_aug()
        self.augments({"EB": 1}, self.get_idle_cap())
        self.gold_diggers(diggers)
        self.adventure(itopod=True, itopodauto=True)

        while self.check_pixel_color(*coords.COLOR_BM_LOCKED):
            self.wandoos(True)
            if self.check_wandoos_bb_status():
                self.augments({"EB": 1}, self.get_idle_cap())
            self.nuke()
            time.sleep(2)
            self.fight()
            self.gold_diggers(diggers)
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
                    self.augments({"EB": 1}, self.get_idle_cap())

                elif current_boss >= 49:
                    if not self.final_aug:
                        self.reclaim_aug()
                        self.final_aug = True
                        time.sleep(1)
                    self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap())
            except ValueError:
                print("couldn't get current boss")
            self.gold_diggers(diggers)
            rb_time = self.get_rebirth_time()

    def speedrun(self, duration):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        self.do_rebirth()
        diggers = [2, 3, 11, 12]
        self.nuke()
        time.sleep(2)
        self.adventure(highest=True)

        try:
            current_boss = int(self.get_current_boss())
            if current_boss > 28 and current_boss < 49:
                self.augments({"EB": 1}, self.get_idle_cap())
            elif current_boss >= 49:
                self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap())
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
            self.gold_diggers(diggers)
        self.blood_magic(8)
        self.wandoos(True)
        self.gold_diggers(diggers)
        self.adventure(itopod=True, itopodauto=True)
        rb_time = self.get_rebirth_time()
        while int(rb_time.timestamp.tm_min) < duration:
            self.nuke()
            self.fight()
            self.gold_diggers(diggers)
            self.wandoos(True)
            if self.check_wandoos_bb_status():
                self.augments({"EB": 0.66, "CS": 0.34}, self.get_idle_cap())
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
        self.set_wandoos(0)  # wandoos 98, use 1 for meh
        self.first_rebirth(3)

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
