"""AP farming script."""

# Helper classes
import classes.helper as helper
from classes.features import Features

feature = Features()
helper.init(feature, True)

while True:  # main loop
    feature.itopod_ap(600)
    feature.pit()
