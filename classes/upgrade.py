"""Buys things for exp."""
import time
import math

from classes.stats  import Stats
from classes.helper import Helper
from classes.features import Navigation
from classes.inputs import Inputs

import coordinates  as coords
import usersettings as userset


class UpgradeEM:
    """Buys things for exp."""

    def __init__(self, ecap, mcap, ebar, mbar, e2m_ratio, report=False):
        """Example: Upgrade(37500, 37500, 2, 1).

        This will result in a 1:37500:2 ratio for energy and 1:37500:1 for
        magic. i.e. 1 power, 37500 ecap and 2 ebars.

        Keyword arguments:

        ecap -- The amount of energy cap in the ratio. Must be over 10000 and
                divisible by 250.
        mcap -- The amount of magic cap in the ratio. Must be over 10000 and
                divisible by 250.
        ebar -- the amount of energy bars to buy in relation to power
        mbar -- the amount of magic bars to buy in relation to power.
        e2m_ratio -- The amount of exp to spend in energy in relation to magic.
                     a value of 5 will buy 5 times more upgrades in energy than
                     in magic, maintaining a 5:1 E:M ratio.
        """
        self.ecap = ecap
        self.mcap = mcap
        self.ebar = ebar
        self.mbar = mbar
        self.e2m_ratio = e2m_ratio
        self.report = report

    def buy(self):
        """Buy upgrades for both energy and magic.

        Requires the confirmation popup button for EXP purchases in settings
        to be turned OFF.

        This uses all available exp, so use with caution.
        """
        if self.ecap < 10000 or self.ecap % 250 != 0:
            print("Ecap value not divisible by 250 or lower than 10000, not" +
                  " spending exp.")
            return
        if self.mcap < 10000 or self.mcap % 250 != 0:
            print("Mcap value not divisible by 250 or lower than 10000, not" +
                  " spending exp.")
            return

        Stats.set_value_with_ocr("XP")
        if Stats.OCR_failed:
            print('OCR failed, exiting upgrade routine.')
            return

        current_exp = Stats.xp

        e_cost = coords.EPOWER_COST + coords.ECAP_COST * self.ecap + (
            coords.EBAR_COST * self.ebar)

        m_cost = coords.MPOWER_COST + coords.MCAP_COST * self.mcap + (
            coords.MBAR_COST * self.mbar)

        total_price = m_cost + self.e2m_ratio * e_cost

        # Skip upgrading if we don't have enough exp to buy at least one
        # complete set of upgrades, in order to maintain our perfect ratios :)

        if total_price > current_exp:
            if self.report:
                print("No XP Upgrade :{:^8} of {:^8}".format(Helper.human_format(current_exp), Helper.human_format(total_price)))
            return

        amount = int(current_exp // total_price)

        e_power = amount * self.e2m_ratio
        e_cap   = amount * self.ecap * self.e2m_ratio
        e_bars  = amount * self.ebar * self.e2m_ratio
        m_power = amount
        m_cap   = amount * self.mcap
        m_bars  = amount * self.mbar

        Navigation.exp()

        Inputs.click(*coords.EM_POW_BOX)
        Inputs.send_string(str(e_power))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_CAP_BOX)
        Inputs.send_string(str(e_cap))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_BAR_BOX)
        Inputs.send_string(str(e_bars))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_POW_BUY)
        Inputs.click(*coords.EM_CAP_BUY)
        Inputs.click(*coords.EM_BAR_BUY)

        Navigation.exp_magic()

        Inputs.click(*coords.EM_POW_BOX)
        Inputs.send_string(str(m_power))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_CAP_BOX)
        Inputs.send_string(str(m_cap))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_BAR_BOX)
        Inputs.send_string(str(m_bars))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_POW_BUY)
        Inputs.click(*coords.EM_CAP_BUY)
        Inputs.click(*coords.EM_BAR_BUY)

        Stats.set_value_with_ocr("XP")

        total_spent  = coords.EPOWER_COST * e_power + coords.ECAP_COST * e_cap + coords.EBAR_COST * e_bars
        total_spent += coords.MPOWER_COST * m_power + coords.MCAP_COST * m_cap + coords.MBAR_COST * m_bars

        if self.report:
            print("Spent XP:{:^8}".format(Helper.human_format(total_spent)))
            print("Energy | Pow:{:^8}{:^3}Cap:{:^8}{:^3}Bar:{:^8}{:^3}Magic | Pow:{:^8}{:^3}Cap:{:^8}{:^3}Bar:{:^8}".format(
                Helper.human_format(e_power), "|",
                Helper.human_format(e_cap),   "|",
                Helper.human_format(e_bars),  "|",
                Helper.human_format(m_power), "|",
                Helper.human_format(m_cap),   "|",
                Helper.human_format(m_bars)
            ))


class UpgradeAdventure(Stats):
    """Buys things for exp."""

    def __init__(self, power, toughness, health, regen, ratio, report=False):
        self.power = power
        self.toughness = toughness
        self.health = health
        self.regen = regen
        self.ratio = ratio
        self.report = report

    def buy(self):
        """Buy upgrades for power, toughness, health and regen

        Requires the confirmation popup button for EXP purchases in settings
        to be turned OFF.

        This uses all available exp, so use with caution.
        """
        Stats.set_value_with_ocr("XP")

        if Stats.OCR_failed:
            print('OCR failed, exiting upgrade routine.')
            return

        current_exp = Stats.xp

        total_price = (coords.APOWER_COST * self.power * self.ratio)
        total_price += (coords.ATOUGHNESS_COST * self.toughness * self.ratio)
        total_price += (coords.AHEALTH_COST * self.health * 10)
        total_price += math.floor(coords.AREGEN_COST * self.regen / 10)

        # Skip upgrading if we don't have enough exp to buy at least one
        # complete set of upgrades, in order to maintain our perfect ratios :)

        if total_price > current_exp:
            if self.report:
                print("No XP Upgrade :{:^8} of {:^8}".format(Helper.human_format(current_exp), Helper.human_format(total_price)))
            return

        amount = int(current_exp // total_price)

        a_power     = amount * self.ratio
        a_toughness = amount * self.ratio
        a_health    = amount * 10
        a_regen     = math.floor(amount / 10)
        if a_regen < 1: a_regen = 1.0

        Navigation.exp_adventure()

        Inputs.click(*coords.EM_ADV_BOX)
        Inputs.send_string(str(a_power))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_POW_BOX)
        Inputs.send_string(str(a_toughness))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_CAP_BOX)
        Inputs.send_string(str(a_health))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_BAR_BOX)
        Inputs.send_string(str(a_regen))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_ADV_BUT)
        Inputs.click(*coords.EM_POW_BUY)
        Inputs.click(*coords.EM_CAP_BUY)
        Inputs.click(*coords.EM_BAR_BUY)

        Stats.set_value_with_ocr("XP")

        total_spent = coords.APOWER_COST * a_power
        total_spent += coords.ATOUGHNESS_COST * a_toughness
        total_spent += coords.AHEALTH_COST * a_health
        total_spent += coords.AREGEN_COST * a_regen

        if self.report:
            print("Spent XP:{:^8}".format(Helper.human_format(total_spent)))
            print("Power:{:^8}{:^3} Defense:{:^8}{:^3} Health:{:^8}{:^3} Regen:{:^8}".format(
                Helper.human_format(a_power), "|",
                Helper.human_format(a_toughness), "|",
                Helper.human_format(a_health), "|",
                Helper.human_format(a_regen)))


class UpgradeRich(Stats):
    """Buys things for exp."""

    def __init__(self, attack, defense, report=False):
        self.attack = attack
        self.defense = defense
        self.report = report

    def buy(self):
        """Buy upgrades for both attack and defense

        Requires the confirmation popup button for EXP purchases in settings
        to be turned OFF.

        This uses all available exp, so use with caution.
        """
        Stats.set_value_with_ocr("XP")

        if Stats.OCR_failed:
            print('OCR failed, exiting upgrade routine.')
            return

        current_exp = Stats.xp

        if current_exp < 1000:
            return

        total_price = (coords.RATTACK_COST * self.attack)
        total_price += (coords.RDEFENSE_COST * self.defense)

        # Skip upgrading if we don't have enough exp to buy at least one
        # complete set of upgrades, in order to maintain our perfect ratios :)

        if total_price > current_exp:
            if self.report:
                print("No XP Upgrade :{:^8} of {:^8}".format(Helper.human_format(current_exp), Helper.human_format(total_price)))
            return

        amount = int(current_exp // total_price)

        a_attack = amount * self.attack
        a_defense = amount * self.defense

        Navigation.exp_rich()

        Inputs.click(*coords.EM_ADV_BOX)
        Inputs.send_string(str(a_attack))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_ADV_BOX)
        Inputs.send_string(str(a_defense))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_ADV_BOX)
        Inputs.click(*coords.EM_ADV_BOX)

        Stats.set_value_with_ocr("XP")

        total_spent = coords.RATTACK_COST * a_attack
        total_spent += coords.RDEFENSE_COST * a_defense

        if self.report:
            print("Spent XP:{:^8}{:^3}Attack:{:^8}{:^3}Defense:{:^8}".format(
                Helper.human_format(total_spent), "|",
                Helper.human_format(a_attack), "|",
                Helper.human_format(a_defense)))


class UpgradeHackPower(Stats):
    """Buys things for exp."""

    def __init__(self, hcap, hbar, hpower, report=False):
        """Example: UpgradeHackPower(10000, 1, 1).

        Keyword arguments:

        hcap -- The amount of hack energy in the ratio. Must be over 1000 and divisible by 250 or 0.
        hbar -- The amount of bars
        hpower -- the amount of new power

        """
        self.hcap = hcap
        self.hbar = hbar
        self.hpower = hpower
        self.report = report

    def buy(self):
        """Buy upgrades for hack energy

        Requires the confirmation popup button for EXP purchases in settings
        to be turned OFF.

        This uses all available exp, so use with caution.
        """
        if (self.hcap < 10000 or self.hcap % 250 != 0) and self.hcap != 0:
            print("Ecap value not divisible by 250 or lower than 10000, not" +
                  " spending exp.")
            return

        Stats.set_value_with_ocr("XP")
        if Stats.OCR_failed:
            print('OCR failed, exiting upgrade routine.')
            return

        current_exp = Stats.xp

        total_price = coords.HPOWER_COST * self.hpower + coords.HCAP_COST * self.hcap + coords.HBAR_COST * self.hbar

        # Skip upgrading if we don't have enough exp to buy at least one
        # complete set of upgrades, in order to maintain our perfect ratios :)

        if total_price > current_exp:
            if self.report:
                print("No XP Upgrade :{:^8} of {:^8}".format(Helper.human_format(current_exp),
                                                             Helper.human_format(total_price)))
            return

        amount = int(current_exp // total_price)

        h_power = amount * self.hpower
        h_cap = amount * self.hcap
        h_bars = amount * self.hbar

        Navigation.exp_hack()

        Inputs.click(*coords.EM_POW_BOX)
        Inputs.send_string(str(h_power))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_CAP_BOX)
        Inputs.send_string(str(h_cap))
        time.sleep(userset.MEDIUM_SLEEP)

        Inputs.click(*coords.EM_BAR_BOX)
        Inputs.send_string(str(h_bars))
        time.sleep(userset.MEDIUM_SLEEP)

        if h_power > 0:
            Inputs.click(*coords.EM_POW_BUY)
        if h_cap > 0:
            Inputs.click(*coords.EM_CAP_BUY)
        if h_bars > 0:
            Inputs.click(*coords.EM_BAR_BUY)

        Stats.set_value_with_ocr("XP")

        total_spent = coords.HPOWER_COST * h_power + coords.HCAP_COST * h_cap + coords.HBAR_COST * h_bars

        if self.report:
            print("Spent XP:{:^8}".format(Helper.human_format(total_spent)))
            print("New | Pow:{:^8}{:^3}Cap:{:^8}{:^3}Bar:{:^8}".format(
                Helper.human_format(h_power), "|",
                Helper.human_format(h_cap), "|",
                Helper.human_format(h_bars)))
