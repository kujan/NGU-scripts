"""24-hour rebirth script."""
import time
# Helper classes
from classes.features   import (AdvancedTraining, Adventure, Augmentation, FightBoss, Inventory, Misc,
                                BloodMagic, GoldDiggers, NGU, Wandoos, TimeMachine, MoneyPit, Rebirth,
                                Questing, Yggdrasil)
from classes.helper     import Helper

# Set these to your own loadouts
respawn_loadout = 1
ygg_loadout = 2

Helper.init()
Helper.requirements()


def rebirth_init(rt):
    """Procedure that handles start of rebirth."""
    Misc.reclaim_all()  # make sure we reset e/m if we run this mid-rebirth
    FightBoss.nuke(101)  # PPP
    Inventory.loadout(respawn_loadout)
    Adventure.adventure(highest=True)
    TimeMachine.time_machine(5e11, magic=True)
    Augmentation.augments({"CI": 0.7, "ML": 0.3}, 1e12)
    BloodMagic.blood_magic(8)
    BloodMagic.toggle_auto_spells()
    GoldDiggers.gold_diggers()

    if rt.timestamp.tm_hour > 0 or rt.timestamp.tm_min >= 13:
        print("assigning adv training")
    else:
        duration = (12.5 - rt.timestamp.tm_min) * 60
        print(f"doing itopod for {duration} seconds while waiting for adv training to activate")
        Adventure.itopod_snipe(duration)

    AdvancedTraining.advanced_training(2e12)
    GoldDiggers.gold_diggers()
    Misc.reclaim_bm()
    Wandoos.wandoos(True)
    NGU.assign_ngu(Misc.get_idle_cap(2), range(1, 9), False)
    NGU.assign_ngu(Misc.get_idle_cap(1), range(1, 7), True)

rt = Rebirth.get_rebirth_time()
rebirth_init(rt)

while True:
    rt = Rebirth.get_rebirth_time()
    FightBoss.nuke()
    GoldDiggers.gold_diggers()
    Inventory.merge_inventory(8)  # merge uneqipped guffs
    spells = BloodMagic.check_spells_ready()
    if spells:  # check if any spells are off CD
        Misc.reclaim_ngu(True)  # take all magic from magic NGUs
        for spell in spells:
            BloodMagic.cast_spell(spell)
        Misc.reclaim_bm()
        NGU.assign_ngu(Misc.get_idle_cap(1), range(1, 7), True)
        BloodMagic.toggle_auto_spells()  # retoggle autospells

    if rt.days > 0:  # rebirth is at >24 hours
        print(f"rebirthing at {rt}")  # debug
        FightBoss.nuke()
        MoneyPit.spin()
        GoldDiggers.deactivate_all_diggers()
        Yggdrasil.ygg(equip=1)  # harvest with equipment set 1
        Yggdrasil.ygg(eat_all=True)
        GoldDiggers.level_diggers()  # level all diggers
        Rebirth.do_rebirth()
        time.sleep(3)
        rt = Rebirth.get_rebirth_time()
        rebirth_init(rt)
    else:
        Yggdrasil.ygg()
        Misc.save_check()
        MoneyPit.pit()
        if rt.timestamp.tm_hour <= 12:  # quests for first 12 hours
            titans = Adventure.check_titan_status()
            if titans:
                for titan in titans:
                    Adventure.kill_titan(titan)
            Inventory.boost_cube()
            Questing.questing()
            time.sleep(3)
        else:  # after hour 12, do itopod in 5-minute intervals
            titans = Adventure.check_titan_status()
            if titans:
                for titan in titans:
                    Adventure.kill_titan(titan)
            Adventure.itopod_snipe(300)
            Inventory.boost_cube()
