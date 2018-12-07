from Object import Object
from Button import Button
from util import *
import globals
from util import *
from Button import Button
from Object import Object

buttons = None
def init():
    global buttons
    
    Object.startGroup()
    
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    
    #Play button
    playButton = Button(width*0.75, height*0.75, r.copy())
    playButton.releaseAction = gotoGameScreen
    playButton.text = "Play"
    
    buttons = Object.endGroup()
    
def draw():
    for o in buttons:
        o.update()
    
    
def gotoGameScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "gameScreen"
