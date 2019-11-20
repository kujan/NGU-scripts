"""Helper functions."""
from classes.window     import Window
from classes.inputs     import Inputs
from classes.features   import Inventory, MoneyPit, Adventure, Yggdrasil, GoldDiggers, Questing

import coordinates as coords


class Helper:
    def init(printCoords :bool =False) -> None:
        """Initialize Window class variables.
        Helper.init() should go at the very top of any script, straight after imports.
        """
        rects = Window.init()
        for window_id, rect in rects.items():
            if printCoords: print(f"Scanning window id: {window_id}")
            w = rect[2] - rect[0]
            h = rect[3] - rect[1]
            Window.id = window_id
            cds = Inputs.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, w, h)
            if cds:
                Window.setPos(*cds)
                break
        if cds is None:
            raise RuntimeError("Game window not found. Maybe it's minimized or the game is not fully visible?")
        # Sometimes the very first click is ignored, this makes sure the first click is unimportant.
        Inputs.click(*coords.WASTE_CLICK)
        
        if printCoords: print(f"Top left found at: {Window.x}, {Window.y}")

    def requirements() -> None:
        """Set everything to the proper requirements to run the script.
        It's strongly recommended to run this straight after init()."""
        Inputs.click(*coords.GAME_SETTINGS)
        Inputs.click(*coords.TO_SCIENTIFIC)
        Inputs.click(*coords.CHECK_FOR_UPDATE_OFF)
        Inputs.click(*coords.FANCY_TITAN_HP_BAR_OFF)
        Inputs.click(*coords.DISABLE_HIGHSCORE)
        Inputs.click(*coords.SETTINGS_PAGE_2)
        Inputs.click(*coords.SIMPLE_INVENTORY_SHORTCUT_ON)

    def loop(idle_majors :bool =False) -> None:
        """Run infinite loop to prevent idling after task is complete.
        
        Keyword arguments
        idle_majors -- Set to True if you wish to idle major and minor quests.
                       Set to False if you wish to idle minor quests only.
                       Currently active quest will be idled regardless.
        """
        Questing.set_use_majors(idle_majors)
        print("Engaging idle loop")
        while True:  # main loop
            Questing.questing(subcontract=True)  # Questing first, as we are already there
            MoneyPit.pit()
            MoneyPit.spin()
            Inventory.boost_cube()
            GoldDiggers.gold_diggers()
            Yggdrasil.ygg()
            Adventure.itopod_snipe(300)

    def human_format(num :float) -> str:
        """Convert large numbers into something readable."""
        suffixes = ['', 'K', 'M', 'B', 'T', 'Q', 'Qi', 'Sx', 'Sp']
        num = float('{:.3g}'.format(num))
        if num > 1e24:
            return '{:.3g}'.format(num)
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), suffixes[magnitude])
