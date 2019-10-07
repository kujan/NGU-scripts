"""Challenge start script."""

# Helper classes
import argparse
from classes.features import Features
from classes.window import Window
from classes.challenge import Challenge
import coordinates as coords

parser = argparse.ArgumentParser()
parser.add_argument("-z", "--zone", required=True, type=int, help="select which zone you wish to snipe")
args = parser.parse_args()
w = Window()
feature = Features()

Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")

import requirements

print(f"Top left found at: {w.x}, {w.y}")

while True:  # main loop
    feature.snipe(args.zone, duration=300, manual=True, bosses=True)
    feature.pit()
