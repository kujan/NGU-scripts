"""Handles different challenges"""

from classes.features   import BloodMagic, Rebirth
from classes.navigation import Navigation
from classes.inputs     import Inputs
from classes.discord    import Discord
from classes.window     import Window

import coordinates  as coords
import usersettings as userset
import time


class Challenge:
    """Handles different challenges."""

    from .challenges.augment     import augment
    from .challenges.basic       import basic
    from .challenges.blind       import blind
    from .challenges.equipment   import equipment
    from .challenges.laser       import laser
    from .challenges.level       import level
    from .challenges.ngu         import ngu
    from .challenges.rebirth     import rebirth
    from .challenges.timemachine import timemachine

    @staticmethod
    def run_challenge(challenge :int, cont :bool =False) -> None:
        """Run the selected challenge.
        
        Keyword arguments
        challenge -- The index of the challenge, starting at 1 for Basic challenge,
                     ending at 11 for No TM challenge
        cont      -- Whether the challenge is already running.
        """
        x = coords.CHALLENGE.x
        y = coords.CHALLENGE.y + challenge * coords.CHALLENGEOFFSET
        post_msg = []

        if   challenge ==  1: # Basic
            cname = "Basic"
            run_script = Challenge.basic

        elif challenge ==  2: # No Augments
            cname = "No Augments"
            run_script = Challenge.augment

        elif challenge ==  3: # 24 h
            cname = "24h"
            try:
                Inputs.click(x, y, button="right")
                time.sleep(userset.LONG_SLEEP)
                target = Inputs.ocr(*coords.OCR_CHALLENGE_24HC_TARGET)
                target = Inputs.get_numbers(target)[0]
                post_msg.append(f"Found target boss: {target}")
                run_script = Challenge.basic

            except ValueError:
                print("Couldn't detect the target level of 24HC")
                Discord.send_message("Couldn't detect the target level of 24HC", Discord.ERROR)
                return

        elif challenge ==  4: # 100 lvl
            cname = "100 Level"
            post_msg.append("IMPORTANT")
            post_msg.append("Set target level for energy buster to 67 and charge shot to 33.")
            post_msg.append("Disable 'Advance Energy' in Augmentation")
            post_msg.append("Disable beards if you cap ultra fast.")
            run_script = Challenge.level

        elif challenge ==  5: # No Equipment
            cname = "No Equipment"
            run_script = Challenge.equipment

        elif challenge ==  6: # TROLL
            # cname = "The Troll"
            print("Troll Challenge, really?")
            print("Nah fam. Do it yourself")
            Window.shake()
            return

        elif challenge ==  7: # No Rebirth
            cname = "No Rebirth"
            run_script = Challenge.rebirth

        elif challenge ==  8: # Laser
            cname = "Laser Sword"
            post_msg.append("LSC doesn't reset your number, make sure your number is high enough to make laser swords.")
            run_script = Challenge.laser

        elif challenge ==  9: # Blind
            cname = "Blind"
            run_script = Challenge.blind

        elif challenge == 10: # No NGU
            cname = "No NGU"
            run_script = Challenge.ngu

        elif challenge == 11: # No TM
            cname = "No TM"
            run_script = Challenge.timemachine

        else: # Wrong Challenge
            print(f"Challenge {challenge} doesn't exist.")
            return

        if cont: pass
        else:
            Inputs.click(x, y)
            time.sleep(userset.LONG_SLEEP)
            Navigation.confirm()

        print(f"Starting {cname} Challenge script.")
        if post_msg != []:
            print(*post_msg)

        run_script()

    @staticmethod
    def start_challenge(challenge :int, quitCurrent :bool =False) -> None:
        """Start the selected challenge. Checks for currently running challenges.
        
        Keyword arguments
        challenge   -- The index of the challenge, starting at 1 for Basic challenge,
                       ending at 11 for No TM challenge
        quitCurrent -- Quit the current challenge if it is different to the desired.
        """
        BloodMagic.toggle_auto_spells(drop=False)
        Navigation.challenges()

        chall = Rebirth.check_challenge(getNum=True)
        if chall and chall != challenge:
            print(f"A challenge is currently running ({chall}).")
            if quitCurrent:
                print("Quitting current challenge.")
                Navigation.challenge_quit()
            else: Challenge.run_challenge(chall, cont=True)

        Challenge.run_challenge(challenge)
