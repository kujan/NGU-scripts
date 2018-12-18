"""Feature class handles the alternative features in the game for Windows Server."""
from classes.inputs import Inputs
from classes.alt_inputs import AltInputs
from classes.navigation import Navigation
from classes.window import Window
from collections import deque, namedtuple
from decimal import Decimal
import math
import ngucon as ncon
import re
import time
import win32con as wcon
import win32gui
import usersettings as userset

class AltFeatures(Navigation, Inputs):
    """Handles the Windows 2018 different features in the game."""

    def alt_merge_equipment(self):
        """Navigate to inventory and merge equipment."""
        self.menu("inventory")
        time.sleep(0.5)
        for slot in self.equipment:
            if (slot == "cube"):
                return
            self.d_click(self.equipment[slot]["x"], self.equipment[slot]["y"])

    def alt_boost_equipment(self):
        """Boost all equipment."""
        self.menu("inventory")
        time.sleep(0.5)
        for slot in self.equipment:
            if (slot == "cube"):
                return
            self.a_click(self.equipment[slot]["x"], self.equipment[slot]["y"])
    def alt_merge_inventory(self, slots):
        """Merge all inventory slots starting from 1 to slots.

        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        self.menu("inventory")
        coords = self.get_inventory_slots(slots)
        for slot in coords:
            self.d_click(slot.x, slot.y)

    def alt_boost_inventory(self, slots):
        """Merge all inventory slots starting from 1 to slots.

        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        self.menu("inventory")
        coords = self.get_inventory_slots(slots)
        for slot in coords:
            self.a_click(slot.x, slot.y)

    def boost_cube(self):
        """Boost cube."""
        self.menu("inventory")
        for slot in self.equipment:
            if (slot == "cube"):
                self.click(self.equipment[slot]["x"],
                            self.equipment[slot]["y"], "right")
                return