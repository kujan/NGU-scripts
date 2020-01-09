"""Guffin Run Class"""

import time

# Helper classes
from classes.features import (
    AdvancedTraining,
    Adventure,
    BloodMagic,
    FightBoss,
    GoldDiggers,
    Hacks,
    Inputs,
    Misc,
    TimeMachine,
    Augmentation,
    MoneyPit,
    Rebirth,
    Questing,
    NGU,
    Wandoos,
)
from classes.wishes import Wishes

import coordinates as coords
import constants as const
from typing import NamedTuple, List, ClassVar


class GuffinRun:

    wishes: ClassVar[Wishes] = None
    advanced_training_locked: ClassVar[bool] = False
    current_boss: ClassVar[int] = 0
    rb_time: ClassVar[int] = 0
    runs: ClassVar[int] = 0

    max_rb_duration: ClassVar[int]
    zone: ClassVar[str]
    gold_zone: ClassVar[str]
    hacks: ClassVar[List[int]]
    diggers: ClassVar[List[int]]
    butter: ClassVar[bool]
    aug: ClassVar[List[str]]
    allocate_wishes: ClassVar[bool]
    wandoos_version: ClassVar[int]
    wish_min_time: ClassVar[int]
    wish_slots: ClassVar[int]

    @staticmethod
    def init(settings: NamedTuple) -> None:
        """Initialize settings."""
        GuffinRun.max_rb_duration = settings.max_rb_duration
        GuffinRun.zone = settings.zone
        GuffinRun.gold_zone = settings.gold_zone
        GuffinRun.hacks = settings.hacks
        GuffinRun.diggers = settings.diggers
        GuffinRun.butter = settings.butter
        GuffinRun.aug = settings.aug
        GuffinRun.allocate_wishes = settings.allocate_wishes
        GuffinRun.wandoos_version = settings.wandoos_version
        GuffinRun.wish_min_time = settings.wish_min_time
        GuffinRun.wish_slots = settings.wish_slots

        if GuffinRun.allocate_wishes:
            GuffinRun.wishes = Wishes(GuffinRun.wish_slots, GuffinRun.wish_min_time)
            lst = [GuffinRun.wishes.epow, GuffinRun.wishes.mpow, GuffinRun.wishes.rpow]
            i = 0
            while 1 in lst:
                print("OCR reading failed for stat breakdowns, trying again...")
                GuffinRun.wishes = Wishes(GuffinRun.wish_slots, GuffinRun.wish_min_time)
                i += 1
                if i > 5:
                    print("Wishes will be disabled.")
                    GuffinRun.wishes = None
                    break

    @staticmethod
    def __update_gamestate() -> None:
        """Update relevant state information."""
        GuffinRun.rb_time = Rebirth.rt_to_seconds()
        try:
            GuffinRun.current_boss = int(FightBoss.get_current_boss())
        except ValueError:
            GuffinRun.current_boss = 1
            print("couldn't get current boss")

        if GuffinRun.advanced_training_locked:
            GuffinRun.advanced_training_locked = Inputs.check_pixel_color(
                *coords.COLOR_ADV_TRAINING_LOCKED
            )

    @staticmethod
    def __do_quest() -> None:
        """Get the amount of available major quests."""
        text = Questing.get_quest_text().lower()
        majors = Questing.get_available_majors()
        if majors == 0 and (
            coords.QUESTING_MINOR_QUEST in text
            or coords.QUESTING_NO_QUEST_ACTIVE in text
        ):
            Questing.questing(duration=2, force=const.QUEST_ZONE_MAP[GuffinRun.zone])
        else:
            if not Inputs.check_pixel_color(*coords.COLOR_QUESTING_USE_MAJOR):
                Inputs.click(*coords.QUESTING_USE_MAJOR)
            Questing.questing(duration=2, butter=GuffinRun.butter)

    @staticmethod
    def run() -> None:
        """Rebirth procedure."""
        GuffinRun.advanced_training_locked = True
        GuffinRun.current_boss = 0
        GuffinRun.rb_time = 0
        GuffinRun.__update_gamestate()
        if GuffinRun.rb_time > GuffinRun.max_rb_duration:
            Rebirth.do_rebirth()
            return
        FightBoss.nuke()
        time.sleep(2)
        Adventure.adventure(const.ZONE_MAP[GuffinRun.gold_zone])
        BloodMagic.toggle_auto_spells(number=False, drop=False)
        GoldDiggers.gold_diggers(GuffinRun.diggers)
        BloodMagic.blood_magic(8)
        NGU.cap_ngu()
        NGU.cap_ngu(magic=True)
        Wandoos.set_wandoos(0)
        Wandoos.wandoos(True, True)
        Augmentation.augments(
            {GuffinRun.aug[0]: 0.66, GuffinRun.aug[1]: 0.34}, Misc.get_idle_cap(1) * 0.5
        )
        TimeMachine.time_machine(Misc.get_idle_cap(1) * 0.1, magic=True)
        GuffinRun.__update_gamestate()
        BloodMagic.toggle_auto_spells(drop=False, gold=False)
        if GuffinRun.wishes:
            GuffinRun.wishes.get_caps()
            GuffinRun.wishes.get_wish_status()
            GuffinRun.wishes.allocate_wishes()

        while GuffinRun.advanced_training_locked:
            GuffinRun.__do_quest()
            FightBoss.nuke()
            GoldDiggers.gold_diggers(GuffinRun.diggers)
            NGU.cap_ngu()
            NGU.cap_ngu(magic=True)
            Hacks.hacks(GuffinRun.hacks, coords.INPUT_MAX)
            Augmentation.augments(
                {GuffinRun.aug[0]: 0.66, GuffinRun.aug[1]: 0.34},
                Misc.get_idle_cap(1) * 0.5,
            )
            TimeMachine.time_machine(coords.INPUT_MAX, magic=True)
            GuffinRun.__update_gamestate()

        Misc.reclaim_tm(energy=True, magic=True)
        Misc.reclaim_aug()
        AdvancedTraining.advanced_training(1e12)
        Wandoos.set_wandoos(GuffinRun.wandoos_version)
        Wandoos.wandoos(True, True)
        Augmentation.augments(
            {GuffinRun.aug[0]: 0.66, GuffinRun.aug[1]: 0.34}, Misc.get_idle_cap(1) * 0.5
        )
        TimeMachine.time_machine(Misc.get_idle_cap(1) * 0.1, magic=True)
        while GuffinRun.rb_time < GuffinRun.max_rb_duration - 140:
            GoldDiggers.gold_diggers(GuffinRun.diggers)
            FightBoss.nuke()
            Hacks.hacks(GuffinRun.hacks, coords.INPUT_MAX)
            GuffinRun.__do_quest()
            GuffinRun.__update_gamestate()

        FightBoss.fight()
        Adventure.adventure(itopodauto=True)
        MoneyPit.pit()
        MoneyPit.spin()
        Misc.save_check()
        while GuffinRun.rb_time < GuffinRun.max_rb_duration:
            time.sleep(1)
            GuffinRun.__update_gamestate()

        FightBoss.nuke()
        Rebirth.do_rebirth()
        # Must wait for game to fully redraw all elements after rebirthing
        time.sleep(1)
        GuffinRun.runs += 1
        print(
            f"Completed guffin run #{GuffinRun.runs} in {time.strftime('%H:%M:%S', time.gmtime(GuffinRun.rb_time))}"
        )
