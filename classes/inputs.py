"""Input class contains functions for mouse and keyboard input."""
from ctypes import windll
import datetime
import os
import re
import time

from PIL import Image as image
from PIL import ImageFilter, ImageEnhance
import cv2
import numpy
import pytesseract
import win32api
import win32con as wcon
import win32gui
import win32ui

import usersettings as userset
from classes.window import Window

class Inputs():
    """This class handles inputs."""

    @staticmethod
    def click(x, y, button="left", fast=False):
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
        if button == "left":
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
        if fast:
            time.sleep(userset.FAST_SLEEP)
        else:
            time.sleep(userset.MEDIUM_SLEEP)

    @staticmethod
    def click_drag(x, y, x2, y2):
        """Click at pixel xy."""
        x += Window.x
        y += Window.y
        x2 += Window.x
        y2 += Window.y
        lParam = win32api.MAKELONG(x, y)
        lParam2 = win32api.MAKELONG(x2, y2)
        # MOUSEMOVE event is required for game to register clicks correctly
        win32gui.PostMessage(Window.id, wcon.WM_MOUSEMOVE, 0, lParam)
        while (win32api.GetKeyState(wcon.VK_CONTROL) < 0 or
               win32api.GetKeyState(wcon.VK_SHIFT) < 0 or
               win32api.GetKeyState(wcon.VK_MENU) < 0):
            time.sleep(0.005)
        win32gui.PostMessage(Window.id, wcon.WM_LBUTTONDOWN,
                             wcon.MK_LBUTTON, lParam)
        time.sleep(userset.LONG_SLEEP * 2)
        win32gui.PostMessage(Window.id, wcon.WM_MOUSEMOVE, 0, lParam2)
        time.sleep(userset.SHORT_SLEEP)
        win32gui.PostMessage(Window.id, wcon.WM_LBUTTONUP,
                             wcon.MK_LBUTTON, lParam2)
        time.sleep(userset.MEDIUM_SLEEP)

    @staticmethod
    def ctrl_click(x, y):
        """Clicks at pixel x, y while simulating the CTRL button to be down."""
        x += Window.x
        y += Window.y
        lParam = win32api.MAKELONG(x, y)
        while (win32api.GetKeyState(wcon.VK_CONTROL) < 0 or
               win32api.GetKeyState(wcon.VK_SHIFT) < 0 or
               win32api.GetKeyState(wcon.VK_MENU) < 0):
            time.sleep(0.005)

        win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN, wcon.VK_CONTROL, 0)
        win32gui.PostMessage(Window.id, wcon.WM_LBUTTONDOWN,
                             wcon.MK_LBUTTON, lParam)
        win32gui.PostMessage(Window.id, wcon.WM_LBUTTONUP,
                             wcon.MK_LBUTTON, lParam)
        win32gui.PostMessage(Window.id, wcon.WM_KEYUP, wcon.VK_CONTROL, 0)
        time.sleep(userset.MEDIUM_SLEEP)

    @staticmethod
    def send_string(string):
        """Send one or multiple characters to the Window."""
        if isinstance(string, str) == float:  # Remove decimal
            string = str(int(string))
        for c in str(string):
            while (win32api.GetKeyState(wcon.VK_CONTROL) < 0 or
                   win32api.GetKeyState(wcon.VK_SHIFT) < 0 or
                   win32api.GetKeyState(wcon.VK_MENU) < 0):
                time.sleep(0.005)
            if c.isdigit():  # Digits only require KEY_UP event.
                win32gui.PostMessage(Window.id, wcon.WM_KEYUP, ord(c.upper()),
                                     0)
                # time.sleep(0.03)  # This can probably be removed
                continue
            win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN, ord(c.upper()), 0)
            time.sleep(userset.SHORT_SLEEP)  # This can probably be removed
            win32gui.PostMessage(Window.id, wcon.WM_KEYUP, ord(c.upper()), 0)
        time.sleep(userset.SHORT_SLEEP)

    @staticmethod
    def get_bitmap():
        """Get and return a bitmap of the Window."""
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
        # bmp.save("asdf.png")
        return bmp

    @classmethod
    def pixel_search(cls, color, x_start, y_start, x_end, y_end):
        """Find the first pixel with the supplied color within area.

        Function searches per row, left to right. Returns the coordinates of
        first match or None, if nothing is found.

        Color must be supplied in hex.
        """
        bmp = cls.get_bitmap()
        width, height = bmp.size
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                if y > height or x > width:
                    continue
                t = bmp.getpixel((x, y))
                if cls.rgb_to_hex(t) == color:
                    return x - 8, y - 8

        return None

    @classmethod
    def image_search(cls, x_start, y_start, x_end, y_end, img, threshold, bmp=None):
        """Search the screen for the supplied picture.

        Returns a tuple with x,y-coordinates, or None if result is below
        the threshold.

        Keyword arguments:
        image -- Filename or path to file that you search for.
        threshold -- The level of fuzziness to use - a perfect match will be
                     close to 1, but probably never 1. In my testing use a
                     value between 0.7-0.95 depending on how strict you wish
                     to be.
        bmp -- a bitmap from the get_bitmap() function, use this if you're
               performing multiple different OCR-readings in succession from
               the same page. This is to avoid to needlessly get the same
               bitmap multiple times. If a bitmap is not passed, the function
               will get the bitmap itself. (default None)
        """
        if not bmp:
            bmp = cls.get_bitmap()
        # Bitmaps are created with a 8px border
        search_area = bmp.crop((x_start + 8, y_start + 8,
                                x_end + 8, y_end + 8))
        search_area = numpy.asarray(search_area)
        search_area = cv2.cvtColor(search_area, cv2.COLOR_RGB2GRAY)
        template = cv2.imread(img, 0)
        res = cv2.matchTemplate(search_area, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val < threshold:
            return None

        return max_loc

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
        bmp = bmp.resize((right*4, lower*4), image.BICUBIC)  # Resize image
        enhancer = ImageEnhance.Sharpness(bmp)
        bmp = enhancer.enhance(0)
        bmp = bmp.filter(ImageFilter.SHARPEN)  # Sharpen image for better OCR

        if debug:
            bmp.save("debug_ocr.png")
        s = pytesseract.image_to_string(bmp, config='--psm 4')
        return s

    def get_pixel_color(self, x, y, debug=False):
        """Get the color of selected pixel in HEX."""
        dc = win32gui.GetWindowDC(Window.id)
        rgba = win32gui.GetPixel(dc, x + 8 + Window.x, y + 8 + Window.y)
        win32gui.ReleaseDC(Window.id, dc)
        r = rgba & 0xff
        g = rgba >> 8 & 0xff
        b = rgba >> 16 & 0xff

        if debug:
            print(self.rgb_to_hex((r, g, b)))

        return self.rgb_to_hex((r, g, b))

    @classmethod
    def check_pixel_color(cls, x, y, checks):
        """Check if coordinate matches with one or more colors."""
        color = cls.get_pixel_color(cls, x, y)
        if isinstance(checks, list):
            for check in checks:
                if check == color:
                    return True

        return color == checks

    @staticmethod
    def remove_letters(s):
        """Remove all non digit characters from string."""
        return re.sub('[^0-9]', '', s)

    @staticmethod
    def rgb_to_hex(tup):
        """Convert RGB value to HEX."""
        return '%02x%02x%02x'.upper() % (tup[0], tup[1], tup[2])

    @staticmethod
    def get_file_path(directory, file):
        """Get the absolute path for a file."""
        working = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(working, directory, file)
        return path

    @classmethod
    def ocr_number(cls, x_1, y_1, x_2, y_2):
        """Remove all non-digits."""
        return int(cls.remove_letters(cls.ocr(cls, x_1, y_1, x_2, y_2)))

    @classmethod
    def ocr_notation(cls, x_1, y_1, x_2, y_2):
        """Convert scientific notation from string to int."""
        return int(float(cls.ocr(cls, x_1, y_1, x_2, y_2)))

    @classmethod
    def save_screenshot(cls):
        """Save a screenshot of the game."""
        bmp = cls.get_bitmap()
        bmp = bmp.crop((Window.x + 8, Window.y + 8, Window.x + 968, Window.y + 608))
        if not os.path.exists("screenshots"):
            os.mkdir("screenshots")
        bmp.save('screenshots/' + datetime.datetime.now().strftime('%d-%m-%y-%H-%M-%S') + '.png')
