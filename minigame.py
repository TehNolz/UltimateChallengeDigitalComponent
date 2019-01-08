from Object import Object
from Button import Button
from util import *
import globals
import textInput
from random import choice
currentCard = None

def init():
    width = 1133
    height = 600
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
    global nextMatchButton
    global startingDiceRoll
    startingDiceRoll = False
    
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
    global showTimeIsUpMsg
    showTimeIsUpMsg = False
    
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
    
    ######################
    # Tic Tac Toe
    ######################
    resetTicTacToe()
    
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    nextMatchButton = Button(width*0.7, height*0.8, r.copy())
    nextMatchButton.releaseAction = nextMatch
    nextMatchButton.text = "Next\nMatch"
    
def draw(mousePressed):
    width = 1133
    height = 600
    pushStyle()
    scale(*globals.baseScaleXY)
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
    global toSelect
    global exitButton
    global startingDiceRoll
    
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
    global showTimeIsUpMsg
    
    #TicTacToe
    global once
    global boarddict
    global winCondition
    global boardfull
    global brackets
    
    if startingDiceRoll:
        exitButton.text = "Start\nGame"
    
    textAlign(CENTER)
    if not challengeActive:
        playerCount = None
        if "dice" in currentCard["minigame"]:
            playerCount = currentCard["minigame"]["dice"]["players"]
        elif "ticTacToe" in currentCard["minigame"]:
            if currentCard["minigame"]["ticTacToe"]["mode"] == "1v6":
                playerCount = 1
            else:
                playerCount = currentCard["minigame"]["ticTacToe"]["players"]
        elif "timer" in currentCard["minigame"] and not "dice" in currentCard["minigame"]:
            playerCount = 1
            
        if 6 > playerCount > 1 or "ticTacToe" in currentCard["minigame"]:
            textheight = 0.2
            var = playerCount-len(players)
            fill(0, 0, 0, 255)
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
        elif playerCount == 1 or playerCount == 6:
            challengeActive = True
            players = [1]
            toRoll = players[:]
            currentPlayer = choice(players)
        if playerCount == 6:
            players = list(range(1, globals.playerCount+1))
            toRoll = players[:]

    else:
        fill(0, 0, 0, 255)
        
        ######################
        if "dice" in currentCard["minigame"]:
            boxHeight = 0.2
            if len(players) > 1:
                for player in players:
                    textSize(30)
                    text(globals.userConfig["players"][str(player)], width*0.08, height*boxHeight)
                    resultBoxes[player-1].y = height*(boxHeight-0.05)
                    resultBoxes[player-1].draw()
                    boxHeight+=0.1
            
            if minigameComplete:
                if len(players) > 1:
                    if startingDiceRoll:
                        text("The game starts with "+globals.userConfig["players"][str(winner)]+"'s turn!", width*0.35, height*0.1)
                    else:
                        text(globals.userConfig["players"][str(winner)]+" wins the game!", width*0.35, height*0.1)
                else:
                    text("You win the game!", width*0.35, height*0.1)
                dice.activators = {}
            else:
                if len(players) > 1:
                    text("Roll the dice, "+globals.userConfig["players"][str(currentPlayer)]+"!", width*0.35, height*0.1)
                else:
                    text("Roll the dice!", width*0.35, height*0.1)
                dice.activators = {LEFT}
            dice.update()
            
            if rolling and not minigameComplete:
                if dice.throwdice == False:
                    rolling = False
                    resultBoxes[currentPlayer-1].text = dice.Rolldice
                    
                    winner = checkWinner()


        elif "ticTacToe" in currentCard["minigame"]:
            textAlign(LEFT)
            pushMatrix()
            text(globals.userConfig["players"][str(currentPlayer)]+"'s turn!", 105, 40)
            field()
            
            if moves == False:
                if mousePressed and not once:
                    x = int((mouseX - 75)/50)
                    y = int((mouseY - 75)/50)
                    if x < 3 and x > -1 and y > -1 and y < 4:
                        if boarddict[x][y] == 0:
                            once = True
                            icons.append((x*50, y*50, currentPlayer))
                            boarddict[x][y] = currentPlayer

                            if currentPlayer == brackets[0][0]:
                                currentPlayer = brackets[0][1]
                                        
                            elif currentPlayer == brackets[0][1]:
                                currentPlayer = brackets[0][0]
                
                elif not mousePressed and once:
                    once = False
                    
            #Win conditions
            c = boarddict
            if c[0][0] == c[0][1] and c[0][1] == c[0][2]:
                if c[0][0] != 0:
                    winConditions()
                    line(25,0,25,150)
                    
            if c[1][0] == c[1][1] and c[1][1] == c[1][2]:
                if c[1][0] != 0:
                    winConditions()
                    line(75,0,75,150)
                    
            if c[2][0] == c[2][1] and c[2][1] == c[2][2]:
                if c[2][0] != 0:
                    winConditions()
                    line(125,0,125,150)
                    
            if c[0][0] == c[1][0] and c[1][0] == c[2][0]:  
                if c[0][0] != 0:
                    winConditions()
                    line(0,25,150,25)
                    
            if c[0][1] == c[1][1] and c[1][1] == c[2][1]:
                if c[0][1] != 0:
                    winConditions()
                    line(0,75,150,75)
                    
            if c[0][2] == c[1][2] and c[1][2] == c[2][2]:
                if c[0][2] != 0:
                    winConditions()
                    line(0,125,150,125)
                    
            if c[0][0] == c[1][1] and c[1][1] == c[2][2]:
                if c[0][0] != 0:
                    winConditions()
                    line(0,0,150,150)
                    
            if c[0][2] == c[1][1] and c[1][1] == c[2][0]:
                if c[0][2] != 0:
                    winConditions()
                    line(150,0,0,150)
            
            boardfull = True
            for x in boarddict.values():
                if 0 in x.values():
                    boardfull = False
            if boardfull:
                Boardfull()
                
            text(globals.userConfig["players"][str(brackets[0][0])] +" vs "+globals.userConfig["players"][str(brackets[0][1])], 0,250)
                
            popMatrix()
        ######################
        elif "primeNumber" in currentCard["minigame"]:
            pass
        
        ######################
        if "timer" in currentCard["minigame"]:
            pushMatrix()
            #if "dice" in currentCard["minigame"]:
            #    translate(0, 0, 0)
            
            actualSecs=(millis()-timeOffset)/1000
            actualMins=(millis()-timeOffset)/1000/60
            scrnSecs = actualSecs - restartSecs
            scrnMins = actualMins - restartMins
            
            if(actualSecs%60==0):
                restartSecs=actualSecs
                scrnSec=startSec
                
            textAlign(CENTER)
            fill(0, 0, 0)
            textSize(100)
            
            if currentCard["minigame"]["timer"] == actualSecs:
                showTimeIsUpMsg = True
                timeMemory = millis()-timeOffset
                stopTimer = True
                pauseTimerButton.text = "Pause"
                if "dice" in currentCard["minigame"]:
                    dice.activators = {}
            
            if stopTimer:
                if showTimeIsUpMsg:
                    text("Time's up!", width/2, height*0.2)
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
# TICTACTOE
######################
def resetTicTacToe():
    global once
    once = False
    global moves
    moves = False
    global icons
    icons = list()
    global boarddict
    boarddict = {
        0:{
            0: 0,
            1: 0,
            2: 0,
        },
        1:{
            0: 0,
            1: 0,
            2: 0,
        },
        2:{
            0: 0,
            1: 0,
            2: 0,
        }
    }

def Boardfull():
    global boarddict, icons, moves
    
    strokeWeight(2)
    stroke(255,0,0)
    moves = True
    
    text("It's a draw!", 0,200)

def field():
    global brackets
    
    strokeWeight(4)
    stroke(0)
    
    translate(75,75)
    line(0,50,150,50)
    line(0,100,150,100)
    line(50,0,50,150)
    line(100,0,100,150)
    
    pushMatrix()
    translate(25,25)
    imageMode(CENTER)
    
    
    for i in icons:
        if i[2] == brackets[0][0]:
            image(globals.imgIndex["tictactoe-cross"], i[0],i[1],30,30)
        else:
            image(globals.imgIndex["tictactoe-circle"],i[0],i[1],30,30)
    popMatrix()
    
    strokeWeight(1)
    
def winConditions():
    global boarddict, icons, moves
    global brackets
    global currentPlayer
    global nextMatchButton
    global currentCard
    strokeWeight(2)
    stroke(255,0,0)
    moves = True
    
    if currentPlayer == brackets[0][0]:
        var = brackets[0][1]
                
    elif currentPlayer == brackets[0][1]:
        var = brackets[0][0]
        
    if len(brackets) > 1 and var == brackets[0][0]:
        text(globals.userConfig["players"][str(var)]+" wins! Click the Next Match button to continue.", 0,200)
        nextMatchButton.update()
    else:
        if playerCount == 2:
            text(globals.userConfig["players"][str(var)]+" wins!", 0,200)
        elif currentCard["minigame"]["ticTacToe"]["mode"] == "1v6" and var == brackets[0][0]:
            text(globals.userConfig["players"][str(var)]+" won all matches!", 0,200)
        else:
            text(globals.userConfig["players"][str(var)]+" wins!", 0,200)
        
def nextMatch(*args):
    global brackets
    global currentPlayer
    brackets.pop(0)
    currentPlayer = choice(brackets[0])
    resetTicTacToe()
        

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
    global minigameComplete
    
    if not minigameComplete:
        if stopTimer == False:
            timeMemory = millis()-timeOffset
            stopTimer = True
            showTimeIsUpMsg = False
            pauseTimerButton.text = "Resume"
        else:
            scrnSecs = timeMemory/1000
            scrnMins = timeMemory/1000/60
            stopTimer = False
            showTimeIsUpMsg = False
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
    showTimeIsUpMsg = False
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
    global currentCard
    global stopTimer
    if stopTimer and "timer" in currentCard["minigame"]:
        startTimer()
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
    global stopTimer
    
    winners = []
    if currentCard["minigame"]["dice"]["mode"] == "HIGHEST":
        toRoll.remove(currentPlayer)
        if toRoll == []:
            var = 0
            for box in resultBoxes:
                if box.text != "":
                    if int(box.text) > var:
                        var = int(box.text)
            for box in resultBoxes:
                if box.text != "":
                    if int(box.text) == var:
                        winners.append(resultBoxes.index(box)+1)
    elif currentCard["minigame"]["dice"]["mode"] == "LOWEST":
        toRoll.remove(currentPlayer)
        if toRoll == []:
            var = 999999999999
            for box in resultBoxes:
                if box.text != "":
                    if int(box.text) < var:
                        var = int(box.text)
            for box in resultBoxes:
                if box.text != "":
                    if int(box.text) == var:
                        winners.append(resultBoxes.index(box)+1)
            
    elif currentCard["minigame"]["dice"]["mode"] == "FIRST":
        toRoll.remove(currentPlayer)
        for box in resultBoxes:
            if box.text != "":
                if int(box.text) == int(currentCard["minigame"]["dice"]["target"]):
                    winners.append(resultBoxes.index(box)+1)
    elif currentCard["minigame"]["dice"]["mode"] == "WITHINTIME":
        if stopTimer == False:
            for box in resultBoxes:
                if box.text != "":
                    if int(box.text) == currentCard["minigame"]["dice"]["target"]:
                        winners.append(resultBoxes.index(box)+1)
    
    if len(winners) > 1:
        minigameComplete = False
        challengeActive = True
        timeMemory = millis()-timeOffset
        showTimeIsUpMsg = False
        players = winners
        toRoll = players[:]
        for box in resultBoxes:
            box.text = ""
            
        pauseTimer()
        
        return "RESTART"
    if len(winners) == 0:
        if len(toRoll) == 0:
            minigameComplete = False
            challengeActive = True
            timeMemory = millis()-timeOffset
            showTimeIsUpMsg = False
            toRoll = players[:]
            for box in resultBoxes:
                box.text = ""
            return None
        else:
            currentPlayer = choice(toRoll)
    
    elif len(winners) == 1:
        timeMemory = millis()-timeOffset
        pauseTimer()
        minigameComplete = True
        showTimeIsUpMsg = False
        return winners[0]

def playMinigame(*args):
    global challengeActive
    global playerCount
    global players
    global currentPlayer
    global currentCard
    global brackets
    if len(players) == playerCount:
        challengeActive = True
        if "dice" in currentCard["minigame"]:
            toRoll = players[:]
            currentPlayer = choice(players)
        elif "ticTacToe" in currentCard["minigame"]:
            if currentCard["minigame"]["ticTacToe"]["mode"] == "1v6":
                brackets = []
                for i in range(1, globals.playerCount+1):
                    if i != players[0]:
                        brackets.append([players[0], i])
            else:
                brackets = [(players[0], players[1])]
            currentPlayer = choice(brackets[0])
    
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
