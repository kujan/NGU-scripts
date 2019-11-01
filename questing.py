"""Manual Questing Script."""

# Helper classes
from classes.features   import Adventure, Questing, GoldDiggers, MoneyPit
from classes.helper     import Helper

import coordinates as coords
import time

Helper.init(True)
Helper.requirements()

choice = ""
answers = {"y": True, "ye": True, "yes": True, "n": False, "no": False}
print("If you currently have an active quest that either is minor or has been subcontracted, consider skipping it before starting if you intend to use butter")
while choice not in answers:
    choice = input("Use butter for major quests? y/n: ").lower()

while True:  # main loop
    titans = Adventure.check_titan_status()
    if titans:
        Adventure.kill_titan(titans[0])
    text = Questing.get_quest_text()
    majors = Questing.get_available_majors()
    if majors == 0 and (coords.QUESTING_MINOR_QUEST in text.lower() or coords.QUESTING_NO_QUEST_ACTIVE in text.lower()):
        Questing.questing(force=3)
    else:
        Questing.set_use_majors()
        Questing.questing(butter=answers[choice])
    MoneyPit.pit()
    GoldDiggers.gold_diggers()
    time.sleep(3)

"""Static itopod script."""

# Helper classes
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window
import coordinates as coords
import itopod
from distutils.util import strtobool
from PyQt5 import QtCore
import time

def run(window, mutex, signal):
    w = Window()
    w.x = window.x
    w.y = window.y
    w.id = window.id
    settings = QtCore.QSettings("Kujan", "NGU-Scripts")
    adv_duration = int(settings.value("line_adv_duration", "5"))
    use_boosts = strtobool(settings.value("check_gear", "False"))
    check_fruits = strtobool(settings.value("check_fruits", "False"))
    boost_equipment = strtobool(settings.value("radio_equipment", "False"))
    boost_inventory = strtobool(settings.value("check_boost_inventory", "False"))
    boost_slots = settings.value("arr_boost_inventory", "False")
    merge_inventory = strtobool(settings.value("check_merge_inventory", "False"))
    merge_slots = settings.value("arr_merge_inventory", "False")
    force = strtobool(settings.value("check_force", "False"))
    force_zone = int(settings.value("combo_force_index", "3"))
    do_major = strtobool(settings.value("check_major", "False"))
    subcontract = strtobool(settings.value("check_subcontract", "False"))
    zone_map = {0: 2, 1: 3, 2: 6, 3: 10, 4: 13, 5: 14, 6: 16, 7: 21, 8: 22, 9: 23}
    feature = Features(w, mutex)
    feature.menu("inventory")

    text = feature.get_quest_text().lower()
    majors = feature.get_available_majors()

    if do_major:
        if majors == 0 and (coords.QUESTING_MINOR_QUEST in text or coords.QUESTING_NO_QUEST_ACTIVE in text):
            itopod.run(w, mutex, signal, duration=adv_duration * 60)
        else:
            if not feature.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                feature.click(*coords.QUESTING_USE_MAJOR)
            feature.questing(signal, adv_duration=adv_duration)
    elif subcontract:
        feature.questing(signal, subcontract=True)
        itopod.run(w, mutex, signal, duration=adv_duration * 60)
    else:
        if majors == 0 and force and (coords.QUESTING_MINOR_QUEST in text or coords.QUESTING_NO_QUEST_ACTIVE in text):
            feature.questing(signal, force=zone_map[force_zone], adv_duration=adv_duration)
        else:
            if not feature.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                feature.click(*coords.QUESTING_USE_MAJOR)
            feature.questing(signal, adv_duration=adv_duration)
    if use_boosts:
        if boost_equipment:
            feature.boost_equipment(signal)
        else:
            feature.boost_cube(signal)
    if boost_inventory:
        feature.boost_inventory(boost_slots, signal)
    if merge_inventory:
        feature.merge_inventory(merge_slots, signal)
    if check_fruits:
        feature.ygg(signal)
