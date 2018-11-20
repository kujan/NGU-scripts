"""Contains functions for running a 100 level challenge."""
from classes.features import Features
import ngucon as ncon
import time


class Level(Features):
    """Contains functions for running a 100 level challenge.

    IMPORTANT

    If you're reusing this code - make sure to check the augments used in the
    first_lc() and speedrun_lc() functions can be used by you as well, or
    if you can use a higher augment for higher speed. Also make sure to put a
    target level on all used augments and time machine, as well as disabling
    all beards before running.
    """

    def first_lc(self):
        """Procedure for first rebirth in a 100LC."""
        start = time.time()
        end = start + 3 * 60
        tm_unlocked = False
        diggers = [3]
        self.fight()
        self.adventure(highest=True)
        try:
            current_boss = int(self.get_current_boss())
        except ValueError:
            print("error reading current boss")
            current_boss = 1

        while current_boss < 25:
            self.fight()
            time.sleep(5)
            try:
                current_boss = int(self.get_current_boss())
            except ValueError:
                print("error reading current boss")
                current_boss = 1
                if time.time() > start + 60:
                    current_boss = 25

        self.augments({"SM": 1}, 1e8)

        while not tm_unlocked:
            self.fight()

            tm_color = self.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
            if tm_color != ncon.TMLOCKEDCOLOR:
                self.time_machine(True)
                tm_unlocked = True

        time.sleep(5)
        self.augments({"EB": 1}, 1e8)
        self.gold_diggers(diggers, True)
        time.sleep(4)

        while time.time() < end + 3:
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(5)

        return

    def lc_speedrun(self):
        """Procedure for first rebirth in a 100LC."""
        self.do_rebirth()
        start = time.time()
        end = time.time() + 3 * 60
        tm_unlocked = False
        diggers = [3]
        self.fight()
        self.adventure(highest=True)
        try:
            current_boss = int(self.get_current_boss())
        except ValueError:
            print("error reading current boss")
            current_boss = 1

        while current_boss < 25:
            self.fight()
            time.sleep(5)
            try:
                current_boss = int(self.get_current_boss())
            except ValueError:
                print("error reading current boss")
                current_boss = 1
                if time.time() > start + 60:
                    current_boss = 25

        if current_boss < 29:  # EB not unlocked
            self.augments({"SM": 1}, 1e8)

        while not tm_unlocked:
            self.fight()

            tm_color = self.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
            if tm_color != ncon.TMLOCKEDCOLOR:
                self.time_machine(True)
                tm_unlocked = True

        time.sleep(5)
        for x in range(5):  # it doesn't add energy properly sometimes.
            self.augments({"EB": 1}, 1e8)

        self.gold_diggers(diggers, True)
        time.sleep(4)

        while current_boss < 38:
            self.fight()
            time.sleep(5)
            try:
                current_boss = int(self.get_current_boss())
            except ValueError:
                print("error reading current boss")
                current_boss = 1
                if time.time() > start + 180:
                    current_boss = 25

        self.menu("bloodmagic")
        time.sleep(0.2)
        self.click(ncon.BMX, ncon.BMY[3])

        while time.time() < end + 3:
            self.fight()
            self.gold_diggers(diggers)
            self.adventure(highest=True)
            time.sleep(5)

        return

    def check_challenge(self):
        """Check if a challenge is active."""
        self.rebirth()
        self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
        time.sleep(ncon.LONG_SLEEP)
        color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
                                     ncon.CHALLENGEACTIVEY)

        return True if color == ncon.CHALLENGEACTIVECOLOR else False

    def lc(self):
        """Handle LC run."""
        self.first_lc()
        while True:
            self.lc_speedrun()
            if not self.check_challenge():
                return
