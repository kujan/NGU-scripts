"""Static questing script."""

# Helper classes
from classes.features   import Adventure, Questing, GoldDiggers, MoneyPit, Inventory, Yggdrasil
from classes.helper     import Helper
from classes.inputs import Inputs
from classes.navigation import Navigation

import coordinates as coords
import itopod
from distutils.util import strtobool
from PyQt5 import QtCore
import time

def run(window, mutex, signal):
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

    Navigation.menu("inventory")

    text = Questing.get_quest_text().lower()
    majors = Questing.get_available_majors()

    if do_major:
        if majors == 0 and (coords.QUESTING_MINOR_QUEST in text or coords.QUESTING_NO_QUEST_ACTIVE in text):
            itopod.run(signal, duration=adv_duration * 60)
        else:
            if not Inputs.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                Inputs.click(*coords.QUESTING_USE_MAJOR)
            Questing.questing(signal, adv_duration=adv_duration)
    elif subcontract:
        Questing.questing(signal, subcontract=True)
        itopod.run(signal, duration=adv_duration * 60)
    else:
        if majors == 0 and force and (coords.QUESTING_MINOR_QUEST in text or coords.QUESTING_NO_QUEST_ACTIVE in text):
            Questing.questing(signal, force=zone_map[force_zone], adv_duration=adv_duration)
        else:
            if not Inputs.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                Inputs.click(*coords.QUESTING_USE_MAJOR)
            Questing.questing(signal, adv_duration=adv_duration)
    if use_boosts:
        if boost_equipment:
            Inventory.boost_equipment(signal)
        else:
            Inventory.boost_cube(signal)
    if boost_inventory:
        Inventory.boost_inventory(boost_slots, signal)
    if merge_inventory:
        Inventory.merge_inventory(merge_slots, signal)
    if check_fruits:
        Yggdrasil.ygg(signal)
