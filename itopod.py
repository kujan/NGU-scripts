"""Static itopod script."""

# Helper classes
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, Tracker
from classes.window import Window
import time
#from PyQt5.QtCore import SIGNAL
def run(window, mutex, signal, duration):
    w = Window()
    w.x = window.x
    w.y = window.y
    w.id = window.id
    i = Inputs(w, mutex)
    nav = Navigation(w, mutex)
    feature = Features(w, mutex)
    tracker = Tracker(w, mutex, duration / 60)
    start_exp = Stats.xp
    start_pp = Stats.pp
    nav.menu("inventory")
    while True:  # main loop
        #QtCore.QThread
        signal.emit(tracker.get_rates())
        signal.emit({"exp": Stats.xp - start_exp, "pp": Stats.pp - start_pp})
        feature.itopod_snipe(duration, signal)
        feature.boost_cube()
        feature.ygg()
        tracker.progress()

