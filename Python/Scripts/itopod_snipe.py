"""24-hour rebirth script"""

# Helper classes
from classes.features import Features
from classes.stats import Tracker
from classes.window import Window

import coordinates as coords

w = Window()
feature = Features()

Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")

print(f"Top left found at: {w.x}, {w.y}")

tracker = Tracker(5)

while True:  # main loop
    feature.itopod_snipe(300)
    feature.pit()
    tracker.progress()
    feature.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
