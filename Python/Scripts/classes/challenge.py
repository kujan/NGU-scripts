"""Handles different challenges"""
from classes.features import Features
from classes.discord import Discord
from challenges.basic import Basic
from challenges.level import Level
from challenges.laser import Laser
from challenges.rebirth import Rebirth
import ngucon as ncon
import usersettings as userset
import time


class Challenge(Features):
    """Handles different challenges."""

    def start_challenge(self, challenge):
        """Start the selected challenge."""
        self.rebirth()
        self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)

        b = Basic()
        level = Level()
        laser = Laser()
        rebirth = Rebirth()

        color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
                                     ncon.CHALLENGEACTIVEY)

        if color == ncon.CHALLENGEACTIVECOLOR:
            text = self.ocr(ncon.OCR_CHALLENGE_NAMEX1,
                            ncon.OCR_CHALLENGE_NAMEY1,
                            ncon.OCR_CHALLENGE_NAMEX2,
                            ncon.OCR_CHALLENGE_NAMEY2)
            print("A challenge is already active: " + text)
            if "basic" in text.lower():
                print("Starting basic challenge script")
                b.basic()

            elif "24 hour" in text.lower():
                print("Starting 24 hour challenge script")
                try:
                    x = ncon.CHALLENGEX
                    y = ncon.CHALLENGEY + challenge * ncon.CHALLENGEOFFSET
                    self.click(x, y, button="right")
                    time.sleep(userset.LONG_SLEEP)
                    target = self.ocr(ncon.OCR_CHALLENGE_24HC_TARGETX1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETX2,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY2)
                    target = int(self.remove_letters(target))
                    print(f"Found target boss: {target}")
                    b.basic(target)
                except ValueError:
                    print("couldn't detect the target level of 24HC")
                    Discord.send_message("Couldn't detect the" +
                                         " target level of 24HC", Discord.ERROR)

            elif "100 level" in text.lower():
                print("starting 100 level challenge script")
                level.lc()

            elif "blind" in text.lower():
                print("starting blind challenge script")
                level.blind()

            elif "laser" in text.lower():
                print("starting laser sword challenge script")
                laser.laser()

            elif "rebirth" in text.lower():
                print("starting no rebirth challenge script")
                rebirth.rebirth_challenge()
            else:
                print("Couldn't determine which script to start from the OCR",
                      "input")
            #  TODO: add other challenges here

        else:
            x = ncon.CHALLENGEX
            y = ncon.CHALLENGEY + challenge * ncon.CHALLENGEOFFSET

            if challenge == 1:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                b.basic(58)

            elif challenge == 3:
                try:
                    self.click(x, y, button="right")
                    time.sleep(userset.LONG_SLEEP)
                    target = self.ocr(ncon.OCR_CHALLENGE_24HC_TARGETX1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETX2,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY2)
                    target = int(self.remove_letters(target))
                    print(f"Found target boss: {target}")
                    self.click(x, y)
                    time.sleep(userset.LONG_SLEEP)
                    self.confirm()
                    time.sleep(userset.LONG_SLEEP)
                    b.basic(target)
                except ValueError:
                    print("couldn't detect the target level of 24HC")
                    Discord.send_message("Couldn't detect the" +
                                         "target level of 24HC", Discord.ERROR)

            elif challenge == 4:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                level.lc()

            elif challenge == 7:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                rebirth.rebirth_challenge()

            elif challenge == 8:
                self.click(x, y)
                time.sleep(userset.LONG_SLEEP)
                self.confirm()
                laser.laser()


    def check_challenge(self):
        """Check if a challenge is active."""
        self.rebirth()
        self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
        time.sleep(userset.LONG_SLEEP)
        color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
                                     ncon.CHALLENGEACTIVEY)

        return True if color == ncon.CHALLENGEACTIVECOLOR else False
