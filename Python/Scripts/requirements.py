# Helper classes
from classes.inputs import Inputs

import coordinates as coords
from time import sleep

i = Inputs()

#sets everything to the proper requirements to run the script

i.click(*coords.GAME_SETTINGS)
i.click(*coords.TO_SCIENTIFIC)
i.click(*coords.CHECK_FOR_UPDATE_OFF)
i.click(*coords.FANCY_TITAN_HP_BAR_OFF)
i.click(*coords.DISABLE_HIGHSCORE)
i.click(*coords.SETTINGS_PAGE_2)
i.click(*coords.SIMPLE_INVENTORY_SHORTCUT_ON)
