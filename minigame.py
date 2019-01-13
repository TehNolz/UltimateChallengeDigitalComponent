from Object import Object
from Button import Button
from util import *
import globals
import textInput
from random import choice
import prime_number_menu
currentCard = None

def init():
    import time
    setupStart = time.clock()
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
    for i in range(6):
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
    for i in range(6):
        textBox = textInput.textBox(width*0.2, 0, 50, 50, writable=False)
        textBox.textAlignment = CENTER
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
    global stopTimer
    stopTimer = True
    global timeMemory
    timeMemory = 0
    global showTimeIsUpMsg
    showTimeIsUpMsg = False
    global timerCache
    timerCache = 0
    global lastTimeMillis
    lastTimeMillis = 0

    offset = 0
    if "dice" in currentCard["minigame"]:
        offset+=0.125
    
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

    globals.log.info('Loading minigame...')
    globals.log.debug('Arguments: '+str(currentCard['minigame'])[1:-1])
    globals.log.info('Loaded minigame.\t['+str(int((time.clock()-setupStart)*10**6))+' us]')
    globals.log.debug(u'\u2514\u2500 Call from f'+getMostRecentCall()[1:])

def draw(mousePressed):
    updatedTime = False
    drawStart = millis()
    width = 1133
    height = 600
    pushStyle()
    scale(*globals.baseScaleXY)
    pushMatrix()
    #Misc
    global timerCache
    global lastTimeMillis
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
        if minigameComplete:
            exitButton.update()
    else:
        exitButton.update()
    
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
            textSize(30)
            textAlign(LEFT)
            var = playerCount-len(players)
            fill(0, 0, 0, 255)
            if var == 1:
                pushStyle()
                txt = "Who will play? Pick "+str(var)+" player."
                text(txt, width*0.05, height*0.1)
                popStyle()
            elif var == 0:
                text("Press play to continue.",  width*0.05, height*0.1)
            else:
                txt = "Who will play? Pick "+str(var)+" players."
                text(txt, width*0.05, height*0.1)
            for player in range(globals.playerCount):
                text(globals.userConfig["players"][player], width*0.15, height*textheight)
                playerButtonCheckboxes[player].update()
                textheight+= 0.1
                
            playButton.update()
        elif playerCount == 1 or playerCount == 6:
            challengeActive = True
            players = [1]
            toRoll = players[:]
            currentPlayer = choice(toRoll)
        if playerCount == 6:
            players = list(range(globals.playerCount))
            toRoll = players[:]

    else:
        fill(0, 0, 0, 255)
        
        ######################
        if "dice" in currentCard["minigame"]:
            pushMatrix()
            pushStyle()
            textAlign(CENTER)
            if "timer" in currentCard["minigame"]:
                translate(width*-0.25, 0)
            textSize(30)
            boxHeight = 0.2
            if len(players) > 1:
                for player in players:
                    textSize(30)
                    text(globals.userConfig["players"][player], width*0.08, height*boxHeight)
                    resultBoxes[player].y = height*(boxHeight-0.05)
                    resultBoxes[player].draw()
                    boxHeight+=0.1
            
            if minigameComplete:
                if len(players) > 1:
                    if startingDiceRoll:
                        text("The game starts with "+globals.userConfig["players"][winner]+"'s turn!", width*0.5, height*0.1)
                    else:
                        text(globals.userConfig["players"][winner]+" wins the game!", width*0.5, height*0.1)
                else:
                    text("You win the game!", width*0.5, height*0.1)
                dice.activators = {}
            else:
                if len(players) > 1:
                    text("Roll the dice, "+globals.userConfig["players"][currentPlayer]+"!", width*0.5, height*0.1)
                else:
                    text("Roll the dice!", width*0.5, height*0.1)
                dice.activators = {LEFT}
            dice.update()
            
            if rolling and not minigameComplete:
                if dice.throwdice == False:
                    rolling = False
                    resultBoxes[currentPlayer].text[0] = str(dice.Rolldice)
                    
                    winner = checkWinner()
            popMatrix()
            popStyle()


        elif "ticTacToe" in currentCard["minigame"]:
            pushMatrix()
            pushStyle()
            textSize(30)
            translate((width-300)/2, (height-300)/2)
            if not moves:
                textAlign(CENTER)
                text(globals.userConfig["players"][currentPlayer]+"'s turn!", 105, 40)
            textAlign(LEFT)
            field()
            
            pushMatrix()
            g.setMatrix(getCurrentInvMatrix())
            mousePos = Vector2(mouseX, mouseY).getModelPos()
            popMatrix()
        
            if moves == False:
                if mousePressed and not once:
                    x = int((mousePos.X)/50)
                    y = int((mousePos.Y)/50)
                    if x < 3 and x > -1 and y > -1 and y < 3:
                        if boarddict[x][y] == 0:
                            once = True
                            icons.append((x*50, y*50, currentPlayer))
                            boarddict[x][y] = currentPlayer+1

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
                
            text(globals.userConfig["players"][brackets[0][0]] +" vs "+globals.userConfig["players"][brackets[0][1]], 0,250)
                
            popMatrix()
            popStyle()
        ######################
        elif "primeNumber" in currentCard["minigame"]:
            prime_number_menu.draw(mousePressed)
        
        ######################
        if "timer" in currentCard["minigame"]:
            pushMatrix()
            pushStyle()
            if "dice" in currentCard["minigame"]:
                translate(width*0.125, 0)
                
            textAlign(CENTER)
            fill(0, 0, 0)
            textSize(100)
            
            if currentCard["minigame"]["timer"] == int(timerCache/1000):
                showTimeIsUpMsg = True
                stopTimer = True
                pauseTimerButton.text = "Pause"
                if "dice" in currentCard["minigame"]:
                    dice.activators = {}
            
            if stopTimer:
                if showTimeIsUpMsg:
                    text("Time's up!", width/2, height*0.2)
            else:
                # timerCache is incremented by the amount of time each draw() took
                # This allows us to stop and reset the clock much more easily
                
                # When the timer is running, we add the delay between this draw() and the previous draw()
                timerCache += millis() - lastTimeMillis
                # Remember the time in millis for the next time
                # helps control the timer cache by checking the time update delay
                lastTimeMillis = millis()
                updatedTime = True
            
            # the modulus makes the value 'loop back' to 0 when it becomes 60
            seconds = int(timerCache / 1000) % 60
            mins = int(timerCache / 1000 / 60)
            
            # Format the time into a string and draw it on screen
            text(nf(mins, 2) + " : " + nf(seconds, 2), width/2, height/2)

            popMatrix()
            popStyle()
            
            #restartButton
            startTimerButton.update()
            #pauseButton
            pauseTimerButton.update()
                
    popStyle()
    popMatrix()
    
    if not updatedTime:
        lastTimeMillis = millis()

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
        text(globals.userConfig["players"][var]+" wins! Click the Next Match button to continue.", 0,200)
        nextMatchButton.update()
    else:
        if playerCount == 2:
            text(globals.userConfig["players"][var]+" wins!", 0,200)
        elif currentCard["minigame"]["ticTacToe"]["mode"] == "1v6" and var == brackets[0][0]:
            text(globals.userConfig["players"][var]+" won all matches!", 0,200)
        else:
            text(globals.userConfig["players"][var]+" wins!", 0,200)
        
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
    global timerCache
    global stopTimer
    global pauseTimerButton
    global minigameComplete
    
    if not minigameComplete:
        if stopTimer == False:
            stopTimer = True
            showTimeIsUpMsg = False
            pauseTimerButton.text = "Resume" if timerCache != 0 else "Start"
        else:
            stopTimer = False
            showTimeIsUpMsg = False
            pauseTimerButton.text = "Pause"
        
    
# This has actually become a  reset button
def startTimer(*args):
    global stopTimer
    global startTimerButton
    global pauseTimerButton
    global timerCache

    if not stopTimer:
        stopTimer = True
        timerCache = 0
        startTimerButton.text = 'Start'
    else:
        stopTimer = False
        startTimerButton.text = 'Reset\nTimer'
    showTimeIsUpMsg = False
    pauseTimerButton.text = "Pause"

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
                if box.getFullText() != "":
                    if int(box.getFullText()) > var:
                        var = int(box.getFullText())
            for box in resultBoxes:
                if box.getFullText() != "":
                    if int(box.getFullText()) == var:
                        winners.append(resultBoxes.index(box))
    elif currentCard["minigame"]["dice"]["mode"] == "LOWEST":
        toRoll.remove(currentPlayer)
        if toRoll == []:
            var = 999999999999
            for box in resultBoxes:
                if box.getFullText() != "":
                    if int(box.getFullText()) < var:
                        var = int(box.getFullText())
            for box in resultBoxes:
                if box.getFullText() != "":
                    if int(box.getFullText()) == var:
                        winners.append(resultBoxes.index(box))
            
    elif currentCard["minigame"]["dice"]["mode"] == "FIRST":
        toRoll.remove(currentPlayer)
        for box in resultBoxes:
            if box.getFullText() != "":
                if int(box.getFullText()) == int(currentCard["minigame"]["dice"]["target"]):
                    winners.append(resultBoxes.index(box))
    elif currentCard["minigame"]["dice"]["mode"] == "WITHINTIME":
        if stopTimer == False:
            for box in resultBoxes:
                if box.getFullText() != "":
                    if int(box.getFullText()) == currentCard["minigame"]["dice"]["target"]:
                        winners.append(resultBoxes.index(box))
    
    if len(winners) > 1:
        minigameComplete = False
        challengeActive = True
        showTimeIsUpMsg = False
        players = winners
        toRoll = players[:]
        currentPlayer = choice(toRoll)
        for box in resultBoxes:
            box.text = ['', '', '']
            
        pauseTimer()
        
        return "RESTART"
    if len(winners) == 0:
        if len(toRoll) == 0:
            minigameComplete = False
            challengeActive = True
            showTimeIsUpMsg = False
            toRoll = players[:]
            currentPlayer = choice(toRoll)
            for box in resultBoxes:
                box.text = ['','','']
            return None
        else:
            currentPlayer = choice(toRoll)
    
    elif len(winners) == 1:
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
            currentPlayer = choice(toRoll)
        elif "ticTacToe" in currentCard["minigame"]:
            if currentCard["minigame"]["ticTacToe"]["mode"] == "1v6":
                brackets = []
                for i in range(globals.playerCount):
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
