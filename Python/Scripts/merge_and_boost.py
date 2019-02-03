"""
Merge and Boost script
No Transformation at this time.
"""

# Helper classes
from classes.features import Features
from classes.alt_features import AltFeatures
from classes.alt_inputs import AltInputs
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, EstimateRate, Tracker
from classes.upgrade import Upgrade
from classes.window import Window
from classes.discord import Discord

import ngucon as ncon
import time

w = Window()
i = Inputs()
nav = Navigation()
feature = Features()
alt_features = AltFeatures()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")

u = Upgrade(37500, 37500, 2, 2, 3)

print(w.x, w.y)
tracker = Tracker(3)

while True:  # main loop to go foreverrrrr
    #Add Money Pit Check
    feature.pit()
    #Add Save Check
    feature.save_check()
    #Add Spin Check
    feature.spin()
    #Add Blood Magic Check
    # feature.speedrun_bloodpill()
    #Ygg
    feature.ygg()
    #Adjust Energy NGU and try to BB
    # feature.set_ngu([1,4,5,6])
    # feature.bb_ngu(4e9, [1,4,5,6], 1.05)
    #Adjust Magic NGU and try to BB
    # feature.set_ngu([2,3], magic=True)
    # feature.bb_ngu(1e9, [2, 3], 1.05, magic=True)
    #Gold diggers
    feature.gold_diggers([4, 5, 6, 7, 8, 9, 10, 11, 12])
    #Equip
    # alt_features.alt_merge_equipment()
    # alt_features.alt_boost_equipment()
    alt_features.alt_merge_inventory(2)
    alt_features.alt_boost_inventory(1)
    alt_features.boost_cube()
    alt_features.clear_keypresses()
    #It will ping you the quest is complete every 3 minutes or so
    #Make it only fire once with a variable
    # if alt_features.quest_complete():
        # feature.adventure(itopod=True, itopodauto=True)
        # Discord.send_message(('Quest Complete! Go turn it in and start a new one'), Discord.ERROR)
    # if not alt_features.quest_complete():
        # count = 0
        # while count <= 12:
            # alt_features.alt_transform_slot(count,threshold=.9,consume=True)
            # count += 1
    # alt_features.alt_transform_slot(4,threshold=.9,consume=True)
    # alt_feature.alt_transform_slot(5,threshold=.9,consume=True)
    # alt_feature.alt_transform_slot(6,threshold=.9,consume=True)
    #Sets you to your designed zone in case you get bumped out somehow
    # feature.adventure(zone=13, highest=False, itopod=False, itopodauto=False)
 
    #Sleep before trying again
    time.sleep(180)
    #
    tracker.progress()
    # feature.snipe(18, 300, once=False, highest=False, bosses=True)