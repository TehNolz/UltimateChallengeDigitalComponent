from Object import Object
from Button import Button
from util import *
import globals
import textInput
import data

buttons = None
def init():
    global buttons
    global boxList
    
    Object.startGroup()
    
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    
    #Play button
    playButton = Button(width*0.75, height*0.75, r.copy())
    playButton.releaseAction = startGame
    playButton.text = "Play"
    buttons = Object.endGroup()
    
    boxHeight = 0.8
    playerCount = 1
    globals.textBoxDict["gameSetupScreen"] = []
    for i in range(1, 7):
        textBox = textInput.textBox(width/5, height*(1-boxHeight), 200, 50)
        textBox.text = "Player "+str(playerCount)
        playerCount+=1
        globals.textBoxDict["gameSetupScreen"].append(textBox)
        boxHeight -= 0.1
    
def draw():
    pushMatrix()
    scale(*globals.baseScaleXY)
    for o in buttons:
        o.update()
    popMatrix()
    
    textHeight = 0.77
    playerCount = 6
        
    for textBox in globals.textBoxDict["gameSetupScreen"]:
        text("Player "+str(playerCount), width*0.01, height*textHeight)
        textHeight-=0.1
        playerCount-=1
        textBox.draw()
    
def startGame(*args):
    if args[1] == LEFT:
        playerCount = 1
        for textBox in globals.textBoxDict["gameSetupScreen"]:
            globals.userConfig["players"][playerCount] = textBox.text
            playerCount +=1
        data.saveData()
        
        globals.currentMenu = "gameScreen"
