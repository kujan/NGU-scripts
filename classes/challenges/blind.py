"""Contains functions for running a blind challenge."""
from classes.features import FightBoss, Adventure, Augmentation, GoldDiggers
from classes.features import Wandoos, TimeMachine, BloodMagic, Rebirth
from classes.inputs   import Inputs

import coordinates as coords
import time


advanced_training_locked = True
bm_locked = True
tm_locked = True

def run(duration):
    """Procedure for Blind Challenge RBs."""
    global advanced_training_locked, bm_locked, tm_locked

    advanced_training_locked = True
    bm_locked = True
    tm_locked = True

    tm_assigned = False
    bm_assigned = False

    end = time.time() + duration * 60 + 10
    FightBoss.nuke()
    time.sleep(2)
    FightBoss.fight()
    diggers = [2, 3, 11, 12]
    Adventure.adventure(highest=True)
    Augmentation.augments({"SS": 1}, 1e12)
    GoldDiggers.gold_diggers(diggers)
    while time.time() < end:
        Augmentation.augments({"EB": 0.66, "CS": 0.34}, 1e13)
        Wandoos.wandoos(True, True)
        FightBoss.nuke()
        FightBoss.fight()
        GoldDiggers.gold_diggers(diggers)
        update_gamestate()
        if not tm_locked and not tm_assigned:
            TimeMachine.time_machine(1e13, m=1e13)
            tm_assigned = True
        if not bm_locked and not bm_assigned:
            BloodMagic.blood_magic(8)
            bm_assigned = True
        if not Rebirth.check_challenge() and end - time.time() > 180:
            return
    if not Rebirth.check_challenge():
        return
    Rebirth.do_rebirth()
    return

def update_gamestate():
    """Update relevant state information."""
    global advanced_training_locked, bm_locked, tm_locked

    if advanced_training_locked:
        advanced_training_locked = Inputs.check_pixel_color(*coords.COLOR_ADV_TRAINING_LOCKED)
    if bm_locked:
        bm_locked = Inputs.check_pixel_color(*coords.COLOR_BM_LOCKED)
    if tm_locked:
        tm_locked = Inputs.check_pixel_color(*coords.COLOR_TM_LOCKED)

def blind():
    """Run blind challenge."""
    for x in range(8):
        run(3)
        if not Rebirth.check_challenge():
            return
    for x in range(5):
        run(7)
        if not Rebirth.check_challenge():
            return
    for x in range(5):
        run(12)
        if not Rebirth.check_challenge():
            return
    for x in range(5):
        run(60)
        if not Rebirth.check_challenge():
            return
