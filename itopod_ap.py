"""AP farming script."""

# Helper classes
from classes.helper   import Helper
from classes.features import Features

Helper.init(True)
Helper.requirements()

while True:  # main loop
    Adventure.itopod_ap(600)
    MoneyPit.pit()
