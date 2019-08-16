"""Challenge start script."""

# Helper classes
import argparse
from classes.features import Features
from classes.window import Window
from classes.challenge import Challenge
import coordinates as coords

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--challenge", required=True, type=int, help="select which challenge you wish to run (1-11")
parser.add_argument("-t", "--times", required=True, type=int, help="number of times to run challenge")
args = parser.parse_args()
w = Window()
feature = Features()

Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")

print(f"Top left found at: {w.x}, {w.y}")

c = Challenge()

print(f"Running challenge #{args.challenge} {args.times} times")
for x in range(args.times):
    c.start_challenge(args.challenge)


while True:  # main loop
    feature.itopod_snipe(300)
    feature.pit()
    feature.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
