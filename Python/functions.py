r"""This is a collection of functions that allows you to automate NGU-Idle.

Features that requires a bitmap, such as image_search and ocr will only work
with firefox, they also requires the window to NOT be minimized and the
computer cannot be locked. They still work fine even if you have another window
on top. Feel free to test any browser, but firefox will work. If firefox is
your main browser and you use these functions, you will notice that your script
will steal the focus from your main browsing window. This can be fixed by using
firefox profiles.

All functions assume the coordinates are relative to the game window, i.e.
the top left corner of the game is 0,0. This is preferable to using absolute
coordinates, because the location of the game window will not matter.

Run this command to install deps.

pip install -r requirements.txt

Install Tesseract OCR

https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.02-20180621.exe

Make sure you add tesseract.exe to your PATH, if you don't know how to, this
link might help you: https://www.java.com/en/download/help/path.xml

IGNORE THIS IF YOU DON'T USE FIREFOX FOR YOUR NORMAL BROWSING

1. In firefox enter "about:profiles" in the address field.
2. Create a new profile and name it (NGU, for example)
3. Go to your firefox installation folder, right click the "firefox.exe" file
   and select create shortcut.
4. Right click the shortcut and select properties.
5. In the target field, enter "-P YOURPROFILENAME -no-remote" after the
   quotation mark
   It should look like this:
   "C:\Program Files\Mozilla Firefox\firefox.exe" -P NGU -no-remote
6. Start firefox via the shortcut and load your NGU save.
"""

import cv2
import numpy
import pytesseract
import re
import time
import win32api
import win32gui
import win32ui


from ctypes import windll
from PIL import Image as image
from PIL import ImageFilter
from win32con import (VK_CONTROL, VK_SHIFT, VK_MENU, WM_KEYUP, WM_KEYDOWN,
                      WM_LBUTTONDOWN, WM_RBUTTONDOWN, WM_LBUTTONUP,
                      WM_RBUTTONUP, WM_MOUSEMOVE, MK_LBUTTON, MK_RBUTTON)
import ctypes
awareness = ctypes.c_int()
ctypes.windll.shcore.SetProcessDpiAwareness(2)


def get_hwnd():
    """Get the hwnd of the NGU IDLE window."""
    win32gui.EnumWindows(window_enumeration_handler, top_windows)
    for i in top_windows:
        if "play ngu idle" in i[1].lower():
            return i[0]


def window_enumeration_handler(hwnd, top_windows):
    """Iterate over active windows for gethwnd()."""
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def send_string(str):
    """Send one or multiple characters to the window."""
    for c in str:
        while (win32api.GetKeyState(VK_CONTROL) < 0 or
               win32api.GetKeyState(VK_SHIFT) < 0 or
               win32api.GetKeyState(VK_MENU) < 0):  # Avoid keyboard modifiers.
            time.sleep(0.005)
        if c.isdigit():  # Digits only require KEY_UP event.
            win32gui.PostMessage(hwnd, WM_KEYUP, ord(c.upper()), 0)
            time.sleep(0.03)  # This can probably be removed
            continue
        win32gui.PostMessage(hwnd, WM_KEYDOWN, ord(c.upper()), 0)
        time.sleep(0.30)  # This can probably be removed
        win32gui.PostMessage(hwnd, WM_KEYUP, ord(c.upper()), 0)

    time.sleep(0.1)  # This can probably be removed


def click(x, y, button="left"):
    """Click at pixel xy."""
    x += NGU_OFFSET_X
    y += NGU_OFFSET_Y
    lParam = win32api.MAKELONG(x, y)
    # MOUSEMOVE event is required for game to register clicks correctly
    win32gui.PostMessage(hwnd, WM_MOUSEMOVE, 0, lParam)

    while (win32api.GetKeyState(VK_CONTROL) < 0 or
           win32api.GetKeyState(VK_SHIFT) < 0 or
           win32api.GetKeyState(VK_MENU) < 0):  # Avoid keyboard modifiers.
        time.sleep(0.005)

    if (button == "left"):
        win32gui.PostMessage(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lParam)
        win32gui.PostMessage(hwnd, WM_LBUTTONUP, MK_LBUTTON, lParam)

    else:
        win32gui.PostMessage(hwnd, WM_RBUTTONDOWN, MK_RBUTTON, lParam)
        win32gui.PostMessage(hwnd, WM_RBUTTONUP, MK_RBUTTON, lParam)

    time.sleep(0.1)


def get_bitmap():
    """Get and return a bitmap of the window."""
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(save_bitmap)
    windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)
    bmpinfo = save_bitmap.GetInfo()
    bmpstr = save_bitmap.GetBitmapBits(True)

    # This creates an Image object from Pillow
    bmp = image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                           bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return bmp


def rgb_to_hex(tup):
    """Convert RGB value to HEX."""
    return '%02x%02x%02x'.upper() % (tup[0], tup[1], tup[2])


def pixel_search(color, x_start, y_start, x_end, y_end):
    """Find the first pixel with the supplied color within area.

    Function searches per row, left to right. Returns the coordinates of
    first match or None, if nothing is found.

    Color must be supplied in hex.
    """
    bmp = get_bitmap()
    for y in range(y_start, y_end):
        for x in range(x_start, x_end):
            t = bmp.getpixel((x, y))
            if (rgb_to_hex(t) == color):
                return x - 8, y - 8
    return None


def get_pixel_color(x, y):
    """Get the color of selected pixel in HEX."""
    return rgb_to_hex(get_bitmap().getpixel((x + 8 + NGU_OFFSET_X, y + 8 +
                                             NGU_OFFSET_Y)))


def ocr(x_start, y_start, x_end, y_end, debug=False):
    """Perform an OCR of the supplied area, returns a string of the result.

    Keyword arguments:
    debug -- saves an image of what is sent to the OCR (default False)
    """
    x_start += NGU_OFFSET_X
    x_end += NGU_OFFSET_X
    y_start += NGU_OFFSET_Y
    y_end += NGU_OFFSET_Y

    bmp = get_bitmap()
    # Bitmaps are created with a 8px border
    bmp = bmp.crop((x_start + 8, y_start + 8, x_end + 8, y_end + 8))
    *_, right, lower = bmp.getbbox()
    bmp = bmp.resize((right*3, lower*3), image.BICUBIC)
    bmp = bmp.filter(ImageFilter.SHARPEN)
    if debug:
        bmp.save("debug.png")
    s = pytesseract.image_to_string(bmp)
    return s


def image_search(x_start, y_start, x_end, y_end, image):
    """Search the screen for the supplied picture.

    Returns a tuple with x,y-coordinates.

    Keyword arguments:
    image -- Filename or path to file that you search for.
    """
    bmp = get_bitmap()
    # Bitmaps are created with a 8px border
    search_area = bmp.crop((x_start + 8, y_start + 8, x_end + 8, y_end + 8))
    search_area = numpy.asarray(search_area)
    search_area = cv2.cvtColor(search_area, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    res = cv2.matchTemplate(search_area, template, cv2.TM_CCOEFF)
    *_, t = cv2.minMaxLoc(res)
    return t


def remove_letters(s):
    """Remove all non digit characters from string."""
    return re.sub('[^0-9]', '', s)


top_windows = []
hwnd = get_hwnd()
NGU_OFFSET_X, NGU_OFFSET_Y = pixel_search("212429", 0, 0, 1920, 1080)
pit_color = get_pixel_color(195, 108)
rebirth_text = ocr(17, 370, 155, 400, True)
# This requires you to have the file "sellout.png"
sellout_shop = image_search(0, 0, 1920, 1080, "sellout.png")

print(f"Found top left of game window at: {NGU_OFFSET_X}, {NGU_OFFSET_Y}\n"
      f"Pit menu color: {pit_color}\nFound Sellout Shop at: {sellout_shop}\n"
      f"OCR found this rebirth information:\n{rebirth_text}")

"""
Expected output
------------------------------------------
Found top left of game window at: 320, 279
Pit color: FFFFFF
Found Sellout Shop at: (516, 751)
OCR found this rebirth information:
Current Rebirth Time:
6:29:22
"""
