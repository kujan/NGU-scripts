"""24-hour rebirth script."""

# Helper classes
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window

import coordinates as coords
import time


def start_procedure(f, rt):
    """Procedure that handles start of rebirth."""
    f.send_string("r")  # make sure we reset e/m if we run this mid-rebirth
    f.send_string("t")
    f.nuke(101)  # PPP
    f.loadout(2)  # respawn loadout with equipment set 2
    f.adventure(highest=True)
    f.time_machine(5e11, magic=True)
    f.augments({"CI": 0.7, "ML": 0.3}, 1e12)
    f.blood_magic(8)
    f.toggle_auto_spells()
    f.gold_diggers([x for x in range(1, 13)])

    if rt >= 13*60:
        print("assigning adv training")
    else:
        duration = 12.5*60 - rt
        print(f"doing itopod for {duration} seconds while waiting for adv training to activate")
        f.itopod_snipe(duration)

    f.advanced_training(2e12)
    f.gold_diggers([x for x in range(1, 13)])
    f.reclaim_bm()
    f.wandoos(True)
    f.assign_ngu(f.get_idle_cap(1), [x for x in range(1, 10)])
    f.assign_ngu(f.get_idle_cap(2), [x for x in range(1, 8)], True)
    #f.hacks(list(range(1, 16)), f.get_idle_cap(3))

w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")
rt = feature.rt_to_seconds()
start_procedure(feature, rt)

max_rb_time = 24*60*60
if feature.get_fertilizer():
    max_rb_time = 23*60*60

while True:
    rt = feature.rt_to_seconds()
    feature.nuke()
    feature.gold_diggers([x for x in range(1, 13)])
    feature.merge_inventory(8)  # merge uneqipped guffs
    spells = feature.check_spells_ready()
    if spells:  # check if any spells are off CD
        feature.reclaim_ngu(True)  # take all magic from magic NGUs
        for spell in spells:
            feature.cast_spell(spell)
        feature.reclaim_bm()
        feature.assign_ngu(feature.get_idle_cap(2), [x for x in range(1, 8)], True)
        feature.toggle_auto_spells()  # retoggle autospells

    if rt > max_rb_time:  # rebirth is at >24 hours
        print(f"rebirthing at {feature.get_rebirth_time()}")  # debug
        feature.nuke()
        feature.spin()
        feature.deactivate_all_diggers()
        feature.ygg(equip=1)  # harvest with equipment set 1
        feature.ygg(eat_all=True)
        feature.level_diggers()  # level all diggers
        feature.do_rebirth()
        time.sleep(3)
        rt = feature.rt_to_seconds()
        start_procedure(feature, rt)
    else:
        feature.ygg()
        feature.save_check()
        feature.pit()
        if rt <= 12*60*60:  # quests for first 12 hours
            feature.boost_cube()
            feature.questing()
        else:  # after hour 12, do itopod in 5-minute intervals
            feature.itopod_snipe(300)
            feature.boost_cube()
