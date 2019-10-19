"""Challenge start script."""

# Helper classes
from classes.features  import *
from classes.helper    import Helper
from classes.challenge import Challenge

import argparse

Helper.init(True)
Helper.requirements()

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--challenge", required=True, type=int, help="select which challenge you wish to run (1-11")
parser.add_argument("-t", "--times", required=True, type=int, help="number of times to run challenge")
args = parser.parse_args()

print(f"Running challenge #{args.challenge} {args.times} times")
for x in range(args.times):
    Challenge.start_challenge(args.challenge)


while True:  # main loop
    Adventure.itopod_snipe(300)
    MoneyPit.pit()
    GoldDiggers.gold_diggers()
