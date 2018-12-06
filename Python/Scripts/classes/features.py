"""Feature class handles the different features in the game."""
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window
from collections import deque, namedtuple
from decimal import Decimal
import math
import ngucon as ncon
import re
import time
import win32con as wcon
import win32gui
import usersettings as userset


class Features(Navigation, Inputs):
    """Handles the different features in the game."""

    def merge_equipment(self):
        """Navigate to inventory and merge equipment."""
        self.menu("inventory")
        for slot in self.equipment:
            if (slot == "cube"):
                return
            self.click(self.equipment[slot]["x"], self.equipment[slot]["y"])
            self.send_string("d")

    def boost_equipment(self):
        """Boost all equipment."""
        self.menu("inventory")
        for slot in self.equipment:
            if (slot == "cube"):
                self.click(self.equipment[slot]["x"],
                           self.equipment[slot]["y"], "right")
                return
            self.click(self.equipment[slot]["x"], self.equipment[slot]["y"])
            self.send_string("a")

    def get_current_boss(self):
        """Go to fight and read current boss number."""
        self.menu("fight")
        boss = self.ocr(ncon.OCRBOSSX1, ncon.OCRBOSSY1, ncon.OCRBOSSX2,
                        ncon.OCRBOSSY2, debug=False)
        return self.remove_letters(boss)

    def nuke(self, boss=None):
        """Navigate to Fight Boss and Nuke or Fast Fight."""
        self.menu("fight")
        if boss:
            for i in range(boss):
                self.click(ncon.FIGHTX, ncon.FIGHTY, fast=True)
            time.sleep(userset.SHORT_SLEEP)
            current_boss = int(self.get_current_boss())
            x = 0
            while current_boss < boss:
                bossdiff = boss - current_boss
                for i in range(0, bossdiff):
                    self.click(ncon.FIGHTX, ncon.FIGHTY, fast=True)
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
            self.click(ncon.NUKEX, ncon.NUKEY)

    def fight(self):
        """Navigate to Fight Boss and click fight."""
        self.menu("fight")
        self.click(ncon.FIGHTX, ncon.FIGHTY)

    def ygg(self, rebirth=False):
        """Navigate to inventory and handle fruits."""
        self.menu("yggdrasil")
        if rebirth:
            for i in ncon.FRUITSX:
                self.click(ncon.FRUITSX[i], ncon.FRUITSY[i])
        else:
            self.click(ncon.HARVESTX, ncon.HARVESTY)

    def spin(self):
        """Spin the wheel."""
        self.menu("pit")
        self.click(ncon.SPIN_MENUX, ncon.SPIN_MENUY)
        self.click(ncon.SPINX, ncon.SPINY)

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
        if itopod:
            self.click(ncon.ITOPODX, ncon.ITOPODY)
            if itopodauto:
                self.click(ncon.ITOPODENDX, ncon.ITOPODENDY)
                # set end to 0 in case it's higher than start
                self.send_string("0")
                self.click(ncon.ITOPODAUTOX, ncon.ITOPODAUTOY)
                self.click(ncon.ITOPODENTERX, ncon.ITOPODENTERY)
                return
            self.click(ncon.ITOPODSTARTX, ncon.ITOPODSTARTY)
            self.send_string(str(itopod))
            self.click(ncon.ITOPODENDX, ncon.ITOPODENDY)
            self.send_string(str(itopod))
            self.click(ncon.ITOPODENTERX, ncon.ITOPODENTERY)
            return
        if highest:
            self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY, button="right")
            return
        else:
            self.click(ncon.LEFTARROWX, ncon.LEFTARROWY, button="right")
            for i in range(zone):
                self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY)
            return

    def snipe(self, zone, duration, once=False, highest=False, bosses=True):
        """Go to adventure and snipe bosses in specified zone.

        Keyword arguments
        zone -- Zone to snipe, 0 is safe zone, 1 is turorial and so on.
                If 0, it will use the current zone (to maintain guffin counter)
        duration -- The duration in seconds the sniping will run before
                    returning.
        once -- If true it will only kill one boss before returning.
        highest -- If set to true, it will go to your highest available
                   non-titan zone.
        bosses -- If set to true, it will only kill bosses
        """
        self.menu("adventure")
        if highest:
            self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY, button="right")
        elif zone > 0:
            self.click(ncon.LEFTARROWX, ncon.LEFTARROWY, button="right")
            for i in range(zone):
                self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY)

        self.click(625, 500)  # click somewhere to move tooltip
        idle_color = self.get_pixel_color(ncon.ABILITY_ATTACKX,
                                          ncon.ABILITY_ATTACKY)

        if idle_color == ncon.IDLECOLOR:
            self.click(ncon.IDLE_BUTTONX, ncon.IDLE_BUTTONY)

        end = time.time() + duration
        while time.time() < end:
            self.click(625, 500)  # click somewhere to move tooltip
            health = self.get_pixel_color(ncon.HEALTHX, ncon.HEALTHY)
            if (health == ncon.NOTDEAD):
                if bosses:
                    crown = self.get_pixel_color(ncon.CROWNX, ncon.CROWNY)
                    if (crown == ncon.ISBOSS):
                        while (health != ncon.DEAD):
                            health = self.get_pixel_color(ncon.HEALTHX,
                                                          ncon.HEALTHY)
                            self.click(ncon.ABILITY_ATTACKX,
                                       ncon.ABILITY_ATTACKY)
                            time.sleep(0.1)
                        if once:
                            break
                    else:
                        # Send left arrow and right arrow to refresh monster.
                        win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN,
                                             wcon.VK_LEFT, 0)
                        time.sleep(0.03)
                        win32gui.PostMessage(Window.id, wcon.WM_KEYUP,
                                             wcon.VK_LEFT, 0)
                        time.sleep(0.03)
                        win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN,
                                             wcon.VK_RIGHT, 0)
                        time.sleep(0.03)
                        win32gui.PostMessage(Window.id, wcon.WM_KEYUP,
                                             wcon.VK_RIGHT, 0)
                else:
                    self.click(ncon.ABILITY_ATTACKX, ncon.ABILITY_ATTACKY)
            time.sleep(0.01)

        self.click(ncon.IDLE_BUTTONX, ncon.IDLE_BUTTONY)

    def itopod_snipe(self, duration):
        """Manually snipes ITOPOD for increased speed PP/h.

        Keyword arguments:
        duration -- Duration in seconds to snipe, before toggling idle mode
                    back on and returning.
        """
        end = time.time() + duration

        self.menu("adventure")
        self.click(625, 500)  # click somewhere to move tooltip
        itopod_active = self.get_pixel_color(ncon.ITOPOD_ACTIVEX,
                                             ncon.ITOPOD_ACTIVEY)
        # check if we're already in ITOPOD, otherwise enter
        if itopod_active != ncon.ITOPOD_ACTIVE_COLOR:
            self.click(ncon.ITOPODX, ncon.ITOPODY)
            self.click(ncon.ITOPODENDX, ncon.ITOPODENDY)
            # set end to 0 in case it's higher than start
            self.send_string("0")
            self.click(ncon.ITOPODAUTOX, ncon.ITOPODAUTOY)
            self.click(ncon.ITOPODENTERX, ncon.ITOPODENTERY)

        idle_color = self.get_pixel_color(ncon.ABILITY_ATTACKX,
                                          ncon.ABILITY_ATTACKY)

        if idle_color == ncon.IDLECOLOR:
            self.click(ncon.IDLE_BUTTONX, ncon.IDLE_BUTTONY)

        while time.time() < end:
            health = self.get_pixel_color(ncon.HEALTHX, ncon.HEALTHY)
            if health != ncon.DEAD:
                self.click(ncon.ABILITY_ATTACKX, ncon.ABILITY_ATTACKY)
            else:
                time.sleep(0.01)

        self.click(ncon.IDLE_BUTTONX, ncon.IDLE_BUTTONY)



    def do_rebirth(self):
        """Start a rebirth or challenge."""
        self.rebirth()

        self.click(ncon.REBIRTHX, ncon.REBIRTHY)
        self.click(ncon.REBIRTHBUTTONX, ncon.REBIRTHBUTTONY)
        self.click(ncon.CONFIRMX, ncon.CONFIRMY)
        return

    def pit(self, loadout=0):
        """Throws money into the pit.

        Keyword arguments:
        loadout -- The loadout you wish to equip before throwing gold
                   into the pit, for gear you wish to shock. Make
                   sure that you don't get cap-blocked by either using
                   the unassign setting in the game or swapping gear that
                   doesn't have e/m cap.
        """
        color = self.get_pixel_color(ncon.PITCOLORX, ncon.PITCOLORY)
        if (color == ncon.PITREADY):
            if loadout:
                self.loadout(loadout)
            self.menu("pit")
            self.click(ncon.PITX, ncon.PITY)
            self.click(ncon.CONFIRMX, ncon.CONFIRMY)

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
                color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
                                             ncon.SANITY_AUG_SCROLLY_BOT)
                while color not in ncon.SANITY_AUG_SCROLL_COLORS:
                    self.click(ncon.AUGMENTSCROLLX, ncon.AUGMENTSCROLLBOTY)
                    time.sleep(userset.MEDIUM_SLEEP)
                    color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
                                                 ncon.SANITY_AUG_SCROLLY_BOT)
                    i += 1
                    if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
                        Navigation.current_menu = ""
                        self.menu("augmentations")
                    elif i > 10:
                        print("Couldn't assign augments")
                        break

            else:
                color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
                                             ncon.SANITY_AUG_SCROLLY_TOP)
                while color not in ncon.SANITY_AUG_SCROLL_COLORS:
                    self.click(ncon.AUGMENTSCROLLX, ncon.AUGMENTSCROLLTOPY)
                    time.sleep(userset.MEDIUM_SLEEP)
                    color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
                                                 ncon.SANITY_AUG_SCROLLY_TOP)
                    i += 1
                    if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
                        Navigation.current_menu = ""
                        self.menu("augmentations")
                    elif i > 10:
                        print("Couldn't assign augments")
                        break
            self.click(ncon.AUGMENTX, ncon.AUGMENTY[k])

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
        magic -- Set to true if you wish to add magic as well"""
        self.menu("timemachine")
        self.input_box()
        self.send_string(e)
        self.click(ncon.TMSPEEDX, ncon.TMSPEEDY)
        if magic or m:
            if m:
                self.input_box()
                self.send_string(m)
            self.click(ncon.TMMULTX, ncon.TMMULTY)

    def blood_magic(self, target):
        """Assign magic to BM."""
        self.menu("bloodmagic")
        for i in range(target):
            self.click(ncon.BMX, ncon.BMY[i])

    def wandoos(self, magic=False):
        """Assign energy and/or magic to wandoos."""
        self.menu("wandoos")
        self.click(ncon.WANDOOSENERGYX, ncon.WANDOOSENERGYY)
        if magic:
            self.click(ncon.WANDOOSMAGICX, ncon.WANDOOSMAGICY)

    def loadout(self, target):
        """Equip targeted loadout."""
        self.menu("inventory")
        self.click(ncon.LOADOUTX[target], ncon.LOADOUTY)

    def speedrun_bloodpill(self):
        """Check if bloodpill is ready to cast."""
        bm_color = self.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
        if bm_color == ncon.BM_PILL_READY:
            start = time.time()
            self.blood_magic(8)
            self.spells()
            self.click(ncon.BM_AUTO_GOLDX, ncon.BM_AUTO_GOLDY)
            self.click(ncon.BM_AUTO_NUMBERX, ncon.BM_AUTO_NUMBERY)

            if userset.PILL == 0:
                duration = 300
            else:
                duration = userset.PILL

            while time.time() < start + duration:
                self.gold_diggers([11])
                time.sleep(5)
            self.spells()
            self.click(ncon.BMPILLX, ncon.BMPILLY)
            time.sleep(userset.LONG_SLEEP)
            self.click(ncon.BM_AUTO_GOLDX, ncon.BM_AUTO_GOLDY)
            self.click(ncon.BM_AUTO_NUMBERX, ncon.BM_AUTO_NUMBERY)
            self.nuke()
            time.sleep(userset.LONG_SLEEP)

    def set_ngu(self, ngu, magic=False):
        """Handle NGU upgrades in a non-dumb way.

        Function will check target levels of selected NGU's and equalize the
        target levels. This means that if one upgrade is ahead of the others,
        the target level for all NGU's that are behind will be set to the
        level of the highest upgrade.

        If they are even, it will instead increase target level
        by 25% of current level. Since the NGU's level at different speeds, I
        would recommend that you currently set the slower separate from the
        faster upgrades, unless energy/magic is a non issue.

        Function returns False if NGU's are uneven, so you know to check back
        occasionally for the proper 25% increase, which can be left unchecked
        for a longer period of time.

        Keyword arguments:

        ngu -- Dictionary containing information on which energy NGU's you
               wish to upgrade. Example: {7: True, 8: False, 9: False} - this
               will use NGU 7 (drop chance), 8 (magic NGU), 9 (PP) in the
               comparisons.

        magic -- Set to True if these are magic NGU's
        """
        if magic:
            self.ngu_magic()
        else:
            self.menu("ngu")

        bmp = self.get_bitmap()
        current_ngu = {}
        try:
            for k in ngu:
                y1 = ncon.OCR_NGU_E_Y1 + k * 35
                y2 = ncon.OCR_NGU_E_Y2 + k * 35
                # remove commas from sub level 1 million NGU's.
                res = re.sub(',', '', self.ocr(ncon.OCR_NGU_E_X1, y1,
                                               ncon.OCR_NGU_E_X2, y2, False,
                                               bmp))
                current_ngu[k] = res
            # find highest and lowest NGU's.
            high = max(current_ngu.keys(),
                       key=(lambda i: float(current_ngu[i])))
            low = min(current_ngu.keys(),
                      key=(lambda i: float(current_ngu[i])))

            # If one NGU is ahead of the others, fix this.
            if high != low:
                for k in current_ngu:
                    if float(current_ngu[k]) <= float(current_ngu[high]):
                        self.click(ncon.NGU_TARGETX, ncon.NGU_TARGETY + 35 * k)

                        """We're casting as float to convert scientific notation
                        into something usable, then casting as int to get rid
                        of decimal."""

                        self.send_string(str(int(float(current_ngu[high]))))
                return False
            # Otherwise increase target level by 25%.
            else:
                for k in current_ngu:
                    self.click(ncon.NGU_TARGETX, ncon.NGU_TARGETY + 35 * k)
                    self.send_string(str(int(float(current_ngu[k]) * 1.25)))
                return True

        except ValueError:
            print("Something went wrong with the OCR reading for NGU's")

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
        self.send_string(str(int(value // len(targets))))
        for i in targets:
            self.click(ncon.NGU_PLUSX, ncon.NGU_PLUSY + i * 35)

    def gold_diggers(self, targets, activate=False):
        """Activate diggers.

        Keyword arguments:
        targets -- Array of diggers to use from 1-12. Example: [1, 2, 3, 4, 9].
        activate -- Set to True if you wish to activate/deactivate these
                    diggers otherwise it will just try to up the cap.
        """
        self.menu("digger")
        for i in targets:
            page = ((i-1)//4)
            item = i - (page * 4)
            self.click(ncon.DIG_PAGEX[page], ncon.DIG_PAGEY)
            self.click(ncon.DIG_CAP[item]["x"], ncon.DIG_CAP[item]["y"])
            if activate:
                self.click(ncon.DIG_ACTIVE[item]["x"],
                           ncon.DIG_ACTIVE[item]["y"])

    def bb_ngu(self, value, targets, overcap=1, magic=False):
        """Estimates the BB value of each supplied NGU.

        Keyword arguments:
        targets -- Array of NGU's to BB. Example: [1, 3, 4, 5, 6]
        magic -- Set to true if these are magic NGUs
        """
        if magic:
            self.ngu_magic()
        else:
            self.menu("ngu")

        self.input_box()
        self.send_string(str(int(value)))

        for target in targets:
            self.click(ncon.NGU_PLUSX, ncon.NGU_PLUSY + target * 35)

        for target in targets:
            energy = 0
            for x in range(198):
                color = self.get_pixel_color(ncon.NGU_BAR_MINX + x,
                                             ncon.NGU_BAR_Y +
                                             ncon.NGU_BAR_OFFSETY * target,
                                             )
                if color == ncon.NGU_BAR_WHITE:
                    pixel_coefficient = x / 198
                    value_coefficient = overcap / pixel_coefficient
                    energy = (value_coefficient * value) - value
                    #print(f"estimated energy to BB this NGU is {Decimal(energy):.2E}")
                    break
            self.input_box()
            self.send_string(str(int(energy)))
            self.click(ncon.NGU_PLUSX, ncon.NGU_PLUSY + target * 35)

    def advanced_training(self, value):
        self.menu("advtraining")
        value = value // 2
        self.input_box()
        self.send_string(value)
        self.click(ncon.ADV_TRAININGX, ncon.ADV_TRAINING1Y)
        self.click(ncon.ADV_TRAININGX, ncon.ADV_TRAINING2Y)

    def titan_pt_check(self, target):
        """Check if we have the recommended p/t to defeat the target Titan.

        Keyword arguments:
        target -- The name of the titan you wish to kill. ["GRB", "GCT",
                  "jake", "UUG", "walderp", "BEAST1", "BEAST2", "BEAST3",
                  "BEAST4"]
        """
        self.menu("adventure")
        bmp = self.get_bitmap()
        power = self.ocr(ncon.OCR_ADV_POWX1, ncon.OCR_ADV_POWY1,
                         ncon.OCR_ADV_POWX2, ncon.OCR_ADV_POWY2, bmp=bmp)
        tough = self.ocr(ncon.OCR_ADV_TOUGHX1, ncon.OCR_ADV_TOUGHY1,
                         ncon.OCR_ADV_TOUGHX2, ncon.OCR_ADV_TOUGHY2, bmp=bmp)

        if (float(power) > ncon.TITAN_PT[target]["p"] and
           float(tough) > ncon.TITAN_PT[target]["t"]):
            return True

        else:
            print(f"Lacking: {Decimal(ncon.TITAN_PT[target]['p'] - float(power)):.2E}"
                  f"/{Decimal(ncon.TITAN_PT[target]['t'] - float(tough)):.2E} P/T"
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
        idle_color = self.get_pixel_color(ncon.ABILITY_ATTACKX,
                                          ncon.ABILITY_ATTACKY)

        if idle_color == ncon.IDLECOLOR:
            self.click(ncon.IDLE_BUTTONX, ncon.IDLE_BUTTONY)

        self.click(ncon.LEFTARROWX, ncon.LEFTARROWY, button="right")
        for i in range(ncon.TITAN_ZONE[target]):
            self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY)

        time.sleep(userset.LONG_SLEEP)

        available = self.ocr(ncon.OCR_ADV_TITANX1, ncon.OCR_ADV_TITANY1,
                             ncon.OCR_ADV_TITANX2, ncon.OCR_ADV_TITANY2)

        if "titan" in available.lower():
            time.sleep(1.5)  # Make sure titans spawn, otherwise loop breaks
            queue = deque(self.get_ability_queue())
            health = ""
            while health != ncon.DEAD:
                if len(queue) == 0:
                    print("NEW QUEUE")
                    queue = deque(self.get_ability_queue())
                    print(queue)

                ability = queue.popleft()
                print(f"using ability {ability}")
                if ability <= 4:
                    x = ncon.ABILITY_ROW1X + ability * ncon.ABILITY_OFFSETX
                    y = ncon.ABILITY_ROW1Y

                if ability >= 5 and ability <= 10:
                    x = ncon.ABILITY_ROW2X + (ability - 5) * ncon.ABILITY_OFFSETX
                    y = ncon.ABILITY_ROW2Y

                if ability > 10:
                    x = ncon.ABILITY_ROW3X + (ability - 11) * ncon.ABILITY_OFFSETX
                    y = ncon.ABILITY_ROW3Y

                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                color = self.get_pixel_color(ncon.ABILITY_ROW1X,
                                             ncon.ABILITY_ROW1Y)
                health = self.get_pixel_color(ncon.HEALTHX, ncon.HEALTHY)

                while color != ncon.ABILITY_ROW1_READY_COLOR:
                    time.sleep(0.03)
                    color = self.get_pixel_color(ncon.ABILITY_ROW1X,
                                                 ncon.ABILITY_ROW1Y)

    def get_ability_queue(self):
        """Return a queue of usable abilities."""
        ready = []
        queue = []

        # Add all abilities that are ready to the ready array
        for i in range(13):
            if i <= 4:
                x = ncon.ABILITY_ROW1X + i * ncon.ABILITY_OFFSETX
                y = ncon.ABILITY_ROW1Y
                color = self.get_pixel_color(x, y)
                if color == ncon.ABILITY_ROW1_READY_COLOR:
                    ready.append(i)
            if i >= 5 and i <= 10:
                x = ncon.ABILITY_ROW2X + (i - 5) * ncon.ABILITY_OFFSETX
                y = ncon.ABILITY_ROW2Y
                color = self.get_pixel_color(x, y)
                if color == ncon.ABILITY_ROW2_READY_COLOR:
                    ready.append(i)
            if i > 10:
                x = ncon.ABILITY_ROW3X + (i - 11) * ncon.ABILITY_OFFSETX
                y = ncon.ABILITY_ROW3Y
                color = self.get_pixel_color(x, y)
                if color == ncon.ABILITY_ROW3_READY_COLOR:
                    ready.append(i)

        health = self.get_pixel_color(ncon.PLAYER_HEAL_THRESHOLDX,
                                      ncon.PLAYER_HEAL_THRESHOLDY)
        # heal if we need to heal
        if health == ncon.PLAYER_HEAL_COLOR:
            if 12 in ready:
                queue.append(12)
            elif 7 in ready:
                queue.append(7)

        # check if offensive buff and ultimate buff are both ready
        buffs = [8, 10]
        if all(i in ready for i in buffs):
            queue.extend(buffs)

        d = ncon.ABILITY_PRIORITY
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
        color = self.get_pixel_color(ncon.SAVEX, ncon.SAVEY)
        if color == ncon.SAVE_READY_COLOR:
            self.click(ncon.SAVEX, ncon.SAVEY)
        return

    def get_inventory_slots(self, slots):
        """Get coords for inventory slots from 1 to slots."""
        point = namedtuple("p", ("x", "y"))
        i = 1
        row = 1
        x_pos = ncon.INVENTORY_SLOTS_X
        y_pos = ncon.INVENTORY_SLOTS_Y
        coords = []

        while i <= slots:
            x = x_pos + (i - (12 * (row - 1))) * 50
            y = y_pos + ((row - 1) * 50)
            coords.append(point(x, y))
            if i % 12 == 0:
                row += 1
            i += 1
        return coords

    def merge_inventory(self, slots):
        """Merge all inventory slots starting from 1 to slots.

        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        self.menu("inventory")
        coords = self.get_inventory_slots(slots)
        for slot in coords:
            self.click(slot.x, slot.y)
            self.send_string("d")

    def boost_inventory(self, slots):
        """Merge all inventory slots starting from 1 to slots.

        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        self.menu("inventory")
        coords = self.get_inventory_slots(slots)
        for slot in coords:
            self.click(slot.x, slot.y)
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
            coords = self.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, self.get_file_path("images", "consumable.png"), threshold)
        else:
            coords = self.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, self.get_file_path("images", "transformable.png"), threshold)

        if coords:
            self.ctrl_click(*slot)
