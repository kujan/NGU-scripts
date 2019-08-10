from classes.features import Features
import constants as const
import coordinates as coords
from functools import reduce
import math
import re
import pprint


class Wishes(Features):
    """Class that handles wishes."""

    def __init__(self, wish_slots):
        """Fetch initial breakdown values."""
        self.wish_slots = wish_slots
        self.wish_speed = 0
        self.epow = 0
        self.ecap = 0

        self.mpow = 0
        self.mcap = 0

        self.rpow = 0
        self.rcap = 0
        self.pp = pprint.PrettyPrinter(indent=4)
        self.wishes_completed = []  # completed wishes
        self.wishes_in_progress = []  # wishes above level 0
        self.wishes_active = []  # wishes that currently are progressing
        self.get_breakdowns()
        self.allocate_wishes()
        #self.get_wish_status()
        #self.allocate_wishes()
        #print(self.wish_speed)

    def get_breakdowns(self):
        """Go to stat breakdowns and fetch the necessary stats."""
        self.stat_breakdown()
        self.click(*coords.BREAKDOWN_E)
        e_list = self.fix_text(self.ocr(*coords.OCR_BREAKDOWN_E))
        self.click(*coords.BREAKDOWN_M)
        m_list = self.fix_text(self.ocr(*coords.OCR_BREAKDOWN_E))
        self.click(*coords.BREAKDOWN_R)
        r_list = self.fix_text(self.ocr(*coords.OCR_BREAKDOWN_E))
        self.click(*coords.BREAKDOWN_MISC)
        misc_list = self.fix_text(self.ocr(*coords.OCR_BREAKDOWN_E))

        fields = ["total energy power:", "total magic power:", "total r power:", "total wish speed:"]

        try:
            for e in e_list:
                if e[0].lower() in fields:
                    self.epow = float(e[1])
        except ValueError:
            print("couldn't fetch energy power")
            self.epow = 0
        try:
            for e in m_list:
                if e[0].lower() in fields:
                    self.mpow = float(e[1])
        except ValueError:
            print("couldn't fetch magic power")
            self.mpow = 0

        try:
            for e in r_list:
                if e[0].lower() in fields:
                    self.rpow = float(e[1])
        except ValueError:
            print("couldn't fetch R3 power")
            self.rpow = 0
        try:
            for e in misc_list:
                if e[0].lower() in fields:
                    self.wish_speed = int(e[1]) / 100
        except ValueError:
            print("Couldn't fetch wish speed, defaulting to 100%")
            self.wish_speed = 1

        self.ecap = self.get_idle_cap(1)
        self.mcap = self.get_idle_cap(2)
        self.rcap = self.get_idle_cap(3)

    def fix_text(self, text):
        """Fix OCR output to something useable."""
        try:
            fields = []
            values = []
            res = []
            for line in text.splitlines():
                if line == "" or line[0].lower() == "x":
                    continue
                if line[0].isdigit():
                    values.append(re.sub(r'[^0-9E+\.]', '', line))
                else:
                    fields.append(line)
            assert(len(fields) == len(values))

            for index, field in enumerate(fields):
                res.append((field, values[index]))
            return res

        except AssertionError:
            print("OCR couldn't determine breakdown values")

    def assign_wishes(self):
        """Will assign any idle resources to wishes in the order as defined in constants.py."""
        self.menu("wishes")
        for y in range(3):
            for x in range(7):
                complete = self.check_pixel_color(coords.WISH_BORDER.x + x * 92,
                                                  coords.WISH_BORDER.y + y * 106,
                                                  coords.COLOR_WISH_COMPLETED)
                if complete:
                    self.completed_wishes.append(1 + x + y + y * 6)
        print(self.completed_wishes)

    def get_wish_status(self):
        """Check which wishes are done and which are level 1 or higher."""
        self.menu("wishes")
        self.click(*coords.WISH_PAGE[1])  # go to page 2 and select the first wish to get rid of the green border
        self.click(*coords.WISH_SELECTION)
        self.click(*coords.WISH_PAGE[0])

        for i, page in enumerate(coords.WISH_PAGE):
            self.click(*page)
            for y in range(3):
                for x in range(7):
                    border_color = self.get_pixel_color(coords.WISH_BORDER.x + x * 92,
                                                        coords.WISH_BORDER.y + y * 106)
                    if border_color == coords.COLOR_WISH_COMPLETED:
                        self.wishes_completed.append(1 + x + y + y * 6 + i * 21)

                    if border_color == coords.COLOR_WISH_STARTED:
                        self.wishes_in_progress.append(1 + x + y + y * 6 + i * 21)

                    active_color = self.get_pixel_color(coords.WISH_SELECTION.x + x * 92,
                                                        coords.WISH_SELECTION.y + y * 106)
                    if active_color == coords.COLOR_WISH_ACTIVE:
                        self.wishes_active.append(1 + x + y + y * 6 + i * 21)
                    if active_color == coords.COLOR_WISH_INACTIVE:
                        self.click(coords.WISH_SELECTION.x + x * 92,
                                   coords.WISH_SELECTION.y + y * 106)
                        self.click(*coords.WISH_CLEAR_WISH)
                        self.wishes_in_progress.append(1 + x + y + y * 6 + i * 21)

            if i == 0:  # after page 1 is scanned, select first wish
                self.click(*coords.WISH_SELECTION)

        used_slots = len(self.wishes_active)
        if used_slots > 0:
            self.wish_slots -= used_slots
            print(f"{used_slots} wish slots are already in use and will be ignored.")


    def allocate_wishes(self):
        """Use the order defined in constants.py to determine which wish to run."""
        available_wishes = const.WISH_ORDER
        costs = {}
        for wish in available_wishes:
            if wish.id in self.wishes_completed:
                available_wishes.remove(wish)
        # TODO: check wish level
        for wish in available_wishes:
            powproduct = (self.epow * self.mpow * self.rpow) ** 0.17
            wish_cap_ticks = 218 * 60 * 50
            capreq = wish.divider * 2 / wish_cap_ticks / self.wish_speed / powproduct

            ratio = [self.ecap / self.rcap, self.mcap / self.rcap, 1]
            capproduct = reduce((lambda x, y: x * y), ratio)
            factor = (capreq / capproduct ** 0.17) ** (1 / .17 / 3)
            vals = []
            for x in ratio:
                vals.append(math.ceil((x * factor)))
            costs[wish.id] = vals
        self.pp.pprint(costs)
