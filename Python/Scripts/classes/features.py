"""Feature class handles the different features in the game."""
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.window import Window
from collections import deque, namedtuple
from decimal import Decimal
from deprecated import deprecated
import coordinates as coords
import math
import re
import time
import win32con as wcon
import win32gui
import usersettings as userset
# TODO: replace ngucon with coordinates

class Features(Navigation, Inputs):
    """Handles the different features in the game."""

    def merge_equipment(self):
        """Navigate to inventory and merge equipment."""
        self.menu("inventory")
        for slot in coords.EQUIPMENT_SLOTS:
            if (slot == "cube"):
                return
            self.click(*coords.EQUIPMENT_SLOTS[slot])
            self.send_string("d")

    def boost_equipment(self):
        """Boost all equipment."""
        self.menu("inventory")
        for slot in coords.EQUIPMENT_SLOTS:
            if (slot == "cube"):
                self.click(*coords.EQUIPMENT_SLOTS[slot], "right")
                return
            self.click(*coords.EQUIPMENT_SLOTS[slot])
            self.send_string("a")

    def get_current_boss(self):
        """Go to fight and read current boss number."""
        self.menu("fight")
        boss = self.ocr(*coords.OCR_BOSS, debug=False)
        return self.remove_letters(boss)

    def nuke(self, boss=None):
        """Navigate to Fight Boss and Nuke or Fast Fight."""
        self.menu("fight")
        if boss:
            for i in range(boss):
                self.click(*coords.FIGHT, fast=True)
            time.sleep(userset.SHORT_SLEEP)
            try:
                current_boss = int(self.get_current_boss())
            except ValueError:
                current_boss = 1
            x = 0
            while current_boss < boss:
                bossdiff = boss - current_boss
                for i in range(0, bossdiff):
                    self.click(*coords.FIGHT, fast=True)
                time.sleep(userset.SHORT_SLEEP)
                try:
                    current_boss = int(self.get_current_boss())
                except ValueError:
                    current_boss = 1
                x += 1
                if x > 7:  # Safeguard if number is too low to reach target boss, otherwise we get stuck here
                    print("Couldn't reach the target boss, something probably went wrong the last rebirth.")
                    break
        else:
            self.click(*coords.NUKE)

    def fight(self):
        """Navigate to Fight Boss and click fight."""
        self.menu("fight")
        self.click(*coords.FIGHT)

    def ygg(self, rebirth=False):
        """Navigate to inventory and handle fruits.

        Keyword arguments:
        rebirth -- Set to true if you're rebirthing, it will force eat all
                   fruit.
        """
        self.menu("yggdrasil")
        if rebirth:
            for key in coords.FRUITS:
                self.click(*coords.FRUITS[key])
        else:
            self.click(*coords.HARVEST)

    def spin(self):
        """Spin the wheel."""
        self.menu("pit")
        self.click(*coords.SPIN_MENU)
        self.click(*coords.SPIN)

    def adventure(self, zone=0, highest=True, itopod=None, itopodauto=False):
        """Go to adventure zone to idle.

        Keyword arguments
        zone -- Zone to idle in, 0 is safe zone, 1 is tutorial and so on.
        highest -- If true, will go to your highest available non-titan zone.
        itopod -- If set to true, it will override other settings and will
                  instead enter the specified ITOPOD floor.
        itopodauto -- If set to true it will click the "optimal" floor button.
        """
        self.menu("adventure")
        if itopod:
            self.click(*coords.ITOPOD)
            if itopodauto:
                self.click(*coords.ITOPOD_END)
                # set end to 0 in case it's higher than start
                self.send_string("0")
                self.click(*coords.ITOPOD_AUTO)
                self.click(*coords.ITOPOD_ENTER)
                return
            self.click(*coords.ITOPOD_START)
            self.send_string(str(itopod))
            self.click(*coords.ITOPOD_END)
            self.send_string(str(itopod))
            self.click(*coords.ITOPOD_ENTER)
            return
        if highest:
            self.click(*coords.RIGHT_ARROW, button="right")
            return
        else:
            self.click(*coords.LEFT_ARROW, button="right")
            for i in range(zone):
                self.click(*coords.RIGHT_ARROW)
            return

    def snipe(self, zone, duration, once=False, highest=False, bosses=True):
        """Go to adventure and snipe bosses in specified zone.

        Keyword arguments
        zone -- Zone to snipe, 0 is safe zone, 1 is turorial and so on.
                If 0, it will use the current zone (to maintain guffin counter)
        duration -- The duration in seconds the sniping will run before
                    returning.
        once -- If true it will only kill one boss before returning.
        highest -- If set to true, it will go to your highest available
                   non-titan zone.
        bosses -- If set to true, it will only kill bosses
        """
        self.menu("adventure")
        if highest:
            self.click(*coords.LEFT_ARROW, button="right")
        elif zone > 0:
            self.click(*coords.LEFT_ARROW, button="right")
            for i in range(zone):
                self.click(*coords.RIGHT_ARROW)

        self.click(625, 500)  # click somewhere to move tooltip

        if self.check_pixel_color(coords.IS_IDLE):
            self.click(*coords.ABILITY_IDLE_MODE)

        end = time.time() + duration
        while time.time() < end:
            self.click(625, 500)  # click somewhere to move tooltip
            if self.check_pixel_color(*coords.IS_ENEMY_ALIVE):
                if bosses:
                    if self.check_pixel_color(*coords.IS_BOSS_CROWN):
                        enemy_alive = True
                        while enemy_alive:
                            enemy_alive = self.check_pixel_color(*coords.IS_ENEMY_ALIVE)
                            self.click(*coords.ABILITY_REGULAR_ATTACK)
                            time.sleep(0.1)
                        if once:
                            break
                    else:
                        # Send left arrow and right arrow to refresh monster.
                        win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN,
                                             wcon.VK_LEFT, 0)
                        time.sleep(0.03)
                        win32gui.PostMessage(Window.id, wcon.WM_KEYUP,
                                             wcon.VK_LEFT, 0)
                        time.sleep(0.03)
                        win32gui.PostMessage(Window.id, wcon.WM_KEYDOWN,
                                             wcon.VK_RIGHT, 0)
                        time.sleep(0.03)
                        win32gui.PostMessage(Window.id, wcon.WM_KEYUP,
                                             wcon.VK_RIGHT, 0)
                else:
                    self.click(*coords.ABILITY_REGULAR_ATTACK)
            time.sleep(0.01)

        self.click(*coords.ABILITY_IDLE_MODE)

    def itopod_snipe(self, duration):
        """Manually snipes ITOPOD for increased speed PP/h.

        Keyword arguments:
        duration -- Duration in seconds to snipe, before toggling idle mode
                    back on and returning.
        """
        end = time.time() + duration

        self.menu("adventure")
        self.click(625, 500)  # click somewhere to move tooltip

        # check if we're already in ITOPOD, otherwise enter
        if not self.check_pixel_color(*coords.IS_ITOPOD_ACTIVE):
            self.click(*coords.ITOPOD)
            self.click(*coords.ITOPOD_END)
            # set end to 0 in case it's higher than start
            self.send_string("0")
            self.click(*coords.ITOPOD_AUTO)
            self.click(*coords.ITOPOD_ENTER)

        if self.check_pixel_color(*coords.IS_IDLE):
            self.click(*coords.ABILITY_IDLE_MODE)

        while time.time() < end:
            enemy_alive = self.check_pixel_color(*coords.IS_ENEMY_ALIVE)
            if enemy_alive:
                self.click(*coords.ABILITY_REGULAR_ATTACK)
            else:
                time.sleep(0.01)

        self.click(*coords.ABILITY_IDLE_MODE)



    def do_rebirth(self):
        """Start a rebirth or challenge."""
        self.rebirth()

        self.click(*coords.REBIRTH)
        self.click(*coords.REBIRTH_BUTTON)
        self.click(*coords.CONFIRM)
        return

    def pit(self, loadout=0):
        """Throws money into the pit.

        Keyword arguments:
        loadout -- The loadout you wish to equip before throwing gold
                   into the pit, for gear you wish to shock. Make
                   sure that you don't get cap-blocked by either using
                   the unassign setting in the game or swapping gear that
                   doesn't have e/m cap.
        """
        if self.check_pixel_color(*coords.IS_PIT_READY):
            if loadout:
                self.loadout(loadout)
            self.menu("pit")
            self.click(*coords.PIT)
            self.click(*coords.CONFIRM)

    def augments(self, augments, energy):
        """Dump energy into augmentations.

        Keyword arguments
        augments -- Dictionary that contains which augments you wish to use and
                    a ratio that tells how much of the total energy you
                    allocated you wish to send. Example:
                    {"SS": 0, "DS": 0, "MI": 0, "DTMT": 0, "CI": 0, "M": 0,
                     "SM": 0, "AA": 0, "EB": 0, "CS": 0, "AE": 0, "ES": 0,
                     "LS": 0.9, "QSL": 0.1}
        Energy -- The total amount of energy you want to use for all augments.
        """
        self.menu("augmentations")
        for k in augments:
            val = math.floor(augments[k] * energy)
            self.input_box()
            self.send_string(str(val))
            # Scroll down if we have to.
            bottom_augments = ["AE", "ES", "LS", "QSL"]
            i = 0
            if (k in bottom_augments):
                color = self.get_pixel_color(*coords.AUG_SCROLL_SANITY_BOT)
                while color not in coords.SANITY_AUG_SCROLL_COLORS:
                    self.click(*coords.AUG_SCROLL_BOT)
                    time.sleep(userset.MEDIUM_SLEEP)
                    color = self.get_pixel_color(*coords.AUG_SCROLL_SANITY_BOT)
                    i += 1
                    if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
                        Navigation.current_menu = ""
                        self.menu("augmentations")
                    elif i > 10:
                        print("Couldn't assign augments")
                        break

            else:
                color = self.get_pixel_color(*coords.AUG_SCROLL_SANITY_TOP)
                while color not in coords.SANITY_AUG_SCROLL_COLORS:
                    self.click(*coords.AUG_SCROLL_TOP)
                    time.sleep(userset.MEDIUM_SLEEP)
                    color = self.get_pixel_color(*coords.AUG_SCROLL_SANITY_TOP)
                    i += 1
                    if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
                        Navigation.current_menu = ""
                        self.menu("augmentations")
                    elif i > 10:
                        print("Couldn't assign augments")
                        break
            self.click(*coords.AUGMENT[k])

    def time_machine(self, e, m=0, magic=False):
        """Add energy and/or magic to TM.

        Example: self.time_machine(1000, 2000)
                 self.time_machine(1000, magic=True)
                 self.time_machine(1000)

        First example will add 1000 energy and 2000 magic to TM.
        Second example will add 1000 energy and 1000 magic to TM.
        Third example will add 1000 energy to TM.

        Keyword arguments:
        e -- The amount of energy to put into TM.
        m -- The amount of magic to put into TM, if this is 0, it will use the
             energy value to save unnecessary clicks to the input box.
        magic -- Set to true if you wish to add magic as well"""
        self.menu("timemachine")
        self.input_box()
        self.send_string(e)
        self.click(*coords.TM_SPEED)
        if magic or m:
            if m:
                self.input_box()
                self.send_string(m)
            self.click(*coords.TM_MULT)

    def blood_magic(self, target):
        """Assign magic to BM."""
        self.menu("bloodmagic")
        for i in range(target):
            self.click(*coords.BM[i])

    def wandoos(self, magic=False):
        """Assign energy and/or magic to wandoos."""
        self.menu("wandoos")
        self.click(*coords.WANDOOS_ENERGY)
        if magic:
            self.click(*coords.WANDOOS_MAGIC)

    def loadout(self, target):
        """Equip targeted loadout."""
        self.menu("inventory")
        self.click(*coords.LOADOUT[target])

    @deprecated(version='0.1', reason="speedrun_bloodpill is deprecated, use iron_pill() instead")
    def speedrun_bloodpill(self):
        self.iron_pill()

    def iron_pill(self):
        """Check if bloodpill is ready to cast."""
        if self.check_pixel_color(*coords.IS_IRON_PILL_READY):
            start = time.time()
            self.blood_magic(8)
            self.spells()
            self.click(*coords.BM_AUTO_GOLD)
            self.click(*coords.BM_AUTO_NUMBER)

            if userset.PILL == 0:  # Default to 5 mins if not set
                duration = 300
            else:
                duration = userset.PILL

            while time.time() < start + duration:
                self.gold_diggers([11])
                time.sleep(5)
            self.spells()
            self.click(*coords.BM_PILL)
            time.sleep(userset.LONG_SLEEP)
            self.click(*coords.BM_AUTO_GOLD)
            self.click(*coords.BM_AUTO_NUMBER)
            self.nuke()
            time.sleep(userset.LONG_SLEEP)

    def assign_ngu(self, value, targets, magic=False):
        """Assign energy/magic to NGU's.

        Keyword arguments:
        value -- the amount of energy/magic that will get split over all NGUs.
        targets -- Array of NGU's to use (1-9).
        magic -- Set to true if these are magic NGUs
        """
        if len(targets) > 9:
            raise RuntimeError("Passing too many NGU's to assign_ngu," +
                               " allowed: 9, sent: " + str(len(targets)))
        if magic:
            self.ngu_magic()
        else:
            self.menu("ngu")

        self.input_box()
        self.send_string(value // len(targets))
        for i in targets:
            NGU = coords.Pixel(coords.NGU_PLUS.x, coords.NGU_PLUS.y + i * 35)
            self.click(*NGU)

    def gold_diggers(self, targets, deactivate=False):
        """Activate diggers.

        Keyword arguments:
        targets -- Array of diggers to use from 1-12. Example: [1, 2, 3, 4, 9].
        deactivate -- Set to True if you wish to deactivate these
                    diggers otherwise it will just try to up the cap.
        """
        self.menu("digger")
        for i in targets:
            page = ((i-1)//4)
            item = i - (page * 4)
            self.click(*coords.DIG_PAGE[page])
            if deactivate:
                self.click(*coords.DIG_ACTIVE[item])
            else:
                self.click(*coords.DIG_CAP[item])

    def deactivate_all_diggers(self):
        self.menu("digger")
        self.click(*coords.DIG_DEACTIVATE_ALL)    

    def bb_ngu(self, value, targets, overcap=1, magic=False):
        """Estimates the BB value of each supplied NGU.

        It will send value into the target NGU's, which will fill the progress bar. It's very
        important that you put enough e/m into the NGU's to trigger the "anti-flicker" (>10% of BB cost),
        otherwise it will not function properly. 

        Keyword arguments:
        value -- The amount of energy used to determine the cost of BBing the target NGU's
        targets -- Array of NGU's to BB. Example: [1, 3, 4, 5, 6]
        overcap -- Use this if you wish to assign more e/m than absolute minimum to BB
                   the NGU's. This might be useful for longer runs to make sure the cost
                   to BB doesn't exceed the assigned e/m. A value of 1.1 assigns 10% extra.
        magic -- Set to true if these are magic NGUs
        """
        if magic:
            self.ngu_magic()
        else:
            self.menu("ngu")

        self.input_box()
        self.send_string(str(int(value)))

        for target in targets:
            NGU = coords.Pixel(coords.NGU_PLUS.x, coords.NGU_PLUS.y + target * 35)
            self.click(*NGU)

        for target in targets:
            energy = 0
            for x in range(198):
                color = self.get_pixel_color(coords.NGU_BAR_MIN.x + x,
                                             coords.NGU_BAR_MIN.y +
                                             coords.NGU_BAR_OFFSET_Y * target,
                                            )
                if color == coords.NGU_BAR_WHITE:
                    pixel_coefficient = x / 198
                    value_coefficient = overcap / pixel_coefficient
                    energy = (value_coefficient * value) - value
                    break
            if energy == 0:
                print(f"Warning: You might be overcapping NGU #{target}")
                
            self.input_box()
            self.send_string(str(int(energy)))
            self.click(coords.NGU_PLUS.x, coords.NGU_PLUS.y + target * 35)

    # TODO: make this actually useful for anything
    def advanced_training(self, value):
        self.menu("advtraining")
        value = value // 2
        self.input_box()
        self.send_string(value)
        self.click(*coords.ADV_TRAINING_POWER)
        self.click(*coords.ADV_TRAINING_TOUGHNESS)

    def titan_pt_check(self, target):
        """Check if we have the recommended p/t to defeat the target Titan.

        Keyword arguments:
        target -- The name of the titan you wish to kill. ["GRB", "GCT",
                  "jake", "UUG", "walderp", "BEAST1", "BEAST2", "BEAST3",
                  "BEAST4"]
        """
        self.menu("adventure")
        bmp = self.get_bitmap()
        power = self.ocr(*coords.OCR_ADV_POW, bmp=bmp)
        tough = self.ocr(*coords.OCR_ADV_TOUGH, bmp=bmp)

        if (float(power) > coords.TITAN_PT[target]["p"] and
           float(tough) > coords.TITAN_PT[target]["t"]):
            return True

        else:
            print(f"Lacking: {Decimal(coords.TITAN_PT[target]['p'] - float(power)):.2E}"
                  f"/{Decimal(coords.TITAN_PT[target]['t'] - float(tough)):.2E} P/T"
                  f" to kill {target}")
            return False

    def kill_titan(self, target):
        """Attempt to kill the target titan.

        Keyword arguments:
        target -- The name of the titan you wish to kill. ["GRB", "GCT",
                  "jake", "UUG", "walderp", "BEAST1", "BEAST2", "BEAST3",
                  "BEAST4"]
        """
        self.menu("adventure")
        if self.check_pixel_color(*coords.IS_IDLE):
            self.click(*coords.ABILITY_IDLE_MODE)

        self.click(*coords.LEFT_ARROW, button="right")
        for i in range(coords.TITAN_ZONE[target]):
            self.click(*coords.RIGHT_ARROW)

        time.sleep(userset.LONG_SLEEP)

        available = self.ocr(*coords.OCR_ADV_TITAN)

        if "titan" in available.lower():
            time.sleep(1.5)  # Make sure titans spawn, otherwise loop breaks
            queue = deque(self.get_ability_queue())
            while self.check_pixel_color(*coords.IS_ENEMY_ALIVE):
                if len(queue) == 0:
                    print("NEW QUEUE")
                    queue = deque(self.get_ability_queue())
                    print(queue)

                ability = queue.popleft()
                print(f"using ability {ability}")
                if ability <= 4:
                    x = coords.ABILITY_ROW1X + ability * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW1Y

                if ability >= 5 and ability <= 10:
                    x = coords.ABILITY_ROW2X + (ability - 5) * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW2Y

                if ability > 10:
                    x = coords.ABILITY_ROW3X + (ability - 11) * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW3Y

                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                color = self.get_pixel_color(coords.ABILITY_ROW1X,
                                             coords.ABILITY_ROW1Y)

                while color != coords.ABILITY_ROW1_READY_COLOR:
                    time.sleep(0.03)
                    color = self.get_pixel_color(coords.ABILITY_ROW1X,
                                                 coords.ABILITY_ROW1Y)

    def get_ability_queue(self):
        """Return a queue of usable abilities."""
        ready = []
        queue = []

        # Add all abilities that are ready to the ready array
        for i in range(13):
            if i <= 4:
                x = coords.ABILITY_ROW1X + i * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW1Y
                color = self.get_pixel_color(x, y)
                if color == coords.ABILITY_ROW1_READY_COLOR:
                    ready.append(i)
            if i >= 5 and i <= 10:
                x = coords.ABILITY_ROW2X + (i - 5) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW2Y
                color = self.get_pixel_color(x, y)
                if color == coords.ABILITY_ROW2_READY_COLOR:
                    ready.append(i)
            if i > 10:
                x = coords.ABILITY_ROW3X + (i - 11) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW3Y
                color = self.get_pixel_color(x, y)
                if color == coords.ABILITY_ROW3_READY_COLOR:
                    ready.append(i)

        health = self.get_pixel_color(coords.PLAYER_HEAL_THRESHOLDX,
                                      coords.PLAYER_HEAL_THRESHOLDY)
        # heal if we need to heal
        if self.check_pixel_color(*coords.PLAYER_HEAL_THRESHOLD):
            if 12 in ready:
                queue.append(12)
            elif 7 in ready:
                queue.append(7)

        # check if offensive buff and ultimate buff are both ready
        buffs = [8, 10]
        if all(i in ready for i in buffs):
            queue.extend(buffs)

        d = coords.ABILITY_PRIORITY
        # Sort the abilities by the set priority
        abilities = sorted(d, key=d.get, reverse=True)
        # Only add the abilities that are ready to the queue
        queue.extend([a for a in abilities if a in ready])

        # If nothing is ready, return a regular attack
        if len(queue) == 0:
            queue.append(0)

        return queue

    def save_check(self):
        """Check if we can do the daily save for AP.

        Make sure no window in your browser pops up when you click the "Save"
        button, otherwise sit will mess with the rest of the script.
        """
        if self.check_pixel_color(*coords.IS_SAVE_READY):
            self.click(*coords.SAVE)
        return

    def get_inventory_slots(self, slots):
        """Get coords for inventory slots from 1 to slots."""
        point = namedtuple("p", ("x", "y"))
        i = 1
        row = 1
        x_pos, y_pos = coords.INVENTORY_SLOTS
        coords = []

        while i <= slots:
            x = x_pos + (i - (12 * (row - 1))) * 50
            y = y_pos + ((row - 1) * 50)
            coords.append(point(x, y))
            if i % 12 == 0:
                row += 1
            i += 1
        return coords

    def merge_inventory(self, slots):
        """Merge all inventory slots starting from 1 to slots.

        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        self.menu("inventory")
        coords = self.get_inventory_slots(slots)
        for slot in coords:
            self.click(*slot)
            self.send_string("d")

    def boost_inventory(self, slots):
        """Merge all inventory slots starting from 1 to slots.

        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        self.menu("inventory")
        coords = self.get_inventory_slots(slots)
        for slot in coords:
            self.click(*slot)
            self.send_string("a")

    def transform_slot(self, slot, threshold=0.8, consume=False):
        """Check if slot is transformable and transform if it is.

        Be careful using this, make sure the item you want to transform is
        not protected, and that all other items are protected, this might
        delete items otherwise. Another note, consuming items will show
        a special tooltip that will block you from doing another check
        for a few seconds, keep this in mind if you're checking multiple
        slots in succession.

        Keyword arguments:
        slot -- The slot you wish to transform, if possible
        threshold -- The fuzziness in the image search, I recommend a value
                     between 0.7 - 0.95.
        consume -- Set to true if item is consumable instead.
        """
        self.menu("inventory")
        slot = self.get_inventory_slots(slot)[-1]
        self.click(*slot)
        time.sleep(userset.SHORT_SLEEP)

        if consume:
            coords = self.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, self.get_file_path("images", "consumable.png"), threshold)
        else:
            coords = self.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, self.get_file_path("images", "transformable.png"), threshold)

        if coords:
            self.ctrl_click(*slot)
            
    def get_idle_cap(self, magic=False):
        """Get the available idle energy or magic."""
        try:
            if magic:
                res = self.ocr(*coords.OCR_MAGIC)
            else:
                res = self.ocr(*coords.OCR_ENERGY)
            match = re.search(".*(\d+\.\d+E\+\d+)", res)
            if match is not None:
                return int(float(match.group(1)))
            elif match is None:
                return 0
        except ValueError:
            print("Couldn't get idle e/m")