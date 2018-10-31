"""Handles different challenges"""
from classes.features import Features
import ngucon as ncon
import time


class Challenge(Features):
    """Handles different challenges."""

    def start_challenge(self, challenge):
        """Start the selected challenge."""
        self.rebirth()
        self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
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
                self.basic()

            elif "24 hour" in text.lower():
                print("Starting 24 hour challenge script")
                try:
                    x = ncon.CHALLENGEX
                    y = ncon.CHALLENGEY + challenge * ncon.CHALLENGEOFFSET
                    self.click(x, y, button="right")
                    time.sleep(0.3)
                    target = self.ocr(ncon.OCR_CHALLENGE_24HC_TARGETX1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETX2,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY2)
                    target = int(self.remove_letters(target))
                    print(f"Found target boss: {target}")
                    self.basic(target)
                except ValueError:
                    print("couldn't detect the target level of 24HC")

            elif "100 level" in text.lower():
                print("starting 100 level challenge script")
                self.lc()

            else:
                print("Couldn't determine which script to start from the OCR",
                      "input")
            #  TODO: add other challenges here

        else:
            x = ncon.CHALLENGEX
            y = ncon.CHALLENGEY + challenge * ncon.CHALLENGEOFFSET

            if challenge == 1:
                self.click(x, y)
                time.sleep(0.3)
                self.confirm()
                self.basic(58)

            elif challenge == 3:
                try:
                    self.click(x, y, button="right")
                    time.sleep(0.3)
                    target = self.ocr(ncon.OCR_CHALLENGE_24HC_TARGETX1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY1,
                                      ncon.OCR_CHALLENGE_24HC_TARGETX2,
                                      ncon.OCR_CHALLENGE_24HC_TARGETY2)
                    target = int(self.remove_letters(target))
                    print(f"Found target boss: {target}")
                    self.click(x, y)
                    time.sleep(0.3)
                    self.confirm()
                    time.sleep(0.3)
                    self.basic(target)
                except ValueError:
                    print("couldn't detect the target level of 24HC")

            elif challenge == 4:
                self.click(x, y)
                time.sleep(0.3)
                self.confirm()
                self.lc()

    def check_challenge(self):
        """Check if a challenge is active."""
        self.rebirth()
        self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
        time.sleep(0.3)
        color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
                                     ncon.CHALLENGEACTIVEY)

        return True if color == ncon.CHALLENGEACTIVECOLOR else False
