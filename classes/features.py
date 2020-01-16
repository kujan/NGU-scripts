"""Feature classes handle the different features in the game."""

import datetime
import math
import re
import time

from collections import deque, namedtuple
from typing      import Dict, List, Tuple
from PIL.Image   import Image as PILImage

from deprecated import deprecated

import constants    as const
import coordinates  as coords
import usersettings as userset

from classes.inputs     import Inputs
from classes.navigation import Navigation
from classes.window     import Window


class FightBoss:
    @staticmethod
    def get_current_boss() -> int:
        """Go to fight and read current boss number."""
        Navigation.menu("fight")
        boss = Inputs.ocr(*coords.OCR_BOSS, debug=False)
        return Inputs.remove_letters(boss)

    @staticmethod
    def nuke(boss :int =None) -> None:
        """Navigate to Fight Boss and Nuke or Fast Fight.

        Keyword arguments
        boss -- If provided, will fight until reached
                If omitted, will hit nuke instead.
        """
        Navigation.menu("fight")
        if boss:
            for _ in range(boss):
                Inputs.click(*coords.FIGHT, fast=True)
            time.sleep(userset.SHORT_SLEEP)
            try:
                current_boss = int(FightBoss.get_current_boss())
            except ValueError:
                current_boss = 1
            x = 0
            while current_boss < boss:
                bossdiff = boss - current_boss
                for _ in range(0, bossdiff):
                    Inputs.click(*coords.FIGHT, fast=True)
                time.sleep(userset.SHORT_SLEEP)
                try:
                    current_boss = int(FightBoss.get_current_boss())
                except ValueError:
                    current_boss = 1
                x += 1
                if x > 7:  # Safeguard if number is too low to reach target boss, otherwise we get stuck here
                    print("Couldn't reach the target boss, something probably went wrong the last rebirth.")
                    break
        else:
            Inputs.click(*coords.NUKE)

    @staticmethod
    def fight() ->None:
        """Navigate to Fight Boss and click fight."""
        Navigation.menu("fight")
        Inputs.click(*coords.FIGHT)

class MoneyPit:
    @staticmethod
    def pit(loadout :int =0) -> None:
        """Throws money into the pit.

        Keyword arguments:
        loadout -- The loadout you wish to equip before throwing gold
                   into the pit, for gear you wish to shock. Make
                   sure that you don't get cap-blocked by either using
                   the unassign setting in the game or swapping gear that
                   doesn't have e/m cap.
        """
        if Inputs.check_pixel_color(*coords.IS_PIT_READY):
            if loadout:
                Inventory.loadout(loadout)
            Navigation.menu("pit")
            Inputs.click(*coords.PIT)
            Inputs.click(*coords.CONFIRM)

    @staticmethod
    def spin() -> None:
        """Spin the wheel."""
        if Inputs.check_pixel_color(*coords.IS_SPIN_READY):
           Navigation.menu("pit")
           Inputs.click(*coords.SPIN_MENU)
           Inputs.click(*coords.SPIN)

class Adventure:
    current_adventure_zone = 0
    itopod_tier_counts = {}
    itopod_tier_map = {
        1: 0,
        2: 50,
        3: 100,
        4: 150,
        5: 200,
        6: 250,
        7: 300,
        8: 350,
        9: 400,
        10: 450,
        11: 500,
        12: 550,
        13: 600,
        14: 650,
        15: 700,
        16: 750,
        17: 800,
        18: 850,
        19: 900,
        20: 950,
    }
    itopod_ap_gained = 0
    itopod_kills = 0

    mega_buff_unlocked = False
    oh_shit_unlocked = False

    @staticmethod
    def adventure(zone=-1, highest :bool =False, itopod :int =None, itopodauto :bool =False) -> None:
        """Go to an adventure zone to idle.
 
        Keyword arguments
        zone -- Zone to idle in, 0 is safe zone, 1 is tutorial and so on.
        highest -- If true, will go to your highest available non-titan zone.
        itopod -- If set to true, it will override other settings and will
                  instead enter the specified ITOPOD floor.
        itopodauto -- If set to true it will click the "optimal" floor button.
        """
        Navigation.menu("adventure")
        Misc.waste_click()
        if not Inputs.check_pixel_color(*coords.IS_IDLE):
            Inputs.click(*coords.ABILITY_IDLE_MODE)
        if itopod or itopodauto:
            Adventure.current_adventure_zone = 0
            Inputs.click(*coords.ITOPOD)
            if itopodauto:
                Inputs.click(*coords.ITOPOD_END)
                # set end to 0 in case it's higher than start
                Inputs.send_string("0")
                Inputs.click(*coords.ITOPOD_AUTO)
                Inputs.click(*coords.ITOPOD_ENTER)
                return
            Inputs.click(*coords.ITOPOD_START)
            Inputs.send_string(str(itopod))
            Inputs.click(*coords.ITOPOD_END)
            Inputs.send_string(str(itopod))
            Inputs.click(*coords.ITOPOD_ENTER)
            return
        if zone == -1 or highest:
            Adventure.current_adventure_zone = 0
            Inputs.click(*coords.RIGHT_ARROW, button="right")
            return
        else:
            Adventure.current_adventure_zone = zone
            Inputs.click(*coords.LEFT_ARROW, button="right")
            for _ in range(zone):
                Inputs.click(*coords.RIGHT_ARROW, fast=True)
            return

    @staticmethod
    def snipe(
        zone :int,
        duration :int,
        once :bool =False,
        highest :bool =False,
        bosses :bool =False,
        manual :bool =False,
        fast :bool =False) -> None:
        """Go to adventure and snipe bosses in specified zone.

        Keyword arguments
        zone -- Zone to snipe, 0 is safe zone, 1 is turorial and so on.
                If 0, it will use the current zone (to maintain guffin counter)
        duration -- The duration in minutes the sniping will run before
                    returning.
        once -- If true it will only kill one boss before returning.
        highest -- If set to true, it will go to your highest available
                   non-titan zone.
        bosses -- If set to true, it will only kill bosses
        manual -- If set to true it will use all available abilities to kill the enemy.
                  In addition it will return after killing one enemy.
        fast   -- If your respawn is lower than your attack speed, use
                  this to remove the overhead from check_pixel_color().
                  It should give you higher xp/h. Remember that move CD
                  is capped at 0.8s, so there's no reason to go lower.
        """
        Navigation.menu("adventure")
        if highest:
            Inputs.click(*coords.LEFT_ARROW, button="right")
            Inputs.click(*coords.RIGHT_ARROW, button="right")
        elif zone > 0 and zone != Adventure.current_adventure_zone:
            Inputs.click(*coords.LEFT_ARROW, button="right")
            for _ in range(zone):
                Inputs.click(*coords.RIGHT_ARROW, fast=True)
        Adventure.current_adventure_zone = zone
        Inputs.click(625, 500)  # click somewhere to move tooltip
        
        if Inputs.check_pixel_color(*coords.IS_IDLE):
            Inputs.click(*coords.ABILITY_IDLE_MODE)
        
        end = time.time() + duration * 60
        while time.time() < end:
            if fast:
                Inputs.click(*coords.ABILITY_REGULAR_ATTACK, fast=True)
                continue

            Inputs.click(625, 500)  # click somewhere to move tooltip
            if not Inputs.check_pixel_color(*coords.IS_DEAD):
                if bosses:
                    if Inputs.check_pixel_color(*coords.IS_BOSS_CROWN):
                        enemy_alive = True
                        if manual:
                            Adventure.kill_enemy()
                        else:
                            while enemy_alive:
                                enemy_alive = not Inputs.check_pixel_color(*coords.IS_DEAD)
                                if Inputs.check_pixel_color(*coords.COLOR_REGULAR_ATTACK_READY):
                                    Inputs.click(*coords.ABILITY_REGULAR_ATTACK)
                                time.sleep(0.1)
                        if once:
                            break
                    else:
                        # Send left arrow and right arrow to refresh monster.
                        Inputs.send_arrow_press(left=True)
                        Inputs.send_arrow_press(left=False)
                else:
                    if manual:
                        Adventure.kill_enemy()
                        return
                    else:
                        Inputs.click(*coords.ABILITY_REGULAR_ATTACK)
            time.sleep(0.01)
        
        Inputs.click(*coords.ABILITY_IDLE_MODE)
    
    @staticmethod
    def itopod_snipe(duration :int, auto :bool =False, fast :bool =False) -> None:
        """Manually snipes ITOPOD for increased speed PP/h.
        
        Keyword arguments:
        duration -- Duration in seconds to snipe, before toggling idle mode
                    back on and returning.
        auto     -- Make sure you're on the optimal floor even if you're
                    already in the ITOPOD
        fast     -- If your respawn is lower than your attack speed, use
                    this to remove the overhead from check_pixel_color().
                    It should give you higher xp/h. Remember that move CD
                    is capped at 0.8s, so there's no reason to go lower.
        """
        end = time.time() + duration
        Adventure.current_adventure_zone = 0
        Navigation.menu("adventure")
        Inputs.click(625, 500)  # click somewhere to move tooltip
        
        # check if we're already in ITOPOD, otherwise enter
        # if auto is true, re-enter ITOPOD to make sure floor is optimal
        if auto or not Inputs.check_pixel_color(*coords.IS_ITOPOD_ACTIVE):
            Inputs.click(*coords.ITOPOD)
            Inputs.click(*coords.ITOPOD_END)
            # set end to 0 in case it's higher than start
            Inputs.send_string("0")
            Inputs.click(*coords.ITOPOD_AUTO)
            Inputs.click(*coords.ITOPOD_ENTER)
        
        if Inputs.check_pixel_color(*coords.IS_IDLE):
            Inputs.click(*coords.ABILITY_IDLE_MODE)
        
        while time.time() < end:
            if fast:
                Inputs.click(*coords.ABILITY_REGULAR_ATTACK, fast=True)
                continue
            if (Inputs.check_pixel_color(*coords.IS_ENEMY_ALIVE) and
               Inputs.check_pixel_color(*coords.COLOR_REGULAR_ATTACK_READY)):
                Inputs.click(*coords.ABILITY_REGULAR_ATTACK)
            else:
                time.sleep(0.01)
        
        Inputs.click(*coords.ABILITY_IDLE_MODE)
    
    @staticmethod
    def kill_enemy() -> None:
        """Attempt to kill enemy in adventure using abilities."""
        start = time.time()
        if Inputs.check_pixel_color(*coords.IS_IDLE):
            Inputs.click(*coords.ABILITY_IDLE_MODE)
        while Inputs.check_pixel_color(*coords.IS_DEAD):
            time.sleep(.1)
            if time.time() > start + 5:
                print("Couldn't detect enemy in kill_enemy()")
                return
        queue = deque(Adventure.get_ability_queue())
        while not Inputs.check_pixel_color(*coords.IS_DEAD):
            if not queue:
                queue = deque(Adventure.get_ability_queue())
            ability = queue.popleft()
            if ability <= 4:
                x = coords.ABILITY_ROW1X + ability * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW1Y
            
            if ability >= 5 and ability <= 10:
                x = coords.ABILITY_ROW2X + (ability - 5) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW2Y
            
            if ability > 10:
                x = coords.ABILITY_ROW3X + (ability - 11) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW3Y
            
            Inputs.click(x, y)
            time.sleep(userset.LONG_SLEEP)
            color = Inputs.get_pixel_color(coords.ABILITY_ROW1X,
                                           coords.ABILITY_ROW1Y)
            
            while color != coords.ABILITY_ROW1_READY_COLOR:
                time.sleep(0.03)
                color = Inputs.get_pixel_color(coords.ABILITY_ROW1X,
                                               coords.ABILITY_ROW1Y)
    
    @staticmethod
    def check_titan_status() -> List[int]:
        """Check to see if any titans are ready."""
        Inputs.click(*coords.MENU_ITEMS["adventure"], button="right")
        text = Inputs.ocr(*coords.OCR_TITAN_RESPAWN).lower()
        ready = []
        i = 1
        for line in text.split('\n'):
            if line == '' or line == '\n':
                continue
            if "ready" in line:
                ready.append(i)
            if "spawn" in line:
                i += 1
        return ready
    
    @staticmethod
    def kill_titan(target :int, mega :bool =True) -> None:
        """Attempt to kill the target titan.
        
        Keyword arguments:
        target -- The id of the titan you wish to kill. 1 for GRB, 2 for GCT and so on.
        mega   -- Use Mega Buff
        """
        Navigation.menu("adventure")
        Inputs.click(*coords.WASTE_CLICK) # close any tooltips
        
        if Inputs.check_pixel_color(*coords.IS_IDLE):
            Inputs.click(*coords.ABILITY_IDLE_MODE)
        
        Inputs.click(*coords.LEFT_ARROW, button="right")
        charge = False
        parry = False
        if mega:
            while not Inputs.check_pixel_color(*coords.COLOR_MEGA_BUFF_READY) or not charge or not parry:
                queue = Adventure.get_ability_queue()
                Inputs.click(625, 600)
                if 2 in queue and not parry:
                    x = coords.ABILITY_ROW1X + 2 * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW1Y
                    Inputs.click(x, y)
                    parry = True
                    time.sleep(1)  # wait for global cooldown
                if 9 in queue and not charge:
                    x = coords.ABILITY_ROW2X + (9 - 5) * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW2Y
                    Inputs.click(x, y)
                    charge = True
                    time.sleep(1)  # wait for global cooldown
                time.sleep(userset.MEDIUM_SLEEP)
        
        else:
            while not Inputs.check_pixel_color(*coords.COLOR_ULTIMATE_BUFF_READY) or not charge or not parry:
                queue = Adventure.get_ability_queue()
                Inputs.click(625, 600)
                if 2 in queue and not parry:
                    x = coords.ABILITY_ROW1X + 2 * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW1Y
                    Inputs.click(x, y)
                    parry = True
                    time.sleep(1)  # wait for global cooldown
                if 9 in queue and not charge:
                    x = coords.ABILITY_ROW2X + 4 * coords.ABILITY_OFFSETX
                    y = coords.ABILITY_ROW2Y
                    Inputs.click(x, y)
                    charge = True
                    time.sleep(1)  # wait for global cooldown
                time.sleep(userset.MEDIUM_SLEEP)
        
        buffs = [2, 9]
        print("Waiting for charge and parry to be ready")
        while not all(x in Adventure.get_ability_queue() for x in buffs):
            time.sleep(.5)
        
        for _ in range(const.TITAN_ZONE[target - 1]):
            Inputs.click(*coords.RIGHT_ARROW, fast=True)
        Adventure.current_adventure_zone = const.TITAN_ZONE[target - 1]
        time.sleep(userset.LONG_SLEEP)
        start = time.time()
        while Inputs.check_pixel_color(*coords.IS_DEAD):  # wait for titan to spawn
            time.sleep(0.05)
            if time.time() > start + 5:
                print("Couldn't detect enemy in kill_titan()")
                return
        
        queue = deque(Adventure.get_ability_queue())
        while not Inputs.check_pixel_color(*coords.IS_DEAD):
            if not queue:
                queue = deque(Adventure.get_ability_queue())
            
            ability = queue.popleft()
            if ability <= 4:
                x = coords.ABILITY_ROW1X + ability * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW1Y
            
            if ability >= 5 and ability <= 10:
                x = coords.ABILITY_ROW2X + (ability - 5) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW2Y
            
            if ability > 10:
                x = coords.ABILITY_ROW3X + (ability - 11) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW3Y
            
            Inputs.click(x, y)
            time.sleep(userset.LONG_SLEEP)
            color = Inputs.get_pixel_color(coords.ABILITY_ROW1X,
                                           coords.ABILITY_ROW1Y)
            
            while color != coords.ABILITY_ROW1_READY_COLOR:
                time.sleep(0.05)
                color = Inputs.get_pixel_color(coords.ABILITY_ROW1X,
                                               coords.ABILITY_ROW1Y)
    
    @staticmethod
    def get_ability_queue() -> List[int]:
        """Return a queue of usable abilities."""
        ready = []
        queue = []
        
        # Add all abilities that are ready to the ready array
        for i in range(1, 16):
            if i <= 4:
                x = coords.ABILITY_ROW1X + i * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW1Y
                color = Inputs.get_pixel_color(x, y)
                if color == coords.ABILITY_ROW1_READY_COLOR:
                    ready.append(i)
            if i >= 5 and i <= 10:
                if Adventure.mega_buff_unlocked and i == 6:
                    continue
                x = coords.ABILITY_ROW2X + (i - 5) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW2Y
                color = Inputs.get_pixel_color(x, y)
                if color == coords.ABILITY_ROW2_READY_COLOR:
                    ready.append(i)
            if i > 10:
                x = coords.ABILITY_ROW3X + (i - 11) * coords.ABILITY_OFFSETX
                y = coords.ABILITY_ROW3Y
                color = Inputs.get_pixel_color(x, y)
                if color == coords.ABILITY_ROW3_READY_COLOR:
                    ready.append(i)
        
        if 15 in ready:
            Adventure.oh_shit_unlocked = True
        if 14 in ready:
            Adventure.mega_buff_unlocked = True
        # heal if we need to heal
        if Inputs.check_pixel_color(*coords.PLAYER_HEAL_THRESHOLD):
            if 15 in ready:
                queue.append(15)
            elif 12 in ready:
                queue.append(12)
            elif 7 in ready:
                queue.append(7)
        
        # check if offensive buff and ultimate buff are both ready
        buffs = [8, 10]
        if 14 in ready:
            queue.append(14)
        elif all(i in ready for i in buffs) and not Adventure.mega_buff_unlocked:
            queue.extend(buffs)
        
        d = coords.ABILITY_PRIORITY
        # Sort the abilities by the set priority
        abilities = sorted(d, key=d.get, reverse=True)
        # Only add the abilities that are ready to the queue
        queue.extend([a for a in abilities if a in ready])
        
        # If nothing is ready, return a regular attack
        if not queue:
            queue.append(0)
        return queue
    
    @staticmethod
    def itopod_ap(duration :int) -> None:
        """Abuse an oversight in the kill counter for AP rewards for mucher higher AP/h in ITOPOD.
        If you use this method, make sure you do not retoggle idle mode in adventure in other parts
        of your script. If you have to, make sure to empty itopod_tier_counts with:
        itopod_tier_counts = {}
        
        Keyword arguments:
        duration -- Duration in seconds to run, before toggling idle mode
                    back on and returning.
        """
        print("WARNING: itopod_ap() is largely untested")
        end = time.time() + duration * 60
        Adventure.current_adventure_zone = 0
        Navigation.menu("adventure")
        Inputs.click(625, 500)  # click somewhere to move tooltip
        if Inputs.check_pixel_color(*coords.IS_IDLE):
            Inputs.click(*coords.ABILITY_IDLE_MODE)
        # check if we're already in ITOPOD, otherwise enter
        if not Adventure.itopod_tier_counts:
            for tier, floor in Adventure.itopod_tier_map.items():
                Inputs.click(*coords.ITOPOD)
                Inputs.click(*coords.ITOPOD_START)
                Inputs.send_string(floor)
                # set end to 0 in case it's higher than start
                Inputs.click(*coords.ITOPOD_ENTER)
                Inputs.click(*coords.ADVENTURE_TOOLTIP)
                count = Inputs.remove_letters(Inputs.ocr(*coords.OCR_AP_KILL_COUNT))
                print(f"Tier {tier}: {count}")
                try:
                    count = int(count)
                except ValueError:
                    print(f"couldn't convert '{count}' to int")
                Adventure.itopod_tier_counts[tier] = count
        print(Adventure.itopod_tier_counts)
        while time.time() < end:
            next_tier = min(Adventure.itopod_tier_counts, key=Adventure.itopod_tier_counts.get)
            print(f"going to itopod tier {next_tier}")
            Inputs.click(*coords.ITOPOD)
            Inputs.click(*coords.ITOPOD_START)
            Inputs.send_string(Adventure.itopod_tier_map[next_tier])
            # set end to 0 in case it's higher than start
            Inputs.click(*coords.ITOPOD_ENTER)
            time.sleep(userset.LONG_SLEEP)
            kc = Adventure.itopod_tier_counts[next_tier]
            while kc > 0:
                if Inputs.check_pixel_color(*coords.IS_ENEMY_ALIVE):
                    Inputs.click(*coords.ABILITY_REGULAR_ATTACK)
                    
                    Adventure.itopod_kills += 1
                    kc -= 1
                    if kc > 0:
                        time.sleep(.7 - userset.MEDIUM_SLEEP)  # Make sure we wait long enough
                    for tier, count in Adventure.itopod_tier_counts.items():
                        Adventure.itopod_tier_counts[tier] -= 1
                        if Adventure.itopod_tier_counts[tier] < 1:
                            Adventure.itopod_tier_counts[tier] = 40 - tier
                else:
                    time.sleep(0.06)
            Adventure.itopod_ap_gained += 1
            print(f"Kills: {Adventure.itopod_kills}\nAP gained: {Adventure.itopod_ap_gained}")
        return

class Inventory:
    @staticmethod
    def merge_equipment() -> None:
        """Navigate to inventory and merge equipment."""
        Navigation.menu("inventory")
        for slot in coords.EQUIPMENT_SLOTS:
            if slot == "cube":
                return
            Inputs.click(*coords.EQUIPMENT_SLOTS[slot])
            Inputs.send_string("d")
    
    @staticmethod
    def boost_equipment(boost_cube :bool =True) -> None:
        """Boost all equipment.
        
        Keyword arguments
        boost_cube -- If True (default), will boost cube after all equipment
                      has been boosted.
        """
        Navigation.menu("inventory")
        for slot in coords.EQUIPMENT_SLOTS:
            if slot == "cube":
                if boost_cube:
                    Inventory.boost_cube()
                return
            Inputs.click(*coords.EQUIPMENT_SLOTS[slot])
            Inputs.send_string("a")
    
    @staticmethod
    def boost_cube() -> None:
        """Boost cube."""
        Navigation.menu("inventory")
        Inputs.click(*coords.EQUIPMENT_SLOTS["cube"], "right")
    
    @staticmethod
    def loadout(target :int) -> None:
        """Equip a loadout.
        
        Keyword arguments
        target -- The loadout to be equiped
        """
        Navigation.menu("inventory")
        Inputs.click(*coords.LOADOUT[target])
    
    @staticmethod
    def get_inventory_slots(slots :int) -> None:
        """Get coords for inventory slots from 1 to slots."""
        point = namedtuple("p", ("x", "y"))
        i = 1
        row = 1
        x_pos, y_pos = coords.INVENTORY_SLOTS
        res = []
        
        while i <= slots:
            x = x_pos + (i - (12 * (row - 1))) * 50
            y = y_pos + ((row - 1) * 50)
            res.append(point(x, y))
            if i % 12 == 0:
                row += 1
            i += 1
        return res
    
    @staticmethod
    def merge_inventory(slots :int) -> None:
        """Merge all inventory slots starting from 1 to slots.
        
        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        Navigation.menu("inventory")
        coord = Inventory.get_inventory_slots(slots)
        for slot in coord:
            Inputs.click(*slot)
            Inputs.send_string("d")
    
    @staticmethod
    def boost_inventory(slots :int) -> None:
        """Merge all inventory slots starting from 1 to slots.
        
        Keyword arguments:
        slots -- The amount of slots you wish to merge
        """
        Navigation.menu("inventory")
        coord = Inventory.get_inventory_slots(slots)
        for slot in coord:
            Inputs.click(*slot)
            Inputs.send_string("a")
    
    @staticmethod
    def transform_slot(slot :int, threshold :float =0.8, consume :bool =False) -> None:
        """Check if slot is transformable and transform if it is.
        Be careful using this, make sure the item you want to transform is
        not protected, and that all other items are protected, this might
        delete items otherwise. Another note, consuming items will show
        a special tooltip that will block you from doing another check
        for a few seconds, keep this in mind if you're checking multiple
        slots in succession.
        
        Keyword arguments:
        slot      -- The slot you wish to transform, if possible
        threshold -- The fuzziness in the image search, I recommend a value
                     between 0.7 - 0.95.
        consume   -- Set to true if item is consumable instead.
        """
        Navigation.menu("inventory")
        slot = Inventory.get_inventory_slots(slot)[-1]
        Inputs.click(*slot)
        time.sleep(userset.SHORT_SLEEP)
        
        if consume:
            coord = Inputs.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600,
                                        Inputs.get_file_path("images", "consumable.png"), threshold)
        else:
            coord = Inputs.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600,
                                        Inputs.get_file_path("images", "transformable.png"), threshold)
        
        if coord:
            Inputs.ctrl_click(*slot)

class Augmentation:
    @staticmethod
    def augments(augments :Dict[str, float], energy :int) -> None:
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
        Navigation.menu("augmentations")
        for k in augments:
            val = math.floor(augments[k] * energy)
            Misc.set_input(val)
            # Scroll down if we have to.
            bottom_augments = ["AE", "ES", "LS", "QSL"]
            i = 0
            if k in bottom_augments:
                color = Inputs.get_pixel_color(*coords.AUG_SCROLL_SANITY_BOT)
                while color not in coords.SANITY_AUG_SCROLL_COLORS:
                    Inputs.click(*coords.AUG_SCROLL_BOT)
                    time.sleep(userset.MEDIUM_SLEEP)
                    color = Inputs.get_pixel_color(*coords.AUG_SCROLL_SANITY_BOT)
                    i += 1
                    if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
                        Navigation.current_menu = ""
                        Navigation.menu("augmentations")
                    elif i > 10:
                        print("Couldn't assign augments")
                        break
            
            else:
                color = Inputs.get_pixel_color(*coords.AUG_SCROLL_SANITY_TOP)
                while color not in coords.SANITY_AUG_SCROLL_COLORS:
                    Inputs.click(*coords.AUG_SCROLL_TOP)
                    time.sleep(userset.MEDIUM_SLEEP)
                    color = Inputs.get_pixel_color(*coords.AUG_SCROLL_SANITY_TOP)
                    i += 1
                    if i > 5 and i <= 10:  # Safeguard if something goes wrong with augs
                        Navigation.current_menu = ""
                        Navigation.menu("augmentations")
                    elif i > 10:
                        print("Couldn't assign augments")
                        break
            Inputs.click(*coords.AUGMENT[k])

class AdvancedTraining:
    @staticmethod
    def advanced_training(energy :int, ability :int =0) -> None:
        """Assign energy to adanced training.
        
        Keyword arguments
        energy  -- Set the total energy to assign to AT.
        ability -- The AT ability to be trained.
                   If this is zero, it'll split the energy evenly between
                   Adv Toughness, Adv Power, Wandoos Energy and Wandoos Magic.
                   Splitting energy is the default behavior.
        """
        Navigation.menu("advtraining")
        if ability == 0:
            energy = energy // 4
            Misc.set_input(energy)
            Inputs.click(*coords.ADV_TRAINING_POWER)
            Inputs.click(*coords.ADV_TRAINING_TOUGHNESS)
            Inputs.click(*coords.ADV_TRAINING_WANDOOS_ENERGY)
            Inputs.click(*coords.ADV_TRAINING_WANDOOS_MAGIC)
        
        else:
            Misc.set_input(energy)
            if ability == 1:
                Inputs.click(*coords.ADV_TRAINING_TOUGHNESS)
            if ability == 2:
                Inputs.click(*coords.ADV_TRAINING_POWER)
            if ability == 3:
                Inputs.click(*coords.ADV_TRAINING_BLOCK)
            if ability == 4:
                Inputs.click(*coords.ADV_TRAINING_WANDOOS_ENERGY)
            if ability == 5:
                Inputs.click(*coords.ADV_TRAINING_WANDOOS_MAGIC)

class TimeMachine:
    @staticmethod
    def time_machine(e :int, m :int =0, magic :bool =False) -> None:
        """Add energy and/or magic to TM.
        
        Example: TimeMachine.time_machine(1000, 2000)
                 TimeMachine.time_machine(1000, magic=True)
                 TimeMachine.time_machine(1000)
        
        First example will add 1000 energy and 2000 magic to TM.
        Second example will add 1000 energy and 1000 magic to TM.
        Third example will add 1000 energy to TM.
        
        Keyword arguments:
        e -- The amount of energy to put into TM.
        m -- The amount of magic to put into TM, if this is 0, it will use the
             energy value to save unnecessary clicks to the input box.
        magic -- Set to true if you wish to add magic as well
        """
        Navigation.menu("timemachine")
        Misc.set_input(e)
        Inputs.click(*coords.TM_SPEED)
        if magic or m:
            if m:
                Misc.set_input(m)
            Inputs.click(*coords.TM_MULT)

class BloodMagic:
    @staticmethod
    def blood_magic(target :int) -> None:
        """Assign magic to BM.
        
        Keyword arguments
        target -- Will cap all rituals till the target ritual
                  Usually run as blood_magic(8)
        """
        Navigation.menu("bloodmagic")
        for i in range(target):
            Inputs.click(*coords.BM[i])
    
    @staticmethod
    def activate_all_bm() -> None:
        """Click activate all in BM menu."""
        Navigation.menu("bloodmagic")
        Inputs.click(*coords.BM_CAP_ALL)

    @staticmethod
    @deprecated(version='0.1', reason="speedrun_bloodpill is deprecated, use iron_pill() instead")
    def speedrun_bloodpill():
        """Deprecated"""
        return
    
    @staticmethod
    @deprecated(version='0.1', reason="iron_pill is deprecated, use cast_spell() instead")
    def iron_pill():
        """Deprecated"""
        return
    
    @staticmethod
    def toggle_auto_spells(number :bool =True, drop :bool =True, gold :bool =True) -> None:
        """Enable/Disable autospells
        
        Keyword arguments
        number, drop, gold -- Spells to be enabled or disabled.
                              If True, enable the spell. If False, disable the spell.
                              If None, ignore the spell.
        """
        Navigation.spells()
        Inputs.click(600, 600)  # move tooltip
        
        if number is not None:
            number_active = Inputs.check_pixel_color(*coords.COLOR_BM_AUTO_NUMBER)
            if (number and not number_active) or (not number and number_active):
                Inputs.click(*coords.BM_AUTO_NUMBER)
        if drop is not None:
            drop_active = Inputs.check_pixel_color(*coords.COLOR_BM_AUTO_DROP)
            if (drop and not drop_active) or (not drop and drop_active):
                Inputs.click(*coords.BM_AUTO_DROP)
        
        if gold is not None:
            gold_active = Inputs.check_pixel_color(*coords.COLOR_BM_AUTO_GOLD)
            if (gold and not gold_active) or (not gold and gold_active):
                Inputs.click(*coords.BM_AUTO_GOLD)
    
    @staticmethod
    def check_spells_ready() -> List[int]:
        """Check which spells are ready to cast.
        
        Returns a list with integers corresponding to which spell is ready. The values on the
        list can be:
            1 - Iron pill
            2 - MacGuffin alpha
            3 - MacGuffin beta
        """
        if Inputs.check_pixel_color(*coords.COLOR_SPELL_READY):
            Navigation.spells()
            Inputs.click(*coords.BM_PILL, button="right")
            spells = []
            res = Inputs.ocr(*coords.OCR_BM_SPELL_TEXT)
            if "cooldown: 0.0s" in res.lower():
                spells.append(1)
            
            Inputs.click(*coords.BM_GUFFIN_A, button="right")
            res = Inputs.ocr(*coords.OCR_BM_SPELL_TEXT)
            if "cooldown: 0.0s" in res.lower():
                spells.append(2)
            
            Inputs.click(*coords.BM_GUFFIN_B, button="right")
            res = Inputs.ocr(*coords.OCR_BM_SPELL_TEXT)
            if "cooldown: 0.0s" in res.lower():
                spells.append(3)
            
            return spells
        else:
            return []
    
    @staticmethod
    def cast_spell(target :int) -> None:
        """Cast target spell.
        
        This method will allocate any idle magic into BM and wait for the
        time set in usersettings.py. Remember to re-enable auto spells after
        calling this method, using toggle_auto_spells().
        
        Keyword arguments
        number -- The spell to be cast. Possible values are:
            1 - Iron pill
            2 - MacGuffin alpha
            3 - MacGuffin beta
        """
        if Inputs.check_pixel_color(*coords.COLOR_SPELL_READY):
            targets = [0, coords.BM_PILL, coords.BM_GUFFIN_A, coords.BM_GUFFIN_B]
            start = time.time()
            BloodMagic.blood_magic(8)
            BloodMagic.toggle_auto_spells(False, False, False)  # disable all auto spells
            
            if userset.SPELL == 0:  # Default to 5 mins if not set
                duration = 300
            else:
                duration = userset.SPELL
            
            while time.time() < start + duration:
                print(f"Sniping itopod for {duration} seconds while waiting to cast spell.")
                Adventure.itopod_snipe(duration)
            Navigation.spells()
            Inputs.click(*targets[target])

class Wandoos:
    @staticmethod
    def wandoos(energy :bool =True, magic :bool =False) -> None:
        """Assign energy and/or magic to wandoos.
        
        Keyword arguments
        energy -- Assign energy to Wandoos (default: True)
        magic  -- Assign magic to Wandoos  (default: False)
        """
        Navigation.menu("wandoos")
        if energy:
            Inputs.click(*coords.WANDOOS_ENERGY)
        if magic:
            Inputs.click(*coords.WANDOOS_MAGIC)
    
    @staticmethod
    def set_wandoos(version :int) -> None:
        """Set wandoos version.
        
        Keyword arguments:
        version -- Wandoos version of choice. Possible values are:
                   0 : Wandoos 98
                   1 : Wandoos Meh
                   2 : Wandoos XL
        """
        Navigation.menu("wandoos")
        Inputs.click(*coords.WANDOOS_VERSION[version])
        Navigation.confirm()
    
    @staticmethod
    def check_wandoos_bb_status(magic :bool =False) -> None:
        """Check if wandoos is currently fully BB'd.
        
        Keyword arguments
        magic -- If True, check if Wandoos magic is BB'd
                 If False (default), check if Wandoos energy is BB'd
        """
        Navigation.menu("wandoos")
        if magic:
            return Inputs.check_pixel_color(*coords.COLOR_WANDOOS_MAGIC_BB)
        return Inputs.check_pixel_color(*coords.COLOR_WANDOOS_ENERGY_BB)

class NGU:
    @staticmethod
    def assign_ngu(value :int, targets :List[int], magic :bool =False) -> None:
        """Assign energy/magic to NGU's.
        
        Keyword arguments:
        value -- the amount of energy/magic that will get split over all NGUs.
        targets -- Array of NGU's to use (1-9).
        magic -- Set to true if these are magic NGUs
        """
        if len(targets) > 9:
            raise RuntimeError("Passing too many NGU's to assign_ngu," +
                               " allowed: 9, sent: " + str(len(targets)))
        if magic: Navigation.ngu_magic()
        else: Navigation.menu("ngu")
        
        Misc.set_input(value // len(targets))
        for i in targets:
            NGU = coords.Pixel(coords.NGU_PLUS.x, coords.NGU_PLUS.y + i * 35)
            Inputs.click(*NGU)
    
    @staticmethod
    @deprecated(version='0.1', reason="bb_ngu() is deprecated since .415 use cap_ngu() instead")
    def bb_ngu(value, targets, overcap=1, magic=False):
        """Estimates the BB value of each supplied NGU.
        It will send value into the target NGU's, which will fill the progress bar. It's very
        important that you put enough e/m into the NGU's to trigger the "anti-flicker"
        (>10% of BB cost), otherwise it will not function properly.
        
        Keyword arguments:
        value -- The amount of energy used to determine the cost of BBing the target NGU's
        targets -- Array of NGU's to BB. Example: [1, 3, 4, 5, 6]
        overcap -- Use this if you wish to assign more e/m than absolute minimum to BB
                   the NGU's. This might be useful for longer runs to make sure the cost
                   to BB doesn't exceed the assigned e/m. A value of 1.1 assigns 10% extra.
        magic -- Set to true if these are magic NGUs
        """
        if magic:
            Navigation.ngu_magic()
        else:
            Navigation.menu("ngu")
        
        Misc.set_input(value)
        
        for target in targets:
            NGU = coords.Pixel(coords.NGU_PLUS.x, coords.NGU_PLUS.y + target * 35)
            Inputs.click(*NGU)
        
        for target in targets:
            energy = 0
            for x in range(198):
                color = Inputs.get_pixel_color(coords.NGU_BAR_MIN.x + x,
                                               coords.NGU_BAR_MIN.y +
                                               coords.NGU_BAR_OFFSET_Y * target,
                                               )
                if color == coords.NGU_BAR_WHITE:
                    pixel_coefficient = x / 198
                    value_coefficient = overcap / pixel_coefficient
                    energy = (value_coefficient * value) - value
                    break
            if energy == 0:
                if magic:
                    print(f"Warning: You might be overcapping magic NGU #{target}")
                else:
                    print(f"Warning: You might be overcapping energy NGU #{target}")
                continue
      
            Misc.set_input(int(energy))
            Inputs.click(coords.NGU_PLUS.x, coords.NGU_PLUS.y + target * 35)

    @staticmethod
    def cap_ngu(targets :List[int] =None, magic :bool =False, cap_all :bool =True) -> None:
        """Cap NGUs.

        Keyword arguments
        targets -- The NGU's you wish to cap
        magic -- Set to true if these are magic NGU's
        cap_all -- Set to true if you wish to cap all NGU's
        """
        targets = targets or []
        if magic:
            Navigation.ngu_magic()
        else:
            Navigation.menu("ngu")
        
        for target in targets:
            NGU = coords.Pixel(coords.NGU_CAP.x, coords.NGU_CAP.y + target * 35)
            Inputs.click(*NGU)
        
        if cap_all and not targets:
            Inputs.click(*coords.NGU_CAP_ALL)
    
    @staticmethod
    def set_ngu_overcap(value :int) -> None:
        """Set the amount you wish to overcap your NGU's."""
        Navigation.menu("ngu")
        Inputs.click(*coords.NGU_OVERCAP)
        Inputs.send_string(value)

class Yggdrasil:
    @staticmethod
    def ygg(eat_all :bool =False, equip :int =0) -> None:
        """Navigate to inventory and handle fruits.
        
        Keyword arguments:
        eat_all  -- Set to true if you're rebirthing, it will force eat all
                   fruit.
        equip    -- Equip loadout with given index. Don't change if zero.
        """
        if equip:
            Misc.reclaim_all()
            Inventory.loadout(equip)
        
        Navigation.menu("yggdrasil")
        if eat_all:
            Inputs.click(*coords.YGG_EAT_ALL)
        else:
            Inputs.click(*coords.HARVEST)

class GoldDiggers:
    @staticmethod
    def gold_diggers(targets :List[int] =const.DEFAULT_DIGGER_ORDER, deactivate :bool =False) -> None:
        """Activate diggers.
        
        Keyword arguments:
        targets -- Array of diggers to use from 1-12. Example: [1, 2, 3, 4, 9].
        deactivate -- Set to True if you wish to deactivate these
                    diggers otherwise it will just try to up the cap.
        """
        Navigation.menu("digger")
        for i in targets:
            page = ((i - 1) // 4)
            item = i - (page * 4)
            Inputs.click(*coords.DIG_PAGE[page])
            if deactivate:
                Inputs.click(*coords.DIG_ACTIVE[item])
            else:
                Inputs.click(*coords.DIG_CAP[item])
    
    @staticmethod
    def deactivate_all_diggers() -> None:
        """Click deactivate all in digger menu."""
        Navigation.menu("digger")
        Inputs.click(*coords.DIG_DEACTIVATE_ALL)
    
    @staticmethod
    def activate_all_diggers() -> None:
        """Click activate all in digger menu."""
        Navigation.menu("digger")
        Inputs.click(*coords.DIG_CAP_ALL)
    
    @staticmethod
    def level_diggers() -> None:
        """Level all diggers."""
        Navigation.menu("digger")
        for page in coords.DIG_PAGE:
            Inputs.click(*page)
            for digger in coords.DIG_LEVEL:
                Inputs.click(*digger, button="right")

class BeardsOfPower:
    """Probably the most useful class ever. -- 4G"""

class Questing:
    inventory_cleaned = False
    
    @staticmethod
    def start_complete() -> None:
        """This starts a new quest if no quest is running.
        If a quest is running, it tries to turn it in.
        """
        Navigation.menu("questing")
        Inputs.click(*coords.QUESTING_START_QUEST)
    
    @staticmethod
    def skip() -> None:
        """This skips your current quest."""
        Navigation.menu("questing")
        time.sleep(userset.MEDIUM_SLEEP)
        Inputs.click(*coords.QUESTING_SKIP_QUEST)
        Navigation.confirm()
    
    @staticmethod
    def get_quest_text() -> str:
        """Check if we have an active quest or not."""
        Navigation.menu("questing")
        Misc.waste_click()  # move tooltip
        time.sleep(userset.SHORT_SLEEP)
        return Inputs.ocr(*coords.OCR_QUESTING_LEFT_TEXT)
    
    @staticmethod
    def get_available_majors() -> int:
        """Return the amount of available major quests."""
        Navigation.menu("questing")
        text = Inputs.ocr(*coords.OCR_QUESTING_MAJORS)
        try:
            match = re.search(r"(\d+)\/\d+", text)
            if match:
                return int(match.group(1))
        except ValueError:
            print("couldn't get current major quests available")
            return -1
    
    @staticmethod
    def questing_consume_items(cleanup :bool =False) -> None:
        """Check for items in inventory that can be turned in."""
        Navigation.menu("inventory")
        Inputs.click(*coords.INVENTORY_PAGE[0])
        bmp = Inputs.get_bitmap()
        for item in coords.QUESTING_FILENAMES:
            path = Inputs.get_file_path("images", item)
            loc = Inputs.image_search(Window.x, Window.y, Window.x + 960, Window.y + 600, path, 0.91, bmp=bmp)
            if loc:
                Inputs.click(*loc, button="right")
                if cleanup:
                    Inputs.send_string("d")
                    Inputs.ctrl_click(*loc)
                time.sleep(3)  # Need to wait for tooltip to disappear after consuming
    
    @staticmethod
    def questing(duration :int =30, major :bool =False, subcontract :bool =False, force :int =0, adv_duration :int =2, butter :bool =False) -> None:
        """Procedure for questing.
        
        ===== IMPORTANT =====
        This method uses imagesearch to find items in your inventory, it will
        both right click and ctrl-click items (quick delete keybind), so make
        sure all items are protected.
        
        The method will only check the inventory page that is currently open,
        so make sure it's set to page 1 and that your inventory has space.
        
        If your inventory fills with mcguffins/other drops while it runs, it
        will get stuck doing the same quest forever. Make sure you will have
        space for the entire duration you will leave it running unattended.
        =====================
        
        Keyword arguments:
        duration     -- The duration in minutes to run if manual mode is selected. If
                        quest gets completed, function will return prematurely.
        major        -- Set to true if you only wish to manually do main quests,
                        if False it will manually do all quests.
        subcontract  -- Set to True if you wish to subcontract all quests.
        force        -- Only quest in this zone. This will skip quests until you
                        recieve one for the selected zone, so make sure you disable
                        "Use major quests if available".
        adv_duration -- The time in minutes to spend sniping before checking inventory.
                        A higher value is good when forcing, because you spend less time
                        scanning the inventory and you will not waste any extra quest items.
                        A value around 2 minutes is good when doing majors because it's very
                        likely that the extra items are lost.
        
        Suggested usages:
        questing(major=True)
        questing(subcontract=True)
        If you only wish to manually do major quests (so you can do ITOPOD)
        then I suggest that you only call questing() every 10-15 minutes because
        subcontracting takes very long to finish. Same obviously goes for subcontracting
        only.
        Remember the default duration is 40, which is there to safeguard if something
        goes wrong to break out of the function. Set this higher/lower after your own
        preferences.
        questing(duration=40)
        This will manually complete any quest you get for 30 minutes, then it returns,
        or it returns when the quest is completed.
        Use this together with harvesting ygg, recapping diggers and so on, or even
        sniping ITOPOD.
        """
        end = time.time() + duration * 60
        Navigation.menu("questing")
        Inputs.click(*coords.WASTE_CLICK)  # move tooltip
        text = Questing.get_quest_text()
        
        if coords.QUESTING_QUEST_COMPLETE in text.lower():
            Questing.start_complete()
            time.sleep(userset.LONG_SLEEP * 2)
            text = Questing.get_quest_text()  # fetch new quest text
        
        if coords.QUESTING_NO_QUEST_ACTIVE in text.lower():  # if we have no active quest, start one
            Questing.start_complete()
            if force and not Questing.inventory_cleaned:
                Questing.questing_consume_items(True)  # we have to clean up the inventory from any old quest items
                Questing.inventory_cleaned = True
            elif not force:
                Questing.questing_consume_items(True)
            Inputs.click(960, 600)  # move tooltip
            time.sleep(userset.LONG_SLEEP)
            text = Questing.get_quest_text()  # fetch new quest text
        
        if force:
            if Inputs.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                Inputs.click(*coords.QUESTING_USE_MAJOR)
            
            while not coords.QUESTING_ZONES[force] in text.lower():
                Questing.skip()
                Questing.start_complete()
                text = Questing.get_quest_text()
        
        if subcontract:
            if Inputs.check_pixel_color(*coords.QUESTING_IDLE_INACTIVE):
                Inputs.click(*coords.QUESTING_SUBCONTRACT)
            return
        
        if major and coords.QUESTING_MINOR_QUEST in text.lower():  # check if current quest is minor
            if Inputs.check_pixel_color(*coords.QUESTING_IDLE_INACTIVE):
                Inputs.click(*coords.QUESTING_SUBCONTRACT)
            return
        
        if not Inputs.check_pixel_color(*coords.QUESTING_IDLE_INACTIVE):  # turn off idle
            Inputs.click(*coords.QUESTING_SUBCONTRACT)
        if butter:
            Inputs.click(*coords.QUESTING_BUTTER)
        for count, zone in enumerate(coords.QUESTING_ZONES, start=0):
            if zone in text.lower():
                current_time = time.time()
                while current_time < end:
                    if current_time + adv_duration * 60 > end:  # adjust adv_duration if it will cause duration to be exceeded
                        adv_duration = (end - current_time) / 60
                        if adv_duration < 0.5:
                            adv_duration = 0
                            return
                    Adventure.snipe(count, adv_duration)
                    Inventory.boost_cube()
                    Questing.questing_consume_items()
                    text = Questing.get_quest_text()
                    current_time = time.time()
                    if coords.QUESTING_QUEST_COMPLETE in text.lower():
                        try:
                            start_qp = int(Inputs.remove_letters(Inputs.ocr(*coords.OCR_QUESTING_QP)))
                        except ValueError:
                            print("Couldn't fetch current QP")
                            start_qp = 0
                        Questing.start_complete()
                        Inputs.click(605, 510)  # move tooltip
                        try:
                            current_qp = int(Inputs.remove_letters(Inputs.ocr(*coords.OCR_QUESTING_QP)))
                        except ValueError:
                            print("Couldn't fetch current QP")
                            current_qp = 0
                        
                        gained_qp = current_qp - start_qp
                        print(f"Completed quest in zone #{count} at {datetime.datetime.now().strftime('%H:%M:%S')} for {gained_qp} QP")
                        
                        return
    
    @staticmethod
    def get_use_majors() -> bool:
        """This returns whether the "Use Major Quests if Available" checkbox is toggled ON."""
        return Inputs.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR)
    
    @staticmethod
    def toggle_use_majors() -> None:
        """This toggles ON/OFF the "Use Major Quests if Available" checkbox."""
        Navigation.menu("questing")
        Inputs.click(*coords.QUESTING_USE_MAJOR)
    
    @staticmethod
    def set_use_majors(set :bool =True) -> None:
        """This enables/disables the "Use Major Quests if Available" checkbox.
        
        Keyword arguments
        set -- If True, enable the checkbox. If False, disable it.
        """
        Navigation.menu("questing")
        if Questing.get_use_majors() != set:  # Toggle if only one is True
            Questing.toggle_use_majors()

class Hacks:
    @staticmethod
    def hacks(targets :List[int] =None, value :int =1e12) -> None:
        """Activate hacks.
        
        Keyword arguments
        targets -- List of hacks to level up. Default value is [1, 2, 3, 4, 5, 6, 7, 8].
        value   -- Resource to spend, default to 1e12.
        """
        targets = targets or []
        Misc.set_input(value // len(targets))
        Navigation.menu("hacks")
        for i in targets:
            page = ((i - 1) // 8)
            item = i - (page * 8)
            Inputs.click(*coords.HACK_PAGE[page])
            Inputs.click(*coords.HACKS[item])

class Wishes:
    completed_wishes = []

class SelloutShop:
    @staticmethod
    def eat_muffin(buy :bool =False) -> None:
        """Eat a MacGuffin Muffin if it's not active.
        
        Keyword arguments:
        buy -- set to True if you wish to buy a muffin if you have enough
        AP and you currently have 0 muffins.
        """
        Navigation.sellout_boost_2()
        muffin_status = Inputs.ocr(*coords.OCR_MUFFIN).lower()
        if "have: 0" in muffin_status and "inactive" in muffin_status:
            print(muffin_status)
            if buy:
                try:
                    ap = int(Inputs.remove_letters(Inputs.ocr(*coords.OCR_AP)))
                except ValueError:
                    print("Couldn't get current AP")
                if ap >= 50000:
                    print(f"Bought MacGuffin Muffin at: {datetime.datetime.now()}")
                    Inputs.click(*coords.SELLOUT_MUFFIN_BUY)
                    Navigation.confirm()
            else:
                return
        else:
            return
        Inputs.click(*coords.SELLOUT_MUFFIN_USE)
        print(f"Used MacGuffin Muffin at: {datetime.datetime.now()}")

class Rebirth:
    @staticmethod
    def do_rebirth() -> None:
        """Start a rebirth or challenge."""
        Navigation.menu("fight")
        Inputs.click(*coords.FIGHT_STOP)
        Navigation.rebirth()
        Adventure.current_adventure_zone = 0
        Inputs.click(*coords.REBIRTH)
        Inputs.click(*coords.REBIRTH_BUTTON)
        Inputs.click(*coords.CONFIRM)
        return
    
    @staticmethod
    def check_challenge(getNum :bool =False) -> int:
        """Check if a challenge is active.
        
        Keyword arguments
        getNum. -- If true, return the number of the active challenge.
                   This is slower.
                   If False or omitted, return if a challenge is active.
        """
        Navigation.rebirth()
        Inputs.click(*coords.CHALLENGE_BUTTON)
        time.sleep(userset.LONG_SLEEP)
        active = Inputs.check_pixel_color(*coords.COLOR_CHALLENGE_ACTIVE)
        
        if not active:
            return False
        if not getNum:
            return True
        
        text = Inputs.ocr(*coords.OCR_CHALLENGE_NAME)
        if "basic" in text.lower():
            return 1
        elif "augs" in text.lower():
            return 2
        elif "24 hour" in text.lower():
            return 3
        elif "100 level" in text.lower():
            return 4
        elif "equipment" in text.lower():
            return 5
        elif "troll" in text.lower():
            return 6
        elif "rebirth" in text.lower():
            return 7
        elif "laser" in text.lower():
            return 8
        elif "blind" in text.lower():
            return 9
        elif "ngu" in text.lower():
            return 10
        elif "time machine" in text.lower():
            return 11
        
        else:
            return -1
    
    @staticmethod
    def get_rebirth_time() -> Tuple[int, time.struct_time]:
        """Get the current rebirth time.
        returns a namedtuple(days, timestamp) where days is the number
        of days displayed in the rebirth time text and timestamp is a
        time.struct_time object.
        """
        Rebirth_time = namedtuple('Rebirth_time', 'days timestamp')
        t = Inputs.ocr(*coords.OCR_REBIRTH_TIME)
        x = re.search(r"((?P<days>[0-9]+) days? )?((?P<hours>[0-9]+):)?(?P<minutes>[0-9]+):(?P<seconds>[0-9]+)", t)
        days = 0
        if x is None:
            timestamp = time.strptime("0:0:0", "%H:%M:%S")
        else:
            if x.group('days') is None:
                days = 0
            else:
                days = int(x.group('days'))
            
            if x.group('hours') is None:
                hours = "0"
            else:
                hours = x.group('hours')
            
            if x.group('minutes') is None:
                minutes = "0"
            else:
                minutes = x.group('minutes')
            
            if x.group('seconds') is None:
                seconds = "0"
            else:
                seconds = x.group('seconds')
            timestamp = time.strptime(f"{hours}:{minutes}:{seconds}", "%H:%M:%S")
        return Rebirth_time(days, timestamp)
    
    @staticmethod
    def rt_to_seconds() -> int:
        """Get the Rebirth time in seconds"""
        rt = Rebirth.get_rebirth_time()
        seconds = ((rt.days * 24 + rt.timestamp.tm_hour) * 60 + rt.timestamp.tm_min) * 60 + rt.timestamp.tm_sec
        return seconds

class Misc:
    @staticmethod
    def reclaim_all() -> None:
        """Reclaim all resources from all features."""
        Inputs.send_string("r")
        Inputs.send_string("t")
        Inputs.send_string("f")
    
    @staticmethod
    def reclaim_res(energy :bool =False, magic :bool =False, r3 :bool =False) -> None:
        """Reclaim resources of choosing from all features.
        
        Keyword arguments
        energy -- If True, reclaim energy.
        magic  -- If True, reclaim magic.
        r3     -- If True, reclaim resource 3.
        """
        if energy:
            Inputs.send_string("r")
        if magic:
            Inputs.send_string("t")
        if r3:
            Inputs.send_string("f")
    
    @staticmethod
    def reclaim_bm() -> None:
        """Remove all magic from BM."""
        Navigation.menu("bloodmagic")
        Misc.set_input(coords.INPUT_MAX)
        for coord in coords.BM_RECLAIM:
            Inputs.click(*coord)
   
    @staticmethod
    def reclaim_ngu(magic :bool =False) -> None:
        """Remove all e/m from NGUs."""
        if magic:
            Navigation.ngu_magic()
        else:
            Navigation.menu("ngu")
        Misc.set_input(coords.INPUT_MAX)
        for i in range(1, 10):
            NGU = coords.Pixel(coords.NGU_MINUS.x, coords.NGU_PLUS.y + i * 35)
            Inputs.click(*NGU)
    
    @staticmethod
    def reclaim_tm(energy :bool =True, magic :bool =False) -> None:
        """Remove all e/m from TM.
        
        Keyword arguments
        energy -- If True, reclaim energy from TM.
        magic  -- If True, reclaim magic from TM.
        """
        Navigation.menu("timemachine")
        Misc.set_input(coords.INPUT_MAX)
        if magic:
            Inputs.click(*coords.TM_MULT_MINUS)
        if energy:
            Inputs.click(*coords.TM_SPEED_MINUS)
    
    @staticmethod
    def reclaim_aug() -> None:
        """Remove all energy from augs"""
        Navigation.menu("augmentations")
        Misc.set_input(coords.INPUT_MAX)
        Inputs.click(*coords.AUG_SCROLL_TOP)
        scroll_down = False
        for i, k in enumerate(coords.AUGMENT.keys()):
            if i >= 10 and not scroll_down:
                Inputs.click(*coords.AUG_SCROLL_BOT)
                Inputs.click(*coords.AUG_SCROLL_BOT)
                time.sleep(1)
                scroll_down = True
            Inputs.click(coords.AUG_MINUS_X, coords.AUGMENT[k].y)
    
    @staticmethod
    def save_check() -> None:
        """Check if we can do the daily save for AP.
        Make sure no window in your browser pops up when you click the "Save"
        button, otherwise sit will mess with the rest of the script.
        """
        if Inputs.check_pixel_color(*coords.IS_SAVE_READY):
            Inputs.click(*coords.SAVE)
        return
    
    # crops the misc breakdown image, cutting off empty space on the right
    @staticmethod
    def __cutoff_right(bmp) -> PILImage:
        first_pix = bmp.getpixel((0, 0))
        width, height = bmp.size
        
        count = 0
        for x in range(8, width):
            dif = False
            for y in range(0, height):
                if not Inputs.rgb_equal(first_pix, bmp.getpixel((x, y))):
                    dif = True
                    break
            
            if dif: count = 0
            else:
                count += 1
                if count > 8:
                    return bmp.crop((0, 0, x , height))
        
        return bmp
    
    # splits the three parts of the resource breakdown (pow, bars, cap)
    @staticmethod
    def __split_breakdown(bmp) -> List[PILImage]:
        first_pix = bmp.getpixel((0, 0))
        width, height = bmp.size
        y1 = 1
        offset_x = coords.OCR_BREAKDOWN_NUM[0] - coords.OCR_BREAKDOWN_COLONS[0]
        
        slices = []
        for _ in range(0, 3):
            for y in range(y1, height):
                if not Inputs.rgb_equal(first_pix, bmp.getpixel((0, y))):
                    y0 = y
                    break
            
            for y in range(y0, height, coords.BREAKDOWN_OFFSET_Y):
                if Inputs.rgb_equal(first_pix, bmp.getpixel((0, y))):
                    y1 = y
                    break
            
            slice = bmp.crop((offset_x, y0 - 8, width, y1))
            slices.append(Misc.__cutoff_right(slice))
        
        return slices
    
    # Goes to stats breakdown, makes a screenshot
    # Gets it split into three containing all the numbers by calling __split_breakdown
    # Sends all thre images to OCR
    # Returns a list of lists of the numbers from stats breakdown
    @staticmethod
    def __get_res_breakdown(resource, ocrDebug=False, bmp=None, debug=False) -> List[List[str]]:
        Navigation.stat_breakdown()
        
        if   resource == 1: Inputs.click(*coords.BREAKDOWN_E)
        elif resource == 2: Inputs.click(*coords.BREAKDOWN_M)
        elif resource == 3: Inputs.click(*coords.BREAKDOWN_R)
        else : raise RuntimeError("Invalid resource")
        
        if bmp is None:
            bmp = Inputs.get_cropped_bitmap(*Window.gameCoords(*coords.OCR_BREAKDOWN_COLONS))
        if debug: bmp.show()

        imgs = Misc.__split_breakdown(bmp)
        
        ress = []
        for img in imgs:
            if debug: img.show()
            s = Inputs.ocr(0, 0, 0, 0, bmp=img, debug=ocrDebug, binf=220, sliced=True)
            s = s.splitlines()
            s2 = [x for x in s if x != ""]  # remove empty lines
            ress.append(s2)
        
        return ress
    
    # Gets the numbers on stats breakdown for the resource and value passed
    # val = 0 for power, 1 for bars and 2 for cap
    @staticmethod
    def __get_res_val(resource, val) -> int:
        s = Misc.__get_res_breakdown(resource)[val][-1]
        return Inputs.get_numbers(s)[0]
    
    @staticmethod
    def get_pow(resource :int) -> int:
        """Get the power for energy, magic, or resource 3.
        
        Keyword arguments
        resource -- The resource to get power for. 1 for energy, 2 for magic and 3 for r3.
        """
        return Misc.__get_res_val(resource, 0)
    
    @staticmethod
    def get_bars(resource :int) -> int:
        """Get the bars for energy, magic, or resource 3.
        
        Keyword arguments
        resource -- The resource to get bars for. 1 for energy, 2 for magic and 3 for r3.
        """
        return Misc.__get_res_val(resource, 1)
    
    @staticmethod
    def get_cap(resource :int) -> int:
        """Get the cap for energy, magic, or resource 3.
        
        Keyword arguments
        resource -- The resource to get cap for. 1 for energy, 2 for magic and 3 for r3.
        """
        return Misc.__get_res_val(resource, 2)
    
    @staticmethod
    def get_idle_cap(resource :int) -> int:
        """Get the available idle energy, magic, or resource 3.
        
        Keyword arguments
        resource -- The resource to get idle cap for. 1 for energy, 2 for magic and 3 for r3.
        """
        try:  # The sliced argument was meant for low values with get_pow/bars/cap
            # But also serves for low idle caps
            if   resource == 1: res = Inputs.ocr(*coords.OCR_ENERGY, sliced=True)
            elif resource == 2: res = Inputs.ocr(*coords.OCR_MAGIC , sliced=True)
            elif resource == 3: res = Inputs.ocr(*coords.OCR_R3    , sliced=True)
            else : raise RuntimeError("Invalid resource")
            
            res = Inputs.get_numbers(res)[0]
            return res
            
        except IndexError:
            print("couldn't get idle cap")
            return 0

    @staticmethod
    def set_input(value :int) -> None:
        """Sets a value in the input box.
        Requires the current menu to have an imput box.
        
        Keyword arguments
        value -- The value to be set
        """
        Navigation.input_box()
        Inputs.send_string(value)
        Misc.waste_click()
    
    @staticmethod
    def waste_click() -> None:
        """Make a click that does nothing"""
        Inputs.click(*coords.WASTE_CLICK)
        time.sleep(userset.FAST_SLEEP)
