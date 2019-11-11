"""Challenge start script."""
import time

# Helper classes
from classes.features import Adventure
from classes.helper   import Helper
from classes.inputs import Inputs
import coordinates as coords
from classes.navigation import Navigation
from classes.window import Window
import usersettings as userset
from typing import NamedTuple

Helper.init(True)

class Reagent(NamedTuple):
    x: int
    y: int
    name: str
    page: int

class Glop:
    
    inv_pages_unlocked = 0
    reagents = {}
    target = 10

    GLOP_ZONE_MAP = {"ice_cream.png": 8,
                     "steak.png": 16,
                     "surstromming.png": 21,
                     "marmite.png": 23,
                     "pineapple.png": 30
                     }

    @staticmethod
    def init(target):
        Glop.target = target
        Navigation.menu("inventory")
        for btn in coords.INVENTORY_PAGE:
            res = Inputs.check_pixel_color(*btn, coords.COLOR_INVENTORY_BG)
            if not res:
                Glop.inv_pages_unlocked += 1
        Glop.update_inventory()

    @staticmethod
    def update_inventory():
        Navigation.menu("inventory")
        for item in coords.GLOP_FILENAMES: Glop.reagents[item] = []

        for page in range(Glop.inv_pages_unlocked):
            Inputs.click(*coords.INVENTORY_PAGE[page])
            time.sleep(userset.MEDIUM_SLEEP)
            bmp = Inputs.get_bitmap()
            
            for item in coords.GLOP_FILENAMES:
                path = Inputs.get_file_path("images", item)
                # Using the whole window instead of cropping out just the inventory yields higher accuracy
                rect = (Window.x, Window.y, Window.x + 960, Window.y + 600)
                res = Inputs.find_all(*rect, path, threshold=0.9, bmp=bmp)
                reagents = list(map(lambda x: Reagent(x[0], x[1], item, page), res))
                if reagents: Glop.reagents[item].extend(reagents)
            
        for item in coords.GLOP_FILENAMES:
            print(f"{item}: {len(Glop.reagents[item])}")

    @staticmethod
    def loop():
        while len(Glop.reagents["glop.png"]) < Glop.target:
            Navigation.menu("inventory")
            # Find the glop reagent we have the fewest of
            target = min(Glop.reagents, key=lambda x: len(Glop.reagents[x]))
            print("Converting glop")
            for reagent in Glop.reagents[target]:
                Inputs.click(*coords.INVENTORY_PAGE[reagent.page])
                Inputs.click(reagent.x, reagent.y, button="right")
                Inputs.ctrl_click(reagent.x, reagent.y)
            print(f"converted {len(Glop.reagents[target])} glops")
            Adventure.snipe(Glop.GLOP_ZONE_MAP[target], 2)
            Glop.update_inventory()
Glop.init(50)
Glop.loop()

#Inputs.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, path, threshold=0.9, find_all=True)