import globals
from Object import Object
from Button import Button
from util import *

class mainMenu:
    def __init__(self):
        global playGame
        r = RoundRect(-150, -150, 300, 300, 50)
        r *= 1
        playGame = Button(width*0.25, height/2, r.copy())
        playGame.releaseAction = gotoGameScreen
        
        playGame = Button(width*0.50, height/2, r.copy())
        playGame.releaseAction = gotoSettingsScreen
        
        playGame = Button(width*0.75, height/2, r.copy())
        playGame.releaseAction = gotoManualScreen
        
    def draw(self):
        playGame.update()

def gotoGameScreen(*args):
    globals.currentMenu = "gamescreen"
def gotoSettingsScreen(*args):
    globals.currentMenu = "settings"
def gotoManualScreen(*args):
    globals.currentMenu = "manual"
