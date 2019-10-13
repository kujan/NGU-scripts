"""Helper functions."""
from classes.window import Window
import coordinates as coords

def init(feature, printCoords=False):
    """Initialize Window class variables."""
    Window.init()
    top_x, top_y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 2000, 1000)
    Window.setPos(top_x, top_y)
    feature.menu("inventory")
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
