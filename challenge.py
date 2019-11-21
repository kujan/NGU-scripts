"""Challenge start script."""

# Helper classes
from classes.features  import Adventure, GoldDiggers, MoneyPit
from classes.helper    import Helper
from classes.challenge import Challenge

import argparse

parser = argparse.ArgumentParser(epilog='\n'.join(Challenge.list()), formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-c", "--challenge", required=True, type=int, help="select which challenge you wish to run (1-11)")
parser.add_argument("-t", "--times", default=1, type=int, help="number of times to run challenge")
parser.add_argument("-i", "--idle", action='store_true', help="run idle loop after finishing running")
args = parser.parse_args()

Helper.init(True)
Helper.requirements()

print(f"Running challenge #{Challenge.list()[args.challenge-1]} {args.times} times")
for x in range(args.times):
    Challenge.start_challenge(args.challenge)

print("Finished doing all challenges")
if args.idle:
    print("Engaging idling loop")
    while True:  # main loop
        Adventure.itopod_snipe(300)
        MoneyPit.pit()
        GoldDiggers.gold_diggers()
else: print("Exiting")
