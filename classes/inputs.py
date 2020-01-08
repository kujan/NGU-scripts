"""Input class contains functions for mouse and keyboard input."""
from ctypes import windll
import win32api
import win32con as wcon
import win32gui
import win32ui

import datetime
import os
import re
import time

from typing import Iterable, Optional, Tuple

from PIL import Image as image
from PIL import ImageFilter
import cv2
import numpy

import pytesseract

import usersettings as userset
from classes.window import Window

class Inputs:
    """This class handles inputs."""

    @staticmethod
    def click(x :int, y :int, button :str ="left", fast :bool =False) -> None:
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
    def click_drag(x :int, y :int, x2 :int, y2 :int) -> None:
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
    def ctrl_click(x :int, y :int) -> None:
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
    def send_arrow_press(left :bool) -> None:
        """Sends either a left or right arrow key press"""
        if left: key = wcon.VK_LEFT
        else   : key = wcon.VK_RIGHT
        
        win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN, key, 0)
        time.sleep(0.05)
        win32gui.PostMessage(Window.id, wcon.WM_KEYUP, key, 0)
        time.sleep(0.05)
    
    @staticmethod
    def send_string(string :str) -> None:
        """Send one or multiple characters to the Window."""
        # Ensure it's a string by converting it to a string
        if isinstance(string, float):
            string = int(string)
        for c in str(string):
            # Make sure no key modifier is pressed
            while (win32api.GetKeyState(wcon.VK_CONTROL) < 0 or
                   win32api.GetKeyState(wcon.VK_SHIFT)   < 0 or
                   win32api.GetKeyState(wcon.VK_MENU)    < 0):
                time.sleep(0.005)
            
            vkc = win32api.VkKeyScan(c)  # Get virtual key code for character c
            # Only one keyup or keydown event needs to be sent
            win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN, vkc, 0)
    
    @staticmethod
    def get_bitmap() -> image:
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

    @staticmethod
    def get_cropped_bitmap(x_start :int =0, y_start :int =0, x_end :int =960, y_end :int =600) -> image:
        return Inputs.get_bitmap().crop(
            (x_start + 8, y_start + 8, x_end + 8, y_end + 8))
    
    @staticmethod
    def pixel_search(color :str, x_start :int, y_start :int, x_end :int, y_end :int) -> Optional[Tuple[int, int]]:
        """Find the first pixel with the supplied color within area.
        
        Function searches per row, left to right. Returns the coordinates of
        first match or None, if nothing is found.
        
        Color must be supplied in hex.
        """
        bmp = Inputs.get_bitmap()
        width, height = bmp.size
        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                if y > height or x > width:
                    continue
                t = bmp.getpixel((x, y))
                if Inputs.rgb_to_hex(t) == color:
                    return x - 8, y - 8
        
        return None

    @staticmethod
    def image_search(x_start :int, y_start :int, x_end :int, y_end :int,
                     img :str, threshold :int, bmp :image =None) -> Optional[Tuple[int, int]]:
        """Search the screen for the supplied picture.
        
        Returns a tuple with x,y-coordinates, or None if result is below
        the threshold.
        
        Keyword arguments:
        image     -- Filename or path to file that you search for.
        threshold -- The level of fuzziness to use - a perfect match will be
                     close to 1, but probably never 1. In my testing use a
                     value between 0.7-0.95 depending on how strict you wish
                     to be.
        bmp       -- a bitmap from the get_bitmap() function, use this if you're
                     performing multiple different OCR-readings in succession
                     from the same page. This is to avoid to needlessly get the
                     same bitmap multiple times. If a bitmap is not passed, the
                     function will get the bitmap itself. (default None)
        """
        if not bmp: bmp = Inputs.get_bitmap()
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

    @staticmethod
    def find_all(
        x_start :int,
        y_start :int,
        x_end :int,
        y_end :int,
        img :str,
        threshold: float,
        bmp :image=None) -> tuple:
        """Search the screen for the supplied picture.
        
        Returns a list with x, y-coordinates with all matches, or None if result is below
        the threshold.
        
        Keyword arguments:
        image     -- Filename or path to file that you search for.
        threshold -- The level of fuzziness to use - a perfect match will be
                     close to 1, but probably never 1. In my testing use a
                     value between 0.7-0.95 depending on how strict you wish
                     to be.
        bmp       -- a bitmap from the get_bitmap() function, use this if you're
                     performing multiple different OCR-readings in succession
                     from the same page. This is to avoid to needlessly get the
                     same bitmap multiple times. If a bitmap is not passed, the
                     function will get the bitmap itself. (default None)
        """
        if not bmp: bmp = Inputs.get_bitmap()
        # Bitmaps are created with a 8px border
        search_area = bmp.crop((x_start + 8, y_start + 8,
                                x_end + 8, y_end + 8))
        search_area = numpy.asarray(search_area)
        search_area = cv2.cvtColor(search_area, cv2.COLOR_RGB2GRAY)
        template = cv2.imread(img, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(search_area, template, cv2.TM_CCOEFF_NORMED)
        locs = numpy.where(res >= threshold)
        lst = []
        for loc in zip(*locs[::-1]):
            lst.append((loc[0] + w // 2, loc[1] + h // 2))
        return lst

    @staticmethod
    def rgb_equal(a :Tuple[int, int, int], b :Tuple[int, int, int]) -> bool:
        if a[0] != b[0]: return False
        if a[1] != b[1]: return False
        if a[2] != b[2]: return False
        return True
    
    @staticmethod
    def ocr(
         x_start :int,
         y_start :int,
         x_end :int,
         y_end :int,
         debug :bool =False,
         bmp :image =None,
         cropb :bool =False,
         filter :bool =True,
         binf :int =0,
         sliced :bool =False
     ) -> str:
        """Perform an OCR of the supplied area, returns a string of the result.
        
        Keyword arguments
        debug  -- Saves an image of what is sent to the OCR (default False)
        bmp    -- A bitmap from the get_bitmap() function, use this if you're
                  performing multiple different OCR-readings in succession from
                  the same page. This is to avoid to needlessly get the same
                  bitmap multiple times. If a bitmap is not passed, the function
                  will get the bitmap itself. (default None)
        cropb  -- Whether the bmp provided should be cropped.
        filter -- Whether to filter the image for better OCR.
        binf   -- Threshold value for binarizing filter. Zero means no filtering.
        sliced -- Whether the image has ben sliced so there's very little blank
                  space. Gets better readings from small values for some reason.
        """
        x_start += Window.x
        x_end   += Window.x
        y_start += Window.y
        y_end   += Window.y

        if bmp is None:
            bmp = Inputs.get_cropped_bitmap(x_start, y_start, x_end, y_end)
        
        elif cropb:
            # Bitmaps are created with a 8px border
            bmp = bmp.crop((x_start + 8, y_start + 8, x_end + 8, y_end + 8))
        
        if binf > 0: # Binarizing Filter
            fn = lambda x : 255 if x > binf else 0
            bmp = bmp.convert('L') # To Monochrome
            bmp = bmp.point(fn, mode='1')
            if debug: bmp.save("debug_ocr_whiten.png")
        
        if filter: # Resizing and sharpening
            *_, right, lower = bmp.getbbox()
            bmp = bmp.resize((right * 4, lower * 4), image.BICUBIC)  # Resize image
            bmp = bmp.filter(ImageFilter.SHARPEN)
            if debug: bmp.save("debug_ocr_filter.png")
            
        if sliced: s = pytesseract.image_to_string(bmp, config='--psm 6')
        else:      s = pytesseract.image_to_string(bmp, config='--psm 4')
        
        return s

    @staticmethod
    def get_pixel_color(x :int, y :int, debug :bool =False) -> str:
        """Get the color of selected pixel in HEX."""
        dc = win32gui.GetWindowDC(Window.id)
        rgba = win32gui.GetPixel(dc, x + 8 + Window.x, y + 8 + Window.y)
        win32gui.ReleaseDC(Window.id, dc)
        r = rgba & 0xff
        g = rgba >> 8 & 0xff
        b = rgba >> 16 & 0xff
        
        if debug: print(Inputs.rgb_to_hex((r, g, b)))
        
        return Inputs.rgb_to_hex((r, g, b))

    @staticmethod
    def check_pixel_color(x :int, y :int, checks :Iterable[str], debug :bool =False) -> bool:
        """Check if coordinate matches with one or more colors."""
        color = Inputs.get_pixel_color(x, y, debug=debug)
        if isinstance(checks, list):
            for check in checks:
                if check == color:
                    return True

        return color == checks

    @staticmethod
    def remove_spaces(s :str) -> str:
        """Remove all spaces from string."""
        return "".join(s.split(" "))

    @staticmethod
    def remove_number_separators(s :str) -> str:
        """Remove all separators from number."""
        return "".join(s.split(","))
    
    @staticmethod
    def remove_letters(s :str) -> str:
        """Remove all non digit characters from string."""
        return re.sub('[^0-9]', '', s)

    @staticmethod
    def get_numbers(s :str) -> Iterable[int]:
        """Finds all numbers in a string"""
        s = Inputs.remove_spaces(s)
        s = Inputs.remove_number_separators(s)
        match = re.findall(r"(\d+(\.\d+E\+\d+)?)", s)
        nums = [int(float(x[0])) for x in match]
        return nums
    
    @staticmethod
    def rgb_to_hex(tup :Tuple[int, int, int]) -> str:
        """Convert RGB value to hex."""
        return '%02x%02x%02x'.upper() % (tup[0], tup[1], tup[2])

    @staticmethod
    def hex_to_rgb(str :str) -> Tuple[int, int, int]:
        """Convert hex value to RGB."""
        return tuple(int(str[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def get_file_path(directory :str, file :str) -> str:
        """Get the absolute path for a file."""
        working = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(working, directory, file)
        return path

    @staticmethod
    def ocr_number(x_1 :int, y_1 :int, x_2 :int, y_2 :int) -> int:
        """Remove all non-digits."""
        return int(Inputs.remove_letters(Inputs.ocr(x_1, y_1, x_2, y_2)))

    @staticmethod
    def ocr_notation(x_1 :int, y_1 :int, x_2 :int, y_2 :int) -> int:
        """Convert scientific notation from string to int."""
        return int(float(Inputs.ocr(x_1, y_1, x_2, y_2)))

    @staticmethod
    def save_screenshot() -> None:
        """Save a screenshot of the game."""
        bmp = Inputs.get_bitmap()
        bmp = bmp.crop((Window.x + 8, Window.y + 8, Window.x + 968, Window.y + 608))
        if not os.path.exists("screenshots"):
            os.mkdir("screenshots")
        bmp.save('screenshots/' + datetime.datetime.now().strftime('%d-%m-%y-%H-%M-%S') + '.png')
