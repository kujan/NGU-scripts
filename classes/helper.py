from classes.window import Window
import coordinates as coords

# This should initialize Window class variables
def init(feature, printCoords=False):
    Window.init()
    top_x, top_y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 2000, 1000)
    Window.setPos(top_x, top_y)
    feature.menu("inventory")
    if (printCoords):
        print(f"Top left found at: {Window.x}, {Window.y}")

# This is called by the task scripts once the task has been completed
def loop(feature):
    print("Engaging ITOPOD snipe loop")
    while True:  # main loop
        feature.pit()
        feature.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        feature.questing(subcontract=True)
        feature.ygg()
        feature.itopod_snipe(300)
