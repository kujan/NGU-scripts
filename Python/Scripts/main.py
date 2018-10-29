"""I should write someting here at some point."""

import cv2
import ngucon as ncon
import math
import numpy
import pytesseract
import re
import time
import win32api
import win32con as wcon
import win32gui
import win32ui
from ctypes import windll
from PIL import Image as image
from PIL import ImageFilter


class Window():
    """This class contains game window coordinates."""

    id = 0
    x = 0
    y = 0

    def __init__(self):
        """Keyword arguments.

        hwnd -- The window ID
        x -- The x-coordinate for the top left corner of the game window.
        y -- The y-coordinate for the top left corner of the game window.
        """
        def window_enumeration_handler(hwnd, top_windows):
            """Add window title and ID to array."""
            top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        top_windows = []
        win32gui.EnumWindows(window_enumeration_handler, top_windows)
        for i in top_windows:
            if "play ngu idle" in i[1].lower():
                Window.id = i[0]


class Inputs():
    """This class handles inputs."""

    def click(self, x, y, button="left"):
        """Click at pixel xy."""
        x += Window.x
        y += Window.y
        lParam = win32api.MAKELONG(x, y)
        # MOUSEMOVE event is required for game to register clicks correctly
        win32gui.PostMessage(Window.id, wcon.WM_MOUSEMOVE, 0, lParam)

        while (win32api.GetKeyState(wcon.VK_CONTROL) < 0 or
               win32api.GetKeyState(wcon.VK_SHIFT) < 0 or
               win32api.GetKeyState(wcon.VK_MENU) < 0):
            time.sleep(0.005)

        if (button == "left"):
            win32gui.PostMessage(Window.id, wcon.WM_LBUTTONDOWN,
                                 wcon.MK_LBUTTON, lParam)
            win32gui.PostMessage(Window.id, wcon.WM_LBUTTONUP,
                                 wcon.MK_LBUTTON, lParam)

        else:
            win32gui.PostMessage(Window.id, wcon.WM_RBUTTONDOWN,
                                 wcon.MK_RBUTTON, lParam)
            win32gui.PostMessage(Window.id, wcon.WM_RBUTTONUP,
                                 wcon.MK_RBUTTON, lParam)
        # Sleep lower than 0.1 might cause issues when clicking in succession
        time.sleep(0.2)

    def send_string(self, str):
        """Send one or multiple characters to the window."""
        for c in str:
            while (win32api.GetKeyState(wcon.VK_CONTROL) < 0 or
                   win32api.GetKeyState(wcon.VK_SHIFT) < 0 or
                   win32api.GetKeyState(wcon.VK_MENU) < 0):
                time.sleep(0.005)
            if c.isdigit():  # Digits only require KEY_UP event.
                win32gui.PostMessage(Window.id, wcon.WM_KEYUP, ord(c.upper()),
                                     0)
                #time.sleep(0.03)  # This can probably be removed
                continue
            win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN, ord(c.upper()), 0)
            time.sleep(0.10)  # This can probably be removed
            win32gui.PostMessage(Window.id, wcon.WM_KEYUP, ord(c.upper()), 0)
        time.sleep(0.1)

    def get_bitmap(self):
        """Get and return a bitmap of the window."""
        left, top, right, bot = win32gui.GetWindowRect(Window.id)
        w = right - left
        h = bot - top
        hwnd_dc = win32gui.GetWindowDC(Window.id)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(save_bitmap)
        windll.user32.PrintWindow(Window.id, save_dc.GetSafeHdc(), 0)
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)

        # This creates an Image object from Pillow
        bmp = image.frombuffer('RGB',
                               (bmpinfo['bmWidth'],
                                bmpinfo['bmHeight']),
                               bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(Window.id, hwnd_dc)
        #bmp.save("asdf.png")
        return bmp

    def pixel_search(self, color, x_start, y_start, x_end, y_end):
        """Find the first pixel with the supplied color within area.

        Function searches per row, left to right. Returns the coordinates of
        first match or None, if nothing is found.

        Color must be supplied in hex.
        """
        bmp = self.get_bitmap()
        width, height = bmp.size
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                if y > height or x > width:
                    continue
                t = bmp.getpixel((x, y))
                if (self.rgb_to_hex(t) == color):
                    return x - 8, y - 8
        return None

    def image_search(self, x_start, y_start, x_end, y_end, image):
        """Search the screen for the supplied picture.

        Returns a tuple with x,y-coordinates.

        Keyword arguments:
        image -- Filename or path to file that you search for.
        """
        bmp = self.get_bitmap()
        # Bitmaps are created with a 8px border
        search_area = bmp.crop((x_start + 8, y_start + 8,
                                x_end + 8, y_end + 8))
        search_area = numpy.asarray(search_area)
        search_area = cv2.cvtColor(search_area, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(image, 0)
        res = cv2.matchTemplate(search_area, template, cv2.TM_CCOEFF)
        *_, t = cv2.minMaxLoc(res)
        return t

    def ocr(self, x_start, y_start, x_end, y_end, debug=False, bmp=None):
        """Perform an OCR of the supplied area, returns a string of the result.

        Keyword arguments:

        debug -- saves an image of what is sent to the OCR (default False)
        bmp -- a bitmap from the get_bitmap() function, use this if you're
               performing multiple different OCR-readings in succession from
               the same page. This is to avoid to needlessly get the same
               bitmap multiple times. If a bitmap is not passed, the function
               will get the bitmap itself. (default None)
        """
        x_start += Window.x
        x_end += Window.x
        y_start += Window.y
        y_end += Window.y

        if not bmp:
            bmp = self.get_bitmap()
        # Bitmaps are created with a 8px border
        bmp = bmp.crop((x_start + 8, y_start + 8, x_end + 8, y_end + 8))
        *_, right, lower = bmp.getbbox()
        bmp = bmp.resize((right*3, lower*3), image.BICUBIC)  # Resize image
        bmp = bmp.filter(ImageFilter.SHARPEN)  # Sharpen image for better OCR
        if debug:
            bmp.save("debug_ocr.png")
        s = pytesseract.image_to_string(bmp)
        return s

    def get_pixel_color(self, x, y):
        """Get the color of selected pixel in HEX."""
        return self.rgb_to_hex(self.get_bitmap().getpixel((x + 8 +
                               Window.x, y + 8 + Window.y)))

    def remove_letters(self, s):
        """Remove all non digit characters from string."""
        return re.sub('[^0-9]', '', s)

    def rgb_to_hex(self, tup):
        """Convert RGB value to HEX."""
        return '%02x%02x%02x'.upper() % (tup[0], tup[1], tup[2])


class Navigation(Inputs):
    """Navigate through menus."""

    menus = ncon.MENUITEMS
    equipment = ncon.EQUIPMENTSLOTS

    def menu(self, target):
        """Navigate through main menu."""
        y = ncon.MENUOFFSETY + ((self.menus.index(target) + 1) *
                                ncon.MENUDISTANCEY)
        self.click(ncon.MENUOFFSETX, y)
        time.sleep(0.3)

    def input_box(self):
        """Click input box."""
        self.click(ncon.NUMBERINPUTBOXX, ncon.NUMBERINPUTBOXY)
        time.sleep(0.1)

    def rebirth(self):
        """Click rebirth menu."""
        self.click(ncon.REBIRTHX, ncon.REBIRTHY)
        time.sleep(0.1)

    def confirm(self):
        """Click yes in confirm window."""
        self.click(ncon.CONFIRMX, ncon.CONFIRMY)
        time.sleep(0.1)

    def ngu_magic(self):
        """Navigate to NGU magic."""
        self.menu("ngu")
        self.click(ncon.NGUMAGICX, ncon.NGUMAGICY)
        time.sleep(0.1)

    def exp(self):
        """Navigate to EXP Menu."""
        self.click(ncon.EXPX, ncon.EXPY)
        time.sleep(0.1)

    def exp_magic(self):
        """Navigate to the magic menu within the EXP menu."""
        self.exp()
        self.click(ncon.MMENUX, ncon.MMENUY)
        time.sleep(0.1)

    def info(self):
        """Click info 'n stuff."""
        self.click(ncon.INFOX, ncon.INFOY)
        time.sleep(0.1)

    def misc(self):
        """Navigate to Misc stats."""
        self.info()
        self.click(ncon.MISCX, ncon.MISCY)
        time.sleep(0.1)

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

    def fight(self):
        """Navigate to Fight Boss and Nuke/attack."""
        self.menu("fight")
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
            time.sleep(0.1)

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
                self.click(ncon.AUGMENTSCROLLX, ncon.AUGMENTSCROLLBOTY)

            time.sleep(0.3)
            val = math.floor(augments[k] * energy)
            self.input_box()
            self.send_string(str(val))
            time.sleep(0.3)
            self.click(ncon.AUGMENTX, ncon.AUGMENTY[k])

    def time_machine(self, magic=False):
        """Add energy and/or magic to TM."""
        self.menu("timemachine")
        self.input_box()
        self.send_string("500000000")
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
        """Try to cast bloodpill, otherwise cast number."""
        bm_color = self.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
        self.menu("bloodmagic")
        self.click(ncon.BMSPELLX, ncon.BMSPELLY)
        if bm_color == ncon.BM_PILL_READY:
            self.send_string("t")
            self.send_string("r")
            self.blood_magic(8)
            self.click(ncon.BMSPELLX, ncon.BMSPELLY)
            time.sleep(300)
            self.click(ncon.BMPILLX, ncon.BMPILLY)
            time.sleep(5)
        self.click(ncon.BMNUMBERX, ncon.BMNUMBERY)

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


class Statistics(Navigation):
    """Handles various statistics."""

    def __init__(self):
        """Store start EXP via OCR."""
        self.misc()
        try:
            self.start_exp = int(float(self.ocr(ncon.OCR_EXPX1,
                                                ncon.OCR_EXPY1,
                                                ncon.OCR_EXPX2,
                                                ncon.OCR_EXPY2, debug=True)))
        except ValueError:
            print("OCR couldn't detect starting XP, defaulting to 0.")
            self.start_exp = 0
        self.start_time = time.time()
        self.rebirth = 1

    def print_exp(self):
        """Print current exp stats."""
        self.misc()
        current_time = time.time()
        try:
            current_exp = int(float(re.sub(',', '', self.ocr(ncon.OCR_EXPX1,
                                                             ncon.OCR_EXPY1,
                                                             ncon.OCR_EXPX2,
                                                             ncon.OCR_EXPY2))))
        except ValueError:
            print("OCR couldn't detect current XP.")
            return
        per_hour = (current_exp - self.start_exp)//((current_time -
                                                     self.start_time) / 3600)
        print(f'Rebirth #{self.rebirth}\nStart exp: {self.start_exp}\nCurrent '
              f'exp: {current_exp}\nPer hour: {per_hour}\n')
        self.rebirth += 1


class Upgrade(Navigation):
    """Buys things for exp."""

    def __init__(self, ecap, mcap, ebar, mbar, e2m_ratio):
        """Example: Upgrade(37500, 37500, 2, 1).

        This will result in a 1:37500:2 ratio for energy and 1:37500:1 for
        magic. i.e. 1 power, 37500 ecap and 2 ebars.

        Keyword arguments:

        ecap -- The amount of energy cap in the ratio. Must be over 10000 and
                divisible by 250.
        mcap -- The amount of magic cap in the ratio. Must be over 10000 and
                divisible by 250.
        ebar -- the amount of energy bars to buy in relation to power
        mbar -- the amount of magic bars to buy in relation to power.
        e2m_ratio -- The amount of exp to spend in energy in relation to magic.
                     a value of 5 will buy 5 times more upgrades in energy than
                     in magic, maintaining a 5:1 E:M ratio. 
        """
        self.ecap = ecap
        self.mcap = mcap
        self.ebar = ebar
        self.mbar = mbar
        self.e2m_ratio = e2m_ratio
        self.OCR_failures = 0

    def em(self):
        """Buy upgrades for both energy and magic.

        Requires the confirmation popup button for EXP purchases in settings
        to be turned OFF.

        This uses all available exp, so use with caution.
        """
        if self.ecap < 10000 or self.ecap % 250 != 0:
            print("Ecap value not divisible by 250 or lower than 10000, not" +
                  " spending exp.")
            return
        if self.mcap < 10000 or self.mcap % 250 != 0:
            print("Mcap value not divisible by 250 or lower than 10000, not" +
                  " spending exp.")
            return

        self.exp()

        try:
            current_exp = int(self.remove_letters(self.ocr(ncon.EXPX1,
                                                           ncon.EXPY1,
                                                           ncon.EXPX2,
                                                           ncon.EXPY2)))

            self.OCR_failures = 0

        except ValueError:
            self.OCR_failures += 1
            if self.OCR_failures <= 3:
                print("OCR couldn't detect current XP, retrying.")
                self.em()
                return
            else:
                print("Something went wrong with the OCR, not buying upgrades")
                return

        e_cost = ncon.EPOWER_COST + ncon.ECAP_COST * self.ecap + (
                 ncon.EBAR_COST * self.ebar)

        m_cost = ncon.MPOWER_COST + ncon.MCAP_COST * self.mcap + (
                 ncon.MBAR_COST * self.mbar)

        total_price = m_cost + self.e2m_ratio * e_cost
        
        """Skip upgrading if we don't have enough exp to buy at least one
        complete set of upgrades, in order to maintain our perfect ratios :)"""

        if total_price > current_exp:
            return

        amount = int(current_exp // total_price)

        e_power = amount * self.e2m_ratio
        e_cap = amount * self.ecap * self.e2m_ratio
        e_bars = amount * self.ebar * self.e2m_ratio
        m_power = amount
        m_cap = amount * self.mcap
        m_bars = amount * self.mbar

        self.exp()

        self.click(ncon.EMPOWBOXX, ncon.EMBOXY)
        self.send_string(str(e_power))
        time.sleep(0.1)

        self.click(ncon.EMCAPBOXX, ncon.EMBOXY)
        self.send_string(str(e_cap))
        time.sleep(0.1)

        self.click(ncon.EMBARBOXX, ncon.EMBOXY)
        self.send_string(str(e_bars))
        time.sleep(0.1)

        self.click(ncon.EMPOWBUYX, ncon.EMBUYY)
        self.click(ncon.EMCAPBUYX, ncon.EMBUYY)
        self.click(ncon.EMBARBUYX, ncon.EMBUYY)

        self.exp_magic()

        self.click(ncon.EMPOWBOXX, ncon.EMBOXY)
        self.send_string(str(m_power))
        time.sleep(0.1)

        self.click(ncon.EMCAPBOXX, ncon.EMBOXY)
        self.send_string(str(m_cap))
        time.sleep(0.1)

        self.click(ncon.EMBARBOXX, ncon.EMBOXY)
        self.send_string(str(m_bars))
        time.sleep(0.1)

        self.click(ncon.EMPOWBUYX, ncon.EMBUYY)
        self.click(ncon.EMCAPBUYX, ncon.EMBUYY)
        self.click(ncon.EMBARBUYX, ncon.EMBUYY)


class Challenge(Features):
    """Handles different challenges."""
    def __init__(self):
        self.challenge_runtime = 0

    def start_challenge(self, challenge):
        """Start the selected challenge."""
        self.rebirth()
        self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
        color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
                                     ncon.CHALLENGEACTIVEY)

        if color == ncon.CHALLENGEACTIVECOLOR:
            text = self.ocr(ncon.OCR_CHALLENGE_NAMEX1,
                            ncon.OCR_CHALLENGE_NAMEY1,
                            ncon.OCR_CHALLENGE_NAMEX2,
                            ncon.OCR_CHALLENGE_NAMEY2)
            print("A challenge is already active: " + text)
            if "basic" in text.lower():
                print("Starting basic challenge script")
                self.basic()

            elif "24 hour" in text.lower():
                print("Starting 24 hour challenge script")
                try:
                    x = ncon.CHALLENGEX
                    y = ncon.CHALLENGEY + challenge * ncon.CHALLENGEOFFSET
                    self.click(x, y, button="right")
                    time.sleep(0.3)
                    target = self.ocr(ncon.OCR_CHALLENGE_24HC_TARGETX1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETX2,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY2)
                    target = int(self.remove_letters(target))
                    print(f"Found target boss: {target}")
                    self.basic(target)
                except ValueError:
                    print("couldn't detect the target level of 24HC")
                
            else:
                print("Couldn't determine which script to start from the OCR input")
            #  TODO: add other challenges here

        else:
            x = ncon.CHALLENGEX
            y = ncon.CHALLENGEY + challenge * ncon.CHALLENGEOFFSET


            if challenge == 1:
                self.click(x, y)
                time.sleep(0.3)
                self.confirm()
                self.basic(58)

            if challenge == 3:
                try:
                    self.click(x, y, button="right")
                    time.sleep(0.3)
                    target = self.ocr(ncon.OCR_CHALLENGE_24HC_TARGETX1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETX2,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY2)
                    target = int(self.remove_letters(target))
                    print(f"Found target boss: {target}")
                    self.click(x, y)
                    time.sleep(0.3)
                    self.confirm()
                    time.sleep(0.3)
                    self.basic(target)
                except ValueError:
                    print("couldn't detect the target level of 24HC")

    def check_challenge(self):
        """Check if a challenge is active."""
        self.rebirth()
        self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
        time.sleep(0.3)
        color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
                                     ncon.CHALLENGEACTIVEY)

        return True if color == ncon.CHALLENGEACTIVECOLOR else False

    def first_rebirth(self):
        """Procedure for first rebirth after number reset."""
        end = time.time() + 3 * 60
        tm_unlocked = False
        bm_unlocked = False
        ci_assigned = False
        diggers = [2, 3, 8]
        self.loadout(1)
        self.fight()
        self.adventure(highest=True)
        while not tm_unlocked:
            if not ci_assigned:
                time.sleep(1)
                self.augments({"CI": 1}, 1e6)
                ci_assigned = True
            self.wandoos(True)
            self.fight()

            tm_color = self.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
            if tm_color != ncon.TMLOCKEDCOLOR:
                self.send_string("r")
                self.send_string("t")
                self.time_machine(True)
                self.loadout(2)
                tm_unlocked = True

        time.sleep(15)
        self.augments({"CI": 1}, 1e8)
        self.gold_diggers(diggers, True)
        self.adventure(highest=True)
        time.sleep(4)
        self.adventure(itopod=True, itopodauto=True)
        while not bm_unlocked:
            self.wandoos(True)
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(5)

            bm_color = self.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
            if bm_color != ncon.BMLOCKEDCOLOR:
                self.menu("bloodmagic")
                time.sleep(0.2)
                self.send_string("t")
                self.send_string("r")
                self.blood_magic(5)
                bm_unlocked = True
                self.augments({"SS": 0.7, "DS": 0.3}, 5e8)

        while time.time() < end:
            self.wandoos(True)
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(5)


    def speedrun(self, duration, target):
        """Start a speedrun.

        Keyword arguments
        duration -- duration in minutes to run
        f -- feature object
        """
        self.do_rebirth()
        start = time.time()
        end = time.time() + (duration * 60)
        magic_assigned = False
        do_tm = True
        augments_assigned = False
        self.fight()
        self.loadout(1)  # Gold drop equipment
        self.adventure(0, True, False, False)
        time.sleep(3)
        self.loadout(2)  # Bar/power equimpent
        self.adventure(zone=0, highest=False, itopod=True, itopodauto=True)
        while time.time() < end - 15:
            bm_color = self.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
            tm_color = self.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
            # Do TM while waiting for magic cap
            if not magic_assigned and tm_color != ncon.TMLOCKEDCOLOR:
                self.time_machine(True)
            # If magic is assigned, continue adding energy to TM
            elif do_tm and tm_color != ncon.TMLOCKEDCOLOR:
                self.time_machine()
            else: 
                self.wandoos(True)
            # Assign augments when energy caps
            if time.time() > end - (duration * 0.75 * 60):
                if do_tm and not augments_assigned:
                    self.send_string("r")
                    self.augments({"SM": 0.7, "AA": 0.3}, 8e8)
                    self.gold_diggers([2, 8, 9], True)
                    do_tm = False
                    augments_assigned = True
                    self.send_string("t")
                    self.wandoos(True)
                    self.boost_equipment()
            # Reassign magic from TM into BM after half the duration
            if (bm_color != ncon.BMLOCKEDCOLOR and not magic_assigned and
               time.time() > end - (duration * 0.75 * 60)):
                self.menu("bloodmagic")
                time.sleep(0.2)
                self.send_string("t")
                self.blood_magic(7)
                magic_assigned = True
                self.wandoos(True)
            # Assign leftovers into wandoos
            if augments_assigned:
                self.wandoos(True)
                self.gold_diggers([2, 8, 9])
            try:
                """If current rebirth is scheduled for more than 3 minutes and
                we already finished the rebirth, we will return here, instead
                of waiting for the duration. Since we cannot start a new
                challenge if less than 3 minutes have passed, we must always
                wait at least 3 minutes."""
                
                current_boss = int(self.get_current_boss())
                if duration > 3 and current_boss > target:
                    if not self.check_challenge():
                        while time.time() < start + 180:
                            time.sleep(1)
                        return
                if current_boss < 101:
                    self.fight()

            except ValueError:
                print("OCR couldn't find current boss")
            #self.boost_equipment()

        self.menu("digger")
        self.gold_diggers([3], True)
        self.fight()
        self.pit()
        self.spin()
        time.sleep(7)
        self.speedrun_bloodpill()
        return

    def basic(self, target):
        """Defeat target boss."""
        self.first_rebirth()
        while True:
            for x in range(8):
                self.speedrun(3, target)
                if not self.check_challenge():
                    return
            for x in range(5):
                self.speedrun(7, target)
                if not self.check_challenge():
                    return
            for x in range(5):
                self.speedrun(12, target)
                if not self.check_challenge():
                    return
            for x in range(5):
                self.speedrun(60, target)
                if not self.check_challenge():
                    return
            speedrun(3, feature)

def speedrun(duration, f):
    """Start a speedrun.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    f.do_rebirth()
    end = time.time() + (duration * 60)
    magic_assigned = False
    do_tm = True
    augments_assigned = False
    f.fight()
    f.loadout(1)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(3)
    f.loadout(2)  # Bar/power equimpent
    f.adventure(itopod=True, itopodauto=True)
    i = 0
    while time.time() < end - 15:
        bm_color = f.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
        tm_color = f.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
        # Do TM while waiting for magic cap
        if not magic_assigned and tm_color != ncon.TMLOCKEDCOLOR:
            f.time_machine(True)
        # If magic is assigned, continue adding energy to TM
        elif do_tm and tm_color != ncon.TMLOCKEDCOLOR:
            f.time_machine()
        else: 
            f.wandoos(True)
        # Assign augments when energy caps
        if time.time() > end - (duration * 0.75 * 60):
            if do_tm and not augments_assigned:
                f.send_string("r")
                f.augments({"SM": 0.7, "AA": 0.3}, 8e8)
                f.gold_diggers([2, 8, 9], True)
                do_tm = False
                augments_assigned = True
                f.send_string("t")
                f.wandoos(True)
                f.boost_equipment()
        # Reassign magic from TM into BM after half the duration
        if (bm_color != ncon.BMLOCKEDCOLOR and not magic_assigned and
           time.time() > end - (duration * 0.75 * 60)):
            f.menu("bloodmagic")
            time.sleep(0.2)
            f.send_string("t")
            f.blood_magic(7)
            magic_assigned = True
            f.wandoos(True)
            #time.sleep(15)
            """try:
                NGU_energy = int(feature.remove_letters(feature.ocr(ncon.OCR_ENERGY_X1,ncon.OCR_ENERGY_Y1,ncon.OCR_ENERGY_X2,ncon.OCR_ENERGY_Y2)))
                feature.assign_ngu(NGU_energy, [1, 2, 4, 5, 6]) 

                NGU_magic = int(feature.remove_letters(feature.ocr(ncon.OCR_MAGIC_X1, ncon.OCR_MAGIC_Y1, ncon.OCR_MAGIC_X2, ncon.OCR_MAGIC_Y2)))
                feature.assign_ngu(NGU_magic, [1], magic=True)
            except:
                print("couldn't assign e/m to NGUs")"""
        # Assign leftovers into wandoos
        if augments_assigned:
            f.wandoos(True)
            #f.assign_ngu(100000000, [1])
            #f.assign_ngu(100000000, [1], magic=True)
        #f.boost_equipment()

    f.menu("digger")
    f.gold_diggers([3], True)
    #f.click(ncon.DIG_ACTIVE[3]["x"], ncon.DIG_ACTIVE[3]["y"])
    f.fight()
    f.pit()
    f.spin()
    time.sleep(7)
    f.speedrun_bloodpill()
    return


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()
c = Challenge()

Window.x, Window.y = i.pixel_search("212429", 0, 0, 400, 600)
nav.menu("inventory")
s = Statistics()
u = Upgrade(37500, 37500, 2, 2, 1)

print(Window.x, Window.y)
u.em()
#print(c.check_challenge())
#c.start_challenge(3)
for x in range(17):
    c.start_challenge(3)
#while True:  # main loop
#    feature.boost_equipment()
#    feature.merge_equipment()
#    feature.ygg()
#    time.sleep(180)
    
#    speedrun(3, feature)
#    s.print_exp()
#    u.em()
