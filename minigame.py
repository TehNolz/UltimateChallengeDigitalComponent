from Object import Object
from Button import Button
from util import *
import globals
import textInput

currentCard = None
def init():
    global challengeActive
    global playerButtonCheckboxes
    global playButton
    global players
    challengeActive = False
    players = []
    
    #Create checkboxes
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    buttonHeight = 0.2
    Object.startGroup()
    for i in range(1, 7):
        button = Button(width*0.3, height*buttonHeight, r.copy()*0.2)
        button.applyStyle('checkbox')
        button.boxColor = color(0,0,0, 128)
        button.name = i
        buttonHeight += 0.1
        button.releaseAction = checkPlayerCount
    playerButtonCheckboxes = Object.endGroup()
    
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    Object.startGroup()
    
    #Play button
    playButton = Button(width*0.5, height/2, r.copy())
    playButton.releaseAction = playMinigame
    playButton.text = "Play"
    
def draw():
    global currentCard
    global challengeActive
    global playerButtonCheckboxes
    global playButton
    global players
    global playerCount
    
    #Debug
    currentCard = {
        "id": "expansion1-1",
        "back": "card-expansion1-back",
        "showStart": True,
        "minigame": globals.cardConfig["expansion1"]["expansion1-1"]
    }
    globals.playerCount = 6
    #End of debug
    
    if not challengeActive:
        playerCount = None
        if "dice" in currentCard["minigame"]:
            playerCount = currentCard["minigame"]["dice"]["players"]
        elif "ticTacToe" in currentCard["minigame"]:
            playerCount = currentCard["minigame"]["ticTacToe"]
        
        if 6 > playerCount > 1:
            textheight = 0.2
            var = playerCount-len(players)
            if var == 1:
                text("Who will play? Pick "+str(var)+" player.",  width*0.16, height*0.1)
            elif var == 0:
                text("Press play to continue.",  width*0.16, height*0.1)
            else:
                text("Who will play? Pick "+str(var)+" players.", width*0.16, height*0.1)
            for player in range(0, globals.playerCount):
                text(globals.userConfig["players"][str(player+1)], width*0.15, height*textheight)
                playerButtonCheckboxes[player].update()
                textheight+= 0.1
                
            playButton.update()
        elif playerCount == None or playerCount == 6:
            challengeActive = True
            players = list(range(1, globals.playerCount))

    else:
        print(players)
        
def playMinigame(*args):
    global challengeActive
    global playerCount
    global players
    if len(players) == playerCount:
        challengeActive = True
    
def checkPlayerCount(*args):
    global players
    global playerCount
    if args[0].activated == True:
        if len(players) == playerCount:
            args[0].activated = False
        else:
            players.append(args[0].name)
    else:
        players.remove(args[0].name)
    print(players)
    print(playerCount)
