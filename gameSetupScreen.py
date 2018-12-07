import globals
from util import *
from Button import Button
from Object import Object

def init():
    global buttons
    
    Object.startGroup()
    
    #Play button
    playButton = Button(width*0.75, height*0.75, RoundRect(-570/2,-114/2,570,114)*0.5)
    playButton.releaseAction = gotoGameScreen
    playButton.text = "Play"
    
    buttons = Object.endGroup()
    
def draw():
    global buttons
    for o in buttons:
        o.update()
    
    
def gotoGameScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "gameScreen"
