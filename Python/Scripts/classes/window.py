"""Window class contains the coordinate for the top left of the game window."""
import win32gui


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
