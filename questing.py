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
    duration = int(settings.value("line_duration"))
    adv_duration = int(settings.value("line_adv_duration"))
    use_boosts = strtobool(settings.value("check_gear"))
    check_fruits = strtobool(settings.value("check_fruits"))
    boost_equipment = strtobool(settings.value("radio_equipment"))
    boost_cube = strtobool(settings.value("radio_cube"))
    boost_inventory = strtobool(settings.value("check_boost_inventory"))
    boost_slots = settings.value("arr_boost_inventory")
    merge_inventory = strtobool(settings.value("check_merge_inventory"))
    merge_slots = settings.value("arr_merge_inventory")
    force = strtobool(settings.value("check_force"))
    force_zone = int(settings.value("combo_force_index"))
    do_major = strtobool(settings.value("check_major"))
    subcontract = strtobool(settings.value("check_subcontract"))
    zone_map = {0: 2, 1: 3, 2: 6, 3: 10, 4: 13, 5: 14, 6: 16, 7: 21, 8: 22, 9: 23}
    feature = Features(w, mutex)
    feature.menu("inventory")

    text = feature.get_quest_text().lower()
    majors = feature.get_available_majors()

    if do_major:
        if majors == 0:
            itopod.run(w, mutex, signal, once=True)
        else:
            feature.questing(signal, duration=duration, adv_duration=adv_duration)
    elif subcontract:
        feature.questing(signal, subcontract=True)
    else:
        if majors == 0 and force and (coords.QUESTING_MINOR_QUEST in text or coords.QUESTING_NO_QUEST_ACTIVE in text):
            feature.questing(signal, duration=duration, force=zone_map[force_zone], adv_duration=adv_duration)
        else:
            feature.questing(signal, duration=duration, adv_duration=adv_duration)
    if use_boosts:
        if boost_equipment:
            feature.boost_equipment(signal)
        if boost_cube:
            feature.boost_cube(signal)
    if boost_inventory:
        feature.boost_inventory(boost_slots, signal)
    if merge_inventory:
        feature.merge_inventory(merge_slots, signal)
    if check_fruits:
        feature.ygg(signal)
