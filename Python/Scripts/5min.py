"""5-minute rebirth script"""

# Helper classes
from classes.features import Features
from classes.alt_features import AltFeatures
from classes.inputs import Inputs
from classes.alt_inputs import AltInputs
from classes.navigation import Navigation
from classes.stats import Stats, EstimateRate, Tracker
from classes.upgrade import Upgrade
from classes.window import Window

import ngucon as ncon
import time


def speedrun(duration, f, af):
    """Start a speedrun.
    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    f.do_rebirth()
    start = time.time()
    end = time.time() + (duration * 60)
    blood_digger_active = False
    itopod_advance = False
    f.nuke()
    time.sleep(2)
    f.loadout(2)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(3)
    f.loadout(1)  # Bar/power equimpent
    f.adventure(itopod=True, itopodauto=True)
    #Sleep so can get enough E/M for augments
    time.sleep(5)
    # f.augments({"CI": 0.3, "ML": 0.7}, 1e8) #100m
    f.augments({"SM": 0.3, "AA": 0.7}, 1e8) #100m
    #Sleep so time machine can get some E/M
    #TODO: Optimize
    time.sleep(10)
    f.blood_magic(5)
    f.time_machine(True)
    af.boost_cube()
    f.gold_diggers([2, 3, 5, 6], True)
    f.wandoos(True)
    #Add turning on diggers here

    while time.time() < end - 20:
        f.wandoos(True)
        f.gold_diggers([2, 3, 5, 6])
        # Don't have blood digger
        # if time.time() > start + 40 and not blood_digger_active:
        #     blood_digger_active = True
        #     f.gold_diggers([11], True)

        #Don't have enough to mess with NGU in short runs yet
        if time.time () > start + 90:
            try:
                NGU_energy = int(f.remove_letters(f.ocr(ncon.OCR_ENERGY_X1, ncon.OCR_ENERGY_Y1, ncon.OCR_ENERGY_X2, ncon.OCR_ENERGY_Y2)))
                feature.assign_ngu(NGU_energy, [6])
                NGU_magic = int(f.remove_letters(f.ocr(ncon.OCR_MAGIC_X1, ncon.OCR_MAGIC_Y1, ncon.OCR_MAGIC_X2, ncon.OCR_MAGIC_Y2)))
                feature.assign_ngu(NGU_magic, [3], magic=True)
            except ValueError:
                print("couldn't assign e/m to NGUs")
            time.sleep(0.5)

        if time.time() > start + 90 and not itopod_advance:
            f.adventure(itopod=True, itopodauto=True)
            itopod_advance = True

        # if time.time() > start + 120 and not blood_digger_active:
        #     blood_digger_active = True
            # f.gold_diggers([11], True)

        time.sleep(0.5)

    time.sleep(2)
    f.nuke()
    time.sleep(2)
    f.fight()
    time.sleep(7)
    f.pit()
    f.spin()
    f.save_check()
    tracker.progress()
    u.em()
    tracker.adjustxp()
    f.speedrun_bloodpill()
    while time.time() < end:
        time.sleep(0.1)

    return

w = Window()
i = Inputs()
ai = AltInputs()
nav = Navigation()
feature = Features()
alt_feature = AltFeatures()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")

u = Upgrade(37500, 37500, 2, 2, 3)

print(w.x, w.y)
tracker = Tracker(5)
count = 0

# while count <= 0: # Adjust # for how many runs you want to do during testing minus 1
    # count += 1
    # speedrun(5, feature, alt_feature)
#
while True:  # main loop to go foreverrrrr
    speedrun(5, feature, alt_feature)