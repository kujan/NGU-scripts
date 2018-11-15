"""3-minute rebirth script"""

# Challenges
from challenges.basic import Basic
from challenges.level import Level

# Helper classes
from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats
from classes.upgrade import Upgrade
from classes.window import Window

import ngucon as ncon
import time


def speedrun(duration, f):
    """Start a speedrun.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    f.do_rebirth()
    start = time.time()
    end = time.time() + (duration * 60)
    blood_digger_active = False
    f.fight()
    current_boss = int(feature.get_current_boss())
    while current_boss < 117:
        print(f"at boss {current_boss}, fighting {116-current_boss + 1} more times")
        feature.fight(116-current_boss + 1)
        current_boss = int(feature.get_current_boss())

    f.loadout(1)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(7)
    f.loadout(2)  # Bar/power equimpent
    f.adventure(itopod=True, itopodauto=True)
    f.time_machine(True)
    f.augments({"EB": 0.7, "CS": 0.3}, 4.5e9)

    f.blood_magic(7)
    f.boost_equipment()
    f.wandoos(True)
    f.gold_diggers([2, 5, 8, 9], True)
    s.print_exp()
    u.em()

    while time.time() < end - 15:
        f.wandoos(True)
        f.gold_diggers([2, 5, 8, 9, 11])
        if time.time() > start + 60 and not blood_digger_active:
            blood_digger_active = True
            f.gold_diggers([11], True)
        if time.time () > start + 90:
            try:
                NGU_energy = int(feature.remove_letters(feature.ocr(ncon.OCR_ENERGY_X1,ncon.OCR_ENERGY_Y1,ncon.OCR_ENERGY_X2,ncon.OCR_ENERGY_Y2)))
                feature.assign_ngu(NGU_energy, [1, 2, 4, 5, 6])
            except ValueError:
                print("couldn't assign e/m to NGUs")
            time.sleep(0.5)
    f.gold_diggers([2, 3, 5, 9, 12], True)
    f.fight()
    f.pit()
    f.spin()
    f.speedrun_bloodpill()
    while time.time() < end:
        time.sleep(0.1)

    return


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()
c = Challenge()
Window.x, Window.y = i.pixel_search("212429", 0, 0, 400, 600)
nav.menu("inventory")
s = Stats()
u = Upgrade(37500, 37500, 4, 4, 10)

print(w.x, w.y)
#u.em()
#print(c.check_challenge())


#feature.bb_ngu(4e8, [1, 2, 3, 4, 5, 6, 7, 8, 9], 1.05)
#feature.speedrun_bloodpill()
while True:  # main loop
    feature.boost_equipment()
    feature.ygg()
    feature.snipe(0, 180, bosses=False)

    #time.sleep(120)
    #c.start_challenge(3)
    #speedrun(3, feature)
