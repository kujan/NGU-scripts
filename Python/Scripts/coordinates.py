from collections import namedtuple

Pixel = namedtuple('Pixel', 'x y')
ColorPixel = namedtuple('ColorPixel', Pixel._fields + ('color',))
OCRBox = namedtuple('OCRBox', 'x1 y1 x2 y2')

# COLORS
TOP_LEFT_COLOR = '000408'
SANITY_AUG_SCROLL_COLORS = ["497C9F", "4C81A5", "4C80A4", "497B9E", "457596"]
NGU_BAR_WHITE = "FFFFFF"
NGU_BAR_GRAY = "FAFAFA"

# Here are the colors I found for Dark_Gold_Theme
#     SANITY_AUG_SCROLL_COLORS, # DIFF ['9E7D11', 'B59012', '94760E' '8B7304'] ('C19915' maybe a bugged value))
#     NGU_BAR_WHITE, # 'B4B3B4'
#     NGU_BAR_GRAY, # NOT USED
#     IS_BOSS_CROWN, # SAME BUT OFF BY 1 pixel in x
#     IS_NOT_DEAD, # SAME
#     IS_DEAD, # SAME
#     IS_ITOPOD_ACTIVE, # SAME
#     IS_IDLE, # SAME
#     IS_SAVE_READY, # '68AD68'
#     IS_PIT_READY, # '568E28'
#     IS_SPIN_READY, # 'AD8E28'
#     IS_CHALLENGE_ACTIVE, # SAME
#     COLOR_TM_LOCKED, # '767776'
#     COLOR_BM_LOCKED, # '767776', {'63375E' w/ iron pill}
#     IS_IRON_PILL_READY, #'7E0D71'
#     PLAYER_HEAL_THRESHOLDX # SAME
# ]

INPUT_MAX = 1000000000000000000

# Adventure Offsets
RIGHT_ARROW = Pixel(930, 220)
LEFT_ARROW = Pixel(325, 225)
ITOPOD = Pixel(405, 225)
ITOPOD_PERKS = Pixel(490, 225)
ITOPOD_START = Pixel(625, 230)
ITOPOD_END = Pixel(625, 265)
ITOPOD_ENTER = Pixel(625, 330)
ITOPOD_AUTO = Pixel(710, 215)
HEALTH = Pixel(706, 411)

# TODO: Rewrite kill_titan
ABILITY_ROW1X = 426
ABILITY_ROW2X = 321
ABILITY_ROW3X = 321
ABILITY_ROW1Y = 113
ABILITY_ROW2Y = 150
ABILITY_ROW3Y = 186

# ROW 1 ABILITIES
ABILITY_IDLE_MODE = Pixel(330, 105)
ABILITY_REGULAR_ATTACK = Pixel(430, 105)

# TODO: FIX TITAN SNIPE
ABILITY_ANCHOR_PIXEL = Pixel(321, 113)
ABILITY_OFFSETX = 106
ABILITY_OFFSETY = 37

# ROW 1 ABILITIES
ABILITY_STRONG_ATTACK = Pixel(531, 113)
ABILITY_PARRY = Pixel(636, 113)
ABILITY_PIERCING_ATTACK = Pixel(741, 113)
ABILITY_ULTIMATE_ATTACK = Pixel(846, 113)
ABILITY_ROW1_READY_COLOR = "F89B9B"
# ROW 2 ABILITIES
ABILITY_BLOCK = Pixel(321, 150)
ABILITY_DEFENSIVE_BUFF = Pixel(426, 150)
ABILITY_HEAL = Pixel(531, 150)
ABILITY_OFFENSIVE_BUFF = Pixel(636, 150)
ABILITY_CHARGE = Pixel(741, 150)
ABILITY_ULTIMATE_BUFF = Pixel(846, 150)
ABILITY_ROW2_READY_COLOR = "F89B9B"
# ROW 3 ABILITIES
ABILITY_PARALYZE_GAZE = Pixel(321, 186)
ABILITY_HYPER_REGEN = Pixel(426, 186)
ABILITY_BEAST_MODE = Pixel(531, 186)
ABILITY_ROW3_READY_COLOR = "C39494"

# TODO: FIX ABILITY NUMBERING TO NEW SCHEME
ABILITY_PRIORITY = {1: 6,  # Strong
                    2: 8,  # Parry
                    3: 9,  # Piercing
                    4: 10,  # Ultimate
                    5: 4,  # Block
                    6: 5,  # Defensive
                    9: 12 # Charge
                    }  # Paralyze

#titan dictionaries
TITAN_PT = {"GRB": {"p": 1.3e3, "t": 1.3e3}, "GCT": {"p": 5e3, "t": 4e3},
            "jake": {"p": 1.4e4, "t": 1.2e4}, "UUG": {"p": 4e5, "t": 3e5},
            "walderp": {"p": 5.5e6, "t": 3.75e6},
            "BEAST1": {"p": 6e8, "t": 6e8}, "BEAST2": {"p": 6e9, "t": 6e9},
            "BEAST3": {"p": 6e10, "t": 6e10}, "BEAST4": {"p": 6e11, "t": 6e11}}

TITAN_ZONE = {"GRB": 7, "GCT": 9, "jake": 12, "UUG": 15, "walderp": 17,
              "BEAST1": 20, "BEAST2": 20, "BEAST3": 20, "BEAST4": 20}

OCR_ADV_POW = OCRBox(370, 296, 483, 313)
OCR_ADV_TOUGH = OCRBox(406, 313, 506, 330)
OCR_ADV_TITAN = OCRBox(560, 277, 685, 330)
OCR_ADV_ENEMY_CHECK = OCRBox(766, 382, 889, 403)
OCR_COMBAT_LOG = OCRBox(310, 496, 600, 589)

#MENU OFFSETS

MENU_OFFSET_X = 230
MENU_FIGHT = Pixel(MENU_OFFSET_X, 75)
MENU_PIT = Pixel(MENU_OFFSET_X, 105)
MENU_ADVENTURE = Pixel(MENU_OFFSET_X, 135)
MENU_INVENTORY = Pixel(MENU_OFFSET_X, 165)
MENU_AUGMENTATIONS = Pixel(MENU_OFFSET_X, 195)
MENU_ADV_TRAINING = Pixel(MENU_OFFSET_X, 225)
MENU_TIME_MACHINE = Pixel(MENU_OFFSET_X, 255)
MENU_BLOOD_MAGIC = Pixel(MENU_OFFSET_X, 285)
MENU_WANDOOS = Pixel(MENU_OFFSET_X, 315)
MENU_NGU = Pixel(MENU_OFFSET_X, 345)
MENU_YGGDRASIL = Pixel(MENU_OFFSET_X, 375)
MENU_DIGGERS = Pixel(MENU_OFFSET_X, 405)
MENU_BEARD = Pixel(MENU_OFFSET_X, 435)
MENU_QUESTING = Pixel(MENU_OFFSET_X, 465)
MENU_HACKS = Pixel(MENU_OFFSET_X, 495)
MENU_ITEMS = {
    'fight': MENU_FIGHT, 'pit': MENU_PIT, 'adventure': MENU_ADVENTURE,
    'inventory': MENU_INVENTORY, 'augmentations': MENU_AUGMENTATIONS,
    'advtraining': MENU_ADV_TRAINING, 'timemachine': MENU_TIME_MACHINE,
    'bloodmagic': MENU_BLOOD_MAGIC, 'wandoos': MENU_WANDOOS, 'ngu': MENU_NGU,
    'yggdrasil': MENU_YGGDRASIL, 'digger': MENU_DIGGERS, 'beard': MENU_BEARD,
    'questing': MENU_QUESTING, 'hacks': MENU_HACKS,
}
NUMBER_INPUT_BOX = Pixel(440, 20)
EXP = Pixel(90, 450)
SAVE = Pixel(23, 483)


#FIGHT BOSS OFFSETS

NUKE = Pixel(620, 265)
FIGHT = Pixel(620, 370)

# INVENTORY OFFSETS
EQUIPMENT_SLOTS = {"accessory1": Pixel(480, 65),
                  "accessory2": Pixel(480, 115),
                  "accessory3": Pixel(480, 165),
                  "accessory4": Pixel(480, 215),
                  "head": Pixel(525, 65),
                  "chest": Pixel(525, 115),
                  "legs": Pixel(525, 165),
                  "boots": Pixel(525, 210),
                  "weapon": Pixel(575, 115),
                  "cube": Pixel(625, 115)}
LOADOUT_Y = 255
LOADOUT = {1: Pixel(330, LOADOUT_Y), 2: Pixel(360, LOADOUT_Y), 3: Pixel(390, LOADOUT_Y), 4: Pixel(420, LOADOUT_Y), 5: Pixel(450, LOADOUT_Y),
           6: Pixel(480, LOADOUT_Y), 7: Pixel(510, LOADOUT_Y), 8: Pixel(540, LOADOUT_Y), 9: Pixel(570, LOADOUT_Y), 10: Pixel(600, LOADOUT_Y)}

INVENTORY_SLOTS = Pixel(300, 330)
INVENTORY_AREA = OCRBox(315, 290, 930, 560)

#TIME MACHINE OFFSETS
TM_SPEED = Pixel(532, 233)
TM_MULT = Pixel(532, 330)
TM_SPEED_MINUS = Pixel(570, 236)
TM_MULT_MINUS = Pixel(570, 335)
#BLOOD MAGIC OFFSETS
BM_LOCKED = Pixel(229, 294)

BM_X = 570
BM = {0: Pixel(BM_X, 228), 1: Pixel(BM_X, 263), 2: Pixel(BM_X, 298), 3: Pixel(BM_X, 333),
      4: Pixel(BM_X, 369), 5: Pixel(BM_X, 403), 6: Pixel(BM_X, 438), 7: Pixel(BM_X, 473)}

BM_SPELL = Pixel(390, 115)
BM_PILL = Pixel(744, 216)
BM_GUFFIN_A = Pixel(395, 435)
BM_GUFFIN_B = Pixel(735, 435)
BM_NUMBER = Pixel(400, 220)
BM_AUTO_NUMBER = Pixel(511, 223)
BM_AUTO_GOLD = Pixel(848, 313)
BM_AUTO_DROP = Pixel(510, 313)

BM_RECLAIM_X = 530
BM_RECLAIM = [Pixel(BM_RECLAIM_X, 228), Pixel(BM_RECLAIM_X, 263), Pixel(BM_RECLAIM_X, 298), Pixel(BM_RECLAIM_X, 333),
              Pixel(BM_RECLAIM_X, 369), Pixel(BM_RECLAIM_X, 403), Pixel(BM_RECLAIM_X, 438), Pixel(BM_RECLAIM_X, 473)]

OCR_BM_SPELL_TEXT = OCRBox(440, 350, 800, 412)

#TODO: AUGMENTATION OFFSETS
AUGMENT_X = 535

AUGMENT = {"SS": Pixel(AUGMENT_X, 263), "DS": Pixel(AUGMENT_X, 292), "MI": Pixel(AUGMENT_X, 329),
           "DTMT": Pixel(AUGMENT_X, 357), "CI": Pixel(AUGMENT_X, 394), "ML": Pixel(AUGMENT_X, 422),
            "SM": Pixel(AUGMENT_X, 459), "AA": Pixel(AUGMENT_X, 487), "EB": Pixel(AUGMENT_X, 525), 
            "CS": Pixel(AUGMENT_X, 552), "AE": Pixel(AUGMENT_X, 450), "ES": Pixel(AUGMENT_X, 478),
            "LS": Pixel(AUGMENT_X, 516), "QSL": Pixel(AUGMENT_X, 544)}

AUG_MINUS_X = 575


AUG_SCROLL_TOP = Pixel(945, 264)
AUG_SCROLL_BOT = Pixel(945, 575)
AUG_SCROLL_SANITY_TOP = Pixel(943, 261)
AUG_SCROLL_SANITY_BOT = Pixel(943, 578)

#TODO: NGU OFFSETS
NGU_TARGET = Pixel(635, 205)
NGU_MAGIC = Pixel(380, 120)
NGU_MINUS = Pixel(551, 207)
NGU_PLUS = Pixel(517, 207)
NGU_CAP = Pixel(590, 207)
NGU_CAP_ALL = Pixel(625, 160)
NGU_OVERCAP = Pixel(430, 135)
NGU_EVIL = ColorPixel(778, 146, "323232")

NGU_BAR_MIN = Pixel(306, 215)
NGU_BAR_MAX = Pixel(503, 215)
NGU_BAR_OFFSET_Y = 35

#TODO: Make into dict ADVTRAINING
ADV_TRAINING_TOUGHNESS = Pixel(890, 230)
ADV_TRAINING_POWER = Pixel(890, 270)
ADV_TRAINING_BLOCK = Pixel(890, 310)
ADV_TRAINING_WANDOOS_ENERGY = Pixel(890, 350)
ADV_TRAINING_WANDOOS_MAGIC = Pixel(890, 390)

#YGGDRASIL OFFSETS
HARVEST = Pixel(814, 450)
FRUIT_GOLD = Pixel(350, 180)
FRUIT_POWER_A = Pixel(560, 180)
FRUIT_ADV = Pixel(775, 180)
FRUIT_KNOWLEDGE = Pixel(350, 270)
FRUIT_POM = Pixel(560, 270)
FRUIT_LUCK = Pixel(775, 270)
FRUIT_POWER_B = Pixel(350, 370)
FRUIT_ARB = Pixel(560, 370)
FRUIT_NUMBERS = Pixel(775, 370)
FRUITS = {
    1: FRUIT_GOLD,
    2: FRUIT_POWER_A,
    3: FRUIT_ADV,
    4: FRUIT_KNOWLEDGE,
    5: FRUIT_POM,
    6: FRUIT_LUCK,
    7: FRUIT_POWER_B,
    8: FRUIT_ARB,
    9: FRUIT_NUMBERS
}

YGG_EAT_ALL = Pixel(815, 490)

#REBIRTH OFFSETS
REBIRTH = Pixel(90, 420)
REBIRTH_BUTTON = Pixel(545, 520)
CONFIRM = Pixel(425, 320)
CHALLENGE_BUTTON = Pixel(700, 520)
CHALLENGE = Pixel(380, 152)
CHALLENGEOFFSET = 30
OCR_REBIRTH_TIME = OCRBox(50, 375, 115, 405) # Old Values: OCRBox(14, 388, 161, 407)

#PIT OFFSETS
PIT_CHECK = Pixel(195, 108)
PIT = Pixel(630, 290)
PIT_CONFIRM = Pixel(437, 317)
SPIN_MENU = Pixel(820, 235)
SPIN = Pixel(713, 562)

#WANDOOS
WANDOOS_ENERGY = Pixel(626, 252)
WANDOOS_MAGIC = Pixel(626, 350)
WANDOOS_VERSION = [Pixel(325, 420), Pixel(325, 445), Pixel(325, 470)]


#OCR OFFSETS
OCR_BOSS = OCRBox(765, 125, 890, 140)
OCR_PP = OCRBox(785, 25, 901, 43)
OCR_EXP = OCRBox(340, 70, 900, 95) #From EXP Menu
OCR_POW = OCRBox(468, 303, 616, 330)
OCR_CAP = OCRBox(627, 303, 776, 330)
OCR_BAR = OCRBox(787, 303, 937, 330)
OCR_ECAP = OCRBox(9, 44, 165, 63)
OCR_TOTAL_EXP = OCRBox(510, 365, 928, 400) #From MISC Info
OCR_NGU_E = OCRBox(820, 190, 940, 219)

#STATS OCR
OCR_ENERGY = OCRBox(12, 28, 165, 50)
OCR_MAGIC = OCRBox(12, 70, 165, 90)

#OCR CHALLENGES
OCR_CHALLENGE_NAME = OCRBox(465, 87, 750, 104)
OCR_CHALLENGE_24HC_TARGET = OCRBox(479, 267, 771, 297)

#BEARD OFFSETS

BEARD_X = {1: 312, 2: 338, 3: 312, 4: 1}

#TODO: DIGGER OFFSETS
DIG_PAGE_Y = 110
DIG_PAGE = [Pixel(340, DIG_PAGE_Y), Pixel(405, DIG_PAGE_Y), Pixel(470, DIG_PAGE_Y)]

DIG_ACTIVE = {1: Pixel(341, 237), 2: Pixel(658, 237), 3: Pixel(341, 427), 4: Pixel(658, 427)}
DIG_CAP = {1: Pixel(550, 185), 2: Pixel(865, 185), 3: Pixel(550, 375), 4: Pixel(865, 375)}

DIG_LEVEL = [Pixel(535, 235), Pixel(850, 235), Pixel(535, 420), Pixel(850, 420)]

DIG_DEACTIVATE_ALL = Pixel(850, 110)

#QUESTING OFFSETS

QUESTING_START_QUEST = Pixel(700, 165)
QUESTING_SKIP_QUEST = Pixel(855, 165)
QUESTING_SUBCONTRACT = Pixel(470, 560)
QUESTING_QUEST_COMPLETE = "this quest can be handed in"
QUESTING_NO_QUEST_ACTIVE = "start quest"
QUESTING_MINOR_QUEST = "this is a minor quest"
QUESTING_USE_MAJOR = Pixel(694, 207)

OCR_QUESTING_QP = OCRBox(500, 60, 683, 84)
OCR_QUESTING_LEFT_TEXT = OCRBox(301, 296, 617, 497)
OCR_QUESTING_MAJORS = OCRBox(790, 300, 857, 317)
QUESTING_ZONES = ["safe zone", "tutorial zone", "sewers", "forest", "cave of many things", "the sky",
                  "high\nsecurity base", "grb", "clock dimension", "gct", "2d universe", "ancient battlefield",
                  "jfa", "a very\nstrange place", "mega\nlands", "uug", "the beardverse", "waldo", "badly drawn world",
                  "boring-ass earth", "thebeasto", "chocolate world", "the evilverse", "pretty pink princess", "greasynerdman", "meta land",
                  "interdimensional party", "thegodmom"]

QUESTING_FILENAMES = ["q1.png", "q2.png", "q3.png", "q4.png", "q5.png", "q6.png", "q7.png", "q8.png", "q9.png", "q10.png"]

#SELLOUT

SELLOUT = Pixel(235, 550)
SELLOUT_BOOST_2 = Pixel(520, 147)
SELLOUT_MUFFIN_USE = Pixel(768, 256)
SELLOUT_MUFFIN_BUY = Pixel(860, 255)
OCR_MUFFIN = OCRBox(785, 204, 936, 240)
OCR_AP = OCRBox(450, 73, 800, 100)

#EXP COSTS PER UNIT
EPOWER_COST = 150
ECAP_COST = 0.004
EBAR_COST = 80
MPOWER_COST = 450
MCAP_COST = 0.012
MBAR_COST = 240

APOWER_COST = 3
ATOUGHNESS_COST = 3
AHEALTH_COST = 0.3
AREGEN_COST = 50

HPOWER_COST = 15000000
HCAP_COST = 400
HBAR_COST = 8000000


RATTACK_COST = 3
RDEFENSE_COST = 3

#EXP MENU
XP_MENU = Pixel(90, 450)
MAGIC_MENU = Pixel(470, 110)
ADVENTURE_MENU = Pixel(570, 110)
RICH_MENU = Pixel(785, 110)
EXP_HACK_MENU = Pixel(420, 140)

EM_POW_BOX = Pixel(537, 522)
EM_CAP_BOX = Pixel(707, 522)
EM_BAR_BOX = Pixel(862, 522)
EM_ADV_BOX = Pixel(367, 522)

EM_POW_BUY = Pixel(542, 557)
EM_CAP_BUY = Pixel(703, 557)
EM_BAR_BUY = Pixel(864, 557)
EM_ADV_BUT = Pixel(367, 577)

EM_RICHA_BOX = Pixel(700, 450)
EM_RICHD_BOX = Pixel(860, 450)

EM_RICHA_BUY = Pixel(700, 490)
EM_RICHD_BUY = Pixel(860, 490)

#INFO
INFO = Pixel(100, 542)
MISC = Pixel(355, 200)

# PIXEL CHECKS
# TODO: CONVERT to ColorPixel of COLOR_
IS_BOSS_CROWN = ColorPixel(715, 277, 'F7EF29')
IS_ENEMY_ALIVE = ColorPixel(*HEALTH, ['D93030', 'EB3434', 'DB3131', 'DA3030']) # If you reduce the enemy healthbar to 1px, the color changes for some reason
IS_DEAD = ColorPixel(*HEALTH, ['EBEBEB', 'ECECEC'])
IS_ITOPOD_ACTIVE = ColorPixel(594, 277, '000000') # Checks color of pixel in "Floor x" text
IS_IDLE = ColorPixel(416, 86, 'FFEB04') # top right yellow pixel
IS_SAVE_READY = ColorPixel(*SAVE, '99FF99')
IS_PIT_READY = ColorPixel(*PIT_CHECK, '7FD23B')
IS_SPIN_READY = ColorPixel(*PIT_CHECK, 'FFD23B')
COLOR_CHALLENGE_ACTIVE = ColorPixel(391, 111, '000000')
COLOR_TM_LOCKED = ColorPixel(188, 257, '96A7B7')
COLOR_BM_LOCKED = ColorPixel(*BM_LOCKED, '96A7B7')
COLOR_BM_LOCKED_ALT = ColorPixel(*BM_LOCKED, '7B4A94')
COLOR_SPELL_READY = ColorPixel(*BM_LOCKED, 'BA13A7')
PLAYER_HEAL_THRESHOLD = ColorPixel(500, 410, 'FFFFFF')
QUESTING_IDLE_INACTIVE = ColorPixel(386, 555, '111111') # Pixel in the subcontracting button
COLOR_BM_AUTO_NUMBER = ColorPixel(*BM_AUTO_NUMBER, '000000')
COLOR_BM_AUTO_DROP = ColorPixel(*BM_AUTO_DROP, '000000')
COLOR_BM_AUTO_GOLD = ColorPixel(*BM_AUTO_GOLD, '000000')
COLOR_QUESTING_USE_MAJOR = ColorPixel(*QUESTING_USE_MAJOR, '000000')

HACKS = {1: Pixel(570, 230), 2: Pixel(890, 230),
         3: Pixel(570, 320), 4: Pixel(890, 320),
         5: Pixel(570, 415), 6: Pixel(890, 415),
         7: Pixel(570, 510), 8: Pixel(890, 510)}

HACK_PAGE_Y = 182
HACK_PAGE = [Pixel(335, HACK_PAGE_Y), Pixel(395, HACK_PAGE_Y)]
