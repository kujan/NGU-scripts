/*
  ControlClick2 - made to work with NGU Idle by Satyric

  Why would I use this? 

  If you want to automate NGU Idle of course! Without having to install a VM in
  order to use your computer while it's running. The browser doesn't need to be 
  visible and the script can also run while the computer is locked, however
  the browser cannot be minimized. 

  If you plan to use PixelSearch or ImageSearch or similar functions,
  the window MUST be visible however. So I recommend doing this at the start 
  of your script and use coordinates and offsets for navigation. 
  If you're running a script that heavily relies on these functions you can
  either use WinActivate to bring it to the foreground or just have the browser
  visible on a second monitor for example.  

  How do I use this?

  You can read about PostMessage here: https://autohotkey.com/docs/commands/PostMessage.htm
  
  I use WindowId as a global in my main script, you can send it into the function if you like as well  

  This is a list of WMs (Window Messages): https://autohotkey.com/docs/misc/SendMessageList.htm

  And finally, the list of VKC's (Virtual-Key Codes): https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes

  So far I only wanted to left/right click and send the 'a' and 'd' keys for merging in the inventory
  so this function is very barebones, but it should be simple enough for you to expand with the links
  above. The sleeps are just arbitrary numbers I picked, you can optimize those further, if the values
  are too low the game might not register your clicks at the correct positions, so don't go too low.
  If your computer is slow I imagine you might need higher values than those used here.

  Usage

  ControlClick2(x-coord, y-coord, input)
  ControlClick2(500, 400, "d")

  This will move the mouse to 500,400 and left click (simply using mousemove only didn't work in my testing)
  and then send 'd' at the location (like when you merge stuff etc).

  Example from my own script

  ControlClick2(NguResolutionX + Accessory1OffsetX, NguResolutionY + Accessory1OffsetY, "d")
  ControlClick2(NguResolutionX + Accessory1OffsetX, NguResolutionY + Accessory2OffsetY, "d")
  ControlClick2(NguResolutionX + HeadOffsetX, NguResolutionY + HeadOffsetY, "d")
  ControlClick2(NguResolutionX + ChestOffsetX, NguResolutionY + ChestOffsetY, "d")
  ControlClick2(NguResolutionX + LegsOffsetX, NguResolutionY + LegsOffsetY, "d")
  ControlClick2(NguResolutionX + BootsOffsetX, NguResolutionY + BootsOffsetY, "d")
  ControlClick2(NguResolutionX + WeaponOffsetX, NguResolutionY + WeaponOffsetY, "d")

  Contact: Satyric#9107 on Discord
  
*/


ControlClick2(X, Y, Button) {  
  Sleep, 100
  PostMessage, 0x200, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_MOUSEMOVE
  Sleep, 100

  if (Button = "Left") {
    PostMessage, 0x201, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_LBUTTONDOWN 
    Sleep, 100
    PostMessage, 0x202, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_LBUTTONUP
  }
  
  else if (Button = "Right") { 
    PostMessage, 0x204, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_RBUTTONDOWN 
    Sleep, 100
    PostMessage, 0x205, 0, X&0xFFFF | Y<<16,, ahk_id %WindowId% ; WM_RBUTTONUP  
  }
}