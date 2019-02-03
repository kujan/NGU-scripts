"""Input class contains alternative functions for mouse and keyboard input on Windows Server."""
from classes.window import Window as window
from ctypes import windll
from PIL import Image as image
from PIL import ImageFilter
import cv2
import ngucon as ncon
import usersettings as userset
import numpy
import pytesseract
import re
import time
import os
import sys
import win32api
import win32con as wcon
import win32gui
import win32ui

class AltInputs():
    
    def a_click(self, x, y):
        x += window.x
        y += window.y
        lParam = win32api.MAKELONG(x, y)
        # MOUSEMOVE event is required for game to register clicks correctly
        win32gui.PostMessage(window.id, wcon.WM_MOUSEMOVE, 0, lParam)
        #Left click then A
        win32gui.PostMessage(window.id, wcon.WM_LBUTTONDOWN,
                                wcon.MK_LBUTTON, lParam)
        win32gui.PostMessage(window.id, wcon.WM_KEYDOWN, 0x41, 0)
        win32gui.PostMessage(window.id, wcon.WM_KEYDOWN, 0x41, 0)
        win32gui.PostMessage(window.id, wcon.WM_LBUTTONUP,
                                wcon.MK_LBUTTON, lParam)
        time.sleep(0.5)

    def d_click(self, x, y):
        x += window.x
        y += window.y
        lParam = win32api.MAKELONG(x, y)
        # MOUSEMOVE event is required for game to register clicks correctly
        win32gui.PostMessage(window.id, wcon.WM_MOUSEMOVE, 0, lParam)
        #Left click then D
        win32gui.PostMessage(window.id, wcon.WM_LBUTTONDOWN,
                                wcon.MK_LBUTTON, lParam)
        win32gui.PostMessage(window.id, wcon.WM_KEYDOWN, 0x44, 0)
        win32gui.PostMessage(window.id, wcon.WM_KEYDOWN, 0x44, 0)
        win32gui.PostMessage(window.id, wcon.WM_LBUTTONUP,
                                wcon.MK_LBUTTON, lParam)
        #TODO: What is this sleep for?
        time.sleep(0.5)