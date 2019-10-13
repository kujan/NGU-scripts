"""ITOPOD Sniping script."""
import time
# Helper classes
import classes.helper as helper
from classes.features import Features
from classes.stats import Tracker

import constants as const

feature = Features()
helper.init(feature, True)
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
