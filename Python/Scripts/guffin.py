"""Guffin script."""

# Helper classes
from classes.features import Features
from classes.window import Window
from classes.wishes import Wishes

import argparse

import coordinates as coords
import time


class Guffin(Features):
    """Guffin run class."""

    def __init__(self, wish_slots, wish_min_time, Butter):
        """Get breakdowns for wishes."""
        ##############
        # EDIT BELOW #
        ##############
        self._max_rb_duration = 1800  # How long in seconds you want to run
        self._zone = 2  # The zone number in which you want to do minor quests (for farming specific guffs)
        #self._hacks = [1, 2, 3, 6, 7, 9, 13, 14, 15]  # stats, adv, TM, NGU E, NGU M, QP, PP, hack, Wish
        self._hacks = [13]
        self._diggers = [1, 2, 3, 4, 5, 6, 9, 10, 11, 12]  # All but beards
        self._butter = Butter  # Butter majors? True/False
        self._aug = ["EB", "CS"]  # Which aug/upgrade to use, see naming convention in augments() in features.py
        self._allocate_wishes = True  # Do you wish to allocate resources to wishes? True/False
        #self._muffins = input("Would you like to have the script automatically use muffins?\n")
        #####################
        # DO NOT EDIT BELOW #
        #####################
        self._wishes = None
        if self._allocate_wishes:
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
        print('majors available : {0}'.format(majors))
        if majors == 0 and (coords.QUESTING_MINOR_QUEST in text or coords.QUESTING_NO_QUEST_ACTIVE in text):
            self.questing(duration=2, force=self._zone)
        else:
            if not self.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                self.click(*coords.QUESTING_USE_MAJOR)
            self.questing(duration=2, butter=self._butter)

    def run(self):
        """Rebirth procedure."""
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
        self.time_machine(self.get_idle_cap(1) * 0.1, self.get_idle_cap(2) * 0.1, True)
        self.__update_gamestate()
        self.toggle_auto_spells(drop=False, gold=False)
        
        while self._advanced_training_locked:
            self.__do_quest()
            self.nuke()
            self.gold_diggers(self._diggers)
            self.cap_ngu()
            self.cap_ngu(magic=True)
            #self.hacks(self._hacks[1], self.get_idle_cap(3) * len(self._hacks)) # too early for more than 1 hack
            self.augments({self._aug[0]: 0.66, self._aug[1]: 0.34}, self.get_idle_cap(1) * 0.5)
            self.time_machine(self.get_idle_cap(2), magic=True)
            self.__update_gamestate()
        
        self.adventure(highest=True)
        self.reclaim_tm(True)
        self.reclaim_tm()
        self.reclaim_aug()
        self.advanced_training(8e10)
        self.set_wandoos(1)
        self.wandoos(True)
        self.augments({self._aug[0]: 0.66, self._aug[1]: 0.34}, self.get_idle_cap(1) * 0.1)

        while self._rb_time < self._max_rb_duration / 2:
            self.gold_diggers(self._diggers)
            self.nuke()
            #self.hacks(self._hacks, self.get_idle_cap(3) * len(self._hacks))
            self.wandoos(True)
            self.cap_ngu()
            self.cap_ngu(magic=True)
            self.__do_quest()
            self.__update_gamestate()

        if self._wishes:
            self._wishes.get_caps()
            self._wishes.get_wish_status()
            self._wishes.allocate_wishes()
        
        while self._rb_time < self._max_rb_duration - 140:
            self.gold_diggers(self._diggers)
            self.nuke()
            #self.hacks(self._hacks, self.get_idle_cap(3) * len(self._hacks))
            self.wandoos(True)
            self.cap_ngu()
            self.cap_ngu(magic=True)
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
        #if self._muffins:
        #    self.eat_muffin();
        self.do_rebirth()
        self.runs += 1
        time.strftime('%H:%M:%S', time.gmtime(12345))
        print(f"Completed guffin run #{self.runs} in {time.strftime('%H:%M:%S', time.gmtime(self._rb_time))}")
    #_____________________________________________________________________________________    
    #Own code:    
    def test(self):
        self.__update_gamestate()
        time.sleep(2)
        self.cap_ngu()
        self.cap_ngu(magic=True)
        self.wandoos(True)
        self.hacks(self._hacks, self.get_idle_cap(3) * len(self._hacks))
        self.advanced_training(8e10)
        self.time_machine(self.get_idle_cap(1), self.get_idle_cap(2), True)
        self.__do_quest()
        
#________________________________________________________________________________________________
#Testable code
w = Window()
feature = Features()
parser = argparse.ArgumentParser()
Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")
parser.add_argument("-r", "--repeat", required=True, type=int, help="Select how many runs you would like to perform")
parser.add_argument("-b", "--Butter", required=True, type=bool, help="Do you want to use butters?")
try:
    args = parser.parse_args()
except:
    print("\nNo arguments passed. will only do one guff run! Kill the code with Ctrl+C to cancel")
    for i in range(0, 10):
        print("starting in {0}".format(10-i))
        time.sleep(1)
    args = parser.parse_args(['--repeat', '0', '--Butter', False])
guffin = Guffin(4, 230, args.Butter)
print(args)
#own code:
#guffin.test()


while guffin.runs < args.repeat:
   guffin.run()
