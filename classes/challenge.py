"""Handles different challenges"""

from classes.features   import BloodMagic, Rebirth
from classes.navigation import Navigation
from classes.inputs     import Inputs
from classes.discord    import Discord
from classes.window     import Window

import coordinates  as coords
import usersettings as userset
import time
from typing import List


class cInfo:
    def __init__(self, name = "", script = None, extra = []):
        self.name = name
        self.script = script
        self.extra = extra

def init(ChList):
    from .challenges.augment     import augment
    from .challenges.basic       import basic
    from .challenges.blind       import blind
    from .challenges.equipment   import equipment
    from .challenges.laser       import laser
    from .challenges.level       import level
    from .challenges.ngu         import ngu
    from .challenges.rebirth     import rebirth
    from .challenges.timemachine import timemachine

    def get24boss():
        try:
            x = coords.CHALLENGE.x
            y = coords.CHALLENGE.y + 3 * coords.CHALLENGEOFFSET
            
            Navigation.challenges()
            Inputs.click(x, y, button="right")
            time.sleep(userset.LONG_SLEEP)
            target = Inputs.ocr(*coords.OCR_CHALLENGE_24HC_TARGET)
            target = Inputs.get_numbers(target)[0]
            return f"Target boss: {target}"
        except ValueError:
            Discord.send_message("Couldn't detect the target level of 24HC", Discord.ERROR)
            return "Couldn't detect the target level of 24HC"

    ChList.append(cInfo("Basic", basic))
    ChList.append(cInfo("No Augments", augment))
    ChList.append(cInfo("24h", basic, [get24boss]))
    ChList.append(cInfo("100 Level", level, [
        "IMPORTANT",
        "Set target level for energy buster to 67 and charge shot to 33.",
        "Disable 'Advance Energy' in Augmentation",
        "Disable beards if you cap ultra fast."
    ]))
    ChList.append(cInfo("No Equipment", equipment))
    ChList.append(cInfo("Troll", Window.shake, ["Do it yourself, fam."]))
    ChList.append(cInfo("No Rebirth", rebirth))
    ChList.append(cInfo("Laser Sword", laser, [
        "LSC doesn't reset your number, make sure your number is high enough to make laser swords."
    ]))
    ChList.append(cInfo("Blind", blind))
    ChList.append(cInfo("No NGU", ngu))
    ChList.append(cInfo("No Time Machine", timemachine))
    
ChList = []
init(ChList)
   
class Challenge:
    """Handles different challenges."""
    
    @staticmethod
    def run_challenge(challenge :int, cont :bool =False) -> None:        
        """Run the selected challenge.
        
        Keyword arguments
        challenge -- The index of the challenge, starting at 1 for Basic challenge,
                     ending at 11 for No TM challenge
        cont      -- Whether the challenge is already running.
        """
        global ChList
        Navigation.challenges()
        
        if cont: pass
        else:
            x = coords.CHALLENGE.x
            y = coords.CHALLENGE.y + challenge * coords.CHALLENGEOFFSET
            Inputs.click(x, y)
            time.sleep(userset.LONG_SLEEP)
            Navigation.confirm()
        
        chall = ChList[challenge-1]
        print(f"Starting {chall.name} Challenge script.")
        for x in chall.extra:
            if callable(x): print(x())
            else: print(x)
        chall.script()
    
    @staticmethod
    def start_challenge(challenge :int, quitCurrent :bool =False) -> None:
        """Start the selected challenge. Checks for currently running challenges.
        
        Keyword arguments
        challenge   -- The index of the challenge, starting at 1 for Basic challenge,
                       ending at 11 for No TM challenge
        quitCurrent -- Quit the current challenge if it is different to the desired.
        """
        BloodMagic.toggle_auto_spells(drop=False)
        
        chall = Rebirth.check_challenge(getNum=True)
        if chall and chall != challenge:
            print(f"A challenge is currently running ({chall}).")
            if quitCurrent:
                print("Quitting current challenge.")
                Navigation.challenge_quit()
            else: Challenge.run_challenge(chall, cont=True)

        Challenge.run_challenge(challenge)
    
    @staticmethod
    def list() -> List[str]:
        """Return the list of challenge names with their corresponding number.
        """
        global ChList
        
        l = []
        for i in range(len(ChList)):
            if i < 9: l.append(f"{i+1}  {ChList[i].name}")
            else:     l.append(f"{i+1} {ChList[i].name}")
        return l
    
