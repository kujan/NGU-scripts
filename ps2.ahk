/*
	PixelGetColor2 & PixelSearch2 - background edition by Satyric

	Requirements: Firefox browser (for real this time ;), the Gdip.ahk library found here

	https://autohotkey.com/boards/viewtopic.php?f=6&t=6517

	Why Firefox?

	The BitmapFromHWND, which allows this to function in the background takes a screenshot
	of the supplied window (hwnd), this does not work with directx applications, and some
	quick googling seems to say that firefox is built upon Skia, which is based on OpenGL.
	To see the difference for yourself you can uncomment the SaveBitmapToFile line and test
	with different browsers (I tested Edge/Chrome/Opera) they all gave me the title bar and
	a black screen.

	If Firefox is your main browser and you're having window focus issues while running these
	functions or ControlClick2, there's a simple fix for that on the NGU discord.

	Why would I use this?

	To add some more complexity to your background running scripts. This is essentially the
	exact same function as the PixelGetColor and PixelSearch in AHK, except it runs in the background.

	How do I use this?

	First off, you need to download the Gdip.ahk library linked above, this adds some functions
	we will be using. Add this at the top of your script.

	#Include Gdip.ahk

	Usage
	
	PixelGetColor2 - Returns RGB color of coords in hex.

	PixelGetcolor2(x-coord, y-coord, RGB color in hex, window id)
	color := PixelGetColor2(500, 600, 0x313131, WindowId)

	PixelSearch2

	Returns true/false if color was found within area. It's a row search (left -> right).
	It's using byref, so the supplied variables will contain the coordinates for the found
	pixel, or they will be empty if nothing was found.

	PixelSearch2(byref x-coord, byref y-coord, color in hex, area, window id)

	x = 710
	y = 670
	PixelSearch2(x, y, 0x313131, 40, hwnd) 
	MsgBox, %x%, %y%

	Notes

	Just like PixelSearch, this function is heavy on the CPU, don't start scanning crazy
	resolutions 

	Contact: Satyric#9107 on Discord
*/

PixelGetColor2(x, y, color, area=0, hwnd) {
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