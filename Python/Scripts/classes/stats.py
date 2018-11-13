"""Handles various statistics."""
from classes.navigation import Navigation
from classes.discord import Discord

import ngucon as ncon
import re
import time


class Stats(Navigation):
    """Handles various statistics."""

    def __init__(self):
        """Store start EXP via OCR."""
        super().__init__()
        self.misc()
        try:
            self.start_exp = int(float(self.ocr(ncon.OCR_EXPX1,
                                                ncon.OCR_EXPY1,
                                                ncon.OCR_EXPX2,
                                                ncon.OCR_EXPY2)))
        except ValueError:
            message = "OCR couldn't detect starting XP, defaulting to 0."
            print(message)
            Discord.send_message(message, Discord.ERROR)
            self.start_exp = 0
        self.start_time = time.time()
        self.rebirth = 1

    def print_exp(self):
        """Print current exp stats."""
        self.misc()
        current_time = time.time()
        try:
            current_exp = int(float(re.sub(',', '', self.ocr(ncon.OCR_EXPX1,
                                                             ncon.OCR_EXPY1,
                                                             ncon.OCR_EXPX2,
                                                             ncon.OCR_EXPY2))))
        except ValueError:
            print("OCR couldn't detect current XP.")
            Discord.send_message("OCR couldn't detect current XP",
                                 Discord.ERROR)
            return
        per_hour = (current_exp - self.start_exp)//((current_time -
                                                     self.start_time) / 3600)
        message = (f'Rebirth #{self.rebirth}\nStart exp: {self.start_exp}\n'
                   f'Current exp: {current_exp}\nPer hour: {per_hour}\n')

        print(message)
        Discord.send_message(message, Discord.INFO)
        self.rebirth += 1
