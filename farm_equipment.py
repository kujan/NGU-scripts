"""Challenge start script."""
import argparse
import time

# Helper classes
from classes.features import Adventure, MoneyPit
from classes.helper   import Helper

Helper.init(True)
Helper.requirements()

parser = argparse.ArgumentParser()
parser.add_argument("-z", "--zone", required=True, type=int, help="select which zone you wish to snipe")
args = parser.parse_args()

while True:  # main loop
    titans = Adventure.check_titan_status()
    if titans:
        for titan in titans:
            Adventure.kill_titan(titan)
    Adventure.snipe(args.zone, duration=5, manual=True, bosses=True)
    MoneyPit.pit()
    time.sleep(3)
