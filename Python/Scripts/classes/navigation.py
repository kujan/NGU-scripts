"""Navigation class handles navigation through the menus."""
from classes.inputs import Inputs
import ngucon as ncon
import time


class Navigation(Inputs):
    """Navigate through menus."""

    menus = ncon.MENUITEMS
    equipment = ncon.EQUIPMENTSLOTS

    def menu(self, target):
        """Navigate through main menu."""
        y = ncon.MENUOFFSETY + ((self.menus.index(target) + 1) *
                                ncon.MENUDISTANCEY)
        self.click(ncon.MENUOFFSETX, y)
        time.sleep(ncon.LONG_SLEEP)

    def input_box(self):
        """Click input box."""
        self.click(ncon.NUMBERINPUTBOXX, ncon.NUMBERINPUTBOXY)
        time.sleep(ncon.SHORT_SLEEP)

    def rebirth(self):
        """Click rebirth menu."""
        self.click(ncon.REBIRTHX, ncon.REBIRTHY)
        time.sleep(ncon.SHORT_SLEEP)

    def confirm(self):
        """Click yes in confirm window."""
        self.click(ncon.CONFIRMX, ncon.CONFIRMY)
        time.sleep(ncon.SHORT_SLEEP)

    def ngu_magic(self):
        """Navigate to NGU magic."""
        self.menu("ngu")
        self.click(ncon.NGUMAGICX, ncon.NGUMAGICY)
        time.sleep(ncon.SHORT_SLEEP)

    def exp(self):
        """Navigate to EXP Menu."""
        self.click(ncon.EXPX, ncon.EXPY)
        time.sleep(ncon.SHORT_SLEEP)

    def exp_magic(self):
        """Navigate to the magic menu within the EXP menu."""
        self.exp()
        self.click(ncon.MMENUX, ncon.MMENUY)
        time.sleep(ncon.SHORT_SLEEP)

    def info(self):
        """Click info 'n stuff."""
        self.click(ncon.INFOX, ncon.INFOY)
        time.sleep(ncon.SHORT_SLEEP)

    def misc(self):
        """Navigate to Misc stats."""
        self.info()
        self.click(ncon.MISCX, ncon.MISCY)
        time.sleep(ncon.SHORT_SLEEP)
