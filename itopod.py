"""Static itopod script."""

# Helper classes
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, Tracker
from classes.window import Window
import time
#from PyQt5.QtCore import SIGNAL
def run(window, signal, duration):
    w = Window()
    w.x = window.x
    w.y = window.y
    w.id = window.id
    i = Inputs(w)
    nav = Navigation(w)
    feature = Features(w)
    tracker = Tracker(w, duration / 60)
    nav.menu("inventory")
    while True:  # main loop
        #QtCore.QThread
        signal.emit(tracker.get_rates())
        feature.itopod_snipe(duration, signal)
        feature.boost_cube()
        feature.ygg()
        tracker.progress()

