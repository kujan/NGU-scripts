
import coordinates as coords
from classes.features import Features
from classes.window import Window
from ctypes import windll
import cv2
import datetime
import numpy
import pyautogui
import pytesseract
import re
import time
import os
import sys
import win32api	
import win32con as wcon
import win32gui
import win32ui

w = Window()
feature = Features()
Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
x = coords.BREAKDOWN_MISC_SCROLL_DRAG_START.x
y = coords.BREAKDOWN_MISC_SCROLL_DRAG_START.y
x2 = coords.BREAKDOWN_MISC_SCROLL_DRAG_END.x
y2 = coords.BREAKDOWN_MISC_SCROLL_DRAG_END.y
x += Window.x
y += Window.y
x2 += Window.x
y2 += Window.y


pyautogui.mouseDown(x, y)
time.sleep(1)
pyautogui.dragTo(x2, y2, duration=1)
pyautogui.mouseUp(x2, y2)