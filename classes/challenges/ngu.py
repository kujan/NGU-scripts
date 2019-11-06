"""Contains functions for running a no NGU challenge."""
from classes.features import FightBoss, Wandoos, Misc, Adventure, GoldDiggers, TimeMachine
from classes.features import Augmentation, Rebirth, AdvancedTraining, BloodMagic
from classes.inputs   import Inputs

import coordinates as coords
import time


current_boss = 1
minutes_elapsed = 0
advanced_training_locked = True
bm_locked = True
tm_locked = True

def first_rebirth(duration):
    """Procedure for first rebirth."""
    global current_boss, minutes_elapsed, advanced_training_locked, bm_locked, tm_locked

    adv_training_assigned = False
    current_boss = 1
    minutes_elapsed = 0
    advanced_training_locked = True
    bm_locked = True
    tm_locked = True

    while current_boss < 18 and minutes_elapsed < duration:
        Wandoos.wandoos(True, True)
        FightBoss.fight()
        update_gamestate()
        if not advanced_training_locked and not adv_training_assigned:
            print("assigning adv")
            AdvancedTraining.advanced_training(4e11)
            adv_training_assigned = True
    Adventure.adventure(highest=True)
    while minutes_elapsed < duration:
        Wandoos.wandoos(True, True)
        Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
        update_gamestate()

def speedrun(duration):
    """Start a speedrun.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    global current_boss, minutes_elapsed, advanced_training_locked, bm_locked, tm_locked

    diggers = [2, 3, 11, 12]
    adv_training_assigned = False
    Rebirth.do_rebirth()
    Wandoos.wandoos(True, True)
    FightBoss.nuke()
    time.sleep(2)
    FightBoss.fight()
    Adventure.adventure(highest=True)
    current_boss = 1
    minutes_elapsed = 0
    advanced_training_locked = True
    bm_locked = True
    tm_locked = True
    update_gamestate()

    while current_boss < 18 and minutes_elapsed < duration:  # augs unlocks after 17
        Wandoos.wandoos(True, True)
        Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
        FightBoss.nuke()
        FightBoss.fight()
        if not advanced_training_locked and not adv_training_assigned:
            print("assigning adv")
            Misc.reclaim_aug()
            AdvancedTraining.advanced_training(4e11)
            Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
            adv_training_assigned = True
        update_gamestate()
    Adventure.adventure(highest=True)

    while current_boss < 29 and minutes_elapsed < duration:  # buster unlocks after 28
        Wandoos.wandoos(True, True)
        FightBoss.nuke()
        FightBoss.fight()
        if not advanced_training_locked and not adv_training_assigned:
            print("assigning adv")
            Misc.reclaim_aug()
            AdvancedTraining.advanced_training(4e11)
            Augmentation.augments({"SS": 1}, Misc.get_idle_cap(1))
            adv_training_assigned = True
        update_gamestate()

    if minutes_elapsed < duration:  # only reclaim if we're not out of time
        Misc.reclaim_aug()

    while current_boss < 31 and minutes_elapsed < duration:  # TM unlocks after 31
        Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
        Wandoos.wandoos(True, True)
        FightBoss.nuke()
        FightBoss.fight()
        if not advanced_training_locked and not adv_training_assigned:
            print("assigning adv")
            Misc.reclaim_aug()
            AdvancedTraining.advanced_training(4e11)
            Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
            adv_training_assigned = True
        update_gamestate()

    if minutes_elapsed < duration:  # only reclaim if we're not out of time
        Misc.reclaim_aug()  # get some energy back for TM
        Misc.reclaim_res(magic=True)  # get all magic back from wandoos
        TimeMachine.time_machine(Misc.get_idle_cap(1) * 0.05, m=Misc.get_idle_cap(2) * 0.05)

    while current_boss < 38 and minutes_elapsed < duration:  # BM unlocks after 37
        GoldDiggers.gold_diggers(diggers)
        Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
        Wandoos.wandoos(True, True)
        FightBoss.nuke()
        FightBoss.fight()
        if not advanced_training_locked and not adv_training_assigned:
            print("assigning adv")
            Misc.reclaim_aug()
            AdvancedTraining.advanced_training(4e11)
            Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
            adv_training_assigned = True
        update_gamestate()

    if minutes_elapsed < duration:
        BloodMagic.blood_magic(8)
        BloodMagic.toggle_auto_spells(drop=False)
        time.sleep(10)
        print("waiting 10 seconds for gold ritual")
        BloodMagic.toggle_auto_spells(drop=False, gold=False)

    while current_boss < 49 and minutes_elapsed < duration:
        GoldDiggers.gold_diggers(diggers)
        Wandoos.wandoos(True, True)
        Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
        FightBoss.nuke()
        FightBoss.fight()
        if not advanced_training_locked and not adv_training_assigned:
            print("assigning adv")
            Misc.reclaim_aug()
            AdvancedTraining.advanced_training(4e11)
            Augmentation.augments({"EB": 1}, Misc.get_idle_cap(1))
            adv_training_assigned = True
        update_gamestate()
    if minutes_elapsed < duration:  # only reclaim if we're not out of time
        Misc.reclaim_aug()

    while minutes_elapsed < duration:
        Augmentation.augments({"EB": 0.66, "CS": 0.34}, Misc.get_idle_cap(1))
        GoldDiggers.gold_diggers(diggers)
        Wandoos.wandoos(True, True)
        FightBoss.nuke()
        FightBoss.fight()
        if not advanced_training_locked and not adv_training_assigned:
            print("assigning adv")
            Misc.reclaim_aug()
            AdvancedTraining.advanced_training(4e11)
            Augmentation.augments({"EB": 0.66, "CS": 0.34}, Misc.get_idle_cap(1))
            adv_training_assigned = True
        update_gamestate()
        if not Rebirth.check_challenge() and minutes_elapsed >= 3:
            return
 
    return

def update_gamestate():
    """Update relevant state information."""
    global current_boss, minutes_elapsed, advanced_training_locked, bm_locked, tm_locked

    rb_time = Rebirth.get_rebirth_time()
    minutes_elapsed = int(rb_time.timestamp.tm_min)
    try:
        current_boss = int(FightBoss.get_current_boss())
    except ValueError:
        current_boss = 1
        print("couldn't get current boss")

    if advanced_training_locked:
        advanced_training_locked = Inputs.check_pixel_color(*coords.COLOR_ADV_TRAINING_LOCKED)
    if bm_locked:
        bm_locked = Inputs.check_pixel_color(*coords.COLOR_BM_LOCKED)
    if tm_locked:
        tm_locked = Inputs.check_pixel_color(*coords.COLOR_TM_LOCKED)

def ngu():
    """Run no NGU challenge."""
    Wandoos.set_wandoos(0)
    first_rebirth(15)
    if not Rebirth.check_challenge():
        return
    for x in range(8):
        speedrun(30)
        if not Rebirth.check_challenge():
            return
    while True:
        speedrun(60)
        if not Rebirth.check_challenge():
            return
    return