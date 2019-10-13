"""ITOPOD Sniping script."""

# Helper classes
from classes.features import Features
from classes.stats import Tracker
from classes.window import Window

import coordinates as coords
import constants as const
import time

Window.__init__(object)

feature = Features()

Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")
import requirements
print(f"Top left found at: {Window.x}, {Window.y}")

tracker = Tracker(5)

while True:  # main loop
    titans = feature.check_titan_status()
    if titans:
        for titan in titans:
            feature.kill_titan(titan)
    feature.itopod_snipe(300)
    feature.pit()
    tracker.progress()
    feature.gold_diggers(const.DEFAULT_DIGGER_ORDER)
    time.sleep(3)  # Need to wait for tooltip to disappear
