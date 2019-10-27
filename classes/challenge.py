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
    def start_challenge(challenge : int) -> None:
        """Start the selected challenge.
        
        Keyword arguments
        challenge -- The index of the challenge, starting at 1 for Basic challenge,
                     ending at 11 for No TM challenge
        """

        BloodMagic.toggle_auto_spells(drop=False)
        Navigation.rebirth()
        Inputs.click(*coords.CHALLENGE_BUTTON)

        chall = Rebirth.check_challenge(getNum=True)
        if chall:
            text = Inputs.ocr(*coords.OCR_CHALLENGE_NAME)
            print("A challenge is already active: " + text)
            if "basic" in text.lower():
                print("Starting basic challenge script")
                Challenge.basic()

            elif "24 hour" in text.lower():
                print("Starting 24 hour challenge script")
                try:
                    x = coords.CHALLENGE.x
                    y = coords.CHALLENGE.y + challenge * coords.CHALLENGEOFFSET
                    Inputs.click(x, y, button="right")
                    time.sleep(userset.LONG_SLEEP)
                    target = Inputs.ocr(*coords.OCR_CHALLENGE_24HC_TARGET)
                    target = int(Inputs.remove_letters(target))
                    print(f"Found target boss: {target}")
                    Challenge.basic()
                except ValueError:
                    print("Couldn't detect the target level of 24HC")
                    Discord.send_message("Couldn't detect the" +
                                         " target level of 24HC", Discord.ERROR)

            elif "100 level" in text.lower():
                print("Starting 100 level challenge script")
                print("IMPORTANT")
                print("Set target level for energy buster to 67 and charge shot to 33.")
                print("Disable 'Advance Energy' in Augmentation")
                print("Disable beards if you cap ultra fast.")
                Challenge.level()

            elif "blind" in text.lower():
                print("Starting blind challenge script")
                Challenge.blind()

            elif "laser" in text.lower():
                print("Starting laser sword challenge script")
                Challenge.laser()

            elif "rebirth" in text.lower():
                print("Starting no rebirth challenge script")
                Challenge.rebirth()
            elif "augs" in text.lower():
                print("Starting no augs challenge script")
                Challenge.augment()
            elif "equipment" in text.lower():
                print("Starting no equipment challenge script")
                Challenge.equipment()
            elif "time machine" in text.lower():
                print("Starting no time machine challenge script")
                Challenge.timemachine()
            elif "ngu" in text.lower():
                print("Starting no NGU challenge script")
                Challenge.ngu()
            else:
                print("Couldn't determine which script to start from the OCR",
                      "input")

        else:
            x = coords.CHALLENGE.x
            y = coords.CHALLENGE.y + challenge * coords.CHALLENGEOFFSET

            if challenge == 1:
                Inputs.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                Navigation.confirm()
                Challenge.basic()

            elif challenge == 2:
                Inputs.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                Navigation.confirm()
                Challenge.augment()

            elif challenge == 3:
                try:
                    Inputs.click(x, y, button="right")
                    time.sleep(userset.LONG_SLEEP)
                    target = Inputs.ocr(*coords.OCR_CHALLENGE_24HC_TARGET)
                    target = int(Inputs.remove_letters(target))
                    print(f"Found target boss: {target}")
                    Inputs.click(x, y)
                    time.sleep(userset.LONG_SLEEP)
                    Navigation.confirm()
                    time.sleep(userset.LONG_SLEEP)
                    Challenge.basic()
                except ValueError:
                    print("couldn't detect the target level of 24HC")
                    Discord.send_message("Couldn't detect the" +
                                         "target level of 24HC", Discord.ERROR)

            elif challenge == 4:
                print("IMPORTANT")
                print("Set target Level for energy buster to 67 and charge shot to 33.")
                print("Disable 'Advance Energy' in Augmentation")
                print("Disable beards if you cap ultra fast.")
                Inputs.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                Navigation.confirm()
                Challenge.level()

            elif challenge == 5:
                Inputs.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                Navigation.confirm()
                Challenge.equipment()

            elif challenge == 6:
                print("Nah fam. Do it yourself")
                while True: Window.shake()
            
            elif challenge == 7:
                Inputs.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                Navigation.confirm()
                Challenge.rebirth()

            elif challenge == 8:
                print("LSC doesn't reset your number, make sure your number is high enough to make laser swords.")
                Inputs.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                Navigation.confirm()
                Challenge.laser()

            elif challenge == 9:
                print("Starting blind challenge")
                Inputs.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                Navigation.confirm()
                Challenge.blind()

            elif challenge == 10:
                Inputs.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                Navigation.confirm()
                Challenge.ngu()

            elif challenge == 11:
                Inputs.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                Navigation.confirm()
                Challenge.timemachine()

            else:
                print(f"invalid challenge: {challenge}")
