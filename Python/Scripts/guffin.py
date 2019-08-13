"""Guffin script."""

# Helper classes
from classes.features import Features
from classes.window import Window
from classes.wishes import Wishes

import coordinates as coords
import time


class Guffin(Features):
    """Guffin run class."""

    def __init__(self, wish_slots, wish_min_time):
        """Get breakdowns for wishes."""
        ##############
        # EDIT BELOW #
        ##############
        self._max_rb_duration = 1800  # How long in seconds you want to run
        self._zone = 3  # The zone number in which you want to do minor quests (for farming specific guffs)
        self._hacks = [2, 9, 11, 13, 14]  # Adv, QP, Exp, PP, Hack
        self._diggers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # All
        self._butter = True  # Butter majors? True/False
        self._aug = ["EB", "CS"]  # Which aug/upgrade to use, see naming convention in augments() in features.py
        #####################
        # DO NOT EDIT BELOW #
        #####################
        print("If you want to use muffins, use them manually. You can eat several muffins at once to extend the duration above 24 hours.")
        input("Press enter to rebirth and start script. ")
        self._wishes = Wishes(wish_slots, wish_min_time)
        lst = [self._wishes.epow, self._wishes.mpow, self._wishes.rpow]
        i = 0
        while 1 in lst:
            print("OCR reading failed for stat breakdowns, trying again...")
            self._wishes = Wishes(wish_slots, wish_min_time)
            i += 1
            if i > 5:
                print("Wishes will be disabled.")
                self._wishes = None
                break

        self.runs = 0
        self.do_rebirth()
        self.run()

    def __update_gamestate(self):
        """Update relevant state information."""
        self._rb_time = self.rt_to_seconds()
        self._advanced_training_locked = True
        try:
            self._current_boss = int(self.get_current_boss())
        except ValueError:
            self._current_boss = 1
            print("couldn't get current boss")

        if self._advanced_training_locked:
            self._advanced_training_locked = self.check_pixel_color(*coords.COLOR_ADV_TRAINING_LOCKED)

    def __do_quest(self):
        """Get the amount of available major quests."""
        text = self.get_quest_text().lower()
        majors = self.get_available_majors()
        if majors == 0 and (coords.QUESTING_MINOR_QUEST in text or coords.QUESTING_NO_QUEST_ACTIVE in text):
            self.questing(duration=2, force=self._zone)
        else:
            if not self.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                self.click(*coords.QUESTING_USE_MAJOR)
            self.questing(duration=2, butter=self._butter)

    def run(self):
        """Rebirth procedure"""
        self.__update_gamestate()
        self.nuke()
        time.sleep(2)
        self.adventure(highest=True)
        self.toggle_auto_spells(number=False, drop=False)
        self.gold_diggers(self._diggers)
        self.blood_magic(8)
        self.cap_ngu()
        self.cap_ngu(magic=True)
        self.set_wandoos(0)
        self.wandoos(True)
        self.augments({self._aug[0]: 0.66, self._aug[1]: 0.34}, self.get_idle_cap(1) * 0.5)
        self.time_machine(self.get_idle_cap(1) * 0.1, magic=True)
        self.__update_gamestate()
        self.toggle_auto_spells(drop=False, gold=False)
        self.hacks(self._hacks, self.get_idle_cap(3))
        if self._wishes:
            self._wishes.get_caps()
            self._wishes.allocate_wishes()

        while self._advanced_training_locked:
            self.__do_quest()
            self.nuke()
            self.gold_diggers(self._diggers)
            self.cap_ngu()
            self.cap_ngu(magic=True)
            self.hacks(self._hacks, self.get_idle_cap(3))
            self.augments({self._aug[0]: 0.66, self._aug[1]: 0.34}, self.get_idle_cap(1) * 0.5)
            self.time_machine(coords.INPUT_MAX, magic=True)
            self.__update_gamestate()

        self.adventure(highest=True)
        self.reclaim_tm(True)
        self.reclaim_aug()
        self.advanced_training(2e12)
        self.set_wandoos(1)
        self.wandoos(True)
        self.augments({self._aug[0]: 0.66, self._aug[1]: 0.34}, self.get_idle_cap(1) * 0.5)

        while self._rb_time < self._max_rb_duration - 140:
            self.gold_diggers(self._diggers)
            self.nuke()
            self.hacks(self._hacks, self.get_idle_cap(3))
            self.__do_quest()
            self.__update_gamestate()

        self.nuke()
        self.fight()
        self.adventure(itopodauto=True)
        self.pit()
        self.save_check()
        while self._rb_time < self._max_rb_duration:
            time.sleep(1)
            self.__update_gamestate()

        self.do_rebirth()
        self.runs += 1
        time.strftime('%H:%M:%S', time.gmtime(12345))
        print(f"Completed guffin run #{self.runs} in {time.strftime('%H:%M:%S', time.gmtime(self._rb_time))}")


w = Window()
feature = Features()
Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")
guffin = Guffin(4, 218)

while True:
    guffin.run()
