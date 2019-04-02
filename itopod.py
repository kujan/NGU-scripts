"""Static itopod script."""

# Helper classes
from classes.features import Features
from classes.window import Window
from distutils.util import strtobool
from PyQt5.QtCore import QSettings

def run(window, mutex, signal, duration=0):
    w = Window()
    w.x = window.x
    w.y = window.y
    w.id = window.id
    settings = QSettings("Kujan", "NGU-Scripts")
    if not duration:
        duration = int(settings.value("line_adv_duration")) * 60
    use_boosts = strtobool(settings.value("check_gear"))
    check_fruits = strtobool(settings.value("check_fruits"))
    boost_equipment = strtobool(settings.value("radio_equipment"))
    boost_cube = strtobool(settings.value("radio_cube"))
    boost_inventory = strtobool(settings.value("check_boost_inventory"))
    boost_slots = settings.value("arr_boost_inventory")
    merge_inventory = strtobool(settings.value("check_merge_inventory"))
    merge_slots = settings.value("arr_merge_inventory")

    feature = Features(w, mutex)
    feature.itopod_snipe(duration, signal)
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
