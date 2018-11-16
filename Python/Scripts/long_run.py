"""24 Hour rebirth script."""

# Challenges
from challenges.basic import Basic
from challenges.level import Level

# Helper classes
from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats
from classes.upgrade import Upgrade
from classes.window import Window

# Constants
import ngucon as ncon

import time


def run(time2cap, f):
    """Start a 24h run."""
    # Time to unlock adv. training
    adv_training = 1350
    start = time.start()
    f.fight()
    f.loadout(1)
    f.adventure(highest=True)
    time.sleep(10)
    f.loadout(2)
    f.adventure(itopod=True, itopodauto=True)
    f.blood_magic(7)
    for s in range(time2cap):  # do TM until we cap
        f.time_machine(True)
        time.sleep(1)

    while time.time() < start + adv_training:
        time.sleep()
        
w = Window()
i = Inputs()
nav = Navigation()
feature = Features()
Window.x, Window.y = i.pixel_search("212429", 0, 0, 400, 600)
nav.menu("inventory")
s = Stats()
u = Upgrade(37500, 37500, 4, 4, 1)

while True:
    run(60, feature)
