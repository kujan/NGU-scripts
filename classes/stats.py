"""Handles various statistics."""
from __future__ import annotations # With the help of the broken time machine
from typing import Tuple

import datetime
import time

import coordinates  as coords
import usersettings as userset

from classes.helper     import Helper
from classes.navigation import Navigation
from classes.inputs     import Inputs
from classes.features   import Misc


class Stats:
    """Handles various statistics."""

    total_xp = 0
    xp = 0
    pp = 0
    start_time = time.time()
    OCR_failures = 0
    OCR_failed = False
    track_xp = True
    track_pp = True
    
    @staticmethod
    def set_value_with_ocr(value :str) -> None:
        """Store start EXP via OCR."""
        try:
            if value == "TOTAL XP":
                Navigation.misc()
                Stats.total_xp = Inputs.ocr_notation(*coords.OCR_TOTAL_EXP)
                # print("OCR Captured TOTAL XP: {:,}".format(Stats.total_xp))
            elif value == "XP":
                Navigation.exp()
                Stats.xp = Inputs.ocr_number(*coords.OCR_EXP)
                # print("OCR Captured Current XP: {:,}".format(Stats.xp))
            elif value == "PP":
                Navigation.perks()
                Misc.waste_click()
                Stats.pp = Inputs.ocr_number(*coords.OCR_PP)
                # print("OCR Captured Current PP: {:,}".format(Stats.pp))
            Stats.OCR_failed = False
            Stats.OCR_failures = 0
        except ValueError:
            Stats.OCR_failures += 1
            if Stats.OCR_failures <= 3:
                print("OCR couldn't detect {}, retrying.".format(value))
                if Stats.OCR_failures >= 2:
                    print("Clearing Navigation.current_menu")
                    Navigation.current_menu = ""
                Stats.set_value_with_ocr(value)
            else:
                print("Something went wrong with the OCR")
                Stats.OCR_failures = 0
                Stats.OCR_failed = True

class EstimateRate:

    def __init__(self :EstimateRate, duration :int, mode :str ='moving_average') -> None:
        self.mode = mode
        self.last_timestamp = time.time()
        if Stats.track_xp:
            Stats.set_value_with_ocr("XP")
        self.last_xp = Stats.xp
        if Stats.track_pp:
            Stats.set_value_with_ocr("PP")
        self.last_pp = Stats.pp
        # Differential time log and value
        self.dtime_log = []
        self.dxp_log = []
        self.dpp_log = []
        # Num runs to keep for moving average
        self.__keep_runs = userset.E_RATE_KEEP_RUNS // duration
        self.__iteration = 0
        self.__elapsed = 0
        self.__alg = {
            'moving_average': self.__moving_average,
            'average': self.__average
        }

    def __average(self :EstimateRate) -> Tuple[float, float]:
        """Returns the average rates"""
        avg_xp = sum(self.dxp_log) / sum(self.dtime_log)
        avg_pp = sum(self.dpp_log) / sum(self.dtime_log)
        return avg_xp, avg_pp

    def __moving_average(self :EstimateRate) -> Tuple[float, float]:
        """Returns the moving average rates"""
        if len(self.dtime_log) > self.__keep_runs:
            self.dtime_log.pop(0)
            if Stats.track_xp:
                self.dxp_log.pop(0)
            if Stats.track_pp:
                self.dpp_log.pop(0)
        avg_xp = sum(self.dxp_log) / sum(self.dtime_log)
        avg_pp = sum(self.dpp_log) / sum(self.dtime_log)
        return avg_xp, avg_pp

    def rates(self :EstimateRate) -> Tuple[float, float]:
        try:
            xpr, ppr = self.__alg[self.mode]()
            return round(3600 * xpr), round(3600 * ppr)
        except ZeroDivisionError:
            return 0, 0

    def stop_watch(self :EstimateRate) -> None:
        """This method needs to be called for rate estimations"""
        self.__iteration += 1
        if Stats.track_xp:
            Stats.set_value_with_ocr("XP")
            if not Stats.OCR_failed:
                cxp = Stats.xp
                dxp = cxp - self.last_xp
                self.dxp_log.append(dxp)
                self.last_xp = cxp
            else:
                print("Problems with OCR, skipping stats for this run")
                self.last_timestamp = time.time()
                return
        if Stats.track_pp:
            Stats.set_value_with_ocr("PP")
            if not Stats.OCR_failed:
                cpp = Stats.pp
                dpp = cpp - self.last_pp
                self.dpp_log.append(dpp)
                self.last_pp = cpp
            else:
                print("Problems with OCR, skipping stats for this run")
                self.last_timestamp = time.time()
                return
        dtime = time.time() - self.last_timestamp
        self.dtime_log.append(dtime)
        self.last_timestamp = time.time()
        print("This run: {:^8}{:^3}This run: {:^8}".format(Helper.human_format(dxp), "|", Helper.human_format(dpp)))

    def update_xp(self :EstimateRate) -> None:
        """This method is used to update last xp after upgrade spends"""
        self.last_xp = Stats.xp

class Tracker:
    """
    The Tracker object collects time and value measurements for stats

    Usage: Initialize the class by calling tracker = Tracker(duration),
           then at the end of each run invoke tracker.progress() to update stats.
    """

    def __init__(
        self :Tracker,
        duration :int,
        track_xp :bool =True,
        track_pp :bool =True,
        mode :str ='moving_average') -> None:
        
        self.__start_time = time.time()
        self.__iteration = 1
        Stats.track_xp = track_xp
        Stats.track_pp = track_pp
        self.__estimaterate = EstimateRate(duration, mode)
        # print(f"{'-' * 15} Run # {self.__iteration} {'-' * 15}")
        print("{0:{fill}{align}40}".format(f" {self.__iteration} ", fill="-", align="^"))
        print("{:^18}{:^3}{:^18}".format("XP", "|", "PP"))
        print("-" * 40)
        self.__show_progress()

    def __update_progress(self :Tracker) -> None:
        self.__iteration += 1

    def __show_progress(self :Tracker)  -> None:
        if self.__iteration == 1:
            print('Starting: {:^8}{:^3}Starting: {:^8}'.format(Helper.human_format(Stats.xp), "|", Helper.human_format(Stats.pp)))
        else:
            elapsed = self.elapsed_time()
            xph, pph = self.__estimaterate.rates()
            report_time = "\n{0:^40}\n".format(elapsed)
            print('Current:  {:^8}{:^3}Current:  {:^8}'.format(Helper.human_format(Stats.xp), "|", Helper.human_format(Stats.pp)))
            print('Per hour: {:^8}{:^3}Per hour: {:^8}'.format(Helper.human_format(xph), "|", Helper.human_format(pph)))
            print(report_time)

    def elapsed_time(self :Tracker) -> str:
        """Print the total elapsed time."""
        elapsed = round(time.time() - self.__start_time)
        elapsed_time = str(datetime.timedelta(seconds=elapsed))
        return elapsed_time

    def progress(self :Tracker) -> None:
        self.__estimaterate.stop_watch()
        self.__update_progress()
        if not Stats.OCR_failed:
            self.__show_progress()
        print("{0:{fill}{align}40}".format(f" {self.__iteration} ", fill="-", align="^"))
        print("{:^18}{:^3}{:^18}".format("XP", "|", "PP"))
        print("-" * 40)

    def adjustxp(self :Tracker) -> None:
        self.__estimaterate.update_xp()
