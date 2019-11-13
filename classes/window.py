"""Window class contains the coordinate for the top left of the game window."""
import ctypes
import platform

import win32gui

from deprecated import deprecated
from typing import Dict, Tuple


class Window:
    """This class contains game window coordinates."""

    id = 0
    x = 0
    y = 0
    dc = 0

    @deprecated(reason="Window() -Window instantiation- is deprecated, use Window.init() instead")
    def __init__(self, debug=False):
        Window.init(debug)

    @staticmethod
    def init(debug :bool =False) -> Dict[int, Tuple[int, int, int, int]]:
        """Finds the game window and returns its coords."""
        if platform.release() == "10":
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        else:
            ctypes.windll.user32.SetProcessDPIAware()

        def window_enumeration_handler(hwnd, top_windows):
            """Add window title and ID to array."""
            top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        if debug:
            window_name = "debugg"
        else:
            window_name = "play ngu idle"

        top_windows = []
        windows = []
        candidates = {}
        win32gui.EnumWindows(window_enumeration_handler, top_windows)
        windows = [window[0] for window in top_windows if window_name in window[1].lower()]
        for window in windows:
            candidates[window] = Window.winRect(window)
        return candidates
    @staticmethod
    def setPos(x :int, y :int) -> None:
        """Set top left coordinates."""
        Window.x = x
        Window.y = y
    
    @staticmethod
    def winRect(window_id :int) -> Tuple[int, int, int, int]:
        """Returns the coordinates of the window"""
        return win32gui.GetWindowRect(window_id)
    
    @staticmethod
    def shake() -> None:
        """Shake that Window"""
        for x in range(1000):
            win32gui.MoveWindow(Window.id, x, 0, 1000, 800, False)
        for y in range(1000):
            win32gui.MoveWindow(Window.id, 1000, y, 1000, 800, False)
        for x in reversed(range(1000)):
            win32gui.MoveWindow(Window.id, x, 1000, 1000, 800, False)
        for y in reversed(range(1000)):
            win32gui.MoveWindow(Window.id, 0, y, 1000, 800, False)
    
    @staticmethod
    def gameCoords(x1 :int, y1 :int, x2 :int, y2 :int) -> Tuple[int, int, int, int]:
        """Converts coords relative to the game to coords relative to the window."""
        return Window.x + x1, Window.y + y1, Window.x + x2, Window.y + y2
