/*
  How do I use this?

  You can read about PostMessage here: https://autohotkey.com/docs/commands/PostMessage.htm
  
  I use WindowId as a global in my main script, you can send it into the function if you like as well
  by adding the parameter.

  This is a list of WMs (Window Messages): https://autohotkey.com/docs/misc/SendMessageList.htm

  And finally, the list of VKC's (Virtual-Key Codes): https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes

  Usage

  ControlSend2(string)
  ControlSend2("abcdefghijklmnopqrstuvwxyz 0123456789")

  Example from my boss sniping script

  Loop {
    if (GetTime(start, "minutes") >= duration) {
      ControlSend2("q")
      Break
    }
    
    h := PixelGetColor2(NguResolutionX + 716, NguResolutionY + 422, WindowId)
    if (h = 0xFF0000) {
      b := PixelGetColor2(NguResolutionX + 708, NguResolutionY + 287, WindowId)
      sleep, 100
      if (b = 0xF7EF29) {
        while (b = 0xF7EF29){
          b := PixelGetColor2(NguResolutionX + 708, NguResolutionY + 287, WindowId)
          ControlSend2("ytew")
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

  Contact: Satyric#9107 on Discord
*/

ControlSend2(str) {
  chars := {"a": 0x41, "b": 0x42, "c": 0x43, "d": 0x44, "e": 0x45, "f": 0x46, "g": 0x47, "h": 0x48
  , "i": 0x49, "j": 0x4A, "k": 0x4B, "l": 0x4C, "m": 0x4D, "n": 0x4E, "o": 0x4F, "p": 0x50, "q": 0x51
  , "r": 0x52, "s": 0x53, "t": 0x54, "u": 0x55, "v": 0x56, "w": 0x57, "x": 0x58, "y": 0x59, "z": 0x5A
  , " ": 0x20}
  numbers := {0: 0x30, 1: 0x31, 2: 0x32, 3: 0x33, 4: 0x34, 5: 0x35, 6: 0x36, 7: 0x37, 8: 0x38, 9: 0x39}
  Loop, parse, str
  {
    if (chars[A_LoopField]) {
      while (GetKeyState("Control") || GetKeyState("Alt")) {

        }     
      PostMessage, 0x100, % chars[A_LoopField],,, ahk_id %WindowId% ; key down
      PostMessage, 0x101, % chars[A_LoopField],,, ahk_id %WindowId% ; key up
      ;Sleep, 50
    }
    else {
      while (GetKeyState("Control") || GetKeyState("Alt")) {

        }     
      PostMessage, 0x101, % numbers[A_LoopField],,, ahk_id %WindowId% ; key up
      ;Sleep, 50
    }
  }
}