"""Manual Questing Script."""

# Helper classes
from classes.features   import Adventure, Questing, GoldDiggers, MoneyPit
from classes.helper     import Helper

import coordinates as coords
import time

Helper.init(True)
Helper.requirements()

choice = ""
answers = {"y": True, "ye": True, "yes": True, "n": False, "no": False}
print("If you currently have an active quest that either is minor or has been subcontracted, consider skipping it before starting if you intend to use butter")
while choice not in answers:
    choice = input("Use butter for major quests? y/n: ").lower()

while True:  # main loop
    titans = Adventure.check_titan_status()
    if titans:
        Adventure.kill_titan(titans[0])
    text = Questing.get_quest_text()
    majors = Questing.get_available_majors()
    if majors == 0 and (coords.QUESTING_MINOR_QUEST in text.lower() or coords.QUESTING_NO_QUEST_ACTIVE in text.lower()):
        Questing.questing(force=3)
    else:
        Questing.set_use_majors()
        Questing.questing(butter=answers[choice])
    MoneyPit.pit()
    GoldDiggers.gold_diggers()
    time.sleep(3)
