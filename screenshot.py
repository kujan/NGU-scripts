from classes.inputs import Inputs
from classes.window import Window
import coordinates as coords

w = Window()
i = Inputs()

Window.x, Window.y = i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)

i.save_screenshot()