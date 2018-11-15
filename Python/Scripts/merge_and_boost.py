"""
Merge and Boost script
No Transformation at this time.
"""

# Helper classes
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window

import time

w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search("212429", 0, 0, 400, 600)
nav.menu("inventory")

print(w.x, w.y)

while True:  # main loop to go foreverrrrr
    feature.merge_equipment()
    feature.boost_equipment()
    feature.merge_inventory()
    feature.boost_inventory()
    #Sets you to your designed zone in case you get bumped out somehow
    feature.adventure(zone=13, highest=False, itopod=False, itopodauto=False)
    feature.ygg()
    time.sleep(120)