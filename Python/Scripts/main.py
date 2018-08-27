import cv2
import ngucon as ncon
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


class Window:
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

    """
    def __init__(self):
        Get the relative coords for game window.
        Window.__init__(self)
        Window.x, Window.y = self.pixel_search("212429", 0, 0, 400, 600)
    """
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

        time.sleep(0.1)

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
                time.sleep(0.03)  # This can probably be removed
                continue
            win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN, ord(c.upper()), 0)
            time.sleep(0.30)  # This can probably be removed
            win32gui.PostMessage(Window.id, wcon.WM_KEYUP, ord(c.upper()), 0)

        time.sleep(0.1)  # This can probably be removed

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

    def ocr(self, x_start, y_start, x_end, y_end, debug=False):
        """Perform an OCR of the supplied area, returns a string of the result.

        Keyword arguments:
        debug -- saves an image of what is sent to the OCR (default False)
        """
        x_start += Window.x
        x_end += Window.x
        y_start += Window.y
        y_end += Window.y

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
        time.sleep(0.1)

    def input_box(self):
        """Click input box."""
        self.click(ncon.NUMBERINPUTBOXX, ncon.NUMBERINPUTBOXY)

    def rebirth(self):
        """Click rebirth menu."""
        self.click(ncon.REBIRTHX, ncon.REBIRTHY)

    def confirm(self):
        """Click yes in confirm window."""
        self.click(ncon.CONFIRMX, ncon.CONFIRMY)

    def ngu_magic(self):
        """Navigate to NGU magic."""
        self.menu("ngu")
        self.click(ncon.NGUMAGICX, ncon.NGUMAGICY)


class Features(Navigation, Inputs):
    """Handles the different features in the game."""


    def merge_equipment(self):
        """Navigate to inventory and merge equipment."""
        self.menu("inventory")
        for slot in self.equipment:
            self.click(self.equipment[slot].x, self.equipment[slot].y)
            self.send_string("d")

    def boost_equipment(self):
        """Boost all equipment."""
        self.menu("inventory")
        for slot in self.equipment:
            self.click(self.equipment[slot].x, self.equipment[slot].y)
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

    def ygg(self, rebirth=True):
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

        if (idle_color == ncon.IDLECOLOR):
            self.send_string("q")

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
                        time.sleep(0.05)
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


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search("212429", 0, 0, 400, 600)
#print(feature.get_current_boss())
#nav = Navigation()

#nav.fight()


pit_color = i.get_pixel_color(195, 108)
rebirth_text = i.ocr(17, 370, 155, 400, True)
# This requires you to have the file "sellout.png"
sellout_shop = i.image_search(0, 0, 1920, 1080, "sellout.png")

print(f"Found top left of game window at: {Window.x}, {Window.y}\n"
      f"Pit menu color: {pit_color}\nFound Sellout Shop at: {sellout_shop}\n"
      f"OCR found this rebirth information:\n{rebirth_text}")

