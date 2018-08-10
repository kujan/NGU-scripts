/*

NGU Idle Multi script

Version 0.1

I created this for myself but figured it might be of some use to someone else.
As this is made for my own personal use, it's missing a lot of features that I have
yet to unlock myself in the game, which is why you might think this script is very
limited.

Another neat feature is that I've avoided using the normal click/keysend features which
practically "steals" your mouse and makes your computer unusable while running, this
means that this script can be run in the background.

Features execute in the following order

Merge gear -> boost gear -> merge inventory -> boost inventory (boost inventory requires merge to be active as well because reasons) -> boost cube


TODO:

Delete mode, delete all items in slots not being automerged. (poor mans improved lootfilter)
Rebirth mode, current plan is to add 1 hour first because it's what's most useful to me.
Better NGU support

NOTES:

Make sure you're in idle mode in adventure.
No Ygg seed planting is supported nor planned, use the EXP shop for autoplanting.
CTRL + E - Show GUI
CTRL - ESC - Exit

*/
#Include Gdip.ahk
#SingleInstance force
#NoEnv
global WinTitle = "Play NGU IDLE"

global NguResolutionX = 0
global NguResolutionY = 0
global EnergyAssigned := false
global MagicAssigned := false

;menu offsets
global MenuOffsetX = 230
global FightBossMenuOffsetY = 75
global PitMenuOffsetY = 105
global AdventureMenuOffsetY = 135
global InventoryMenuOffsetY = 165
global AugmentationMenuOffsetY = 195
global AdvTrainingMenuOffsetY = 225
global TimeMachineMenuOffsetY = 255
global BloodMagicMenuOffsetY = 285
global WanadoosMenuOffsetY = 315
global NguMenuOffsetY = 345
global YggdrasilMenuOffsetY = 375
global BeardMenuOffsetY = 405
global NumberInputBoxX = 345
global NumberInputBoxY = 50

;fight boss offsets

global NukeX = 620
global NukeY = 110
global FightX = 620
global FightY = 220

;inventory offsets
global Accessory1OffsetX = 480
global Accessory1OffsetY = 65
global Accessory2OffsetX = 480
global Accessory2OffsetY = 112
global Accessory3OffsetX = 0
global Accessory4OffsetX = 0
global HeadOffsetX = 525
global HeadOffsetY = 65
global ChestOffsetX = 527
global ChestOffsetY = 114
global LegsOffsetX = 527
global LegsOffsetY = 163
global BootsOffsetX = 527
global BootsOffsetY = 212
global WeaponOffsetX = 575
global WeaponOffsety = 115
global CubeOffsetX = 627
global CubeOffsetY = 115

;time machine offsets
global TmSpeedX = 532
global TmSpeedY = 233
global TmMultX = 532
global TmMultY = 330

;blood magic offsets

global BmX = 495
global Bm1 = 228
global Bm2 = 263
global Bm3 = 298
global Bm4 = 333
global Bm5 = 369
global Bm6 = 403
global Bm7 = 438
global Bm8 = 473

global BmSpellsX = 395
global BmSpellsY = 115

;Augmentation offsets
global AugmentX = 535
global AugmentScissorsY = 265
global AugmentDScissorsY = 292

global Times := { Augmentations: 15, TimeMachine: 0, BloodMagic: 15, NGU: 40, AdvTraining: 40}
global Ratios := { Augmentations: 1, TimeMachine: 1, BloodMagic: 1, NGU: 0, AdvTraining: 0.1}

global eCap := 11500000
global mCap := 400000
global eSpeed := 18875
global mSpeed := 650

;NGU offsets

global NguX := 530
global Ngu1Y := 243
global Ngu2Y := 278
global Ngu3Y := 313
global Ngu4Y := 349
global Ngu5Y := 384
global Ngu6Y := 453

;AdvTraining offsets

global AdvTrainingX := 890
global AdvTraining1Y := 230
global AdvTraining2Y := 270
global AdvTraining3Y := 310
global AdvTraining4Y := 350
global AdvTraining5Y := 390

;yggdrasil offsets

global HarvestX := 814
global HarvestY := 450
global Fruit1X := 350
global Fruit1Y := 180
global Fruit2X := 560
global Fruit2Y := 180
global Fruit3X := 775
global Fruit3Y := 180
global Fruit4X := 350
global Fruit4Y := 270
global Fruit5X := 560
global Fruit5Y := 270
global Fruit6X := 775
global Fruit6Y := 270
global Fruit7X := 350
global Fruit7Y := 370
global Fruit8X := 560
global Fruit8Y := 370
global Fruit9X := 775
global Fruit9Y := 370

;rebirth offsets
global RebirthX := 90
global RebirthY := 420
global RebirthButtonX := 545
global RebirthButtonY := 520
global RebirthConfirmX := 425 
global RebirthConfirmY := 320
global AdventureZone := 6

;pit offsets

global PitConfirmX := 437
global PitConfirmY := 317

;Press Escape to end the script
^Esc::ExitApp 

; Press CTRL+e to start
^e:: 
if (IsRunning) {
  return
}
IsRunning := True

IfWinNotExist, Play NGU IDLE
{
  MsgBox, Error: Could not detect NGU Idle window
  exit
}

WinActivate, Play NGU IDLE
WinGet, WindowId, ID, A
;WindowId := WinExist("A")
WinGetPos,,,WinW,WinH 
global WinW := WinW
global WinH := WinH
global WindowId := WindowId
Sleep, 500
CoordMode, Pixel, Screen
;FF: 6386A5
;opera: 0x6983A3
PixelSearch, NguResolutionX, NguResolutionY, 0, 0, %WinW%, %WinH%, 0x6386A5, 1, Fast RGB
if (ErrorLevel = 2) {
  MsgBox Couldn't do image search (game.png), do you have the image files in the correct folder?
  ;exit
}
else if (ErrorLevel = 1) {
  MsgBox Couldn't find pixel
  ;exit
}

ShowGUI:
  Gui Add, Text, Checked1 x10 y200 w300 h23 +0x200, Check the slots you want to automerge on page 1
  Gui Add, Text, Checked1 x30 y10 w300 h23 +0x200, Auto merge equipment
  Gui Add, Text, Checked1 x30 y30 w300 h23 +0x200, Auto boost equipment
  Gui Add, Text, Checked1 x30 y50 w300 h23 +0x200, Auto merge selected slots in page 1 inventory
  Gui Add, Text, x30 y70 w300 h23 r2 +0x200, Auto boost selected slots in page 1 inventory
  ;Gui Add, Text, x30 y90 w300 h23 r2 +0x200, Delete mode - trash all unchecked slots `n USE WITH CAUTION - Any unticked boxes below will be CTRL-Clicked
  Gui Add, Text, x30 y110 w300 h23 +0x200, Auto rebirth (background) This doesnt do anything currently

  Gui Add, CheckBox, vAutoMergeEquipment x10 y14 w15 h15, CheckBox
  Gui Add, CheckBox, vAutoBoostEquipment x10 y34 w15 h15, CheckBox
  Gui Add, CheckBox, vAutoMergeInventory x10 y54 w15 h15, CheckBox
  Gui Add, CheckBox, vAutoBoostInventory x10 y74 w15 h15, CheckBox
  Gui Add, CheckBox, vAutoRebirthBlind x10 y114 w15 h15, CheckBox
  ;Gui Add, CheckBox, vAutoDelete x10 y94 w15 h15, CheckBox

  i = 1
  xPos = 10
  yPos = 230

  ; Generate some checkboxes 
  while (i <= 60) {
    Gui Add, Checkbox, vinv%i% x%xPos% y%yPos% w15 h15, Checkbox
    xPos += 20
    if (Mod(i, 12) = 0) {
      xPos = 10
      yPos += 20
    }
    i++
  }

  Gui Add, Button, x90 y330 w80 h30 gButtonSubmit, Run
  Gui Show, w255 h370, Auto NGU by Satyric

  Return
ButtonSubmit:
  Gui, Submit
  if (AutoDelete = 1) {
    MsgBox, You have enabled Auto Delete, make sure you have protected any important items
  }
  Gui, Destroy

Loop {
  ;DoSnipe(11, 4)
  ;DoInventory()
  ;DoYgg()
  ;Rebirth(eCap, mCap, eSpeed, mSpeed, 30)

  /*

  3 min    0.00000
  4 min    0.00003
  5 min    0.00016
  7 min    0.00090
  10 min    0.00521
  12 min    0.02500
  15 min    0.06250
  30 min    0.25000
  1 hour    1.00000


  104 exp

  */
  
}


Navigate(target) {
  local x := NguResolutionX + MenuOffsetX
  local y := 0
  if (target = "inventory") {
    y := NguResolutionY + InventoryMenuOffsetY
  }
  else if (target = "timemachine") {
    y := NguResolutionY + TimeMachineMenuOffsetY
  }
  else if (target = "ngu") {
    y := NguResolutionY + NguMenuOffsetY
  }
  else if (target = "augmentations") {
    y := NguResolutionY + AugmentationMenuOffsetY
  }
  else if (target = "bloodmagic") {
    y := NguResolutionY + BloodMagicMenuOffsetY
  }
  else if (target = "advtraining") {
    y := NguResolutionY + AdvTrainingMenuOffsetY
  }
  else if (target = "adventure") {
    y := NguResolutionY + AdventureMenuOffsetY
  }
  else if (target = "yggdrasil") {
    y := NguResolutionY + YggdrasilMenuOffsetY
  }
  else if (target = "rebirth") {
    x := NguResolutionX + RebirthX
    y := NguResolutionY + RebirthY
  }
  else if (target = "pit") {
    y := NguResolutionY + PitMenuOffsetY
  }
  ControlClick2(x,y, "Left")
  return
}



ControlClick2(X, Y, Button) {  
  Sleep, 100
  PostMessage, 0x200, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_MOUSEMOVE
  Sleep, 100
  if (Button = "Left") {
    PostMessage, 0x201, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_LBUTTONDOWN 
    Sleep, 50
    PostMessage, 0x202, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_LBUTTONUP
  }
  
  else if (Button = "Right") { 
    PostMessage, 0x204, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_RBUTTONDOWN 
    Sleep, 50
    PostMessage, 0x205, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_RBUTTONUP  
  }
  else if (Button = "a") {
    PostMessage, 0x201, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_LBUTTONDOWN 
    Sleep, 50
    PostMessage, 0x202, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_LBUTTONUP    
    while (GetKeyState("Control") || GetKeyState("Alt")) {
      
      }  
    PostMessage, 0x100, 0x41,,, ahk_id %WindowId%
    Sleep, 50
    PostMessage, 0x101, 0x41,,, ahk_id %WindowId%
  }
  else if (Button = "d") {
    PostMessage, 0x201, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_LBUTTONDOWN 
    Sleep, 50
    PostMessage, 0x202, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_LBUTTONUP   
    while (GetKeyState("Control") || GetKeyState("Alt")) {
      
    }   
    PostMessage, 0x100, 0x44,,, ahk_id %WindowId%
    Sleep, 50
    PostMessage, 0x101, 0x44,,, ahk_id %WindowId%
  }
}

PixelGetColor2(x, y, hwnd) {
  If !pToken := Gdip_Startup()
    {
        MsgBox, 48, gdiplus error!, Gdiplus failed to start. Please ensure you have gdiplus on your system
        ExitApp
    }

  ;Gdip_BitmapFromHWND() creates a 8px border around the picture
  x += 8
  y += 8

  pBitmap:=GDIP_BitmapFromHWND(hwnd)
  ; uncomment the line below if you want to see what the function sees 
  ;GDIP_SaveBitmapToFile(pBitmap, "output.png", 100)
  ARGB := GDIP_GetPixel(pBitmap, x, y)
  SetFormat, Integer, Hex
  ;GetPixel returns ARGB, this removes the alpha
  RGB := ARGB & 0x00FFFFFF
  SetFormat, Integer, D
  GDIP_DisposeImage(pBitMap)
  GDIP_Shutdown(pToken)

  return RGB
}

PixelSearch2(byref x, byref y, color, area, hwnd) {
  If !pToken := Gdip_Startup()
  {
      MsgBox, 48, gdiplus error!, Gdiplus failed to start. Please ensure you have gdiplus on your system
      ExitApp
  }

  ;Gdip_BitmapFromHWND() creates a 8px border around the picture
  x += 7
  y += 7
  startX := x
  pBitmap:=GDIP_BitmapFromHWND(hwnd)
  Loop, %area%
  {
    x := startX
    Loop, %area% {
      ARGB := GDIP_GetPixel(pBitmap, x, y)
      SetFormat, Integer, Hex
      ;GetPixel returns ARGB, this removes the alpha
      RGB := ARGB & 0x00FFFFFF
      SetFormat, Integer, D
      if (RGB = color) {
        return True
      }
      x += 1
    }
    y += 1
  }
  x =
  y = 
  GDIP_DisposeImage(pBitMap)
  GDIP_Shutdown(pToken)
  return False
}

SendString(str) {
  global

  KeyCodes := {"a": 0x41, "d": 0x44, "e": 0x45, "q": 0x51, "r": 0x52, "t": 0x54, "w": 0x57, "y": 0x59, 0: 0x30, 1: 0x31, 2: 0x32, 3: 0x33
      , 4: 0x34, 5: 0x35, 6: 0x36, 7: 0x37, 8: 0x38, 9: 0x39}

  Loop, parse, str
  {
    c := A_LoopField
    if (c = "a" or c = "d" or c = "r" or c = "t" or c = "y" or c = "e" or c = "w" or c = "q") {
        while (GetKeyState("Control") || GetKeyState("Alt")) {
          Sleep, 50
        }     
        PostMessage, 0x100, % KeyCodes[A_LoopField],,, ahk_id %WindowId% ; key down
        Sleep, 25
    }
    PostMessage, 0x101, % KeyCodes[A_LoopField],,, ahk_id %WindowId% ; key up
    Sleep, 50
  }
}

Rebirth(eCap, mCap, eS, mS, duration) {
  global

  DoRebirth()

  start := A_TickCount
  eT := Ceil(eCap/eS/60)
  mT := Ceil(mCap/mS/60)

  DoFight()
  DoAdventure()
  Loop {
    DoInventory()
    AssignEnergy()
    AssignMagic()
    if (EnergyAssigned && MagicAssigned) {
      Loop {
        if (GetTime(start, "minutes") > 25 && !AdvancedTrainingAssigned) {
          DoAdvancedTraining()
          AdvancedTrainingAssigned := true
        }
        DoInventory()
        if (GetTime(start, "minutes") >= duration * 0.75 && !BossPush) {
          DoFight()
          DoAdventure()
          BossPush := true
        }
        if (GetTime(start, "minutes") >= duration) {
          DoFight()
          DoYgg()
          DoPit()
          Sleep, 15000
          EnergyAssigned := false
          MagicAssigned := false
          AdvancedTrainingAssigned := false
          BossPush := false
          return
        }
      }
    }
  }
}

DoPit() {
  Navigate("pit")
  Sleep, 50
  ControlClick2(NguResolutionX + 630, NguResolutionY + 290, "left")
  ControlClick2(NguResolutionX + PitConfirmX, NguResolutionY + PitConfirmY, "left")
}

DoRebirth() {
  Navigate("rebirth")
  ControlClick2(NguResolutionX + RebirthX, NguResolutionY + RebirthY, "left")
  ControlClick2(NguResolutionX + RebirthButtonX, NguResolutionY + RebirthButtonY, "left")
  ControlClick2(NguResolutionX + RebirthConfirmX, NguResolutionY + RebirthConfirmY, "left")
}

DoAdvancedTraining() {
  Navigate("advtraining")
  ControlClick2(NguResolutionX + NumberInputBoxX, NguResolutionY + NumberInputBoxY, "left")
  advE := Floor(ecap * Ratios["AdvTraining"] * 0.5)
  SendString(advE)
  ControlClick2(NguResolutionX + AdvTrainingX, NguResolutionY + AdvTraining1Y, "left")
  ControlClick2(NguResolutionX + AdvTrainingX, NguResolutionY + AdvTraining2Y, "left")
}

DoYgg() {
  Navigate("yggdrasil")
  ControlClick2(NguResolutionX + HarvestX, NguResolutionY + HarvestY, "left")

  
  /*
  ;manually clicks each individual eat/harvest button, useful to do just before rebirthing

  Loop, 9 
  {
    Sleep, 100
    ControlClick2(NguResolutionX + Fruit%A_Index%X, NguResolutionY + Fruit%A_Index%Y, "left")
  }
  */
  
}

DoAdventure() {
  Navigate("adventure")

  ;make sure we are in spawn for debugging purposes
  Loop, 20
  {
    PostMessage, 0x100, 0x25,,, ahk_id %WindowId% ; LEFT ARROW DOWN 
    Sleep, 25
    PostMessage, 0x101, 0x25,,, ahk_id %WindowId% ; LEFT ARROW UP
    Sleep, 25
  }

  ;TODO: itopod support, kill a mob for time machine then enter itopod(?)

  Loop, %AdventureZone%
  {
    PostMessage, 0x100, 0x27,,, ahk_id %WindowId% ; RIGHT ARROW DOWN 
    Sleep, 25
    PostMessage, 0x101, 0x27,,, ahk_id %WindowId% ; RIGHT ARROW UP
    Sleep, 25
  }
}

DoFight() {
  Navigate("fight")
  ControlClick2(NguResolutionX + MenuOffsetX, NguResolutionY + FightBossMenuOffsetY, "left")
  ControlClick2(NguResolutionX + NukeX, NguResolutionY + NukeY, "left")
  Sleep, 3000
  ControlClick2(NguResolutionX + FightX, NguResolutionY + FightY, "left")
}

DoSnipe(zone, duration) {
  Navigate("adventure")
  ;make sure we are in spawn for debugging purposes

  Loop, 20
  {
    PostMessage, 0x100, 0x25,,, ahk_id %WindowId% ; LEFT ARROW DOWN 
    Sleep, 25
    PostMessage, 0x101, 0x25,,, ahk_id %WindowId% ; LEFT ARROW UP
    Sleep, 25
  }
  ;move tooltip out of the way
  ControlClick2(NguResolutionX + 625, NguResolutionY + 335, "left")
  Loop, %zone%
  {
    PostMessage, 0x100, 0x27,,, ahk_id %WindowId% ; RIGHT ARROW DOWN 
    Sleep, 25
    PostMessage, 0x101, 0x27,,, ahk_id %WindowId% ; RIGHT ARROW UP
    Sleep, 25
  }

  i := PixelGetColor2(NguResolutionX + 430, NguResolutionY + 100, WindowId) 
  if (i != 0xF89B9B) {
    SendString("q")
  } 
  ;F89B9B idle active
  ;F7EF29 boss icon ´ff - 708, 287‏px
  ;FF0000 healthbar ff - 716, 422‏px

  start := A_TickCount
  Loop {
    if (GetTime(start, "minutes") >= duration) {
      SendString("q")
      Break
    }
    
    h := PixelGetColor2(NguResolutionX + 716, NguResolutionY + 422, WindowId)
    ;msgbox, %b%, %h%
    if (h = 0xFF0000) {
      b := PixelGetColor2(NguResolutionX + 708, NguResolutionY + 287, WindowId)
      sleep, 100
      if (b = 0xF7EF29) {
        ;d := PixelGetColor2(NguResolutionX + 713, NguResolutionY + 424, WindowId)
        while (b = 0xF7EF29){
          b := PixelGetColor2(NguResolutionX + 708, NguResolutionY + 287, WindowId)
          SendString("ytew")
          sleep, 150
        }
      }
      else {
        PostMessage, 0x100, 0x25,,, ahk_id %WindowId% ; LEFT ARROW DOWN 
        Sleep, 25
        PostMessage, 0x101, 0x25,,, ahk_id %WindowId% ; LEFT ARROW UP
        Sleep, 25
        PostMessage, 0x100, 0x27,,, ahk_id %WindowId% ; RIGHT ARROW DOWN 
        Sleep, 25
        PostMessage, 0x101, 0x27,,, ahk_id %WindowId% ; RIGHT ARROW UP
        Sleep, 25
      } 

    }
    sleep, 300
  }
  sleep, 300
}

GetTime(start, unit) {
  local Current := A_TickCount - start
  if (unit = "seconds") {
    return Floor(Current / 1000)
  }
  else if (unit = "minutes") {
    return Floor(Current / 60000)
  }
  else {
    return Current
  }
}

AssignEnergy() {
  local curE := GetTime(start, "seconds") * eSpeed
  ;local curE = 99999999999999
  if (curE < eCap) {
    Navigate("timemachine")
    Sleep, 200
    ControlClick2(NguResolutionX + NumberInputBoxX, NguResolutionY + NumberInputBoxY, "left")
    Sleep, 200
    SendString(eCap)
    Sleep, 200
    ControlClick2(NguResolutionX + TmSpeedX, NguResolutionY + TmSpeedY, "left")
  }
  else if (curE > eCap && GetTime(start, "minutes") >= Times["Augmentations"] && !EnergyAssigned) {
    ControlClick2(NguResolutionX + 10, NguResolutionY + 10, "left")
    sleep, 2000
    SendString("r")
    Navigate("augmentations")
    ControlClick2(NguResolutionX + NumberInputBoxX, NguResolutionY + NumberInputBoxY, "left")
    local eS := Floor(eCap * Ratios["Augmentations"] * 0.95)
    local eDs := Floor(eCap * Ratios["Augmentations"] * 0.05)
    SendString(eS)
    ControlClick2(NguResolutionX + AugmentX, NguResolutionY + AugmentScissorsY, "left")
    ControlClick2(NguResolutionX + NumberInputBoxX, NguResolutionY + NumberInputBoxY, "left")
    SendString(eDs)
    ControlClick2(NguResolutionX + AugmentX, NguResolutionY + AugmentDScissorsY, "left")

    Navigate("ngu")
    ControlClick2(NguResolutionX + NumberInputBoxX, NguResolutionY + NumberInputBoxY, "left")
    local nguE := Floor(ecap * Ratios["NGU"])
    SendString(nguE)
    ControlClick2(NguResolutionX + NguX, NguResolutionY + Ngu1Y, "left")

    EnergyAssigned := true
  }

}

AssignMagic() {
  local curM := GetTime(start, "seconds") * mSpeed

  if (curM < mCap) {
    Navigate("timemachine")
    ControlClick2(NguResolutionX + NumberInputBoxX, NguResolutionY + NumberInputBoxY, "left")
    Sleep, 100
    SendString(mCap)
    ControlClick2(NguResolutionX + TmMultX, NguResolutionY + TmMultY, "left")
  }
  else if (curM > mCap && GetTime(start, "minutes") >= Times["BloodMagic"] && !MagicAssigned) {
    SendString("t")
    Navigate("bloodmagic")
    ControlClick2(NguResolutionX + NumberInputBoxX, NguResolutionY + NumberInputBoxY, "left")
    SendString(mCap)
    ControlClick2(NguResolutionX + BmX, NguResolutionY + Bm2, "Left")
    /*
    loop, 8 {
      ControlClick2(NguResolutionX + BmX, NguResolutionY + Bm%A_Index%, "left")
    }
    */
    MagicAssigned := true

  }
}

DoInventory() {
  global
  Navigate("inventory")
  InInventory := false
  InvStartTime := A_TickCount
  loop { 
    t := A_TickCount - InvStartTime
    if (A_TickCount - InvStartTime >= 10000) {
       return
    }
    if (AutoMergeEquipment = 1) {
      ControlClick2(NguResolutionX + Accessory1OffsetX, NguResolutionY + Accessory1OffsetY, "d")
      ControlClick2(NguResolutionX + Accessory1OffsetX, NguResolutionY + Accessory2OffsetY, "d")
      ControlClick2(NguResolutionX + HeadOffsetX, NguResolutionY + HeadOffsetY, "d")
      ControlClick2(NguResolutionX + ChestOffsetX, NguResolutionY + ChestOffsetY, "d")
      ControlClick2(NguResolutionX + LegsOffsetX, NguResolutionY + LegsOffsetY, "d")
      ControlClick2(NguResolutionX + BootsOffsetX, NguResolutionY + BootsOffsetY, "d")
      ControlClick2(NguResolutionX + WeaponOffsetX, NguResolutionY + WeaponOffsetY, "d")
    }
    if (AutoBoostEquipment = 1) {
      ControlClick2(NguResolutionX + Accessory1OffsetX, NguResolutionY + Accessory1OffsetY, "a")
      ControlClick2(NguResolutionX + Accessory1OffsetX, NguResolutionY + Accessory2OffsetY, "a")
      ControlClick2(NguResolutionX + HeadOffsetX, NguResolutionY + HeadOffsetY, "a")
      ControlClick2(NguResolutionX + ChestOffsetX, NguResolutionY + ChestOffsetY, "a")
      ControlClick2(NguResolutionX + LegsOffsetX, NguResolutionY + LegsOffsetY, "a")
      ControlClick2(NguResolutionX + BootsOffsetX, NguResolutionY + BootsOffsetY, "a")
      ControlClick2(NguResolutionX + WeaponOffsetX, NguResolutionY + WeaponOffsetY, "a")
    }
    if (AutoMergeInventory) {
      i = 1
      xPos = 300
      yPos = 330
      row = 1

      while (i <= 60) {
        if (inv%i% = 1) {
          x := NguResolutionX + xPos + (i - (12 * (row - 1))) * 50
          y :=  NguResolutionY + yPos + ((row - 1) * 50)
          ControlClick2(x, y, "d")
          if (AutoBoostInventory) {
            ControlClick2(x, y, "a")
          }
        }
        else if (inv%i% = 1 && AutoDelete = 1) {
          ;TODO
        }
        if (Mod(i, 12) = 0) {
          row++
          }
        i++
      } 
    }
    ; boost cube last
    ;ControlClick2(NguResolutionX + CubeOffsetX, NguResolutionY + CubeOffsetY, "Right")
    if (AutoBoostCube = 1) {
      
    }  
  }
}
