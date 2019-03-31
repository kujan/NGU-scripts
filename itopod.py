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
#from PyQt5.QtCore import SIGNAL
def run(window, mutex, signal, duration):
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
    boost_inventory = int(settings.value("line_boost_inventory"))
    merge_inventory = int(settings.value("line_merge_inventory"))

    i = Inputs(w, mutex)
    nav = Navigation(w, mutex)
    feature = Features(w, mutex)
    tracker = Tracker(w, mutex, duration / 60)
    start_exp = Stats.xp
    start_pp = Stats.pp
    #boost_equipment = 
    nav.menu("inventory")
    while True:  # main loop
        signal.emit(tracker.get_rates())
        signal.emit({"exp": Stats.xp - start_exp, "pp": Stats.pp - start_pp})
        #feature.itopod_snipe(duration, signal)
        if use_boosts:
            if boost_equipment:
                feature.boost_equipment(signal)
        feature.boost_cube(signal)
        feature.ygg(signal)
        tracker.progress()

