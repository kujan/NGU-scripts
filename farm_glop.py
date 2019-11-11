"""Challenge start script."""
import time

# Helper classes
from classes.features import Adventure, MoneyPit
from classes.helper   import Helper
from classes.inputs import Inputs
import coordinates as coords
from classes.navigation import Navigation
from classes.window import Window
import usersettings as userset

Helper.init(True)

class Glop:
    
    inv_pages_unlocked = 0
    reagents = {}

    @staticmethod
    def init():
        Navigation.menu("inventory")
        for btn in coords.INVENTORY_PAGE:
            res = Inputs.check_pixel_color(*btn, coords.COLOR_INVENTORY_BG)
            if not res:
                Glop.inv_pages_unlocked += 1

    @staticmethod
    def update_inventory():
        for item in coords.GLOP_FILENAMES: Glop.reagents[item] = []

        for page in range(Glop.inv_pages_unlocked):
            print(page)
            Inputs.click(*coords.INVENTORY_PAGE[page])
            time.sleep(userset.MEDIUM_SLEEP)
            Glop.scan()
            
        for item in coords.GLOP_FILENAMES:
            print(f"{item}: {len(Glop.reagents[item])}")

    @staticmethod
    def scan():
        start = time.time()
        bmp = Inputs.get_bitmap()
        for item in coords.GLOP_FILENAMES:
            path = Inputs.get_file_path("images", item)
            # Using the whole window instead of cropping out just the inventory yields higher accuracy
            rect = (Window.x, Window.y, Window.x + 960, Window.y + 600)
            res = Inputs.find_all(*rect, path, threshold=0.9, bmp=bmp)
            print(f"glop {Glop.reagents}")
            print()
            print(res)
            if res: Glop.reagents[item].extend(res)
Glop.init()
Glop.update_inventory()

#Inputs.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, path, threshold=0.9, find_all=True)