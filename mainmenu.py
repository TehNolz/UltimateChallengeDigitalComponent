import globals
from Object import Object
from Button import Button
from util import *

def init():
    global playGame
    global buttons
    
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    Object.startGroup()
    settingsButton = Button(width*0.25, height/2, r.copy())
    settingsButton.releaseAction = gotoSettingsScreen
    settingsButton.text = "Settings"
    
    playButton = Button(width*0.50, height/2, r.copy())
    playButton.releaseAction = gotoGameScreen
    playButton.text = "Play"
    
    manualButton = Button(width*0.75, height/2, r.copy())
    manualButton.releaseAction = gotoManualScreen
    manualButton.text = "Manual"
    buttons = Object.endGroup()
    
def draw():
    global buttons
    for o in buttons:
        o.update()

def gotoGameScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "gameScreen"
def gotoSettingsScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "settings"
def gotoManualScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "manual"
