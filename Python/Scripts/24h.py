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
from classes.upgrade import UpgradeEM
from classes.window import Window

import coordinates as coords
import datetime
import time

def start_procedure(f, rt):
    f.send_string("r") # make sure we reset e/m if we run this mid-rebirth
    f.send_string("t")
    f.nuke(101)
    time.sleep(3)
    f.loadout(2) # respawn
    f.adventure(highest=True)
    time.sleep(4)
    f.time_machine(5e11, magic=True)
    f.augments({"CI": 0.7, "ML": 0.3}, 5e11)
    f.blood_magic(8)
    f.gold_diggers([x for x in range(1, 13)])

    if rt.timestamp.tm_hour > 0 or rt.timestamp.tm_min >= 13:
        print("assigning adv training")
    else:
        end = time.time() + (12.5 - rt.timestamp.tm_min) * 60
        print("doing itopod while waiting for adv training to activate")
        f.itopod_snipe(int(end - time.time()))

    f.advanced_training(2e12)

    if rt.timestamp.tm_hour < 1:
        end = time.time() + (54 - rt.timestamp.tm_min) * 60
        print("doing itopod while waiting for wandoos to boot")
        f.itopod_snipe(int(end - time.time()))
    f.gold_diggers([[x for x in range(1, 13)]])
    f.send_string("t")
    f.menu("timemachine")
    f.click(*coords.TM_MULT)
    f.wandoos(True)
    f.assign_ngu(f.get_idle_cap(), [x for x in range(1, 10)])
    f.assign_ngu(f.get_idle_cap(True), [x for x in range(1, 8)], True)

w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")

print(w.x, w.y)

# 24 hour script

rt = feature.get_rebirth_time()
#start_procedure(feature, rt)

while True:
    rt = feature.get_rebirth_time()
    print(rt)
    feature.gold_diggers([x for x in range(1, 13)])
    feature.merge_inventory(9)
    if rt.days > 0:
        print(f"rebirthing at {rt}")
        feature.nuke()
        feature.spin()
        feature.ygg(equip=1)
        feature.save_screenshot()
        feature.do_rebirth()
        rt = feature.get_rebirth_time()
        start_procedure(feature, rt)
    else:
        feature.ygg()
        feature.save_check()
        feature.pit()
        if rt.timestamp.tm_hour <= 12: # quests for first 12 hours
            feature.boost_cube()
            feature.questing()
        else:
            feature.itopod_snipe(300)
            feature.boost_cube()
            feature.merge_inventory(9) # merge guffs