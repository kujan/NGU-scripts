"""Feature class handles the different features in the game."""
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window
from collections import deque, namedtuple
from decimal import Decimal
from deprecated import deprecated
import coordinates as coords
import datetime
import math
import re
import time
import win32con as wcon
import win32gui
import usersettings as userset


class Features(Navigation, Inputs):
    """Handles the different features in the game."""

    current_adventure_zone = 0
    inventory_cleaned = False

    def merge_equipment(self):
        """Navigate to inventory and merge equipment."""
        self.menu("inventory")
        for slot in coords.EQUIPMENT_SLOTS:
            if (slot == "cube"):
                return
            self.click(*coords.EQUIPMENT_SLOTS[slot])
            self.send_string("d")

    def boost_equipment(self):
        """Boost all equipment."""
        self.menu("inventory")
        for slot in coords.EQUIPMENT_SLOTS:
            if (slot == "cube"):
                self.click(*coords.EQUIPMENT_SLOTS[slot], "right")
                return
            self.click(*coords.EQUIPMENT_SLOTS[slot])
            self.send_string("a")

    def boost_cube(self):
        """Boost cube."""
        self.menu("inventory")
        self.click(*self.equipment["cube"], "right")

    def get_current_boss(self):
        """Go to fight and read current boss number."""
        self.menu("fight")
        boss = self.ocr(*coords.OCR_BOSS, debug=False)
        return self.remove_letters(boss)

    def nuke(self, boss=None):
        """Navigate to Fight Boss and Nuke or Fast Fight."""
        self.menu("fight")
        if boss:
            for i in range(boss):
                self.click(*coords.FIGHT, fast=True)
            time.sleep(userset.SHORT_SLEEP)
            try:
                current_boss = int(self.get_current_boss())
            except ValueError:
                current_boss = 1
            x = 0
            while current_boss < boss:
                bossdiff = boss - current_boss
                for i in range(0, bossdiff):
                    self.click(*coords.FIGHT, fast=True)
                time.sleep(userset.SHORT_SLEEP)
                try:
                    current_boss = int(self.get_current_boss())
                except ValueError:
                    current_boss = 1
                x += 1
                if x > 7:  # Safeguard if number is too low to reach target boss, otherwise we get stuck here
                    print("Couldn't reach the target boss, something probably went wrong the last rebirth.")
                    break
        else:
            self.click(*coords.NUKE)

    def fight(self):
        """Navigate to Fight Boss and click fight."""
        self.menu("fight")
        self.click(*coords.FIGHT)

    def ygg(self, eat_all=False, equip=0):
        """Navigate to inventory and handle fruits.

        Keyword arguments:
        rebirth -- Set to true if you're rebirthing, it will force eat all
                   fruit.
        """
        self.menu("yggdrasil")
        if eat_all:
            self.click(*coords.YGG_EAT_ALL)
            return
        if equip:
            self.send_string("t")
            self.send_string("r")
            self.loadout(equip)
            self.menu("yggdrasil")
            self.click(*coords.HARVEST)
        else:
            self.click(*coords.HARVEST)

    def spin(self):
        """Spin the wheel."""
        self.menu("pit")
        self.click(*coords.SPIN_MENU)
        self.click(*coords.SPIN)

    def adventure(self, zone=0, highest=True, itopod=None, itopodauto=False):
        """Go to adventure zone to idle.

        Keyword arguments
        zone -- Zone to idle in, 0 is safe zone, 1 is tutorial and so on.
        highest -- If true, will go to your highest available non-titan zone.
        itopod -- If set to true, it will override other settings and will
                  instead enter the specified ITOPOD floor.
        itopodauto -- If set to true it will click the "optimal" floor button.
        """
        self.menu("adventure")
        self.click(625, 500)  # click somewhere to move tooltip
        if not self.check_pixel_color(*coords.IS_IDLE):
            self.click(*coords.ABILITY_IDLE_MODE)
        if itopod:
            self.current_adventure_zone = 0
            self.click(*coords.ITOPOD)
            if itopodauto:
                self.click(*coords.ITOPOD_END)
                # set end to 0 in case it's higher than start
                self.send_string("0")
                self.click(*coords.ITOPOD_AUTO)
                self.click(*coords.ITOPOD_ENTER)
                return
            self.click(*coords.ITOPOD_START)
            self.send_string(str(itopod))
            self.click(*coords.ITOPOD_END)
            self.send_string(str(itopod))
            self.click(*coords.ITOPOD_ENTER)
            return
        if highest:
            self.current_adventure_zone = 0
            self.click(*coords.RIGHT_ARROW, button="right")
            return
        else:
            self.current_adventure_zone = zone
            self.click(*coords.LEFT_ARROW, button="right")
            for i in range(zone):
                self.click(*coords.RIGHT_ARROW)
            return

    def snipe(self, zone, duration, once=False, highest=False, bosses=False, manual=False):
        """Go to adventure and snipe bosses in specified zone.

        Keyword arguments
        zone -- Zone to snipe, 0 is safe zone, 1 is turorial and so on.
                If 0, it will use the current zone (to maintain guffin counter)
        duration -- The duration in minutes the sniping will run before
                    returning.
        once -- If true it will only kill one boss before returning.
        highest -- If set to true, it will go to your highest available
                   non-titan zone.
        bosses -- If set to true, it will only kill bosses
        manual -- If set to true it will use all available abilities to kill the enemy.
                  In addition it will return after killing one enemy.
        """
        self.menu("adventure")
        if highest:
            self.click(*coords.LEFT_ARROW, button="right")
            self.click(*coords.RIGHT_ARROW, button="right")
        elif zone > 0 and zone != self.current_adventure_zone:
            self.click(*coords.LEFT_ARROW, button="right")
            for i in range(zone):
                self.click(*coords.RIGHT_ARROW)
        self.current_adventure_zone = zone
        self.click(625, 500)  # click somewhere to move tooltip

        if self.check_pixel_color(*coords.IS_IDLE):
            self.click(*coords.ABILITY_IDLE_MODE)

        end = time.time() + duration * 60
        while time.time() < end:
            self.click(625, 500)  # click somewhere to move tooltip
            if not self.check_pixel_color(*coords.IS_DEAD):
                if bosses:
                    if self.check_pixel_color(*coords.IS_BOSS_CROWN):
                        enemy_alive = True
                        if manual:
                            self.kill_enemy()
                        else:
                            while enemy_alive:
                                enemy_alive = not self.check_pixel_color(*coords.IS_DEAD)
                                self.click(*coords.ABILITY_REGULAR_ATTACK)
                                time.sleep(0.1)
                        if once:
                            break
                    else:
                        # Send left arrow and right arrow to refresh monster.
                        win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN,
                                             wcon.VK_LEFT, 0)
                        time.sleep(0.05)
                        win32gui.PostMessage(Window.id, wcon.WM_KEYUP,
                                             wcon.VK_LEFT, 0)
                        time.sleep(0.05)
                        win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN,
                                             wcon.VK_RIGHT, 0)
                        time.sleep(0.05)
                        win32gui.PostMessage(Window.id, wcon.WM_KEYUP,
                                             wcon.VK_RIGHT, 0)
                else:
                    if manual:
                        self.kill_enemy()
                        return
                    else:
                        self.click(*coords.ABILITY_REGULAR_ATTACK)
            time.sleep(0.01)

        self.click(*coords.ABILITY_IDLE_MODE)

    def itopod_snipe(self, duration):
        """Manually snipes ITOPOD for increased speed PP/h.

        Keyword arguments:
        duration -- Duration in seconds to snipe, before toggling idle mode
                    back on and returning.
        """
        end = time.time() + duration
        self.current_adventure_zone = 0
        self.menu("adventure")
        self.click(625, 500)  # click somewhere to move tooltip

        # check if we're already in ITOPOD, otherwise enter
        if not self.check_pixel_color(*coords.IS_ITOPOD_ACTIVE):
            self.click(*coords.ITOPOD)
            self.click(*coords.ITOPOD_END)
            # set end to 0 in case it's higher than start
            self.send_string("0")
            self.click(*coords.ITOPOD_AUTO)
            self.click(*coords.ITOPOD_ENTER)

        if self.check_pixel_color(*coords.IS_IDLE):
            self.click(*coords.ABILITY_IDLE_MODE)

        while time.time() < end:
            if self.check_pixel_color(*coords.IS_ENEMY_ALIVE):
                self.click(*coords.ABILITY_REGULAR_ATTACK)
            else:
                time.sleep(0.01)

        self.click(*coords.ABILITY_IDLE_MODE)

    def kill_enemy(self):
        """Attempt to kill enemy in adventure using abilities."""
        start = time.time()
        if self.check_pixel_color(*coords.IS_IDLE):
            self.click(*coords.ABILITY_IDLE_MODE)
        while self.check_pixel_color(*coords.IS_DEAD):
            time.sleep(.1)
            if time.time() > start + 5:
                print("Couldn't detect enemy in kill_enemy()")
                return
        queue = deque(self.get_ability_queue())
        while not self.check_pixel_color(*coords.IS_DEAD):
            if len(queue) == 0:
                queue = deque(self.get_ability_queue())
            ability = queue.popleft()
            if ability <= 4:
                x = coords.ABILITY_ROW1X + ability * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW1Y

            if ability >= 5 and ability <= 10:
                x = coords.ABILITY_ROW2X + (ability - 5) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW2Y

            if ability > 10:
                x = coords.ABILITY_ROW3X + (ability - 11) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW3Y

            self.click(x, y)
            time.sleep(userset.LONG_SLEEP)
            color = self.get_pixel_color(coords.ABILITY_ROW1X,
                                         coords.ABILITY_ROW1Y)

            while color != coords.ABILITY_ROW1_READY_COLOR:
                time.sleep(0.03)
                color = self.get_pixel_color(coords.ABILITY_ROW1X,
                                             coords.ABILITY_ROW1Y)

    def do_rebirth(self):
        """Start a rebirth or challenge."""
        self.rebirth()
        self.current_adventure_zone = 0
        self.click(*coords.REBIRTH)
        self.click(*coords.REBIRTH_BUTTON)
        self.click(*coords.CONFIRM)
        return

    def check_challenge(self):
        """Check if a challenge is active."""
        self.rebirth()
        self.click(*coords.CHALLENGE_BUTTON)
        time.sleep(userset.LONG_SLEEP)
        return True if self.check_pixel_color(*coords.COLOR_CHALLENGE_ACTIVE) else False

    def pit(self, loadout=0):
        """Throws money into the pit.

        Keyword arguments:
        loadout -- The loadout you wish to equip before throwing gold
                   into the pit, for gear you wish to shock. Make
                   sure that you don't get cap-blocked by either using
                   the unassign setting in the game or swapping gear that
                   doesn't have e/m cap.
        """
        if self.check_pixel_color(*coords.IS_PIT_READY):
            if loadout:
                self.loadout(loadout)
            self.menu("pit")
            self.click(*coords.PIT)
            self.click(*coords.CONFIRM)

    def augments(self, augments, energy):
        """Dump energy into augmentations.

        Keyword arguments
        augments -- Dictionary that contains which augments you wish to use and
                    a ratio that tells how much of the total energy you
                    allocated you wish to send. Example:
                    {"SS": 0, "DS": 0, "MI": 0, "DTMT": 0, "CI": 0, "M": 0,
                     "SM": 0, "AA": 0, "EB": 0, "CS": 0, "AE": 0, "ES": 0,
                     "LS": 0.9, "QSL": 0.1}
        Energy -- The total amount of energy you want to use for all augments.
        """
        self.menu("augmentations")
        for k in augments:
            val = math.floor(augments[k] * energy)
            self.input_box()
            self.send_string(str(val))
            # Scroll down if we have to.
            bottom_augments = ["AE", "ES", "LS", "QSL"]
            i = 0
            if (k in bottom_augments):
                color = self.get_pixel_color(*coords.AUG_SCROLL_SANITY_BOT)
                while color not in coords.SANITY_AUG_SCROLL_COLORS:
                    self.click(*coords.AUG_SCROLL_BOT)
                    time.sleep(userset.MEDIUM_SLEEP)
                    color = self.get_pixel_color(*coords.AUG_SCROLL_SANITY_BOT)
                    i += 1
                    if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
                        Navigation.current_menu = ""
                        self.menu("augmentations")
                    elif i > 10:
                        print("Couldn't assign augments")
                        break

            else:
                color = self.get_pixel_color(*coords.AUG_SCROLL_SANITY_TOP)
                while color not in coords.SANITY_AUG_SCROLL_COLORS:
                    self.click(*coords.AUG_SCROLL_TOP)
                    time.sleep(userset.MEDIUM_SLEEP)
                    color = self.get_pixel_color(*coords.AUG_SCROLL_SANITY_TOP)
                    i += 1
                    if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
                        Navigation.current_menu = ""
                        self.menu("augmentations")
                    elif i > 10:
                        print("Couldn't assign augments")
                        break
            self.click(*coords.AUGMENT[k])

    def time_machine(self, e, m=0, magic=False):
        """Add energy and/or magic to TM.

        Example: self.time_machine(1000, 2000)
                 self.time_machine(1000, magic=True)
                 self.time_machine(1000)

        First example will add 1000 energy and 2000 magic to TM.
        Second example will add 1000 energy and 1000 magic to TM.
        Third example will add 1000 energy to TM.

        Keyword arguments:
        e -- The amount of energy to put into TM.
        m -- The amount of magic to put into TM, if this is 0, it will use the
             energy value to save unnecessary clicks to the input box.
        magic -- Set to true if you wish to add magic as well
        """
        self.menu("timemachine")
        self.input_box()
        self.send_string(e)
        self.click(*coords.TM_SPEED)
        if magic or m:
            if m:
                self.input_box()
                self.send_string(m)
            self.click(*coords.TM_MULT)

    def blood_magic(self, target):
        """Assign magic to BM."""
        self.menu("bloodmagic")
        for i in range(target):
            self.click(*coords.BM[i])

    def wandoos(self, magic=False):
        """Assign energy and/or magic to wandoos."""
        self.menu("wandoos")
        self.click(*coords.WANDOOS_ENERGY)
        if magic:
            self.click(*coords.WANDOOS_MAGIC)

    def set_wandoos(self, version):
        """Set wandoos version.

        Keyword arguments:
        version -- 0 = Wandoos, 1 = Meh, 2 = XL"""
        self.menu("wandoos")
        self.click(*coords.WANDOOS_VERSION[version])
        self.confirm()

    def loadout(self, target):
        """Equip targeted loadout."""
        self.menu("inventory")
        self.click(*coords.LOADOUT[target])

    @deprecated(version='0.1', reason="speedrun_bloodpill is deprecated, use iron_pill() instead")
    def speedrun_bloodpill(self):
        return

    @deprecated(version='0.1', reason="iron_pill is deprecated, use cast_spell() instead")
    def iron_pill(self):
        return

    def toggle_auto_spells(self, number=True, drop=True, gold=True):
        """Check and toggle autospells according to booleans."""
        self.spells()
        self.click(600, 600)  # move tooltip
        number_active = self.check_pixel_color(*coords.COLOR_BM_AUTO_NUMBER)
        drop_active = self.check_pixel_color(*coords.COLOR_BM_AUTO_DROP)
        gold_active = self.check_pixel_color(*coords.COLOR_BM_AUTO_GOLD)

        if (number and not number_active) or (not number and number_active):
            self.click(*coords.BM_AUTO_NUMBER)
        if (drop and not drop_active) or (not drop and drop_active):
            self.click(*coords.BM_AUTO_DROP)
        if (gold and not gold_active) or (not gold and gold_active):
            self.click(*coords.BM_AUTO_GOLD)

    def check_spells_ready(self):
        """Check which spells are ready to cast.

        returns a list with integers corresponding to which spell is ready.
        1 - Iron pill
        2 - MacGuffin alpha
        3 - MacGuffin beta
        """
        if self.check_pixel_color(*coords.COLOR_SPELL_READY):
            self.spells()
            self.click(*coords.BM_PILL, button="right")
            spells = []
            res = self.ocr(*coords.OCR_BM_SPELL_TEXT)
            if "cooldown: 0.0s" in res.lower():
                spells.append(1)

            self.click(*coords.BM_GUFFIN_A, button="right")
            res = self.ocr(*coords.OCR_BM_SPELL_TEXT)
            if "cooldown: 0.0s" in res.lower():
                spells.append(2)

            self.click(*coords.BM_GUFFIN_B, button="right")
            res = self.ocr(*coords.OCR_BM_SPELL_TEXT)
            if "cooldown: 0.0s" in res.lower():
                spells.append(3)

            return spells
        else:
            return []

    def cast_spell(self, target):
        """Cast target spell.

        This method will allocate any idle magic into BM and wait for the
        time set in usersettings.py. Remember to re-enable auto spells after
        calling this method, using toggle_auto_spells().

        1 - Iron pill
        2 - MacGuffin alpha
        3 - MacGuffin beta
        """
        if self.check_pixel_color(*coords.COLOR_SPELL_READY):
            targets = [0, coords.BM_PILL, coords.BM_GUFFIN_A, coords.BM_GUFFIN_B]
            start = time.time()
            self.blood_magic(8)
            self.toggle_auto_spells(False, False, False)  # disable all auto spells

            if userset.SPELL == 0:  # Default to 5 mins if not set
                duration = 300
            else:
                duration = userset.SPELL

            while time.time() < start + duration:
                print(f"Sniping itopod for {duration} seconds while waiting to cast spell.")
                self.itopod_snipe(duration)
            self.spells()
            self.click(*targets[target])

    def reclaim_bm(self):
        """Remove all magic from BM."""
        self.menu("bloodmagic")
        self.input_box()
        self.send_string(coords.INPUT_MAX)
        for coord in coords.BM_RECLAIM:
            self.click(*coord)

    def reclaim_ngu(self, magic=False):
        """Remove all e/m from NGUs."""
        if magic:
            self.ngu_magic()
        else:
            self.menu("ngu")
        self.input_box()
        self.send_string(coords.INPUT_MAX)
        for i in range(1, 10):
            NGU = coords.Pixel(coords.NGU_MINUS.x, coords.NGU_PLUS.y + i * 35)
            self.click(*NGU)

    def reclaim_tm(self, magic=False):
        """Remove all e/m from TM."""
        self.menu("timemachine")
        self.input_box()
        self.send_string(coords.INPUT_MAX)
        if magic:
            self.click(*coords.TM_MULT_MINUS)
            return
        self.click(*coords.TM_SPEED_MINUS)

    def reclaim_aug(self):
        """Remove all energy from augs"""
        self.menu("augmentations")
        self.input_box()
        self.send_string(coords.INPUT_MAX)
        self.click(*coords.AUG_SCROLL_TOP)
        scroll_down = False
        for i, k in enumerate(coords.AUGMENT.keys()):
            if i >= 10 and not scroll_down:
                self.click(*coords.AUG_SCROLL_BOT)
                self.click(*coords.AUG_SCROLL_BOT)
                time.sleep(1)
                scroll_down = True
            self.click(coords.AUG_MINUS_X, coords.AUGMENT[k].y)

    def assign_ngu(self, value, targets, magic=False):
        """Assign energy/magic to NGU's.

        Keyword arguments:
        value -- the amount of energy/magic that will get split over all NGUs.
        targets -- Array of NGU's to use (1-9).
        magic -- Set to true if these are magic NGUs
        """
        if len(targets) > 9:
            raise RuntimeError("Passing too many NGU's to assign_ngu," +
                               " allowed: 9, sent: " + str(len(targets)))
        if magic:
            self.ngu_magic()
        else:
            self.menu("ngu")

        self.input_box()
        self.send_string(value // len(targets))
        for i in targets:
            NGU = coords.Pixel(coords.NGU_PLUS.x, coords.NGU_PLUS.y + i * 35)
            self.click(*NGU)

    def gold_diggers(self, targets, deactivate=False):
        """Activate diggers.

        Keyword arguments:
        targets -- Array of diggers to use from 1-12. Example: [1, 2, 3, 4, 9].
        deactivate -- Set to True if you wish to deactivate these
                    diggers otherwise it will just try to up the cap.
        """
        self.menu("digger")
        for i in targets:
            page = ((i-1)//4)
            item = i - (page * 4)
            self.click(*coords.DIG_PAGE[page])
            if deactivate:
                self.click(*coords.DIG_ACTIVE[item])
            else:
                self.click(*coords.DIG_CAP[item])

    def deactivate_all_diggers(self):
        """Click deactivate all in digger menu."""
        self.menu("digger")
        self.click(*coords.DIG_DEACTIVATE_ALL)

    def level_diggers(self):
        """Level all diggers."""
        self.menu("digger")
        for page in coords.DIG_PAGE:
            self.click(*page)
            for digger in coords.DIG_LEVEL:
                self.click(*digger, button="right")

    @deprecated(version='0.1', reason="bb_ngu() is deprecated since .415 use cap_ngu() instead")
    def bb_ngu(self, value, targets, overcap=1, magic=False):
        """Estimates the BB value of each supplied NGU.

        It will send value into the target NGU's, which will fill the progress bar. It's very
        important that you put enough e/m into the NGU's to trigger the "anti-flicker" (>10% of BB cost),
        otherwise it will not function properly.

        Keyword arguments:
        value -- The amount of energy used to determine the cost of BBing the target NGU's
        targets -- Array of NGU's to BB. Example: [1, 3, 4, 5, 6]
        overcap -- Use this if you wish to assign more e/m than absolute minimum to BB
                   the NGU's. This might be useful for longer runs to make sure the cost
                   to BB doesn't exceed the assigned e/m. A value of 1.1 assigns 10% extra.
        magic -- Set to true if these are magic NGUs
        """
        if magic:
            self.ngu_magic()
        else:
            self.menu("ngu")

        self.input_box()
        self.send_string(str(int(value)))

        for target in targets:
            NGU = coords.Pixel(coords.NGU_PLUS.x, coords.NGU_PLUS.y + target * 35)
            self.click(*NGU)

        for target in targets:
            energy = 0
            for x in range(198):
                color = self.get_pixel_color(coords.NGU_BAR_MIN.x + x,
                                             coords.NGU_BAR_MIN.y +
                                             coords.NGU_BAR_OFFSET_Y * target,
                                             )
                if color == coords.NGU_BAR_WHITE:
                    pixel_coefficient = x / 198
                    value_coefficient = overcap / pixel_coefficient
                    energy = (value_coefficient * value) - value
                    break
            if energy == 0:
                if magic:
                    print(f"Warning: You might be overcapping magic NGU #{target}")
                else:
                    print(f"Warning: You might be overcapping energy NGU #{target}")
                continue

            self.input_box()
            self.send_string(str(int(energy)))
            self.click(coords.NGU_PLUS.x, coords.NGU_PLUS.y + target * 35)

    def cap_ngu(self, targets=[], magic=False, cap_all=True):
        """Cap NGU's.

        Keyword arguments
        targets -- The NGU's you wish to cap
        magic -- Set to true if these are magic NGU's
        cap_all -- Set to true if you wish to cap all NGU's

        """
        if magic:
            self.ngu_magic()
        else:
            self.menu("ngu")

        for target in targets:
            NGU = coords.Pixel(coords.NGU_CAP.x, coords.NGU_CAP.y + target * 35)
            self.click(*NGU)

        if cap_all and not targets:
            self.click(*coords.NGU_CAP_ALL)

    def set_ngu_overcap(self, value):
        """Set the amount you wish to overcap your NGU's."""
        self.menu("ngu")
        self.click(*coords.NGU_OVERCAP)
        self.send_string(value)

    # TODO: make this actually useful for anything
    def advanced_training(self, value):
        """Assign energy to adventure power/thoughness and wandoos."""
        self.menu("advtraining")
        value = value // 4
        self.input_box()
        self.send_string(value)
        self.click(*coords.ADV_TRAINING_POWER)
        self.click(*coords.ADV_TRAINING_TOUGHNESS)
        self.click(*coords.ADV_TRAINING_WANDOOS_ENERGY)
        self.click(*coords.ADV_TRAINING_WANDOOS_MAGIC)

    def titan_pt_check(self, target):
        """Check if we have the recommended p/t to defeat the target Titan.

        Keyword arguments:
        target -- The name of the titan you wish to kill. ["GRB", "GCT",
                  "jake", "UUG", "walderp", "BEAST1", "BEAST2", "BEAST3",
                  "BEAST4"]
        """
        self.menu("adventure")
        bmp = self.get_bitmap()
        power = self.ocr(*coords.OCR_ADV_POW, bmp=bmp)
        tough = self.ocr(*coords.OCR_ADV_TOUGH, bmp=bmp)

        if (float(power) > coords.TITAN_PT[target]["p"] and
           float(tough) > coords.TITAN_PT[target]["t"]):
            return True

        else:
            print(f"Lacking: {Decimal(coords.TITAN_PT[target]['p'] - float(power)):.2E}"
                  f"/{Decimal(coords.TITAN_PT[target]['t'] - float(tough)):.2E} P/T"
                  f" to kill {target}")
            return False

    def kill_titan(self, target):
        """Attempt to kill the target titan.

        Keyword arguments:
        target -- The name of the titan you wish to kill. ["GRB", "GCT",
                  "jake", "UUG", "walderp", "BEAST1", "BEAST2", "BEAST3",
                  "BEAST4"]
        """
        self.menu("adventure")
        if self.check_pixel_color(*coords.IS_IDLE):
            self.click(*coords.ABILITY_IDLE_MODE)

        self.click(*coords.LEFT_ARROW, button="right")
        for i in range(coords.TITAN_ZONE[target]):
            self.click(*coords.RIGHT_ARROW)
        self.current_adventure_zone = coords.TITAN_ZONE[target]
        time.sleep(userset.LONG_SLEEP)

        available = self.ocr(*coords.OCR_ADV_TITAN)

        if "titan" in available.lower():
            time.sleep(1.5)  # Make sure titans spawn, otherwise loop breaks
            queue = deque(self.get_ability_queue())
            while self.check_pixel_color(*coords.IS_ENEMY_ALIVE):
                if len(queue) == 0:
                    print("NEW QUEUE")
                    queue = deque(self.get_ability_queue())
                    print(queue)

                ability = queue.popleft()
                print(f"using ability {ability}")
                if ability <= 4:
                    x = coords.ABILITY_ROW1X + ability * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW1Y

                if ability >= 5 and ability <= 10:
                    x = coords.ABILITY_ROW2X + (ability - 5) * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW2Y

                if ability > 10:
                    x = coords.ABILITY_ROW3X + (ability - 11) * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW3Y

                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                color = self.get_pixel_color(coords.ABILITY_ROW1X,
                                             coords.ABILITY_ROW1Y)

                while color != coords.ABILITY_ROW1_READY_COLOR:
                    time.sleep(0.05)
                    color = self.get_pixel_color(coords.ABILITY_ROW1X,
                                                 coords.ABILITY_ROW1Y)

    def get_ability_queue(self):
        """Return a queue of usable abilities."""
        ready = []
        queue = []

        # Add all abilities that are ready to the ready array
        for i in range(13):
            if i <= 4:
                x = coords.ABILITY_ROW1X + i * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW1Y
                color = self.get_pixel_color(x, y)
                if color == coords.ABILITY_ROW1_READY_COLOR:
                    ready.append(i)
            if i >= 5 and i <= 10:
                x = coords.ABILITY_ROW2X + (i - 5) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW2Y
                if color == coords.ABILITY_ROW2_READY_COLOR:
                    ready.append(i)
            if i > 10:
                x = coords.ABILITY_ROW3X + (i - 11) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW3Y
                color = self.get_pixel_color(x, y)
                if color == coords.ABILITY_ROW3_READY_COLOR:
                    ready.append(i)

        # heal if we need to heal
        if self.check_pixel_color(*coords.PLAYER_HEAL_THRESHOLD):
            if 12 in ready:
                queue.append(12)
            elif 7 in ready:
                queue.append(7)

        # check if offensive buff and ultimate buff are both ready
        buffs = [8, 10]
        if all(i in ready for i in buffs):
            queue.extend(buffs)

        d = coords.ABILITY_PRIORITY
        # Sort the abilities by the set priority
        abilities = sorted(d, key=d.get, reverse=True)
        # Only add the abilities that are ready to the queue
        queue.extend([a for a in abilities if a in ready])

        # If nothing is ready, return a regular attack
        if len(queue) == 0:
            queue.append(0)
        return queue

    def save_check(self):
        """Check if we can do the daily save for AP.

        Make sure no window in your browser pops up when you click the "Save"
        button, otherwise sit will mess with the rest of the script.
        """
        if self.check_pixel_color(*coords.IS_SAVE_READY):
            self.click(*coords.SAVE)
        return

    def get_inventory_slots(self, slots):
        """Get coords for inventory slots from 1 to slots."""
        point = namedtuple("p", ("x", "y"))
        i = 1
        row = 1
        x_pos, y_pos = coords.INVENTORY_SLOTS
        res = []

        while i <= slots:
            x = x_pos + (i - (12 * (row - 1))) * 50
            y = y_pos + ((row - 1) * 50)
            res.append(point(x, y))
            if i % 12 == 0:
                row += 1
            i += 1
        return res

    def merge_inventory(self, slots):
        """Merge all inventory slots starting from 1 to slots.

        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        self.menu("inventory")
        coords = self.get_inventory_slots(slots)
        for slot in coords:
            self.click(*slot)
            self.send_string("d")

    def boost_inventory(self, slots):
        """Merge all inventory slots starting from 1 to slots.

        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        self.menu("inventory")
        coords = self.get_inventory_slots(slots)
        for slot in coords:
            self.click(*slot)
            self.send_string("a")

    def transform_slot(self, slot, threshold=0.8, consume=False):
        """Check if slot is transformable and transform if it is.

        Be careful using this, make sure the item you want to transform is
        not protected, and that all other items are protected, this might
        delete items otherwise. Another note, consuming items will show
        a special tooltip that will block you from doing another check
        for a few seconds, keep this in mind if you're checking multiple
        slots in succession.

        Keyword arguments:
        slot -- The slot you wish to transform, if possible
        threshold -- The fuzziness in the image search, I recommend a value
                     between 0.7 - 0.95.
        consume -- Set to true if item is consumable instead.
        """
        self.menu("inventory")
        slot = self.get_inventory_slots(slot)[-1]
        self.click(*slot)
        time.sleep(userset.SHORT_SLEEP)

        if consume:
            coords = self.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600,
                                       self.get_file_path("images", "consumable.png"), threshold)
        else:
            coords = self.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600,
                                       self.get_file_path("images", "transformable.png"), threshold)

        if coords:
            self.ctrl_click(*slot)

    def get_idle_cap(self, magic=False):
        """Get the available idle energy or magic."""
        try:
            if magic:
                res = self.ocr(*coords.OCR_MAGIC)
            else:
                res = self.ocr(*coords.OCR_ENERGY)
            match = re.search(r".*(\d+\.\d+E\+\d+)", res)
            if match is not None:
                return int(float(match.group(1)))
            elif match is None:
                return 0
        except ValueError:
            print("Couldn't get idle e/m")

    def get_quest_text(self):
        """Check if we have an active quest or not."""
        self.menu("questing")
        self.click(950, 590)  # move tooltip
        time.sleep(userset.SHORT_SLEEP)
        return self.ocr(*coords.OCR_QUESTING_LEFT_TEXT)

    def get_available_majors(self):
        self.menu("questing")
        text = self.ocr(*coords.OCR_QUESTING_MAJORS)
        try:
            match = re.search(r"(\d+)\/\d+", text)
            if match:
                return int(match.group(1))
        except ValueError:
            print("couldn't get current major quests available")
            return -1

    def questing_consume_items(self, cleanup=False):
        """Check for items in inventory that can be turned in."""
        self.menu("inventory")
        bmp = self.get_bitmap()
        for item in coords.QUESTING_FILENAMES:
            path = self.get_file_path("images", item)
            loc = self.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, path, 0.91, bmp=bmp)
            if loc:
                self.click(*loc, button="right")
                if cleanup:
                    self.send_string("d")
                    self.ctrl_click(*loc)
                time.sleep(3)  # Need to wait for tooltip to disappear after consuming

    def questing(self, duration=30, major=False, subcontract=False, force=0, adv_duration=2):
        """Procedure for questing.

        Keyword arguments:
        duration -- The duration in minutes to run if manual mode is selected. If
                    quest gets completed, function will return prematurely.
        major -- Set to true if you only wish to manually do main quests,
                if False it will manually do all quests.
        subcontract -- Set to True if you wish to subcontract all quests.
        force -- Only quest in this zone. This will skip quests until you
                 recieve one for the selected zone, so make sure you disable
                 "Use major quests if available".
        adv_duration -- The time in minutes to spend sniping before checking inventory.
                        A higher value is good when forcing, because you spend less time
                        scanning the inventory and you will not waste any extra quest items.
                        A value around 2 minutes is good when doing majors because it's very
                        likely that the extra items are lost.

        Suggested usages:

        questing(major=True)
        questing(subcontract=True)

        If you only wish to manually do major quests (so you can do ITOPOD)
        then I suggest that you only call questing() every 10-15 minutes because
        subcontracting takes very long to finish. Same obviously goes for subcontracting
        only.

        Remember the default duration is 40, which is there to safeguard if something
        goes wrong to break out of the function. Set this higher/lower after your own
        preferences.

        questing(duration=40)

        This will manually complete any quest you get for 30 minutes, then it returns,
        or it returns when the quest is completed.

        Use this together with harvesting ygg, recapping diggers and so on, or even
        sniping ITOPOD.

        ===== IMPORTANT =====

        This method uses imagesearch to find items in your inventory, it will
        both right click and ctrl-click items (quick delete keybind), so make
        sure all items are protected.

        The method will only check the inventory page that is currently open,
        so make sure it's set to page 1 and that your inventory has space.
        If your inventory fills with mcguffins/other drops while it runs, it
        will get stuck doing the same quest forever. Make sure you will have
        space for the entire duration you will leave it running unattended.
        """
        end = time.time() + duration * 60
        self.menu("questing")
        self.click(950, 590)  # move tooltip
        text = self.get_quest_text()

        if coords.QUESTING_QUEST_COMPLETE in text.lower():
            self.click(*coords.QUESTING_START_QUEST)
            time.sleep(userset.LONG_SLEEP * 2)
            text = self.get_quest_text()  # fetch new quest text

        if coords.QUESTING_NO_QUEST_ACTIVE in text.lower():  # if we have no active quest, start one
            self.click(*coords.QUESTING_START_QUEST)
            if force and not self.inventory_cleaned:
                self.questing_consume_items(True)  # we have to clean up the inventory from any old quest items
                self.inventory_cleaned = True
            elif not force:
                self.questing_consume_items(True)
            self.click(960, 600)  # move tooltip
            time.sleep(userset.LONG_SLEEP)
            text = self.get_quest_text()  # fetch new quest text

        if force:
            if self.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                self.click(*coords.QUESTING_USE_MAJOR)

            while not coords.QUESTING_ZONES[force] in text.lower():
                self.click(*coords.QUESTING_SKIP_QUEST)
                self.click(*coords.CONFIRM)
                self.click(*coords.QUESTING_START_QUEST)
                text = self.get_quest_text()

        if subcontract:
            if self.check_pixel_color(*coords.QUESTING_IDLE_INACTIVE):
                self.click(*coords.QUESTING_SUBCONTRACT)
            return

        if major and coords.QUESTING_MINOR_QUEST in text.lower():  # check if current quest is minor
            if self.check_pixel_color(*coords.QUESTING_IDLE_INACTIVE):
                self.click(*coords.QUESTING_SUBCONTRACT)
            return

        if not self.check_pixel_color(*coords.QUESTING_IDLE_INACTIVE):  # turn off idle
            self.click(*coords.QUESTING_SUBCONTRACT)

        for count, zone in enumerate(coords.QUESTING_ZONES, start=0):
            if zone in text.lower():
                current_time = time.time()
                while current_time < end:
                    if current_time + adv_duration * 60 > end:  # adjust adv_duration if it will cause duration to be exceeded
                        adv_duration = (end - current_time) / 60
                        if adv_duration < 0.5:
                            adv_duration = 0
                            return
                    self.snipe(count, adv_duration)
                    self.boost_cube()
                    self.questing_consume_items()
                    text = self.get_quest_text()
                    current_time = time.time()
                    if coords.QUESTING_QUEST_COMPLETE in text.lower():
                        try:
                            start_qp = int(self.remove_letters(self.ocr(*coords.OCR_QUESTING_QP)))
                        except ValueError:
                            print("Couldn't fetch current QP")
                        self.click(*coords.QUESTING_START_QUEST)
                        self.click(605, 510)  # move tooltip
                        try:
                            current_qp = int(self.remove_letters(self.ocr(*coords.OCR_QUESTING_QP)))
                        except ValueError:
                            print("Couldn't fetch current QP")
                        gained_qp = current_qp - start_qp
                        print(f"Completed quest in zone #{count} at {datetime.datetime.now().strftime('%H:%M:%S')} for {gained_qp} QP")

                        return

    def get_rebirth_time(self):
        """Get the current rebirth time.

        returns a namedtuple(days, timestamp) where days is the number
        of days displayed in the rebirth time text and timestamp is a
        time.time_struct object.
        """
        Rebirth_time = namedtuple('Rebirth_time', 'days timestamp')
        t = self.ocr(*coords.OCR_REBIRTH_TIME)
        x = re.search(r"((?P<days>[0-9]+) days? )?((?P<hours>[0-9]+):)?(?P<minutes>[0-9]+):(?P<seconds>[0-9]+)", t)
        days = 0
        if x is None:
            timestamp = time.strptime("0:0:0", "%H:%M:%S")
        else:
            if x.group('days') is None:
                days = 0
            else:
                days = int(x.group('days'))

            if x.group('hours') is None:
                hours = "0"
            else:
                hours = x.group('hours')

            if x.group('minutes') is None:
                minutes = "0"
            else:
                minutes = x.group('minutes')

            if x.group('seconds') is None:
                seconds = "0"
            else:
                seconds = x.group('seconds')
            timestamp = time.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S")
        return Rebirth_time(days, timestamp)

    def eat_muffin(self, buy=False):
        """Eat a MacGuffin Muffin if it's not active.

        Keyword arguments:
        buy -- set to True if you wish to buy a muffin if you have enough
        AP and you currently have 0 muffins.
        """
        self.sellout_boost_2()
        muffin_status = self.ocr(*coords.OCR_MUFFIN).lower()
        if "have: 0" in muffin_status and "inactive" in muffin_status:
            print(muffin_status)
            if buy:
                try:
                    ap = int(self.remove_letters(self.ocr(*coords.OCR_AP)))
                except ValueError:
                    print("Couldn't get current AP")
                if ap >= 50000:
                    print(f"Bought MacGuffin Muffin at: {datetime.datetime.now()}")
                    self.click(*coords.SELLOUT_MUFFIN_BUY)
                    self.confirm()
            else:
                return
        else:
            return
        self.click(*coords.SELLOUT_MUFFIN_USE)
        print(f"Used MacGuffin Muffin at: {datetime.datetime.now()}")

    def hacks(self, targets=[1, 2, 3, 4, 5, 6, 7, 8], value=1e12):
        """Activate hacks."""
        self.input_box()
        self.send_string(value // len(targets))
        self.menu("hacks")
        for i in targets:
            page = ((i-1)//8)
            item = i - (page * 8)
            self.click(*coords.HACK_PAGE[page])
            self.click(*coords.HACKS[item])
