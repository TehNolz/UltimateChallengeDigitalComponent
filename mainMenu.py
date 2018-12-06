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
    playGame = Button(width*0.25, height/2, r.copy())
    playGame.releaseAction = gotoGameScreen
    playGame.text = "Play"
    
    playGame = Button(width*0.50, height/2, r.copy())
    playGame.releaseAction = gotoSettingsScreen
    
    playGame = Button(width*0.75, height/2, r.copy())
    playGame.releaseAction = gotoManualScreen
    buttons = Object.endGroup()
    
def draw():
    global buttons
    for o in buttons:
        o.update()

def gotoGameScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "gameScreen"
def gotoSettingsScreen(*args):
    globals.currentMenu = "settings"
def gotoManualScreen(*args):
    globals.currentMenu = "manual"
