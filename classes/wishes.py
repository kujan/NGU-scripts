"""Class that handles wish allocation."""
from decimal import Decimal
from functools import reduce
import math
import re
import time

from classes.features   import Misc
from classes.inputs     import Inputs
from classes.navigation import Navigation

import coordinates  as coords
import constants    as const
import usersettings as userset


class Wishes:
    """Class that handles wishes."""

    def __init__(self, wish_slots, wish_min_time):
        """Fetch initial breakdown values."""
        print(const.WISH_DISCLAIMER)

        self.wish_slots = wish_slots
        self.available_slots = 0
        self.wish_min_time = wish_min_time
        self.wish_speed = 0
        self.epow = 0
        self.ecap = 0
        self.mpow = 0
        self.mcap = 0
        self.rpow = 0
        self.rcap = 0
        self.wishes_completed = []  # completed wishes
        self.wishes_in_progress = []  # wishes above level 0
        self.wishes_active = []  # wishes that currently are progressing
        self.get_breakdowns()
        self.get_wish_status()
        # self.allocate_wishes()

    def get_breakdowns(self):
        """Go to stat breakdowns and fetch the necessary stats."""
        Navigation.stat_breakdown()
        Inputs.click(*coords.BREAKDOWN_E)
        time.sleep(userset.MEDIUM_SLEEP)
        print("OCR is scanning a large area, this might take a few seconds")
        e_list = self.fix_text(Inputs.ocr(*coords.OCR_BREAKDOWN))
        Inputs.click(*coords.BREAKDOWN_M)
        time.sleep(userset.MEDIUM_SLEEP)
        m_list = self.fix_text(Inputs.ocr(*coords.OCR_BREAKDOWN))
        Inputs.click(*coords.BREAKDOWN_R)
        time.sleep(userset.MEDIUM_SLEEP)
        r_list = self.fix_text(Inputs.ocr(*coords.OCR_BREAKDOWN))
        Inputs.click(*coords.BREAKDOWN_MISC)
        time.sleep(userset.MEDIUM_SLEEP)
        Inputs.click_drag(*coords.BREAKDOWN_MISC_SCROLL_DRAG_START, *coords.BREAKDOWN_MISC_SCROLL_DRAG_END)
        misc_list = self.fix_text(Inputs.ocr(*coords.OCR_BREAKDOWN))

        fields = ["total energy power:", "total magic power:", "total r power:", "total wish speed:"]

        try:
            for e in e_list:
                if e[0].lower() in fields:
                    self.epow = float(e[1])
        except ValueError:
            print("couldn't fetch energy power")
            self.epow = 1
        try:
            for e in m_list:
                if e[0].lower() in fields:
                    self.mpow = float(e[1])
        except ValueError:
            print("couldn't fetch magic power")
            self.mpow = 1

        try:
            for e in r_list:
                if e[0].lower() in fields:
                    self.rpow = float(e[1])
        except ValueError:
            print("couldn't fetch R3 power")
            self.rpow = 1
        try:
            for e in misc_list:
                if e[0].lower() in fields:
                    self.wish_speed = int(e[1]) / 100

        except ValueError:
            print("Couldn't fetch wish speed, defaulting to 100%")
            self.wish_speed = 1

        if not self.wish_speed:
            print("Couldn't get wish speed")
            self.wish_speed = 1
        if not self.epow:
            print("Couldn't get epow")
            self.epow = 1
        if not self.mpow:
            print("Couldn't get mpow")
            self.mpow = 1
        if not self.rpow:
            print("Couldn't get rpow")
            self.rpow = 1

        self.get_caps()

    def get_caps(self):
        """Get all available idle resources."""
        self.ecap = Misc.get_idle_cap(1)
        self.mcap = Misc.get_idle_cap(2)
        self.rcap = Misc.get_idle_cap(3)

    def fix_text(self, text):
        """Fix OCR output to something useable."""
        try:
            fields = []
            values = []
            res = []
            method = 0
            for line in text.splitlines():
                match = re.search(r"[a-zA-Z\s]+:\s*[xX]\s*\d+\%?", line)
                if match is not None:
                    method = 1
                    break
            if method == 1:
                for line in text.splitlines():
                    if line == "":
                        continue
                    else:
                        match = re.match(r"(^[a-zA-Z\s]+:?)", line)
                        if match is not None:
                            fields.append(match.group(1))
                            values.append(Inputs.remove_letters(line))
            else:
                for line in text.splitlines():

                    if line == "" or line[0].lower() == "x":
                        continue
                    if line[0].isdigit():
                        values.append(re.sub(r'[^0-9E+\.]', '', line))
                    else:
                        fields.append(line)
            assert len(fields) == len(values)

            for index, field in enumerate(fields):
                res.append((field, values[index]))
            return res

        except AssertionError:
            print("OCR couldn't determine breakdown values")
            return []

    def get_wish_status(self):
        """Check which wishes are done and which are level 1 or higher."""
        Navigation.menu("wishes")
        self.wishes_completed = []  # completed wishes
        self.wishes_in_progress = []  # wishes above level 0
        self.wishes_active = []  # wishes that currently are progressing
        Inputs.click(*coords.WISH_PAGE[1])  # go to page 2 and select the first wish to get rid of the green border
        time.sleep(userset.MEDIUM_SLEEP)
        Inputs.click(*coords.WISH_PORTRAIT)
        time.sleep(userset.MEDIUM_SLEEP)
        Inputs.click(*coords.WISH_PAGE[0])

        for i, page in enumerate(coords.WISH_PAGE):
            Inputs.click(*page)
            for y in range(3):
                for x in range(7):
                    border_color = Inputs.get_pixel_color(coords.WISH_BORDER.x + x * 92,
                                                          coords.WISH_BORDER.y + y * 106)
                    if border_color == coords.COLOR_WISH_COMPLETED:
                        self.wishes_completed.append(1 + x + y + y * 6 + i * 21)

                    if border_color == coords.COLOR_WISH_STARTED:
                        self.wishes_in_progress.append(1 + x + y + y * 6 + i * 21)

                    active_color = Inputs.get_pixel_color(coords.WISH_SELECTION.x + x * 92,
                                                          coords.WISH_SELECTION.y + y * 106)
                    if active_color == coords.COLOR_WISH_ACTIVE:
                        self.wishes_active.append(1 + x + y + y * 6 + i * 21)
                    if active_color == coords.COLOR_WISH_INACTIVE:
                        Inputs.click(coords.WISH_SELECTION.x + x * 92,
                                     coords.WISH_SELECTION.y + y * 106)
                        Inputs.click(*coords.WISH_CLEAR_WISH)
                        self.wishes_in_progress.append(1 + x + y + y * 6 + i * 21)

            if i == 0:  # after page 1 is scanned, select first wish
                Inputs.click(*coords.WISH_PORTRAIT)
        used_slots = len(self.wishes_active)
        self.available_slots = self.wish_slots - used_slots
        if used_slots > 0:
            print(f"{used_slots} wish slots are already in use and will be ignored.")

    def allocate_wishes(self):
        """Use the order defined in constants.py to determine which wish to run."""
        available_wishes = const.WISH_ORDER.copy()
        costs = {}
        tmp = []

        # Find and remove wishes that are completed or are currently active.
        for wish in available_wishes:
            if wish.id in self.wishes_completed or wish.id in self.wishes_active:
                tmp.append(wish)
        for t in tmp:
            available_wishes.remove(t)

        # Calculate the required EMR to run the wishes at full speed at the last level.
        for wish in available_wishes:
            powproduct = (self.epow * self.mpow * self.rpow) ** 0.17
            wish_cap_ticks = self.wish_min_time * 60 * 50
            # TODO: fetch current wish level instead of using max(?).
            capreq = wish.divider * wish.levels / wish_cap_ticks / self.wish_speed / powproduct

            ratio = [self.ecap / self.rcap, self.mcap / self.rcap, 1]
            capproduct = reduce((lambda x, y: x * y), ratio, 1)
            factor = (capreq / capproduct ** 0.17) ** (1 / .17 / 3)
            vals = []
            for x in ratio:
                vals.append(math.ceil((x * factor)))
            costs[wish.id] = vals

        best = {}
        best_cost = math.inf
        # Iterate through all available wishes to find the combination with highest priority and lowest cost to cap.
        while len(available_wishes) > self.available_slots:
            candidates = {}
            for _ in range(self.available_slots):
                for wish in available_wishes:
                    if wish.id not in candidates:
                        candidates[wish.id] = costs[wish.id]
                        break
            rcap_cost = 0
            for wish in candidates:
                rcap_cost += candidates[wish][2]
            if rcap_cost < self.rcap:
                best = candidates
                break
            else:
                if rcap_cost < best_cost:
                    best = candidates
                    best_cost = rcap_cost

                for wish in available_wishes:
                    if wish.id == max(candidates.items(), key=lambda x: x[1][2])[0]:
                        available_wishes.remove(wish)

        rcap = self.rcap
        r = 0
        for wish in best:
            r += best[wish][2]
        if r > rcap:
            r_min = min(best.items(), key=lambda x: x[1][2])[1][2]
            r_max = max(best.items(), key=lambda x: x[1][2])[1][2]
            if r_max / r_min <= 100000:
                cap_div = r / rcap
                rcap_cost = 0
                tmp = {}
                for wish in best:
                    tmp[wish] = [math.ceil(best[wish][0] / cap_div), math.ceil(best[wish][1] / cap_div),
                                 math.ceil(best[wish][2] / cap_div)]
                best = tmp
            else:
                print("wish dividers too far apart, splitting resources evenly")
                tmp = {}
                for wish in best:
                    tmp[wish] = [math.ceil(self.ecap / self.wish_slots), math.ceil(self.mcap / self.wish_slots),
                                 math.ceil(self.rcap / self.wish_slots)]
                best = tmp

        for k in best:
            for w in const.WISH_ORDER:
                if w.id == k:
                    e = '%.2E' % Decimal(best[k][0])
                    m = '%.2E' % Decimal(best[k][1])
                    r = '%.2E' % Decimal(best[k][2])
                    print(f"Allocating {e} E | {m} M | {r} R to {w.name}")
                    self.add_emr(w, best[k])

    def add_emr(self, wish, emr):
        """Add EMR to wish."""
        alloc_coords = [coords.WISH_E_ADD, coords.WISH_M_ADD, coords.WISH_R_ADD]
        Navigation.menu("wishes")
        page = ((wish.id - 1) // 21)
        Inputs.click(*coords.WISH_PAGE[page])
        x = coords.WISH_SELECTION.x + ((wish.id - 1) % 21 % 7) * coords.WISH_SELECTION_OFFSET.x
        y = coords.WISH_SELECTION.y + ((wish.id - 1) % 21 // 7) * coords.WISH_SELECTION_OFFSET.y
        # have to add to add some offset here, otherwise the clicks don't register for some reason.
        Inputs.click(x + 20, y + 20)
        for i, e in enumerate(emr):
            Navigation.input_box()
            Inputs.send_string(e)
            Inputs.click(*alloc_coords[i])
