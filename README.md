# NGU-scripts

This is a collection of functions I created for AHK and Python with the purpose of automating different aspects of the game [NGU-IDLE](https://www.kongregate.com/games/somethingggg/ngu-idle). This project first started because the built-in functions ControlClick/ControlSend in AHK did not work with the game, because of how Unity handles input. I first created replacements for these functions in AHK, but later moved over to Python because there was little reason to use AHK when the input was being sent directly via the Windows API.

### Features
You should use these functions if you want to create a script in AHK or Python that can run in the background. These functions will send input to the game without using your keyboard or mouse, and they don't require the window to be active.
The supplied functions found in ```functions.ahk``` or ```functions.py``` can help you create your own scripts to run. You can also see my implementations in the ```Python/Scripts/main.py``` file for inspiration of what you can do. This file changes as I progress myself and should only be used as a base for your own creations!

### Disclaimer
If you're automating the game using these or any other scripts, please consider disabling the high score submissions in the game settings.
