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

#sets everything to the proper requirements to run the script
i.click(*coords.GAME_SETTINGS)
i.click(*coords.TO_SCIENTIFIC)
i.click(*coords.CHECK_FOR_UPDATE_OFF)
i.click(*coords.FANCY_TITAN_HP_BAR_OFF)
i.click(*coords.DISABLE_HIGHSCORE)
i.click(*coords.SETTINGS_PAGE_2)
i.click(*coords.SIMPLE_INVENTORY_SHORTCUT_ON)
