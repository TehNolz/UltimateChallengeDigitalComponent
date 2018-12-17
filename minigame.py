from Object import Object
from Button import Button
from util import *
import globals
import textInput
from random import choice
currentCard = None

def init():
    # ######################
    # Misc stuff
    ######################
    global challengeActive
    challengeActive = False
    global playerButtonCheckboxes
    global playButton
    global players
    players = []
    global currentCard
    global minigameComplete
    minigameComplete = False
    global exitButton
    
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
    
    ######################
    # Dice stuff
    ######################
    global resultBoxes
    global dice
    global rolling
    rolling = False
    
    #Create dice result boxes
    resultBoxes = []
    boxHeight = 0.2
    for i in range(1, 7):
        textBox = textInput.textBox(width*0.2, 0, 50, 50, writable=False)
        resultBoxes.append(textBox)
        
    #Create dice
    r = RoundRect(-150, -150, 300, 300, 50)
    dice = Button(width*0.5, height*0.5, r.copy())
    dice.applyStyle("dice")
    dice.releaseAction = roll
    
    #Create exit button
    r *= 0.5
    exitButton = Button(width*0.9, height*0.8, r.copy())
    exitButton.releaseAction = gotoGameScreen
    exitButton.text = "Exit\nChallenge"
    
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    Object.startGroup()
    
    #Play button
    playButton = Button(width*0.5, height/2, r.copy())
    playButton.releaseAction = playMinigame
    playButton.text = "Play"
    
    ######################
    # Timer stuff
    ######################
    global startSec
    startSec=0
    global startMins
    startMins=0
    global scrnMins
    scrnMins=0
    global scrnSecs
    scrnSecs=0
    global restartSecs
    restartSecs=0
    global restartMins
    restartMins=0
    global stopTimer
    stopTimer = True
    global timeOffset
    timeOffset = 0
    global timeMemory
    timeMemory = 0
    
    offset = 0
    if "dice" in currentCard["minigame"]:
        offset+=0.25
    
    global startTimerButton
    r*=0.5
    startTimerButton = Button(width*(0.4+offset), height*0.8, r.copy())
    startTimerButton.releaseAction = startTimer
    startTimerButton.text = "Start"
    
    global pauseTimerButton
    pauseTimerButton = Button(width*(0.6+offset), height*0.8, r.copy())
    pauseTimerButton.releaseAction = pauseTimer
    pauseTimerButton.text = "Pause"
    
def draw():
    pushStyle()
    pushMatrix()
    #Misc
    global currentCard
    global challengeActive
    global playerButtonCheckboxes
    global playButton
    global players
    global playerCount
    global currentPlayer
    global minigameComplete
    global winner
    global exitButton
    
    #Dice
    global resultBoxes
    global dice
    global rolling
    global toRoll
    
    #Timer
    global restartSecs
    global restartMins
    global stopTimer
    global timeOffset
    global timeMemory
    global actualSecs
    global actualMins
    
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
            players = list(range(1, globals.playerCount+1))
            currentPlayer = choice(players)
            toRoll = players[:]

    else:
        print(currentCard)
        #Code for dice rolls
        if "dice" in currentCard["minigame"]:
            boxHeight = 0.2
            if len(players) > 1:
                for player in players:
                    text(globals.userConfig["players"][str(player)], width*0.08, height*boxHeight)
                    resultBoxes[player-1].y = height*(boxHeight-0.05)
                    resultBoxes[player-1].draw()
                    boxHeight+=0.1
            
            if minigameComplete:
                text(str(winner)+" wins the game!", width*0.35, height*0.1)
                dice.activators = {}
            else:
                text("Roll the dice, "+globals.userConfig["players"][str(currentPlayer)]+"!", width*0.35, height*0.1)
                dice.activators = {LEFT}
            dice.update()
            
            if rolling and not minigameComplete:
                if dice.throwdice == False:
                    rolling = False
                    resultBoxes[currentPlayer-1].text = dice.Rolldice
                    if currentCard["minigame"]["dice"]["mode"] == "FIRST":
                        if dice.Rolldice == currentCard["minigame"]["dice"]["target"]:
                            minigameComplete = True
                            winner = currentPlayer
                    
                    toRoll.remove(currentPlayer)
                    if len(toRoll) == 0:
                        minigameComplete = True
                        winner = checkWinner()
                    else:
                        currentPlayer = choice(toRoll)    

        elif "ticTacToe" in currentCard["minigame"]:
            pass
        elif "primeNumber" in currentCard["minigame"]:
            pass
        
        if "timer" in currentCard["minigame"]:
            pushMatrix()
            if "dice" in currentCard["minigame"]:
                translate(0, width, 0)
            
            actualSecs=(millis()-timeOffset)/1000
            print(actualSecs)
            actualMins=(millis()-timeOffset)/1000/60
            scrnSecs = actualSecs - restartSecs
            scrnMins = actualMins - restartMins
            
            if(actualSecs%60==0):
                restartSecs=actualSecs
                scrnSec=startSec
                
            textAlign(CENTER)
            fill(255)
            textSize(86)
            if stopTimer:
                # show memorized time
                stopTimeSec = timeMemory/1000
                stopTimeMin = timeMemory/1000/60
                
                text(nf(stopTimeMin, 2) + " : " + nf(stopTimeSec, 2), width/2, height/2)
            else:
                text(nf(scrnMins, 2) + " : " + nf(scrnSecs, 2), width/2, height/2)
            #restartButton
            startTimerButton.update()
            #pauseButton
            pauseTimerButton.update()

            if stopTimer == True:
                timeOffset = millis()
            popMatrix()
                    
        exitButton.update()
            
    popStyle()
    popMatrix()

######################
# TIMER
######################
def pauseTimer(*args):
    global timeMemory
    global stopTimer
    global timeOffset
    global pauseTimerButton
    global scrnSecs
    global scrnMins
    
    if stopTimer == False:
        timeMemory = millis()-timeOffset
        stopTimer = True
        pauseTimerButton.text = "Resume"
    else:
        scrnSecs = timeMemory/1000
        scrnMins = timeMemory/1000/60
        stopTimer = False
        pauseTimerButton.text = "Pause"
        
    
    
def startTimer(*args):
    global stopTimer
    global restartSecs
    global scrnSec
    global restartMins
    global scrnMins
    global actualSecs
    global actualMins
    global startTimerButton
    
    stopTimer = False
    restartSecs = actualSecs
    scrnSec = startSec
    restartMins = actualMins
    scrnMins = startMins
    startTimerButton.text = "Restart\nTimer"

######################
# DICE
######################
def roll(*args):
    global rolling
    rolling = True

######################
# MISC
######################
def checkWinner():
    global currentCard
    global resultBoxes
    global players
    global minigameComplete
    global challengeActive
    global toRoll
    global currentPlayer
    
    if currentCard["minigame"]["dice"]["target"] == "HIGHEST":
        var = 0
        for box in resultBoxes:
            if int(box.text) > var:
                var = int(box.text)
    elif currentCard["minigame"]["dice"]["target"] == "LOWEST":
        var = 999999999999
        for box in resultBoxes:
            if int(box.text) < var:
                var = int(box.text)
    
    if currentCard["minigame"]["dice"]["mode"] == "FIRST":
        winners = players
    else:
        winners = []
        for box in resultBoxes:
            if int(box.text) == var:
                winners.append(resultBoxes.index(box)+1)
                
    if len(winners) > 1:
        minigameComplete = False
        challengeActive = True
        players = winners
        currentPlayer = choice(players)
        toRoll = players[:]
        for box in resultBoxes:
            box.text = ""
        
        return None
    else:
        return winners[0]

def playMinigame(*args):
    global challengeActive
    global playerCount
    global players
    global currentPlayer
    if len(players) == playerCount:
        currentPlayer = choice(players)
        challengeActive = True
        toRoll = players[:]
    
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
        
def gotoGameScreen(*args):
    init()
    if args[1] == LEFT:
        globals.currentMenu = "gameScreen"