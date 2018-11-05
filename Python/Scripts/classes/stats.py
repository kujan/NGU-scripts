"""Handles various statistics."""
from classes.navigation import Navigation

import ngucon as ncon
import re
import time


class Stats(Navigation):
    """Handles various statistics."""

    def __init__(self):
        """Store start EXP via OCR."""
        self.misc()
        try:
            self.start_exp = int(float(self.ocr(ncon.OCR_EXPX1,
                                                ncon.OCR_EXPY1,
                                                ncon.OCR_EXPX2,
                                                ncon.OCR_EXPY2)))
        except ValueError:
            print("OCR couldn't detect starting XP, defaulting to 0.")
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
            return
        per_hour = (current_exp - self.start_exp)//((current_time -
                                                     self.start_time) / 3600)
        print(f'Rebirth #{self.rebirth}\nStart exp: {self.start_exp}\nCurrent '
              f'exp: {current_exp}\nPer hour: {per_hour}\n')
        self.rebirth += 1
