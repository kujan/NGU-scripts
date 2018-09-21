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
            time.sleep(0.30)  # This can probably be removed
            win32gui.PostMessage(Window.id, wcon.WM_KEYUP, ord(c.upper()), 0)

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

        return bmp

    def pixel_search(self, color, x_start, y_start, x_end, y_end):
        """Find the first pixel with the supplied color within area.

        Function searches per row, left to right. Returns the coordinates of
        first match or None, if nothing is found.

        Color must be supplied in hex.
        """
        bmp = self.get_bitmap()
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
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
            bmp.save("debug.png")
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

    def do_rebirth(self, challenge=None):
        """Start a rebirth or challenge."""
        self.ygg(rebirth=True)  # Eat/harvest all fruit first
        self.rebirth()

        if challenge:
            time.sleep(0.1)
            self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
            color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
                                         ncon.CHALLENGEACTIVEY)
            if (color == ncon.CHALLENGEACTIVECOLOR):
                self.do_rebirth()  # Do normal rebirth if challenge is active
                return
            self.click(ncon.CHALLENGEX, ncon.CHALLENGEY)
            self.click(ncon.CONFIRMX, ncon.CONFIRMY)
            return
        else:
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
            time.sleep(0.1)
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
        self.input_box()
        self.send_string("10000000")
        self.click(ncon.WANDOOSENERGYX, ncon.WANDOOSENERGYY)
        if magic:
            self.click(ncon.WANDOOSMAGICX, ncon.WANDOOSMAGICY)

    def loadout(self, target):
        """Equip targeted loadout."""
        self.menu("inventory")
        self.click(ncon.LOADOUTX[target], ncon.LOADOUTY)

    def speedrun_bloodpill(self):
        """Try to cast bloodpill, otherwise cast number."""
        self.menu("bloodmagic")
        self.click(ncon.BMSPELLX, ncon.BMSPELLY)
        self.click(ncon.BMPILLX, ncon.BMPILLY)
        self.click(ncon.BMNUMBERX, ncon.BMNUMBERY)
        time.sleep(2)
        self.click(ncon.BMNUMBERX, ncon.BMNUMBERY)


class Statistics(Navigation):
    """Handles various statistics."""

    def __init__(self):
        """Store start EXP via OCR."""
        self.misc()
        try:
            self.start_exp = int(self.remove_letters(self.ocr(ncon.OCR_EXPX1,
                                                              ncon.OCR_EXPY1,
                                                              ncon.OCR_EXPX2,
                                                              ncon.OCR_EXPY2)))
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
            current_exp = int(self.remove_letters(self.ocr(ncon.OCR_EXPX1,
                                                           ncon.OCR_EXPY1,
                                                           ncon.OCR_EXPX2,
                                                           ncon.OCR_EXPY2)))
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
    f.snipe(0, 2, once=True, highest=True)  # Kill one boss in the highest zone
    time.sleep(0.1)
    f.loadout(2)  # Bar/power equimpent
    f.adventure(zone=0, highest=False, itopod=True, itopodauto=True)
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
        if time.time() > end - (duration * 0.5 * 60):
            if do_tm and not augments_assigned:
                f.send_string("r")
                f.augments({"SS": 0.5, "DS": 0.5}, 70000000)
                f.fight()
                f.loadout(1)  # Gold drop equipment
                # Kill one boss in the highest zone
                f.snipe(0, 2, once=True, highest=True)
                time.sleep(0.1)
                f.loadout(2)  # Bar/power equimpent
                f.adventure(zone=0, highest=False, itopod=True, itopodauto=True)
                do_tm = False
                augments_assigned = True
        # Reassign magic from TM into BM after half the duration
        if (bm_color != ncon.BMLOCKEDCOLOR and not magic_assigned and
           time.time() > end - (duration * 0.5 * 60)):
            f.menu("bloodmagic")
            time.sleep(0.2)
            f.send_string("t")
            f.blood_magic(4)
            magic_assigned = True
        # Assign leftovers into wandoos
        if augments_assigned:
            f.wandoos(True)
        #f.boost_equipment()
        i += 1
        if i > 50:
            f.fight()
            i = 0
    f.menu("digger")
    f.click(ncon.DIG_CAP[3]["x"], ncon.DIG_CAP[3]["y"])
    f.click(ncon.DIG_ACTIVE[3]["x"], ncon.DIG_ACTIVE[3]["y"])
    f.fight()
    f.pit()
    time.sleep(5)
    f.speedrun_bloodpill()
    return


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()


Window.x, Window.y = i.pixel_search("212429", 0, 0, 400, 600)
nav.menu("inventory")
s = Statistics()
u = Upgrade(37500, 37500, 2, 2, 5)

while True:  # main loop
    #feature.snipe(0, 5, once=False, highest=True)
    #feature.click(ncon.LEFTARROWX, ncon.LEFTARROWY, button="right")
    #feature.ygg()
    #feature.merge_equipment()
    #feature.boost_equipment()
    #time.sleep(120)
    #feature.menu("digger")
    speedrun(5, feature)
    s.print_exp()
    u.em()
