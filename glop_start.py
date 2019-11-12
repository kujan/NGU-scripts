"""Glop startup script."""
import scripts.glop
from classes.helper import Helper

print("How many glops do you wish to farm? The script will farm UP TO this amount:")
target_glops = int(input())
Helper.init(True)
Helper.requirements()
scripts.glop.Glop.init(target_glops)
scripts.glop.Glop.loop()
Helper.loop()
