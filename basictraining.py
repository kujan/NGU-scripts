from classes.features   import (BasicTraining)
from classes.helper     import Helper
from classes.inputs   import Inputs

import coordinates as coords

Helper.init(True)
Helper.requirements()

# Input is divided by 2 and put equally into Idle/Block
# AutoAdvance is REQUIRED
BasicTraining.basic_training(3000)
