"""Challenge start script."""

# Helper classes
from classes.features  import Adventure, GoldDiggers, MoneyPit
from classes.helper    import Helper
from classes.challenge import Challenge

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--challenge", required=True, type=int, help="select which challenge you wish to run (1-11)")
parser.add_argument("-t", "--times", default=1, type=int, help="number of times to run challenge")
args = parser.parse_args()

Helper.init(True)
Helper.requirements()

print(f"Running challenge #{args.challenge} {args.times} times")
for x in range(args.times):
    Challenge.start_challenge(args.challenge)

print("Finished doing all challenges")
print("Engaging idling loop")
while True:  # main loop
    Adventure.itopod_snipe(300)
    MoneyPit.pit()
    GoldDiggers.gold_diggers()
