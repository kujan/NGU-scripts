"""AP farming script."""

# Helper classes
from classes.features import Features
from classes.window import Window

import coordinates as coords

w = Window()
feature = Features()

Window.x, Window.y = feature.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
feature.menu("inventory")

print(f"Top left found at: {w.x}, {w.y}")

while True:  # main loop
    feature.itopod_ap(600)
    feature.pit()
