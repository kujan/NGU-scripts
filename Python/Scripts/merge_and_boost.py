"""
Merge and Boost script
No Transformation at this time.
"""

# Challenges
from challenges.basic import Basic
from challenges.level import Level

# Helper classes
from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, EstimateRate, Tracker
from classes.upgrade import Upgrade
from classes.window import Window

import ngucon as ncon
import time

w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")

u = Upgrade(37500, 37500, 2, 2, 3)

print(w.x, w.y)

while True:  # main loop to go foreverrrrr
    feature.merge_equipment()
    feature.boost_equipment()
    feature.merge_inventory(12)
    feature.boost_inventory(12)
    feature.boost_cube()
    #Sets you to your designed zone in case you get bumped out somehow
    # feature.adventure(zone=13, highest=False, itopod=False, itopodauto=False)

    #Add Money Pit Check
    feature.pit()
    #Add Save Check
    feature.save_check()
    #Add Spin Check
    feature.spin()
    #Add Blood Magic Check
    feature.speedrun_bloodpill()
    #Ygg
    feature.ygg()
    #Sleep before trying again
    time.sleep(120)
    # feature.snipe(18, 300, once=False, highest=False, bosses=True)