from Object import Object
from Button import Button
from util import *
import globals
import textInput
import data
import gameScreen

buttons = None
def init():
    global buttons
    global boxList
    global playerCount
    global addPlayerButton
    global remPlayerButton
    global baseToggle
    global exp1Toggle
    global exp2Toggle
    playerCount = 4
    
    Object.startGroup()
    
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    
    #Play button
    playButton = Button(width*0.9, height*0.8, r.copy())
    playButton.releaseAction = startGame
    playButton.text = "Play"
    
    baseToggle = Button(width*0.8, height*0.18, r.copy()*0.2)
    baseToggle.applyStyle('checkbox')
    baseToggle.boxColor = color(0,0,0, 255)
    baseToggle.releaseAction = toggleBase
    if "base" in globals.userConfig["settings"]["useDecks"]:
        baseToggle.activated = True
    
    exp1Toggle = Button(width*0.8, height*0.28, r.copy()*0.2)
    exp1Toggle.applyStyle('checkbox')
    exp1Toggle.boxColor = color(0,0,0, 255)
    exp1Toggle.releaseAction = toggleExp1
    if "expansion1" in globals.userConfig["settings"]["useDecks"]:
        exp1Toggle.activated = True
    
    exp2Toggle = Button(width*0.8, height*0.38, r.copy()*0.2)
    exp2Toggle.applyStyle('checkbox')
    exp2Toggle.boxColor = color(0,0,0, 255)
    exp2Toggle.releaseAction = toggleExp2
    if "expansion2" in globals.userConfig["settings"]["useDecks"]:
        exp2Toggle.activated = True
    
    buttons = Object.endGroup()
    
    #Add player
    r = RoundRect(-100, -65, 200, 130, 25)
    r *= 0.5
    addPlayerButton = Button(width*0.1, height*0.2, r.copy())
    addPlayerButton.releaseAction = addPlayer
    addPlayerButton.text = "Add \nplayer."
    addPlayerButton.textSize = 20
    
    #Remove player
    remPlayerButton = Button(width*0.2, height*0.2, r.copy())
    remPlayerButton.releaseAction = remPlayer
    remPlayerButton.text = "Remove \nplayer."
    remPlayerButton.textSize = 20

    #Create textboxes
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
    
    #Update buttons
    for o in buttons:
        o.update()
    if playerCount < 6:
        addPlayerButton.update()
    if playerCount > 4:
        remPlayerButton.update()
    popMatrix()
    
    baseX, baseY = globals.baseScaleXY
    
    #Header text
    textSize(40*baseX)
    text("Enter your name!", width*0.01, height*0.1)
    text("Use which decks?", width*0.5, height*0.1)
    
    #Add text boxes + text
    textSize(30*baseX)
    textHeight = 0.65
    for player in range(0, playerCount):
        textBox = globals.textBoxDict["gameSetupScreen"][player]
        text("Player "+str(player+1), width*0.01, height*(1-textHeight))
        textHeight-=0.1
        textBox.draw()
    
    text("Base Deck", width*0.5, height*0.2)
    text("Expansion Deck 1", width*0.5, height*0.3)
    text("Expansion Deck 2", width*0.5, height*0.4)
    
    popStyle()
    
def startGame(*args):
    global baseToggle
    global exp1Toggle
    global exp2Toggle
    
    if args[1] == LEFT:
        if len(globals.userConfig["settings"]["useDecks"]) > 0:
            for player in range(0, playerCount):
                textBox = globals.textBoxDict["gameSetupScreen"][player]
                globals.userConfig["players"][str(player)] = textBox.text
            
            data.saveData()
            globals.currentMenu = "gameScreen"
            gameScreen.newCard()
        else:
            pass
        
#Add/remove players.
def addPlayer(*args):
    global playerCount
    if playerCount != 6:
        playerCount+=1
def remPlayer(*args):
    global playerCount
    if playerCount != 4:
        playerCount-=1

#Toggle decks
def toggleBase(*args):
    toggleDeck("base")
def toggleExp1(*args):
    toggleDeck("expansion1")
def toggleExp2(*args):
    toggleDeck("expansion2")
    
def toggleDeck(deck):
    useDecks = globals.userConfig["settings"]["useDecks"]
    if deck in useDecks:
        print("rem")
        useDecks.remove(deck)
    else:
        print("add")
        useDecks.append(deck)
    print(useDecks)
    globals.userConfig["settings"]["useDecks"] = useDecks
