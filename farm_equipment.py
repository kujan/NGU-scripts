"""Challenge start script."""
import argparse
import time
# Helper classes
from classes.features import Features
import classes.helper as helper

parser = argparse.ArgumentParser()
parser.add_argument("-z", "--zone", required=True, type=int, help="select which zone you wish to snipe")
args = parser.parse_args()

feature = Features()
helper.init(feature, True)

while True:  # main loop
    titans = feature.check_titan_status()
    if titans:
        for titan in titans:
            feature.kill_titan(titan)
    feature.snipe(args.zone, duration=300, manual=True, bosses=True)
    feature.pit()
    time.sleep(3)
