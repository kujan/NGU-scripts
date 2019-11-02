"""Contains functions for running a no rebirth challenge."""
from classes.features import FightBoss, GoldDiggers, Adventure, Augmentation
from classes.features import BloodMagic, Wandoos, TimeMachine, Misc
from classes.features import Rebirth as RB
from classes.inputs   import Inputs

import coordinates  as coords
import time


def first_rebirth():
    """Procedure for first rebirth."""
    final_aug   = False
    ss_assigned = False

    end = time.time() + 3 * 60

    FightBoss.nuke()
    time.sleep(2)

    FightBoss.fight()
    Adventure.adventure(highest=True)
    while Inputs.check_pixel_color(*coords.COLOR_TM_LOCKED):
        if not ss_assigned:
            time.sleep(1)
            Augmentation.augments({"SS": 1}, 3e12)
            ss_assigned = True
        Wandoos.wandoos(True, True)
        FightBoss.nuke()
        time.sleep(2)
        FightBoss.fight()

    TimeMachine.time_machine(1e9, magic=True)
    Augmentation.augments({"DS": 1}, 1e12)
    GoldDiggers.gold_diggers()
    Adventure.adventure(itopod=True, itopodauto=True)

    while Inputs.check_pixel_color(*coords.COLOR_BM_LOCKED) or Inputs.check_pixel_color(*coords.COLOR_BM_LOCKED_ALT):
        Wandoos.wandoos(True, True)
        FightBoss.nuke()
        time.sleep(2)
        FightBoss.fight()
        GoldDiggers.gold_diggers()
    BloodMagic.blood_magic(8)
    BloodMagic.toggle_auto_spells(drop=False, number=False)
    while time.time() < end - 90:
        Wandoos.wandoos(True, True)
        FightBoss.nuke()
        time.sleep(2)
        try:
            current_boss = int(FightBoss.get_current_boss())
            if current_boss > 36:
                Augmentation.augments({"SS": 0.67, "DS": 0.33}, Misc.get_idle_cap(1))
        except ValueError:
            print("couldn't get current boss")
        GoldDiggers.gold_diggers()

    while True:
        Wandoos.wandoos(True, True)
        FightBoss.nuke()
        time.sleep(1)
        try:
            current_boss = int(FightBoss.get_current_boss())
            if current_boss > 45:
                if not final_aug:
                    Misc.reclaim_aug()
                    final_aug = True
                Augmentation.augments({"SM": 0.67, "AA": 0.33}, Misc.get_idle_cap(1))
        except ValueError:
            print("couldn't get current boss")
        FightBoss.fight()
        GoldDiggers.gold_diggers()

        if time.time() > end and not RB.check_challenge():
            return

def rebirth():
    """Run no rebirth challenge."""
    first_rebirth()
