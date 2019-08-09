"""Guffin script."""

# Helper classes
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window

import coordinates as coords
import datetime
import time


def speedrun(f):
    """Procedure that handles start of rebirth."""
    end = time.time() + 30 * 60
    rt = f.get_rebirth_time()
    toggle_number = False
    f.nuke()  # PPP
    time.sleep(2)
    f.loadout(7)  # gold
    f.adventure(highest=True)
    f.toggle_auto_spells(number=False, drop=False)
    f.gold_diggers([x for x in range(1, 13)])
    f.blood_magic(8)
    f.set_ngu_overcap(102)
    if feature.check_pixel_color(*coords.NGU_EVIL):
        f.click(778, 122)
    f.cap_ngu()
    f.cap_ngu(magic=True)
    f.set_wandoos(0)
    f.wandoos(True)
    f.augments({"CI": 0.66, "ML": 0.34}, f.get_idle_cap(1) * 0.5)
    f.time_machine(coords.INPUT_MAX, magic=True)
    f.loadout(3)

    while rt.timestamp.tm_hour < 1 and rt.timestamp.tm_min < 13:
        if rt.timestamp.tm_min > 1 and not toggle_number:
            f.toggle_auto_spells(drop=False, gold=False)
            toggle_number = True
        text = f.get_quest_text()
        majors = f.get_available_majors()
        if majors == 0 and (coords.QUESTING_MINOR_QUEST in text.lower() or coords.QUESTING_NO_QUEST_ACTIVE in text.lower()):
            f.questing(duration=2, force=3)
        else:
            if not f.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                f.click(*coords.QUESTING_USE_MAJOR)
            f.questing(duration=2)
        f.nuke()
        f.gold_diggers([x for x in range(1, 13)])
        f.time_machine(coords.INPUT_MAX, magic=True)
        f.augments({"CI": 0.66, "ML": 0.34}, f.get_idle_cap(1) * 0.5)
        f.time_machine(coords.INPUT_MAX, magic=True)
        rt = f.get_rebirth_time()

    f.adventure(highest=True)
    f.reclaim_tm(True)
    f.reclaim_aug()
    f.advanced_training(2e12)
    f.set_wandoos(1)
    f.wandoos(True)
    f.augments({"CI": 0.66, "ML": 0.34}, f.get_idle_cap(1) * 0.5)
    f.time_machine(coords.INPUT_MAX, magic=True)

    while time.time() < end - 140:
        f.gold_diggers([x for x in range(1, 13)])
        f.nuke()
        rt = f.get_rebirth_time()
        text = f.get_quest_text()
        majors = f.get_available_majors()
        if majors == 0 and (coords.QUESTING_MINOR_QUEST in text.lower() or coords.QUESTING_NO_QUEST_ACTIVE in text.lower()):
            f.questing(duration=2, force=3)
        else:
            if not f.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                f.click(*coords.QUESTING_USE_MAJOR)
            f.questing(duration=2)
    f.nuke()
    f.fight()
    f.adventure(itopodauto=True)
    f.pit()
    f.save_check()
    while time.time() < end + 2:
        time.sleep(1)
    f.nuke()
    f.do_rebirth()


w = Window()
feature = Features()

Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")
print(f"Top left found at: {w.x}, {w.y}")

print("If you want to use muffins, use them manually. You can eat several muffins at once to extend the duration above 24 hours.")
input("Press enter to rebirth and start script. ")
feature.do_rebirth()
runs = 1
while True:
    speedrun(feature)
    print(f"Completed guffin run #{runs} at {datetime.datetime.now().strftime('%H:%M:%S')}")
    runs += 1
