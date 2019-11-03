"""Static itopod script."""

# Helper classes
from classes.features import Adventure, Inventory, Yggdrasil
from classes.window import Window
from gui import ScriptThread
from distutils.util import strtobool
from PyQt5.QtCore import QSettings

def run():
    settings = QSettings("Kujan", "NGU-Scripts")
    if not ScriptThread.duration:
        ScriptThread.duration = int(settings.value("line_adv_duration")) * 60
    use_boosts = strtobool(settings.value("check_gear"))
    check_fruits = strtobool(settings.value("check_fruits"))
    boost_equipment = strtobool(settings.value("radio_equipment"))
    boost_cube = strtobool(settings.value("radio_cube"))
    boost_inventory = strtobool(settings.value("check_boost_inventory"))
    boost_slots = settings.value("arr_boost_inventory")
    merge_inventory = strtobool(settings.value("check_merge_inventory"))
    merge_slots = settings.value("arr_merge_inventory")

    Adventure.itopod_snipe(ScriptThread.duration, ScriptThread.signal)
    if use_boosts:
        if boost_equipment:
            Inventory.boost_equipment(ScriptThread.signal)
        else:
            Inventory.boost_cube(ScriptThread.signal)
    if boost_inventory:
        Inventory.boost_inventory(boost_slots, ScriptThread.signal)
    if merge_inventory:
        Inventory.merge_inventory(merge_slots, ScriptThread.signal)
    if check_fruits:
        Yggdrasil.ygg(ScriptThread.signal)
