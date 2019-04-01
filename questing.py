"""Static itopod script."""

# Helper classes
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, Tracker
from classes.window import Window
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
    use_boosts = strtobool(settings.value("check_gear"))
    check_fruits = strtobool(settings.value("check_fruits"))
    boost_equipment = strtobool(settings.value("radio_equipment"))
    boost_cube = strtobool(settings.value("radio_cube"))
    boost_inventory = strtobool(settings.value("check_boost_inventory"))
    boost_slots = int(settings.value("line_boost_inventory"))
    merge_inventory = strtobool(settings.value("check_merge_inventory"))
    merge_slots = int(settings.value("line_merge_inventory"))
    force = strtobool(settings.value("check_force"))
    force_zone = int(settings.value("combo_force_index"))
    do_major = strtobool(settings.value("check_major"))
    subcontract = strtobool(settings.value("check_subcontract"))
    zone_map = {0: 2, 1: 3, 2: 6, 3: 10, 4: 13, 5: 14, 6: 16, 7: 21, 8: 22, 9: 23}
    i = Inputs(w, mutex)
    nav = Navigation(w, mutex)
    feature = Features(w, mutex)
    tracker = Tracker(w, mutex, duration / 60)
    start_exp = Stats.xp
    start_pp = Stats.pp
    nav.menu("inventory")
    while True:  # main loop
        signal.emit(tracker.get_rates())
        signal.emit({"exp": Stats.xp - start_exp, "pp": Stats.pp - start_pp})
        if force:
            feature.questing(signal, force=zone_map[force_zone], adv_duration=duration / 60)
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
        tracker.progress()

