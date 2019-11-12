"""Guffin startup script."""
import scripts.glop
from classes.helper import Helper
from typing import NamedTuple, List
import constants as const


Helper.init(True)
Helper.requirements()

target_glops = 50

scripts.glop.Glop.init(target_glops)
scripts.glop.Glop.loop()
Helper.loop()
