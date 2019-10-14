"""Challenge start script."""

# Helper classes
import argparse
from classes.features import Features
from classes.window import Window
from classes.challenge import Challenge
import usersettings as userset
import coordinates as coords
import time

parser = argparse.ArgumentParser()
parser.add_argument("-z", "--zone", required=True, type=int, help="select which zone you wish to snipe")
args = parser.parse_args()
Window.init()
feature = Features()

Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")

print(f"Top left found at: {w.x}, {w.y}")

feature.menu("adventure")
feature.click(*coords.LEFT_ARROW, button="right")
feature.click(625, 500)
time.sleep(userset.MEDIUM_SLEEP)
if feature.check_pixel_color(*coords.IS_IDLE):
    feature.click(*coords.ABILITY_IDLE_MODE)
    

while True:  # main loop
    if feature.check_pixel_color(*coords.IS_IDLE):
        feature.click(*coords.ABILITY_IDLE_MODE)
    feature.click(625, 500)
    color = feature.get_pixel_color(647, 176)
    if color == coords.ABILITY_ROW3_READY_COLOR:
        feature.snipe(args.zone, 1, manual=True, bosses=True, once=True)
        feature.click(*coords.LEFT_ARROW, button="right")
        feature.current_adventure_zone = 0
    feature.pit()
    time.sleep(0.1)
