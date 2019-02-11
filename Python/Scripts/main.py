"""3-minute rebirth script"""

# Challenges
from challenges.basic import Basic
from challenges.level import Level

# Helper classes
from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, EstimateRate, Tracker
from classes.upgrade import Upgrade
from classes.window import Window

import coordinates as coords
import time


def speedrun(duration, f):
    """Start a speedrun.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    f.do_rebirth()
    start = time.time()
    end = time.time() + (duration * 60) + 1
    blood_digger_active = False
    itopod_advance = False
    f.nuke(125)
    f.loadout(1)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(4)
    f.loadout(2)  # Bar/power equimpent
    f.adventure(itopod=True, itopodauto=True)
    f.time_machine(1e8, magic=True)
    f.augments({"AE": 0.7, "ES": 0.3}, 1.8e10)

    f.blood_magic(8)
    f.boost_equipment()
    f.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    f.augments({"AE": 0.7, "ES": 0.3}, 1.5e10)
    f.wandoos(True)
    while time.time() < end - 20:
        f.wandoos(True)
        f.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        if time.time () > start + 40:
            try:
                NGU_energy = f.get_idle_cap()
                feature.assign_ngu(NGU_energy, [1, 2, 4, 5, 6, 7, 8, 9])
                NGU_magic = f.get_idle_cap(magic=True)
                feature.assign_ngu(NGU_magic, [1, 2, 3, 4], magic=True)
            except ValueError:
                print("couldn't assign e/m to NGUs")
            time.sleep(0.5)
        if time.time() > start + 90 and not itopod_advance:
            f.adventure(itopod=True, itopodauto=True)
            itopod_advance = True
    f.nuke()
    time.sleep(2)
    f.fight()
    f.pit()
    f.spin()
    f.save_check()
    tracker.progress()
    u.em()
    tracker.adjustxp()
    while time.time() < end:
        time.sleep(0.1)

    return


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")

u = Upgrade(37500, 37500, 2, 2, 3)

print(w.x, w.y)

tracker = Tracker(3)
c = Challenge()

while True:  # main loop
    feature.questing()
    #feature.boost_equipment()
    #feature.ygg()
    #feature.snipe(13, 120)

    #time.sleep(120)
    #c.start_challenge(9)
    #speedrun(3, feature)
