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
    while (win32api.GetKeyState(VK_CONTROL) < 0 or win32api.GetKeyState(VK_SHIFT) < 0):
      time.sleep(0.005)
    if c.isdigit():
      win32gui.PostMessage(hwnd, WM_KEYUP, ord(c.upper()), 0)
      time.sleep(0.030)
      continue
    win32gui.PostMessage(hwnd, WM_KEYDOWN, ord(c.upper()), 0)
    time.sleep(0.30)
    win32gui.PostMessage(hwnd, WM_KEYUP, ord(c.upper()), 0)

  time.sleep(0.1)

def click(x, y, button="left"):
  x += NGU_OFFSET_X
  y += NGU_OFFSET_Y
  lParam = win32api.MAKELONG(x, y)
  win32gui.PostMessage(hwnd, WM_MOUSEMOVE, 0, lParam)
  if (button == "left"):
    win32gui.PostMessage(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, lParam)
    win32gui.PostMessage(hwnd, WM_LBUTTONUP, MK_LBUTTON, lParam)
  else:
    win32gui.PostMessage(hwnd, WM_RBUTTONDOWN, MK_RBUTTON, lParam)
    win32gui.PostMessage(hwnd, WM_RBUTTONUP, MK_RBUTTON, lParam)
  time.sleep(0.1)

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
  for y in range(y_start, y_end):
    for x in range(x_start, x_end):
      t = bmp.getpixel((x, y))
      if (rgb_to_hex(t) == color):
        return x - 8, y - 8
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
  return rgb_to_hex(get_bitmap().getpixel((x + 8 + NGU_OFFSET_X, y + 8 + NGU_OFFSET_Y)))

def ocr(x_start, y_start, x_end, y_end, debug=False):
  x_start += NGU_OFFSET_X
  x_end   += NGU_OFFSET_X
  y_start += NGU_OFFSET_Y
  y_end   += NGU_OFFSET_Y

  bmp = get_bitmap()
  bmp = bmp.crop((x_start + 8, y_start + 8, x_end + 8, y_end + 8))
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
  search_area = bmp.crop((x_start + 8, y_start + 8, x_end + 8, y_end + 8))
  search_area = numpy.asarray(search_area)
  search_area = cv2.cvtColor(search_area, cv2.COLOR_BGR2GRAY)
  template = cv2.imread(image, 0)
  res = cv2.matchTemplate(search_area, template, cv2.TM_CCOEFF)
  *_, t = cv2.minMaxLoc(res)
  return t

def navigate(target):
  y = 0
  x = MENUOFFSETX
  if (target == "inventory"):
    y += INVENTORYMENUOFFSETY
  elif (target == "timemachine"):
    y += TIMEMACHINEMENUOFFSETY
  elif (target == "ngu"):
    y += NGUMENUOFFSETY
  elif (target == "augmentations"):
    y += AUGMENTATIONMENUOFFSETY
  elif (target == "bloodmagic"):
    y += BLOODMAGICMENUOFFSETY
  elif (target == "advtraining"):
    y += ADVTRAININGMENUOFFSETY
  elif (target == "adventure"):
    y += ADVENTUREMENUOFFSETY
  elif (target == "yggdrasil"):
    y += YGGDRASILMENUOFFSETY
  elif (target == "rebirth"):
    x = REBIRTHX
    y += REBIRTHY
  elif (target == "pit"):
    y += PITMENUOFFSETY
  elif (target == "fight"):
    y += FIGHTBOSSMENUOFFSETY
  elif (target == "exp"):
    x = EXPX
    y += EXPY
  elif (target == "wandoos"):
    y += WANADOOSMENUOFFSETY
  click(x,y, button="left")
  time.sleep(0.050)

def do_inventory():
  navigate("inventory")
  t_end = time.time() + 10
  while time.time() < t_end:
    if (AUTOMERGEEQUIPMENT):
      click(ACCESSORY1OFFSETX, ACCESSORY1OFFSETY, button="left")
      send_string("d")
      click(ACCESSORY2OFFSETX, ACCESSORY2OFFSETY, button="left")
      send_string("d")
      click(HEADOFFSETX, HEADOFFSETY, button="left")
      send_string("d")
      click(CHESTOFFSETX, CHESTOFFSETY, button="left")
      send_string("d")
      click(LEGSOFFSETX, LEGSOFFSETY, button="left")
      send_string("d")
      click(BOOTSOFFSETX, BOOTSOFFSETY, button="left")
      send_string("d")
      click(WEAPONOFFSETX, WEAPONOFFSETY, button="left")
    if (AUTOBOOSTEQUIPMENT):
      click(ACCESSORY1OFFSETX, ACCESSORY1OFFSETY, button="left")
      send_string("a")
      click(ACCESSORY2OFFSETX, ACCESSORY2OFFSETY, button="left")
      send_string("a")
      click(HEADOFFSETX, HEADOFFSETY, button="left")
      send_string("a")
      click(CHESTOFFSETX, CHESTOFFSETY, button="left")
      send_string("a")
      click(LEGSOFFSETX, LEGSOFFSETY, button="left")
      send_string("a")
      click(BOOTSOFFSETX, BOOTSOFFSETY, button="left")
      send_string("a")
      click(WEAPONOFFSETX, WEAPONOFFSETY, button="left")
      send_string("a")
    if (CUBE):
      click(CUBEOFFSETX, CUBEOFFSETY, button="right")

def do_fight():
  navigate("fight")
  click(NUKEX, NUKEY, button="left")
  time.sleep(2)
  click(FIGHTX, FIGHTY, button="left")

def do_adventure(zone=0, highest=True, itopod=None, itopodauto=None):
  navigate("adventure")

  if itopod:
    click(ITOPODX, ITOPODY, button="left")
    if itopodauto:
      click(ITOPODENDX, ITOPODENDY, button="left")
      send_string("0") # set end to 0 in case it's higher than start
      click(ITOPODAUTOX, ITOPODAUTOY, button="left")
      click(ITOPODENTERX, ITOPODENTERY, button="left")
      return
    
    click(ITOPODSTARTX, ITOPODSTARTY, button="left")
    send_string(itopod)
    click(ITOPODENDX, ITOPODENDY, button="left")
    send_string(itopod)
    click(ITOPODENTERX, ITOPODENTERY, button="left")
    return
  if highest:
    click(RIGHTARROWX, RIGHTARROWY, button="right")
    return
  else:
    click(LEFTARROWX, LEFTARROWY, button="right")
    for i in range(zone):
      click(RIGHTARROWX, RIGHTARROWY, button="left")
    return

def do_snipe(zone, duration, once=False, highest=False):
  navigate("adventure")
  if highest:
    click(RIGHTARROWX, RIGHTARROWY, button="right")
  else:
    click(LEFTARROWX, LEFTARROWY, button="right")

    for i in range(zone):
      click(RIGHTARROWX, RIGHTARROWY, button="left")

  idle = pixel_get_color(IDLEX, IDLEY)

  #if (idle != IDLECOLOR):
  #  send_string("q")

  t_end = time.time() + (duration * 60)
  while time.time() < t_end:
    health = pixel_get_color(HEALTHX, HEALTHY)
    if (health == NOTDEAD):
      crown = pixel_get_color(CROWNX, CROWNY)
      if (crown == ISBOSS):
        while (health != DEAD):
          health = pixel_get_color(HEALTHX, HEALTHY)
          send_string("ytew")
          time.sleep(0.15)

        if once:
          break

      else:
        win32gui.PostMessage(hwnd, WM_KEYDOWN, VK_LEFT, 0)
        time.sleep(0.03)
        win32gui.PostMessage(hwnd, WM_KEYUP, VK_LEFT, 0)
        win32gui.PostMessage(hwnd, WM_KEYDOWN, VK_RIGHT, 0)  
        time.sleep(0.03)
        win32gui.PostMessage(hwnd, WM_KEYUP, VK_RIGHT, 0)
    time.sleep(0.1)
  #send_string("q")
        
def do_pit():
  color = pixel_get_color(PITCOLORX, PITCOLORY)
  if (color == PITREADY): 
    navigate("pit")
    click(PITX, PITY)
    click(PITCONFIRMX, PITCONFIRMY, button="left")
  return

def do_rebirth(challenge=None):
  navigate("yggdrasil")
  for i in range(1, 10):
    click(FRUITSX[i], FRUITSY[i], button="left")

  navigate("rebirth")
  if challenge:
    print("chall")
    time.sleep(1)
    click(CHALLENGEBUTTONX, CHALLENGEBUTTONY, button="left")
    color = pixel_get_color(CHALLENGEACTIVEX, CHALLENGEACTIVEY)
    if (color == CHALLENGEACTIVECOLOR):
      do_rebirth()
      return
    click(CHALLENGEX, CHALLENGEY + (CHALLENGEOFFSET * challenge), button="left")
    click(REBIRTHCONFIRMX, REBIRTHCONFIRMY, button="left")
    return
  else:
    click(REBIRTHX, REBIRTHY, button="left")
    click(REBIRTHBUTTONX, REBIRTHBUTTONY, button="left")
    click(REBIRTHCONFIRMX, REBIRTHCONFIRMY, button="left")
  return

def do_advanced_training():
  navigate("advtraining")
  click(NUMBERINPUTBOXX, NUMBERINPUTBOXY, button="left")
  send_string("1337")
  click(ADVTRAININGX, ADVTRAINING1Y, button="left")
  click(NUMBERINPUTBOXX, NUMBERINPUTBOXY, button="left")
  send_string("1447")
  
  click(ADVTRAININGX, ADVTRAINING2Y, button="left")

def do_time_machine(mult=False):
  navigate("timemachine")
  click(NUMBERINPUTBOXX, NUMBERINPUTBOXY, button="left")
  send_string("5000000")
  click(TMSPEEDX, TMSPEEDY, button="left")
  if mult:
    click(TMMULTX, TMMULTY, button="left")
  return

def do_blood_magic():
  navigate("bloodmagic")
  click(NUMBERINPUTBOXX, NUMBERINPUTBOXY, button="left")
  send_string("10000000")
  click(BMX, BM3, button="left")
def get_values():
  navigate("exp")
  values = {}

def do_wandoos(magic=False):
  navigate("wandoos")
  click(NUMBERINPUTBOXX, NUMBERINPUTBOXY, button="left")
  send_string("500000000")
  click(WANDOOSENERGYX, WANDOOSENERGYY, button="left")
  if magic:
    click(WANDOOSMAGICX, WANDOOSMAGICY, button="left")
def challenge2():
  t_end = time.time() + (60 * 60)
  magic_assigned = False
  do_tm = True
  early_wandoos = True
  do_rebirth(challenge=2)
  do_fight()
  do_snipe(0, 2, once=True, highest=True)
  time.sleep(1)
  do_adventure(zone=0, highest=False, itopod=True, itopodauto=True)
  i = 0
  while time.time() < t_end:
    bm_color = pixel_get_color(BMLOCKEDX, BMLOCKEDY)
    tm_color = pixel_get_color(TMLOCKEDX, TMLOCKEDY)
    if not magic_assigned and tm_color != TMLOCKEDCOLOR:
      print("doing tm with mult")
      do_time_machine(True)
    elif do_tm and tm_color != TMLOCKEDCOLOR:
      print("doing tm without mult")
      do_time_machine()
    if time.time() > t_end - (30 * 60):
      if do_tm:
        send_string("r")
        do_tm = False
      do_wandoos()
    
    if (bm_color != BMLOCKEDCOLOR and not magic_assigned and time.time() > t_end - (30 * 60)):
      print("assigning magic")
      send_string("t")
      do_blood_magic()
      magic_assigned = True
    elif early_wandoos and bm_color == BMLOCKEDCOLOR and tm_color == TMLOCKEDCOLOR: #add magic to wandoos if BM is not unlock
      do_wandoos(magic=True)

    do_inventory()
    i += 1
    if i > 15:
      do_fight()
      i = 0
  do_fight()
  do_pit()
  time.sleep(15)
  return

AUTOMERGEEQUIPMENT = True
AUTOBOOSTEQUIPMENT = True
CUBE = True
time.sleep(1)
top_windows = []
hwnd = get_hwnd()
NGU_OFFSET_X, NGU_OFFSET_Y = pixel_search("212429", 0, 0, 500, 1070)


while True:
  challenge2()

#print("window id: " + str(hwnd))

#print("top left corner at: " + str(NGU_OFFSET_X) + ", " + str(NGU_OFFSET_Y))
#print("reclaiming energy and magic")
#send_string("tr")
#print("clicking fight boss")
#navigate("fight")
#time.sleep(0.4)
#s = ocr(765, 125, 890, 140, True)
#print("current boss: " + s)
#pix = pixel_get_color(512, 440)
#print("money pit menu color: " + pix)
#i1 = image_search(0,0,1920,1080, 'img.png')
#i2 = image_search(0,0,1920,1080, 'fight.png')
#i3 = image_search(0,0,1920,1080, 'stats.png')
#print("found bossfight image at: " + str(i1))
#print("found fight button image at: " + str(i2))
#print("found stats text image at: " + str(i3))
#do_fight()
#do_inventory()
#do_adventure(0, 0, 1, 1)
#pixel_search2(212429, 0,0,500,1000)
#do_snipe(5, 1, once=True)
#do_pit()
#do_advanced_training()
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