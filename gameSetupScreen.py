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
    global playerCount
    global addPlayerButton
    global remPlayerButton
    playerCount = 4
    
    Object.startGroup()
    
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    
    #Play button
    playButton = Button(width*0.9, height*0.8, r.copy())
    playButton.releaseAction = startGame
    playButton.text = "Play"
    buttons = Object.endGroup()
    
    #Add player
    r = RoundRect(-25, -75, 200, 150, 25)
    r *= 0.5
    addPlayerButton = Button(width*0.1, height*0.2, r.copy())
    addPlayerButton.releaseAction = addPlayer
    addPlayerButton.text = "+"
    addPlayerButton.textSize = 40
    
    #Remove player
    remPlayerButton = Button(width*0.2, height*0.2, r.copy())
    remPlayerButton.releaseAction = remPlayer
    remPlayerButton.text = "-"
    remPlayerButton.textSize = 40
    
    #Rem player
    
    
    boxHeight = 0.7
    var = 1
    globals.textBoxDict["gameSetupScreen"] = []
    for i in range(1, 7):
        textBox = textInput.textBox(width/6, height*(1-boxHeight), 200, 50)
        textBox.text = "Player "+str(var)
        var+=1
        globals.textBoxDict["gameSetupScreen"].append(textBox)
        boxHeight -= 0.1
    
def draw():
    global playerCount
    
    pushStyle()
    pushMatrix()
    scale(*globals.baseScaleXY)
    for o in buttons:
        o.update()
    if playerCount < 6:
        addPlayerButton.update()
    if playerCount > 4:
        remPlayerButton.update()
        
        
    popMatrix()
    baseX, baseY = globals.baseScaleXY
    
    textSize(40*baseX)
    text("Enter your name!", width*0.01, height*0.1)
    textSize(30*baseX)
    
    textHeight = 0.65
    print(playerCount)
    for player in range(0, playerCount):
        textBox = globals.textBoxDict["gameSetupScreen"][player]
        text("Player "+str(player+1), width*0.01, height*(1-textHeight))
        textHeight-=0.1
        textBox.draw()
    popStyle()
    
def startGame(*args):
    if args[1] == LEFT:
        playerCount = 1
        for textBox in globals.textBoxDict["gameSetupScreen"]:
            globals.userConfig["players"][playerCount] = textBox.text
            playerCount +=1
        data.saveData()
        
        globals.currentMenu = "gameScreen"
        
def addPlayer(*args):
    print("add")
    global playerCount
    if playerCount != 6:
        playerCount+=1
    print(playerCount)
def remPlayer(*args):
    print("rem")
    global playerCount
    if playerCount != 4:
        playerCount-=1
    print(playerCount)
