"""Guffin script."""

# Helper classes
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window

import coordinates as coords
import datetime
import time


def run(window, feature, mutex, signal, duration=0):
    """Procedure that handles start of rebirth."""
    rt = feature.get_rebirth_time()

    if rt.timestamp.tm_hour > 0 or rt.timestamp.tm_min > 30:
        feature.do_rebirth()

    time.sleep(3)
    end = time.time() + 30 * 60
    rt = feature.get_rebirth_time()
    toggle_number = False
    feature.nuke()  # PPP
    time.sleep(2)
    #f.loadout(7)  # gold
    feature.adventure(highest=True)
    feature.toggle_auto_spells(number=False, drop=False)
    feature.gold_diggers([x for x in range(1, 13)])
    feature.set_ngu_overcap(102)
    if feature.check_pixel_color(*coords.NGU_EVIL):
        feature.click(778, 122)
    feature.cap_ngu()
    feature.cap_ngu(magic=True)
    feature.set_wandoos(0)
    feature.wandoos(True)
    feature.augments({"CI": 0.66, "ML": 0.34}, feature.get_idle_cap() * 0.5)
    feature.blood_magic(8)
    feature.time_machine(coords.INPUT_MAX, magic=True)
    #f.loadout(3)

    while rt.timestamp.tm_hour < 1 and rt.timestamp.tm_min < 13:
        if rt.timestamp.tm_min > 1 and not toggle_number:
            feature.toggle_auto_spells(drop=False, gold=False)
            toggle_number = True
        text = feature.get_quest_text()
        majors = feature.get_available_majors()
        if majors == 0 and (coords.QUESTING_MINOR_QUEST in text.lower() or coords.QUESTING_NO_QUEST_ACTIVE in text.lower()):
            feature.questing(duration=2, force=3)
        else:
            if not feature.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                feature.click(*coords.QUESTING_USE_MAJOR)
            feature.questing(duration=2)
        feature.nuke()
        feature.gold_diggers([x for x in range(1, 13)])
        feature.time_machine(coords.INPUT_MAX, magic=True)
        feature.augments({"CI": 0.66, "ML": 0.34}, feature.get_idle_cap() * 0.5)
        feature.time_machine(coords.INPUT_MAX, magic=True)
        rt = feature.get_rebirth_time()

    feature.adventure(highest=True)
    feature.reclaim_tm(True)
    feature.reclaim_aug()
    feature.advanced_training(2e12)
    feature.set_wandoos(1)
    feature.wandoos(True)
    feature.augments({"CI": 0.66, "ML": 0.34}, feature.get_idle_cap() * 0.5)
    feature.time_machine(coords.INPUT_MAX, magic=True)

    while time.time() < end - 140:
        feature.gold_diggers([x for x in range(1, 13)])
        feature.nuke()
        rt = feature.get_rebirth_time()
        text = feature.get_quest_text()
        majors = feature.get_available_majors()
        if majors == 0 and (coords.QUESTING_MINOR_QUEST in text.lower() or coords.QUESTING_NO_QUEST_ACTIVE in text.lower()):
            feature.questing(duration=2, force=3)
        else:
            if not feature.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                feature.click(*coords.QUESTING_USE_MAJOR)
            feature.questing(duration=2)
    feature.nuke()
    feature.fight()
    feature.adventure(itopodauto=True)
    feature.loadout(2)
    feature.pit()
    feature.save_check()
    while time.time() < end + 2:
        time.sleep(1)
    feature.nuke()
    feature.do_rebirth()
