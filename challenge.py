"""Challenge start script."""

# Helper classes
import argparse
from classes.features import Features
import classes.helper as helper
from classes.challenge import Challenge

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--challenge", required=True, type=int, help="select which challenge you wish to run (1-11")
parser.add_argument("-t", "--times", required=True, type=int, help="number of times to run challenge")
args = parser.parse_args()
feature = Features()
helper.init(feature, True)
c = Challenge()

print(f"Running challenge #{args.challenge} {args.times} times")
for x in range(args.times):
    c.start_challenge(args.challenge)


while True:  # main loop
    feature.itopod_snipe(300)
    feature.pit()
    feature.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
