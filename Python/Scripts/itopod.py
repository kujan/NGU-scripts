"""Static itopod script."""

# Helper classes
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window
import coordinates as coords

w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.save_screenshot()
nav.menu("inventory")

def run(window):
    w = Window()
    i = Inputs()
    nav = Navigation()
    feature = Features()
    Window.x = window.x
    Window.y = window.y
    nav.menu("inventory")
    while True:  # main loop
        feature.itopod_snipe(300)
        feature.boost_cube()
        feature.ygg()
