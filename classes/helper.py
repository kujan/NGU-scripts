"""Helper functions."""
import win32gui
from classes.window import Window
import coordinates as coords

def init(feature, printCoords=False):
    """Initialize Window class variables."""
    Window.init()
    rect = win32gui.GetWindowRect(Window.id)
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    top_x, top_y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, h, w)
    Window.setPos(top_x, top_y)
    feature.menu("inventory")  # Sometimes the very first click is ignored, this makes sure the first click is unimportant.

    # Set everything to the proper requirements to run the script.
    feature.click(*coords.GAME_SETTINGS)
    feature.click(*coords.TO_SCIENTIFIC)
    feature.click(*coords.CHECK_FOR_UPDATE_OFF)
    feature.click(*coords.FANCY_TITAN_HP_BAR_OFF)
    feature.click(*coords.DISABLE_HIGHSCORE)
    feature.click(*coords.SETTINGS_PAGE_2)
    feature.click(*coords.SIMPLE_INVENTORY_SHORTCUT_ON)

    if printCoords:
        print(f"Top left found at: {Window.x}, {Window.y}")

def loop(feature):
    """Run infinite loop to prevent idling after task is complete."""
    print("Engaging ITOPOD snipe loop")
    while True:  # main loop
        feature.pit()
        feature.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        feature.questing(subcontract=True)
        feature.ygg()
        feature.itopod_snipe(300)

def human_format(num):
    """Convert large numbers into something readable."""
    suffixes = ['', 'K', 'M', 'B', 'T', 'Q', 'Qi', 'Sx', 'Sp']
    num = float('{:.3g}'.format(num))
    if num > 1e24:
        return num
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), suffixes[magnitude])
