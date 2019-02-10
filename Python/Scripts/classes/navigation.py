"""Navigation class handles navigation through the menus."""
import time
from classes.inputs import Inputs
import coordinates as coords
import usersettings as userset


class Navigation(Inputs):
    """Navigate through menus."""

    menus = coords.MENUITEMS
    equipment = coords.EQUIPMENT_SLOTS
    current_menu = ''

    def menu(self, target):
        """Navigate through main menu."""
        if Navigation.current_menu == target:
            return
        self.click(*Navigation.menus[target])
        time.sleep(userset.LONG_SLEEP)
        Navigation.current_menu = target

    def input_box(self):
        """Click input box."""
        self.click(*coords.NUMBER_INPUT_BOX)
        time.sleep(userset.SHORT_SLEEP)

    def rebirth(self):
        """Click rebirth menu."""
        if Navigation.current_menu == 'rebirth':
            return
        self.click(*coords.REBIRTH)
        time.sleep(userset.SHORT_SLEEP)
        Navigation.current_menu = 'rebirth'

    def confirm(self):
        """Click yes in confirm window."""
        self.click(*coords.CONFIRM)
        time.sleep(userset.SHORT_SLEEP)

    def ngu_magic(self):
        """Navigate to NGU magic."""
        if Navigation.current_menu == 'ngu_magic':
            return
        self.menu('ngu')
        self.click(*coords.NGU_MAGIC)
        time.sleep(userset.SHORT_SLEEP)
        Navigation.current_menu = 'ngu_magic'

    def exp(self):
        """Navigate to EXP Menu."""
        if Navigation.current_menu == 'exp':
            return
        self.click(*coords.XP_MENU)
        time.sleep(userset.SHORT_SLEEP)
        Navigation.current_menu = 'exp'

    def exp_magic(self):
        """Navigate to the magic menu within the EXP menu."""
        if Navigation.current_menu == 'exp_magic':
            return
        self.exp()
        self.click(*coords.MAGIC_MENU)
        time.sleep(userset.SHORT_SLEEP)
        Navigation.current_menu = 'exp_magic'

    def info(self):
        """Click info 'n stuff."""
        if Navigation.current_menu == 'info':
            return
        self.click(*coords.INFO)
        time.sleep(userset.SHORT_SLEEP)
        Navigation.current_menu = 'info'

    def misc(self):
        """Navigate to Misc stats."""
        if Navigation.current_menu == 'misc':
            return
        self.info()
        self.click(*coords.MISC)
        time.sleep(userset.SHORT_SLEEP)
        Navigation.current_menu = 'misc'

    def perks(self):
        """Navigate to Perks screen."""
        if Navigation.current_menu == 'perks':
            return
        self.menu('adventure')
        self.click(*coords.ITOPOD_PERKS)
        time.sleep(userset.SHORT_SLEEP)
        Navigation.current_menu = 'perks'

    def spells(self):
        """Navigate to the spells menu within the magic menu."""
        if Navigation.current_menu == 'spells':
            return
        self.menu('bloodmagic')
        self.click(*coords.BM_SPELL)
        time.sleep(userset.SHORT_SLEEP)
        Navigation.current_menu = 'spells'
