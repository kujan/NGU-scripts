import math
#TOP LEFT COLOR

TOP_LEFT_COLOR = "000408"

# PERSONAL OFFSETS
XMULTI = 1065 / 960
YMULTI = 665 / 600

#ADVENTURE OFFSETS
RIGHTARROWX = math.floor(930 * XMULTI)
RIGHTARROWY = math.floor(220 * YMULTI)
LEFTARROWX = math.floor(325 * XMULTI)
LEFTARROWY = math.floor(225 * YMULTI)
ITOPODX = math.floor(405 * XMULTI)
ITOPODPERKSOFFSETX = math.floor(85 * XMULTI)
ITOPODY = math.floor(225 * YMULTI)
ITOPODSTARTX = math.floor(625 * XMULTI)
ITOPODSTARTY = math.floor(230 * YMULTI)
ITOPODENDX = math.floor(625 * XMULTI)
ITOPODENDY = math.floor(265 * YMULTI)
ITOPODENTERX = math.floor(625 * XMULTI)
ITOPODENTERY = math.floor(330 * YMULTI)
ITOPODAUTOX = math.floor(710 * XMULTI)
ITOPODAUTOY = math.floor(250 * YMULTI)
CROWNX = math.floor(705 * XMULTI)
CROWNY = math.floor(275 * YMULTI)
HEALTHX = math.floor(703 * XMULTI)
HEALTHY = math.floor(411 * YMULTI)
ABILITY_ATTACKX = math.floor(430 * XMULTI)
ABILITY_ATTACKY = math.floor(105 * YMULTI)
IDLE_BUTTONX = math.floor(330 * XMULTI)
IDLE_BUTTONY = math.floor(105 * YMULTI)
ITOPOD_ACTIVEX = math.floor(594 * XMULTI)
ITOPOD_ACTIVEY = math.floor(277 * YMULTI)
ITOPOD_ACTIVE_COLOR = "000000"
IDLECOLOR = "7C4E4E"
NOTDEAD = "EB3434"
ISBOSS = "F7EF29"
DEAD = "EBEBEB"

TITAN_PT = {"GRB": {"p": 1.3e3, "t": 1.3e3}, "GCT": {"p": 5e3, "t": 4e3},
            "jake": {"p": 1.4e4, "t": 1.2e4}, "UUG": {"p": 4e5, "t": 3e5},
            "walderp": {"p": 5.5e6, "t": 3.75e6},
            "BEAST1": {"p": 6e8, "t": 6e8}, "BEAST2": {"p": 6e9, "t": 6e9},
            "BEAST3": {"p": 6e10, "t": 6e10}, "BEAST4": {"p": 6e11, "t": 6e11}}

TITAN_ZONE = {"GRB": 7, "GCT": 9, "jake": 12, "UUG": 15, "walderp": 17,
              "BEAST1": 20, "BEAST2": 20, "BEAST3": 20, "BEAST4": 20}

ABILITY_ROW1X = math.floor(426 * XMULTI)
ABILITY_ROW2X = math.floor(321 * XMULTI)
ABILITY_ROW3X = math.floor(321 * XMULTI)
ABILITY_OFFSETX = math.floor(105 * XMULTI)
ABILITY_ROW1Y = math.floor(113 * YMULTI)
ABILITY_ROW2Y = math.floor(150 * YMULTI)
ABILITY_ROW3Y = math.floor(186 * YMULTI)

ABILITY_ROW1_READY_COLOR = "F89B9B"
ABILITY_ROW2_READY_COLOR = "6687A3"
ABILITY_ROW3_READY_COLOR = "C39494"

ABILITY_PRIORITY = {1: 6,  # Strong
                    2: 8,  # Parry
                    3: 9,  # Piercing
                    4: 10,  # Ultimate
                    5: 4,  # Block
                    6: 5,  # Defensive
                    9: 12 # Charge
                    }  # Paralyze

PLAYER_HEAL_THRESHOLDX = math.floor(512 * XMULTI)
PLAYER_HEAL_THRESHOLDY = math.floor(392 * YMULTI)
PLAYER_HEAL_COLOR = "FFFFFF"

OCR_ADV_POWX1 = math.floor(370 * XMULTI)
OCR_ADV_POWY1 = math.floor(296 * YMULTI)
OCR_ADV_POWX2 = math.floor(483 * XMULTI)
OCR_ADV_POWY2 = math.floor(313 * YMULTI)

OCR_ADV_TOUGHX1 = math.floor(406 * XMULTI)
OCR_ADV_TOUGHY1 = math.floor(313 * YMULTI)
OCR_ADV_TOUGHX2 = math.floor(506 * XMULTI)
OCR_ADV_TOUGHY2 = math.floor(330 * YMULTI)

OCR_ADV_TITANX1 = math.floor(560 * XMULTI)
OCR_ADV_TITANY1 = math.floor(277 * YMULTI)
OCR_ADV_TITANX2 = math.floor(685 * XMULTI)
OCR_ADV_TITANY2 = math.floor(330 * YMULTI)

OCR_ADV_ENEMY_CHECKX1 = math.floor(766 * XMULTI)
OCR_ADV_ENEMY_CHECKY1 = math.floor(382 * YMULTI)
OCR_ADV_ENEMY_CHECKX2 = math.floor(889 * XMULTI)
OCR_ADV_ENEMY_CHECKY2 = math.floor(403 * YMULTI)

OCR_COMBAT_LOGX1 = math.floor(310 * XMULTI)
OCR_COMBAT_LOGY1 = math.floor(496 * YMULTI)
OCR_COMBAT_LOGX2 = math.floor(600 * XMULTI)
OCR_COMBAT_LOGY2 = math.floor(589 * YMULTI)

#MENU OFFSETS
MENUITEMS = ["fight", "pit", "adventure", "inventory", "augmentations",
             "advtraining", "timemachine", "bloodmagic", "wandoos", "ngu",
             "yggdrasil", "digger", "beard"]

MENUOFFSETX = math.floor(230 * XMULTI)
MENUOFFSETY = math.floor(45 * YMULTI)
MENUDISTANCEY = math.floor(30 * YMULTI)
FIGHTBOSSMENUOFFSETY = math.floor(75 * YMULTI)
PITMENUOFFSETY = math.floor(105 * YMULTI)
ADVENTUREMENUOFFSETY = math.floor(135 * YMULTI)
INVENTORYMENUOFFSETY = math.floor(165 * YMULTI)
AUGMENTATIONMENUOFFSETY = math.floor(195 * YMULTI)
ADVTRAININGMENUOFFSETY = math.floor(225 * YMULTI)
TIMEMACHINEMENUOFFSETY = math.floor(255 * YMULTI)
BLOODMAGICMENUOFFSETY = math.floor(285 * YMULTI)
WANADOOSMENUOFFSETY = math.floor(315 * YMULTI)
NGUMENUOFFSETY = math.floor(345 * YMULTI)
YGGDRASILMENUOFFSETY = math.floor(375 * YMULTI)
BEARDMENUOFFSETY = math.floor(405 * YMULTI)
NUMBERINPUTBOXX = math.floor(375 * XMULTI)
NUMBERINPUTBOXY = math.floor(65 * YMULTI)
EXPX = math.floor(90 * XMULTI)
EXPY = math.floor(450 * YMULTI)
SAVEX = math.floor(23 * XMULTI)
SAVEY = math.floor(483 * YMULTI)
SAVE_READY_COLOR = "99FF99"
#FIGHT BOSS OFFSETS

NUKEX = math.floor(620 * XMULTI)
NUKEY = math.floor(110 * YMULTI)
FIGHTX = math.floor(620 * XMULTI)
FIGHTY = math.floor(220 * YMULTI)

#INVENTORY OFFSETS
EQUIPMENTSLOTS = {"head": {"x": math.floor(525 * XMULTI), "y": math.floor(65 * YMULTI)},
                  "chest": {"x": math.floor(527 * XMULTI), "y": math.floor(114 * YMULTI)},
                  "legs": {"x": math.floor(527 * XMULTI), "y": math.floor(163 * YMULTI)},
                  "boots": {"x": math.floor(527 * XMULTI), "y": math.floor(212 * YMULTI)},
                  "weapon": {"x": math.floor(575 * XMULTI), "y": math.floor(115 * YMULTI)},
                  "accessory1" : {"x": math.floor(480 * XMULTI), "y": math.floor(65 * YMULTI)},
                  "accessory2": {"x": math.floor(480 * XMULTI), "y": math.floor(115 * YMULTI)},
                  "accessory3": {"x": math.floor(480 * XMULTI), "y": math.floor(165 * YMULTI)},
                  "accessory4": {"x": math.floor(480 * XMULTI), "y": math.floor(215 * YMULTI)},
                  "cube": {"x": math.floor(627 * XMULTI), "y": math.floor(115 * YMULTI)}}

LOADOUTX = {1: math.floor(330 * XMULTI), 2: math.floor(360 * XMULTI), 3: math.floor(390 * XMULTI), 4: math.floor(420 * XMULTI), 5: math.floor(450 * XMULTI), 6: math.floor(480 * XMULTI), 7: math.floor(510 * XMULTI), 8: math.floor(540 * XMULTI), 9: math.floor(570 * XMULTI), 10: math.floor(600 * XMULTI)}
LOADOUTY = math.floor(255 * YMULTI)

INVENTORY_SLOTS_X = math.floor(300 * XMULTI)
INVENTORY_SLOTS_Y = math.floor(330 * YMULTI)
#TIME MACHINE OFFSETS
TMSPEEDX = math.floor(532 * XMULTI)
TMSPEEDY = math.floor(233 * YMULTI)
TMMULTX = math.floor(532 * XMULTI)
TMMULTY = math.floor(330 * YMULTI)
TMLOCKEDX = math.floor(188 * XMULTI)
TMLOCKEDY = math.floor(257 * YMULTI)
TMLOCKEDCOLOR = "97A8B5"
#BLOOD MAGIC OFFSETS
BMLOCKEDCOLOR = "97A8B5"
BM_PILL_READY = "BA13A7"
BMLOCKEDX = math.floor(229 * XMULTI)
BMLOCKEDY = math.floor(294 * YMULTI)
BMX = math.floor(570 * XMULTI)
BMY = {0: math.floor(228 * YMULTI), 1: math.floor(263 * YMULTI), 2: math.floor(298 * YMULTI), 3: math.floor(333 * YMULTI), 4: math.floor(369 * YMULTI), 5: math.floor(403 * YMULTI), 6: math.floor(438 * YMULTI), 7: math.floor(473 * YMULTI)}
BMSPELLX = math.floor(390 * XMULTI)
BMSPELLY = math.floor(115 * YMULTI)
BMPILLX = math.floor(744 * XMULTI)
BMPILLY = math.floor(216 * YMULTI)
BMNUMBERX = math.floor(400 * XMULTI)
BMNUMBERY = math.floor(220 * YMULTI)
BM_AUTO_NUMBERX = math.floor(514 * XMULTI)
BM_AUTO_NUMBERY = math.floor(222 * YMULTI)
BM_AUTO_GOLDX = math.floor(848 * XMULTI)
BM_AUTO_GOLDY = math.floor(308 * YMULTI)
BM_AUTO_DROPX = math.floor(514 * XMULTI)
BM_AUTO_DROPY = math.floor(360 * YMULTI)

#AUGMENTATION OFFSETS
AUGMENTX = math.floor(535 * XMULTI)
AUGMENTY = {"SS": math.floor(263 * YMULTI), "DS": math.floor(292 * YMULTI), "MI": math.floor(329 * YMULTI), "DTMT": math.floor(357 * YMULTI), "CI": math.floor(394 * YMULTI), "ML": math.floor(422 * YMULTI),
            "SM": math.floor(459 * YMULTI), "AA": math.floor(487 * YMULTI), "EB": math.floor(525 * YMULTI), "CS": math.floor(552 * YMULTI), "AE": math.floor(450 * YMULTI), "ES": math.floor(478 * YMULTI),
            "LS": math.floor(516 * YMULTI), "QSL": math.floor(544)}
AUGMENTSCROLLX = math.floor(945 * XMULTI)
AUGMENTSCROLLBOTY = math.floor(575 * YMULTI)
AUGMENTSCROLLTOPY = math.floor(264 * YMULTI)
SANITY_AUG_SCROLLX = math.floor(943 * XMULTI)
SANITY_AUG_SCROLLY_TOP = math.floor(261  * YMULTI)
SANITY_AUG_SCROLLY_BOT = math.floor(578  * YMULTI)
SANITY_AUG_SCROLL_COLORS = ["497C9F", "4C81A5", "4C80A4", "497B9E"]

#NGU OFFSETS

NGU_TARGETX = math.floor(635 * XMULTI)
NGU_TARGETY = math.floor(205 * YMULTI)
NGUMAGICX = math.floor(380 * XMULTI)
NGUMAGICY = math.floor(120 * YMULTI)
NGU_MINUSX = math.floor(565 * XMULTI)
NGU_MINUSY = math.floor(207 * YMULTI)
NGU_PLUSX = math.floor(529 * XMULTI)
NGU_PLUSY = math.floor(207 * YMULTI)

NGU_BAR_MINX = math.floor(306 * XMULTI)
NGU_BAR_MAXX = math.floor(503 * XMULTI)
NGU_BAR_Y = math.floor(215 * YMULTI)
NGU_BAR_OFFSETY = math.floor(35 * YMULTI)
NGU_BAR_WHITE = "FFFFFF"
NGU_BAR_GRAY = "FAFAFA"

#ADVTRAINING

ADV_TRAININGX = math.floor(890 * XMULTI)
ADV_TRAINING1Y = math.floor(230 * YMULTI)
ADV_TRAINING2Y = math.floor(270 * YMULTI)
ADV_TRAINING3Y = math.floor(310 * YMULTI)
ADV_TRAINING4Y = math.floor(350 * YMULTI)
ADV_TRAINING5Y = math.floor(390 * YMULTI)

#YGGDRASIL OFFSETS

HARVESTX = math.floor(814 * XMULTI)
HARVESTY = math.floor(450 * YMULTI)
FRUITSX = {1: math.floor(350 * XMULTI), 2: math.floor(560 * XMULTI), 3: math.floor(775 * XMULTI), 4: math.floor(350 * XMULTI), 5: math.floor(560 * XMULTI),
           6: math.floor(775 * XMULTI), 7: math.floor(350 * XMULTI), 8: math.floor(560 * XMULTI), 9: math.floor(775 * XMULTI)}
FRUITSY = {1: math.floor(180 * YMULTI), 2: math.floor(180 * YMULTI), 3: math.floor(180 * YMULTI), 4: math.floor(270 * YMULTI), 5: math.floor(270 * YMULTI),
           6: math.floor(270 * YMULTI), 7: math.floor(370 * YMULTI), 8: math.floor(370 * YMULTI), 9: math.floor(370 * YMULTI)}


#REBIRTH OFFSETS
REBIRTHX = math.floor(90 * XMULTI)
REBIRTHY = math.floor(420 * YMULTI)
REBIRTHBUTTONX = math.floor(545 * XMULTI)
REBIRTHBUTTONY = math.floor(520 * YMULTI)
CONFIRMX = math.floor(425  * XMULTI)
CONFIRMY = math.floor(320 * YMULTI)
CHALLENGEBUTTONX = math.floor(700 * XMULTI)
CHALLENGEBUTTONY = math.floor(520 * YMULTI)
CHALLENGEX = math.floor(380 * XMULTI)
CHALLENGEY = math.floor(152 * YMULTI)
CHALLENGEOFFSET = math.floor(30 * XMULTI)
CHALLENGEACTIVEX = math.floor(391 * XMULTI)
CHALLENGEACTIVEY = math.floor(111 * YMULTI)
CHALLENGEACTIVECOLOR = "000000"
#PIT OFFSETS
PITCOLORX = math.floor(195 * XMULTI)
PITCOLORY = math.floor(108 * YMULTI)
PITREADY = "7FD23B"
PITSPIN = "FFD23B"
PITX = math.floor(630 * XMULTI)
PITY = math.floor(290 * YMULTI)
PITCONFIRMX = math.floor(437 * XMULTI)
PITCONFIRMY = math.floor(317 * YMULTI)

SPIN_MENUX = math.floor(350 * XMULTI)
SPIN_MENUY = math.floor(50 * YMULTI)
SPINX = math.floor(713 * XMULTI)
SPINY = math.floor(562 * YMULTI)

#WANDOOS 626
WANDOOSENERGYX = math.floor(626 * XMULTI)
WANDOOSENERGYY = math.floor(252 * YMULTI)
WANDOOSMAGICX = math.floor(626 * XMULTI)
WANDOOSMAGICY = math.floor(350 * YMULTI)

#OCR OFFSETS

OCRBOSSX1 = math.floor(765 * XMULTI)
OCRBOSSX2 = math.floor(890 * XMULTI)
OCRBOSSY1 = math.floor(125 * YMULTI)
OCRBOSSY2 = math.floor(140 * YMULTI)

#PP OCR

PPX1 = math.floor(785 * XMULTI)
PPX2 = math.floor(901 * XMULTI)
PPY1 = math.floor(25 * YMULTI)
PPY2 = math.floor(43 * YMULTI)

#EXP OCR

EXPX1 = math.floor(340 * XMULTI)
EXPX2 = math.floor(900 * XMULTI)
EXPY1 = math.floor(70 * YMULTI)
EXPY2 = math.floor(95 * YMULTI)

OCR_POWX1 = math.floor(468 * XMULTI)
OCR_POWX2 = math.floor(616 * XMULTI)
OCR_POWY1 = math.floor(303 * YMULTI)
OCR_POWY2 = math.floor(330 * YMULTI)

OCR_CAPX1 = math.floor(627 * XMULTI)
OCR_CAPX2 = math.floor(776 * XMULTI)
OCR_CAPY1 = math.floor(303 * YMULTI)
OCR_CAPY2 = math.floor(330 * YMULTI)

OCR_BARX1 = math.floor(787 * XMULTI)
OCR_BARX2 = math.floor(937 * XMULTI)
OCR_BARY1 = math.floor(303 * YMULTI)
OCR_BARY2 = math.floor(330 * YMULTI)

OCR_ECAPX1 = math.floor(9 * XMULTI)
OCR_ECAPX2 = math.floor(165 * XMULTI)
OCR_ECAPY1 = math.floor(44 * YMULTI)
OCR_ECAPY2 = math.floor(63 * YMULTI)

OCR_EXPX1 = math.floor(510 * XMULTI)
OCR_EXPX2 = math.floor(928 * XMULTI)
OCR_EXPY1 = math.floor(365 * YMULTI)
OCR_EXPY2 = math.floor(400 * YMULTI)

OCR_NGU_E_X1 = math.floor(820 * XMULTI)
OCR_NGU_E_X2 = math.floor(940 * XMULTI)
OCR_NGU_E_Y1 = math.floor(190 * YMULTI)
OCR_NGU_E_Y2 = math.floor(219 * YMULTI)

#STATS OCR

OCR_ENERGY_X1 = math.floor(12 * XMULTI)
OCR_ENERGY_X2 = math.floor(165 * XMULTI)
OCR_ENERGY_Y1 = math.floor(28 * YMULTI)
OCR_ENERGY_Y2 = math.floor(50 * YMULTI)

OCR_MAGIC_X1 = math.floor(12 * XMULTI)
OCR_MAGIC_X2 = math.floor(165 * XMULTI)
OCR_MAGIC_Y1 = math.floor(70 * YMULTI)
OCR_MAGIC_Y2 = math.floor(90 * YMULTI)

#OCR CHALLENGES

OCR_CHALLENGE_NAMEX1 = math.floor(465 * XMULTI)
OCR_CHALLENGE_NAMEX2 = math.floor(750 * XMULTI)
OCR_CHALLENGE_NAMEY1 = math.floor(87 * YMULTI)
OCR_CHALLENGE_NAMEY2 = math.floor(104 * YMULTI)

OCR_CHALLENGE_24HC_TARGETX1 = math.floor(479 * XMULTI)
OCR_CHALLENGE_24HC_TARGETX2 = math.floor(771 * XMULTI)
OCR_CHALLENGE_24HC_TARGETY1 = math.floor(267 * YMULTI)
OCR_CHALLENGE_24HC_TARGETY2 = math.floor(297 * YMULTI)

#BEARD OFFSETS

BEARD_X = {1: math.floor(312 * XMULTI), 2: math.floor(338 * XMULTI), 3: math.floor(312 * XMULTI), 4: math.floor(1 * XMULTI)}

#DIGGER OFFSETS

DIG_PAGEX = [math.floor(340 * XMULTI), math.floor(405 * XMULTI), math.floor(470 * XMULTI)]
DIG_PAGEY = math.floor(110 * YMULTI)
DIG_ACTIVE = {1: {"x": math.floor(341 * XMULTI), "y": math.floor(237 * YMULTI)}, 2: {"x": math.floor(658 * XMULTI), "y": math.floor(237 * YMULTI)}, 3: {"x": math.floor(341 * XMULTI), "y": math.floor(427 * YMULTI)}, 4: {"x": math.floor(658 * XMULTI), "y": math.floor(427 * YMULTI)}}
DIG_CAP = {1: {"x": math.floor(550 * XMULTI), "y": math.floor(185 * YMULTI)}, 2: {"x": math.floor(865 * XMULTI), "y": math.floor(185 * YMULTI)}, 3: {"x": math.floor(550 * XMULTI), "y": math.floor(375 * YMULTI)}, 4: {"x": math.floor(865 * XMULTI), "y": math.floor(375 * YMULTI)}}


#EXP COSTS PER UNIT
EPOWER_COST = 150
ECAP_COST = 0.004
EBAR_COST = 80
MPOWER_COST = 450
MCAP_COST = 0.012
MBAR_COST = 240

#EXP MENU
EMENUX = math.floor(350 * XMULTI)
EMENUY = math.floor(110 * YMULTI)
EMBOXY = math.floor(522 * YMULTI)
EMPOWBOXX = math.floor(537 * XMULTI)
EMCAPBOXX = math.floor(707 * XMULTI)
EMBARBOXX = math.floor(862 * XMULTI)
EMBUYY = math.floor(557 * YMULTI)
EMPOWBUYX = math.floor(542 * XMULTI)
EMCAPBUYX = math.floor(703 * XMULTI)
EMBARBUYX = math.floor(864 * XMULTI)

MMENUX = math.floor(420 * XMULTI)
MMENUY = math.floor(110 * YMULTI)

#INFO

INFOX = math.floor(84 * XMULTI)
INFOY = math.floor(542 * YMULTI)
MISCX = math.floor(355 * XMULTI)
MISCY = math.floor(200 * YMULTI)
