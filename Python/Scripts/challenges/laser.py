"""Contains functions for running a basic challenge."""
from classes.features import Features
from classes.inputs import Inputs
import ngucon as ncon
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
        duration = 3
        self.do_rebirth()
        start = time.time()
        end = time.time() + (duration * 60)
        blood_digger_active = False
        self.fight(116)
        current_boss = int(self.get_current_boss())
        while current_boss < 117:
            print(f"at boss {current_boss}, fighting {116-current_boss + 1} more times")
            self.fight(116-current_boss + 1)
            current_boss = int(self.get_current_boss())

        self.loadout(1)  # Gold drop equipment
        self.adventure(highest=True)
        time.sleep(7)
        self.loadout(2)  # Bar/power equimpent
        self.adventure(itopod=True, itopodauto=True)
        self.time_machine(True)
        self.augments({"EB": 0.7, "CS": 0.3}, 3.5e9)

        self.blood_magic(7)
        self.boost_equipment()
        self.wandoos(True)
        self.gold_diggers([2, 8, 9], True)


        while time.time() < end - 45:
            self.wandoos(True)
            self.gold_diggers([2, 8, 9, 11])
            if time.time() > start + 80 and not blood_digger_active:
                blood_digger_active = True
                self.gold_diggers([11], True)
            time.sleep(0.5)

        self.send_string("r")
        self.augments({"LS": 0.9, "QSL": 0.1}, 6.5e9)

        while self.check_challenge():
            time.sleep(5)

        self.gold_diggers([2, 3, 12], True)
        self.fight()
        self.pit()

        while time.time() < end:
            time.sleep(0.1)

        return

    def check_challenge(self):
        """Check if a challenge is active."""
        self.rebirth()
        self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
        time.sleep(ncon.LONG_SLEEP)
        color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
                                     ncon.CHALLENGEACTIVEY)

        return True if color == ncon.CHALLENGEACTIVECOLOR else False

    def laser(self):
        """Defeat target boss."""
        self.speedrun()
