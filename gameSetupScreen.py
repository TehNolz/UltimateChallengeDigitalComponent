from Object import Object
from Button import Button
from util import *
import globals
import textInput

buttons = None
def init():
    global buttons
    global box1
    global box2
    
    Object.startGroup()
    
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    
    #Play button
    playButton = Button(width*0.75, height*0.75, r.copy())
    playButton.releaseAction = gotoGameScreen
    playButton.text = "Play"
    buttons = Object.endGroup()
    
    box1 = textInput.textBox(width/2, height/2, 200, 50)
    box2 = textInput.textBox(width/4, height/2, 200, 50)
    
    globals.textBoxDict["gameSetupScreen"] = []
    globals.textBoxDict["gameSetupScreen"].append(box1)
    globals.textBoxDict["gameSetupScreen"].append(box2)
    
    
    
def draw():
    for o in buttons:
        o.update()
    
    box1.draw()
    box2.draw()
    
def gotoGameScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "gameScreen"
