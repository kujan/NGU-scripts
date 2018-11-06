"""12-minute rebirth script"""

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

def speedrun(duration, f):
    #TODO: Add in debug statements 
    """Start a speedrun.
    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    f.do_rebirth()
    start = time.time()
    end = time.time() + (duration * 60)
    magic_assigned = False
    augments_assigned = False
    blood_digger_active = False
    f.fight()
    #TODO: What is the point of this?
    # current_boss = int(feature.get_current_boss())
    # while current_boss < 60:
    #     print(f"at boss {current_boss}, fighting {60-current_boss + 1} more times")
    #     feature.fight(60-current_boss + 1)
    #     current_boss = int(feature.get_current_boss())

    f.loadout(1)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(7)
    f.loadout(2)  # Bar/power equimpent
    f.adventure(itopod=True, itopodauto=True)
    #Sleep so can get enough E/M for time machine
    time.sleep(60)
    f.augments({"SS": 0.3, "DS": 0.7}, 5.5e6) #5.5m
    #Sleep so time machine can get some E/M
    #TODO: Optimize
    time.sleep(60)
    f.time_machine(True)
    
    while time.time() < end - 15:
        if time.time() > end - (duration * 0.85 * 60):
            if not augments_assigned:
                # f.send_string("r")

                augments_assigned = True
                f.boost_equipment()
        # Reassign magic from TM into BM after half the duration
        if not magic_assigned and time.time() > end - (duration * 0.75 * 60):
                f.menu("bloodmagic")
                time.sleep(0.2)
                f.blood_magic(2)
                magic_assigned = True
                f.wandoos(True)
                f.gold_diggers([2], True)


        """
       if time.time() > end - (duration * 0.74 * 60):
                                 try:
                                     NGU_energy = int(feature.remove_letters(feature.ocr(ncon.OCR_ENERGY_X1,ncon.OCR_ENERGY_Y1,ncon.OCR_ENERGY_X2,ncon.OCR_ENERGY_Y2)))
                                     feature.assign_ngu(NGU_energy, [1, 2, 4, 5, 6]) 
                     
                                     NGU_magic = int(feature.remove_letters(feature.ocr(ncon.OCR_MAGIC_X1, ncon.OCR_MAGIC_Y1, ncon.OCR_MAGIC_X2, ncon.OCR_MAGIC_Y2)))
                                     feature.assign_ngu(NGU_magic, [1, 2], magic=True)
                                 except ValueError:
                                     print("couldn't assign e/m to NGUs")"""
        # Do some early fights to open up furthest area for gold
        if time.time() < end - (duration * 0.75 * 60):
            #Make sure we're making maximum gold as the run progresses
            f.adventure(highest=True)
            time.sleep(7)
            f.adventure(itopod=True, itopodauto=True)

        # Assign leftovers into wandoos, turn on digger, fight for boss
        if augments_assigned:
            f.wandoos(True)
            f.gold_diggers([2], True)
            f.fight()

        # if time.time() > start + 120 and not blood_digger_active:
        #     blood_digger_active = True
            # f.gold_diggers([11], True)

        time.sleep(0.5)

    f.gold_diggers([2])
    f.fight()
    f.pit()
    f.spin()
    time.sleep(7)
    f.speedrun_bloodpill()

import time

w = Window()
i = Inputs()
nav = Navigation()
feature = Features()
c = Challenge()

Window.x, Window.y = i.pixel_search("212429", 0, 0, 400, 600)
nav.menu("inventory")
s = Stats()
u = Upgrade(37500, 37500, 1, 1, 5)
# How much XP is this?

print(w.x, w.y)

count = 0

while count <=5: #Adjust # for how many runs you want to do during testing
    count += 1
    speedrun(12, feature)
    s.print_exp()
    u.em()

# while True:  # main loop
#     # feature.boost_equipment()
#     # feature.merge_equipment()
#     # feature.ygg(True)
#     # time.sleep(120)
#     speedrun(12, feature)
#     s.print_exp()
#     u.em()