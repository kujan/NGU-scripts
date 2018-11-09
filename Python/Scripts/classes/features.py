"""Feature class handles the different features in the game."""
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window
from decimal import Decimal
import math
import ngucon as ncon
import re
import time
import win32con as wcon
import win32gui


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

    def fight(self, target=None):
        """Navigate to Fight Boss and Nuke/attack."""
        self.menu("fight")
        if target:
            for x in range(target + 1):
                self.click(ncon.FIGHTX, ncon.FIGHTY, fast=True)
            return
        self.click(ncon.NUKEX, ncon.NUKEY)
        time.sleep(2)
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

    def snipe(self, zone, duration, once=False, highest=False):
        """Go to adventure and snipe bosses in specified zone.

        Keyword arguments
        zone -- Zone to snipe, 0 is safe zone, 1 is turorial and so on.
        duration -- The duration in minutes the sniping will run before
                    returning.
        once -- If true it will only kill one boss before returning.
        highest -- If set to true, it will go to your highest available
                   non-titan zone.
        """
        self.menu("adventure")
        if highest:
            self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY, button="right")
        else:
            self.click(ncon.LEFTARROWX, ncon.LEFTARROWY, button="right")
            for i in range(zone):
                self.click(ncon.RIGHTARROWX, ncon.RIGHTARROWY)
        idle_color = self.get_pixel_color(ncon.IDLEX, ncon.IDLEY)

        #if (idle_color != ncon.IDLECOLOR):
        #    self.send_string("q")

        end = time.time() + (duration * 60)
        while time.time() < end:
            health = self.get_pixel_color(ncon.HEALTHX, ncon.HEALTHY)
            if (health == ncon.NOTDEAD):
                crown = self.get_pixel_color(ncon.CROWNX, ncon.CROWNY)
                if (crown == ncon.ISBOSS):
                    while (health != ncon.DEAD):
                        health = self.get_pixel_color(ncon.HEALTHX,
                                                      ncon.HEALTHY)
                        self.send_string("ytew")
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
            time.sleep(ncon.SHORT_SLEEP)

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

    def pit(self):
        """Throws money into the pit."""
        color = self.get_pixel_color(ncon.PITCOLORX, ncon.PITCOLORY)
        if (color == ncon.PITREADY):
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
            # Make sure we are scrolled up in the augment screen.
            self.click(ncon.AUGMENTSCROLLX, ncon.AUGMENTSCROLLTOPY)
            # Scroll down if we have to.
            if (k == "AE" or k == "ES" or k == "LS" or k == "QSL"):

                color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
                                             ncon.SANITY_AUG_SCROLLY)

                while (color != ncon.SANITY_AUG_SCROLL_BOTTOM_COLOR):
                    self.click(ncon.AUGMENTSCROLLX, ncon.AUGMENTSCROLLBOTY)
                    time.sleep(ncon.MEDIUM_SLEEP)
                    color = self.get_pixel_color(ncon.SANITY_AUG_SCROLLX,
                                                 ncon.SANITY_AUG_SCROLLY)
                    print(color)

            time.sleep(ncon.LONG_SLEEP)
            val = math.floor(augments[k] * energy)
            self.input_box()
            self.send_string(str(val))
            time.sleep(ncon.LONG_SLEEP)
            self.click(ncon.AUGMENTX, ncon.AUGMENTY[k])

    def time_machine(self, magic=False):
        """Add energy and/or magic to TM."""
        self.menu("timemachine")
        self.input_box()
        self.send_string("600000000")
        self.click(ncon.TMSPEEDX, ncon.TMSPEEDY)
        if magic:
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
            self.menu("bloodmagic")
            self.click(ncon.BMSPELLX, ncon.BMSPELLY)
            start = time.time()
            self.send_string("t")
            self.send_string("r")
            self.blood_magic(8)
            self.click(ncon.BMSPELLX, ncon.BMSPELLY)
            self.click(ncon.BM_AUTO_GOLDX, ncon.BM_AUTO_GOLDY)
            self.click(ncon.BM_AUTO_NUMBERX, ncon.BM_AUTO_NUMBERY)
            self.gold_diggers([11], True)
            while time.time() < start + 300:
                self.time_machine(True)
                self.gold_diggers([11])
                time.sleep(5)
            self.menu("bloodmagic")
            self.click(ncon.BMSPELLX, ncon.BMSPELLY)
            self.click(ncon.BMPILLX, ncon.BMPILLY)
            time.sleep(5)
            self.click(ncon.BM_AUTO_GOLDX, ncon.BM_AUTO_GOLDY)
            self.click(ncon.BM_AUTO_NUMBERX, ncon.BM_AUTO_NUMBERY)

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
        start = time.time()

        if magic:
            self.ngu_magic()
        else:
            self.menu("ngu")

        self.input_box()
        self.send_string(str(int(value)))

        for target in targets:
            self.click(ncon.NGU_PLUSX, ncon.NGU_PLUSY + target * 35)

        for target in targets:
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
