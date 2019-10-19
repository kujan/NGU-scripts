"""Guffin script."""

from classes.guffin import Guffin
from classes.helper import Helper

Helper.init(True)
Helper.requirements()

guffin = Guffin()
while True: guffin.run()
