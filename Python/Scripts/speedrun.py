"""24-hour rebirth script"""

# Challenges
from challenges.basic import Basic
from challenges.level import Level

# Helper classes
from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, EstimateRate, Tracker
from classes.upgrade import UpgradeEM
from classes.window import Window

import coordinates as coords
import time


def speedrun(duration, f):
    """Start a speedrun.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    time.sleep(1)
    rt = f.rt_to_seconds()
    end = (duration * 60) + 1

    if rt > end:
        f.do_rebirth()
        time.sleep(1)
        rt = f.rt_to_seconds()
    itopod_advance = False
    f.nuke()
    f.loadout(3)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(4)
    f.loadout(4)  # Bar/power equimpent
    f.adventure(itopod=True, itopodauto=True)
    f.time_machine(1e8, magic=True)
    f.augments({"AE": 0.7, "ES": 0.3}, 1.8e10)

    f.blood_magic(8)
    f.boost_equipment()
    f.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    f.augments({"AE": 0.7, "ES": 0.3}, 1.5e10)
    f.wandoos(True)

    while rt < end - 20:
        f.wandoos(True)
        f.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

        if rt > 40:
            try:
                f.assign_ngu(f.get_idle_cap(2), [x for x in range(1, 10)])
                f.cap_ngu([x for x in range(1, 10)])
                f.assign_ngu(f.get_idle_cap(1), [x for x in range(1, 8)], True)
                f.cap_ngu([x for x in range(1, 8)], True)
                if r3unlocked:
                    f.hacks(list(range(1, 16)), f.get_idle_cap(3))
            except ValueError:
                print("couldn't assign e/m to NGUs")
            time.sleep(0.5)
        if rt > 90 and not itopod_advance:
            f.adventure(itopod=True, itopodauto=True)
            itopod_advance = True
        rt = f.rt = f.rt_to_seconds()

    f.nuke()
    time.sleep(2)
    f.fight()
    f.pit()
    f.spin()
    f.save_check()
    tracker.progress()
    u.buy()
    tracker.adjustxp()

    while f.get_rebirth_time_in_seconds() < end:
        time.sleep(0.1)
    return


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")

u = UpgradeEM(37500, 37500, 2, 2, 3)
r3unlocked = False

print(f"Top left found at: {w.x}, {w.y}")

tracker = Tracker(3)

while True:  # main loop
    speedrun(3, feature)
    tracker.progress()
