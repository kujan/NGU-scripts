"""ITOPOD Sniping script."""
import time
# Helper classes
from classes.features import Adventure, GoldDiggers, MoneyPit, Inventory
from classes.helper   import Helper
from classes.stats    import Tracker

import constants as const

Helper.init(True)
Helper.requirements()

tracker = Tracker(5)

while True:  # main loop
    titans = Adventure.check_titan_status()
    if titans:
        for titan in titans:
            Adventure.kill_titan(titan)
    Adventure.itopod_snipe(300)
    MoneyPit.pit()
    tracker.progress()
    GoldDiggers.gold_diggers(const.DEFAULT_DIGGER_ORDER)
    Inventory.boost_equipment(boost_cube=True)
    time.sleep(3)  # Need to wait for tooltip to disappear
