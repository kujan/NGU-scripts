"""I should write someting here at some point."""

# Challenges
from challenges.basic import Basic
from challenges.level import Level

from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats
from classes.upgrade import Upgrade
from classes.window import Window

# Helper classes
import ngucon as ncon
import time


def speedrun(duration, f):
    """Start a speedrun.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    f.do_rebirth()
    end = time.time() + (duration * 60)
    magic_assigned = False
    do_tm = True
    augments_assigned = False
    f.fight()
    f.loadout(1)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(3)
    f.loadout(2)  # Bar/power equimpent
    f.adventure(itopod=True, itopodauto=True)
    while time.time() < end - 15:
        bm_color = f.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
        tm_color = f.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
        # Do TM while waiting for magic cap
        if not magic_assigned and tm_color != ncon.TMLOCKEDCOLOR:
            f.time_machine(True)
        # If magic is assigned, continue adding energy to TM
        elif do_tm and tm_color != ncon.TMLOCKEDCOLOR:
            f.time_machine()
        else:
            f.wandoos(True)
        # Assign augments when energy caps
        if time.time() > end - (duration * 0.75 * 60):
            if do_tm and not augments_assigned:
                f.send_string("r")
                f.augments({"SM": 0.7, "AA": 0.3}, 8e8)
                f.gold_diggers([2, 8, 9], True)
                do_tm = False
                augments_assigned = True
                f.send_string("t")
                f.wandoos(True)
                f.boost_equipment()
        # Reassign magic from TM into BM after half the duration
        if (bm_color != ncon.BMLOCKEDCOLOR and not magic_assigned and
           time.time() > end - (duration * 0.75 * 60)):
            f.menu("bloodmagic")
            time.sleep(0.2)
            f.send_string("t")
            f.blood_magic(7)
            magic_assigned = True
            f.wandoos(True)
            #time.sleep(15)

        if time.time() > end - (duration * 0.5 * 60):
            try:
                NGU_energy = int(feature.remove_letters(feature.ocr(ncon.OCR_ENERGY_X1,ncon.OCR_ENERGY_Y1,ncon.OCR_ENERGY_X2,ncon.OCR_ENERGY_Y2)))
                feature.assign_ngu(NGU_energy, [1, 2, 4, 5, 6]) 

                NGU_magic = int(feature.remove_letters(feature.ocr(ncon.OCR_MAGIC_X1, ncon.OCR_MAGIC_Y1, ncon.OCR_MAGIC_X2, ncon.OCR_MAGIC_Y2)))
                feature.assign_ngu(NGU_magic, [1, 2], magic=True)
            except:
                print("couldn't assign e/m to NGUs")
        # Assign leftovers into wandoos
        if augments_assigned:
            f.wandoos(True)
            f.gold_diggers([2, 8, 9])
            # f.assign_ngu(100000000, [1])
            # f.assign_ngu(100000000, [1], magic=True)
        # f.boost_equipment()

    f.menu("digger")
    f.gold_diggers([3], True)
    f.fight()
    f.pit()
    f.spin()
    time.sleep(7)
    f.speedrun_bloodpill()
    return


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()
c = Challenge()

Window.x, Window.y = i.pixel_search("212429", 0, 0, 400, 600)
nav.menu("inventory")
s = Stats()
u = Upgrade(37500, 37500, 2, 2, 1)

print(w.x, w.y)
#u.em()
#print(c.check_challenge())

#for x in range(20):
#    c.start_challenge(4)

while True:  # main loop
    #feature.boost_equipment()
    #feature.merge_equipment()
    #feature.ygg()
    #time.sleep(180)
    
    speedrun(3, feature)
    s.print_exp()
    u.em()
