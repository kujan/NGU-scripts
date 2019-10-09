"""Challenge start script."""

# Helper classes
import argparse
from classes.features import Features
from classes.window import Window
from classes.challenge import Challenge
import coordinates as coords
import time
parser = argparse.ArgumentParser()
parser.add_argument("-z", "--zone", required=True, type=int, help="select which zone you wish to snipe")
args = parser.parse_args()
Window.__init__(object)
feature = Features()

Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")

import requirements

print(f"Top left found at: {Window.x}, {Window.y}")

while True:  # main loop
    titans = feature.check_titan_status()
    if titans:
        for titan in titans:
            feature.kill_titan(titan)
    feature.snipe(args.zone, duration=300, manual=True, bosses=True)
    feature.pit()
    time.sleep(3)
