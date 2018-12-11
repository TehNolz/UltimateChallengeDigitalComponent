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
    
    #Settings button
    settingsButton = Button(width*0.25, height/2, r.copy())
    settingsButton.releaseAction = gotoSettingsScreen
    settingsButton.text = "Settings"
    
    #Play button
    playButton = Button(width*0.50, height/2, r.copy()*0.25)
    #playButton.releaseAction = gotoGameSetupScreen
    playButton.text = "Play"
    
    #Manual button
    manualButton = Button(width*0.75, height/2, r.copy())
    manualButton.releaseAction = gotoManualScreen
    manualButton.text = "Manual"
    
    buttons = Object.endGroup()
    for o in buttons:
        o.applyStyle('pulsate')
        o.pulseAmplitude = 0.1
    
    playButton.applyStyle('radio')
    
def draw():
    scale(*globals.baseScaleXY)
    global buttons
    for o in buttons:
        o.update()

#Goto menu functions
def gotoGameSetupScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "gameSetupScreen"
def gotoGameScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "gameScreen"
def gotoSettingsScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "settings"
def gotoManualScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "manual"
