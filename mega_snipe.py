"""Snipe with Mega Buff."""
import argparse
import time

# Helper classes
from classes.features   import Adventure, GoldDiggers, MoneyPit, Inventory, Yggdrasil
from classes.helper     import Helper
from classes.inputs     import Inputs

import usersettings as userset
import coordinates  as coords

Helper.init(True)
Helper.requirements()

parser = argparse.ArgumentParser()
parser.add_argument("-z", "--zone", required=True, type=int, help="select which zone you wish to snipe")
args = parser.parse_args()

Adventure.adventure(0)
if Inputs.check_pixel_color(*coords.IS_IDLE):
    Inputs.click(*coords.ABILITY_IDLE_MODE)
time.sleep(userset.MEDIUM_SLEEP)

while True:  # main loop
    GoldDiggers.gold_diggers([4, 1])
    
    if Inputs.check_pixel_color(*coords.COLOR_MEGA_BUFF_READY):
        Adventure.snipe(args.zone, 1, manual=True, bosses=False, once=True)
        Adventure.adventure(0)  # go wait at safe zone
        if Inputs.check_pixel_color(*coords.IS_IDLE):
            Inputs.click(*coords.ABILITY_IDLE_MODE)
            Inputs.click(*coords.WASTE_CLICK)
        
    else:
        MoneyPit.pit()
        MoneyPit.spin()
        Yggdrasil.ygg()
        Inventory.merge_equipment()
        Inventory.boost_equipment()
