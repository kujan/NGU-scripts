"""Handles different challenges"""
from classes.features import Features
from classes.discord import Discord
from classes.window import Window
from challenges.augment import Augment
from challenges.basic import Basic
from challenges.equipment import Equipment
from challenges.level import Level
from challenges.laser import Laser
from challenges.ngu import Ngu
from challenges.rebirth import Rebirth
from challenges.timemachine import Timemachine
import coordinates as coords
import usersettings as userset
import time
import win32api
import win32con as wcon
import win32gui

class Challenge(Features):
    """Handles different challenges."""

    def start_challenge(self, challenge):
        """Start the selected challenge."""
        
        self.toggle_auto_spells(drop=False)
        self.rebirth()
        self.click(*coords.CHALLENGE_BUTTON)

        basic = Basic()
        level = Level()
        laser = Laser()
        rebirth = Rebirth()
        augment = Augment()
        equipment = Equipment()
        timemachine = Timemachine()
        ngu = Ngu()
        if self.check_pixel_color(*coords.COLOR_CHALLENGE_ACTIVE):
            text = self.ocr(*coords.OCR_CHALLENGE_NAME)
            print("A challenge is already active: " + text)
            if "basic" in text.lower():
                print("Starting basic challenge script")
                basic.start()

            elif "24 hour" in text.lower():
                print("Starting 24 hour challenge script")
                try:
                    x = coords.CHALLENGE.x
                    y = coords.CHALLENGE.y + challenge * coords.CHALLENGEOFFSET
                    self.click(x, y, button="right")
                    time.sleep(userset.LONG_SLEEP)
                    target = self.ocr(*coords.OCR_CHALLENGE_24HC_TARGET)
                    target = int(self.remove_letters(target))
                    print(f"Found target boss: {target}")
                    basic.start()
                except ValueError:
                    print("couldn't detect the target level of 24HC")
                    Discord.send_message("Couldn't detect the" +
                                         " target level of 24HC", Discord.ERROR)

            elif "100 level" in text.lower():
                print("starting 100 level challenge script")
                print("IMPORTANT")
                print("Set target level for energy buster to 67 and charge shot to 33.")
                print("Disable 'Advance Energy'' in augments")
                print("Disable beards if you cap ultra fast.")
                level.start()

            elif "blind" in text.lower():
                print("blind challenge is not supported")

            elif "laser" in text.lower():
                print("starting laser sword challenge script")
                laser.start()

            elif "rebirth" in text.lower():
                print("starting no rebirth challenge script")
                rebirth.rebirth_challenge()
            elif "augs" in text.lower():
                print("starting no augs challenge script")
                augment.start()
            elif "equipment" in text.lower():
                print("starting no equipment challenge script")
                equipment.start()
            elif "time machine" in text.lower():
                print("starting no time machine challenge script")
                timemachine.start()
            elif "ngu" in text.lower():
                print("starting no NGU challenge script")
                ngu.start()
            else:
                print("Couldn't determine which script to start from the OCR",
                      "input")
            #  TODO: add other challenges here

        else:
            x = coords.CHALLENGE.x
            y = coords.CHALLENGE.y + challenge * coords.CHALLENGEOFFSET

            if challenge == 1:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                basic.start()

            elif challenge == 2:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                augment.start()

            elif challenge == 3:
                try:
                    self.click(x, y, button="right")
                    time.sleep(userset.LONG_SLEEP)
                    target = self.ocr(*coords.OCR_CHALLENGE_24HC_TARGET)
                    target = int(self.remove_letters(target))
                    print(f"Found target boss: {target}")
                    self.click(x, y)
                    time.sleep(userset.LONG_SLEEP)
                    self.confirm()
                    time.sleep(userset.LONG_SLEEP)
                    basic.start()
                except ValueError:
                    print("couldn't detect the target level of 24HC")
                    Discord.send_message("Couldn't detect the" +
                                         "target level of 24HC", Discord.ERROR)

            elif challenge == 4:
                print("IMPORTANT")
                print("Set target level for energy buster to 67 and charge shot to 33.")
                print("Disable 'Advance Energy'' in augments")
                print("Disable beards if you cap ultra fast.")
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                level.lc()

            elif challenge == 5:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                equipment.start()

            elif challenge == 6:
                print("Nah fam. Do it yourself")
                while True:
                    for x in range(1000):
                        win32gui.MoveWindow(Window.id, x, 0, 1000, 800, False)
                    for y in range(1000):
                        win32gui.MoveWindow(Window.id, 1000, y, 1000, 800, False)
                    for x in reversed(range(1000)):
                        win32gui.MoveWindow(Window.id, x, 1000, 1000, 800, False)
                    for y in reversed(range(1000)):
                        win32gui.MoveWindow(Window.id, 0, y, 1000, 800, False)

            elif challenge == 7:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                rebirth.rebirth_challenge()

            elif challenge == 8:
                print("LSC doesn't reset your number, make sure your number is high enough to make laser swords.")
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                laser.start()

            elif challenge == 9:
                print("Blind challenge is not supported")

            elif challenge == 10:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                ngu.start()

            elif challenge == 11:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                timemachine.start()

            else:
                print(f"invalid challenge: {challenge}")
