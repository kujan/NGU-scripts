import cv2
import io
import numpy
import pytesseract
import re
import time
import win32api
import win32gui
import win32ui


from ctypes import windll
from ngucon import *
from PIL import Image as image
from PIL import ImageEnhance, ImageFilter
from win32con import *

"""
Run this command to install deps.
pip install -r requirements.txt

Install Tesseract OCR: https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.02-20180621.exe
Make sure you add tesseract.exe to your PATH, if you don't know how to, this link might help you
https://www.java.com/en/download/help/path.xml
"""

def get_hwnd():
  win32gui.EnumWindows(window_enumeration_handler, top_windows)
  for i in top_windows:
    if "play ngu idle" in i[1].lower():
      return i[0]

def window_enumeration_handler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def send_string(str):
  for c in str:
    win32gui.PostMessage(hwnd, WM_KEYDOWN, ord(c.upper()), 0)
    win32gui.PostMessage(hwnd, WM_KEYUP, ord(c.upper()), 0)

def click(x, y, button="left"):
  x += ngu_offset_x
  y += ngu_offset_y

  lParam = win32api.MAKELONG(x, y)
  win32gui.PostMessage(hwnd, WM_MOUSEMOVE, 0, lParam)
  if (button == "left"):
    win32gui.PostMessage(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lParam)
    win32gui.PostMessage(hwnd, WM_LBUTTONUP, MK_LBUTTON, lParam)
  else:
    win32gui.PostMessage(hwnd, WM_RBUTTONDOWN, MK_RBUTTON, lParam)
    win32gui.PostMessage(hwnd, WM_RBUTTONUP, MK_RBUTTON, lParam)
  time.sleep(0.015)

def get_bitmap():
  left, top, right, bot = win32gui.GetWindowRect(hwnd)
  w = right - left
  h = bot - top
  hwnd_dc = win32gui.GetWindowDC(hwnd)
  mfc_dc  = win32ui.CreateDCFromHandle(hwnd_dc)
  save_dc = mfc_dc.CreateCompatibleDC()

  save_bitmap = win32ui.CreateBitmap()
  save_bitmap.CreateCompatibleBitmap(mfc_dc, w, h)

  save_dc.SelectObject(save_bitmap)

  result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 0)

  bmpinfo = save_bitmap.GetInfo()
  bmpstr = save_bitmap.GetBitmapBits(True)

  bmp = image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr, 'raw', 'BGRX', 0, 1)

  win32gui.DeleteObject(save_bitmap.GetHandle())
  save_dc.DeleteDC()
  mfc_dc.DeleteDC()
  win32gui.ReleaseDC(hwnd, hwnd_dc)

  return bmp

def rgb_to_hex(tup):
  return '%02x%02x%02x'.upper() % (tup[0], tup[1], tup[2])

def pixel_search(color, x_start, y_start, x_end, y_end):
  bmp = get_bitmap()
  for y in range(y_start + 8, y_end):
    for x in range(x_start + 8, x_end):
      t = bmp.getpixel((x, y))
      if (rgb_to_hex(t) == color):
        return x + 8, y + 8
  return None
"""
def pixel_search2(color, x_start, y_start, x_end, y_end):
  bmp = get_bitmap()
  bmp = numpy.asarray(bmp)
  print(bmp.shape)
  for y in range(y_start, y_end):
    for x in range(x_start, x_end):
      pixel = bmp[y, x]
      if (rgb_to_hex((pixel[0], pixel[1], pixel[2])) == color):
        print(x, y)
        return
      #print(x,y)
      #print(rgb_to_hex((pixel[0], pixel[1], pixel[2])))
"""
def pixel_get_color(x, y):
  return rgb_to_hex(get_bitmap().getpixel((x + 8 + ngu_offset_x, y + 8 + ngu_offset_y)))

def ocr(x_start, y_start, x_end, y_end, debug=False):
  x_start += ngu_offset_x
  x_end   += ngu_offset_x
  y_start += ngu_offset_y
  y_end   += ngu_offset_y

  bmp = get_bitmap()
  bmp = bmp.crop((x_start + 8, y_start + 8, x_end, y_end))
  *_, right, lower = bmp.getbbox()
  bmp = bmp.resize((right*3, lower*3), image.BICUBIC)
  #bmp = ImageEnhance.Contrast(bmp).enhance(0.5)
  #bmp = bmp.ImageEnhance(bmp)
  bmp = bmp.filter(ImageFilter.SHARPEN)
  if debug: 
    bmp.save("debug.png")
  s = pytesseract.image_to_string(bmp)
  return re.sub('[^0-9]','', s)

def image_search(x_start, y_start, x_end, y_end, image):
  bmp = get_bitmap()
  search_area = bmp.crop((x_start + 8, y_start + 8, x_end, y_end))
  search_area = numpy.asarray(search_area)
  search_area = cv2.cvtColor(search_area, cv2.COLOR_BGR2GRAY)
  template = cv2.imread(image, 0)
  res = cv2.matchTemplate(search_area, template, cv2.TM_CCOEFF)
  *_, t = cv2.minMaxLoc(res)
  return t

def navigate(target):
  y = NguResolutionY
  x = NguResolutionX
  if (target == "inventory"):
    y += InventoryMenuOffsetY
  elif (target == "timemachine"):
    y += TimeMachineMenuOffsetY
  elif (target == "ngu"):
    y += NguMenuOffsetY
  elif (target == "augmentations"):
    y += AugmentationMenuOffsetY
  elif (target == "bloodmagic"):
    y += BloodMagicMenuOffsetY
  elif (target == "advtraining"):
    y += AdvTrainingMenuOffsetY
  elif (target == "adventure"):
    y += AdventureMenuOffsetY
  elif (target == "yggdrasil"):
    y += YggdrasilMenuOffsetY
  elif (target == "rebirth"):
    x += RebirthX
    y += RebirthY
  elif (target == "pit"):
    y += PitMenuOffsetY
  click(x,y)


#time.sleep(1)
top_windows = []
hwnd = get_hwnd()

print("window id: " + str(hwnd))
ngu_offset_x, ngu_offset_y = pixel_search("212429", 0, 0, 500, 1070)
print("top left corner at: " + str(ngu_offset_x) + ", " + str(ngu_offset_y))
print("reclaiming energy and magic")
#send_string("tr")
print("clicking fight boss")
click(230,75)
time.sleep(0.2)
s = ocr(760, 112, 875, 132)
print("current boss: " + s)
pix = pixel_get_color(512, 440)
print("money pit menu color: " + pix)
i1 = image_search(0,0,1920,1080, 'img.png')
i2 = image_search(0,0,1920,1080, 'fight.png')
i3 = image_search(0,0,1920,1080, 'stats.png')
print("found bossfight image at: " + str(i1))
print("found fight button image at: " + str(i2))
print("found stats text image at: " + str(i3))

#pixel_search2(212429, 0,0,500,1000)
"""
Output
------------------------------
window id: 1639182
top left corner at: 336, 346
reclaiming energy and magic
clicking fight boss
current boss: 28
money pit menu color: 6889A4
found bossfight image at: (840, 338)
found fight button image at: (877, 518)
found stats text image at: (373, 337)
[Finished in 1.7s]

"""