import globals
import minigame
from util import *
from Button import Button
from Object import Object
from random import choice

def init():
    global turnImage
    global imgRot
    global imgPos
    global imgRet
    global retractImage
    global minigameButtons
    global defaultButtons
    global miscButtons
    global pool
    global b
    
    pool = {}
    turnImage = False
    imgRot = 0
    imgPos = "foreground"
    imgRet = 0
    retractImage = False
    
    Object.startGroup()
    #New card
    b = Button(width*0.5, height*0.90, RoundRect(-285,-57,570,114)*0.5)
    b.releaseAction = startTurn
    b.text = "Pick a new card."
    
    defaultButtons = Object.endGroup()
    
    Object.startGroup()
    
    r = RoundRect(-140,-57,280,114)
    challengeNextCard = Button(width*0.57, height*0.9, r.copy()*0.5)
    challengeNextCard.releaseAction = startTurn
    challengeNextCard.text = "Pick a new card."
    
    startChallenge = Button(width*0.43, height*0.9, r.copy()*0.5)
    startChallenge.releaseAction = gotoMinigame
    startChallenge.text = "Start challenge."
    
    minigameButtons = Object.endGroup()
    
    Object.startGroup()
    
    #Back button
    backButton = Button(37, 37, RoundRect(-25, -25, 50, 50) * 0.75)
    backButton.releaseAction = gotoMainMenu
    backButton.textSize *= 3
    backButton.applyStyle('compact')
    backButton.description = 'End game'
    backButton.icon = globals.imgIndex['tictactoe-cross'].copy()
    backButton.iconScale = 0.5
    backButton.iconColor = color(0,0)
    
    miscButtons = Object.endGroup()
    
def startTurn(*args):
    global turnImage
    if args[1] == LEFT:
        turnImage = True

def draw():
    global turnImage
    global imgRot
    global imgPos
    global imgRet
    global retractImage
    global currentCard
    
    pushMatrix()
    translate(width/2, 0, 0)
    
    baseScale = globals.baseScale
    imgIndex = globals.imgIndex
    
    #Challenge card flip. When turnImage is true, the card will flip and show a new challenge.
    if turnImage:
        b.text = "Pick a new card."
        imgRot += 10
        if imgRot == 360:
            imgRot = 0
    if turnImage and (imgRot == 0):
        turnImage = False
    elif imgRot == 180:
        if turnImage:
            newCard()
        if currentCard["deck"] == "expansion2":
            turnImage = False
            fill(0, 0, 0, 255)
            textAlign(CENTER)
            textSize(30*baseScale)
            text("Current player, please look away from the screen!", 0, height*0.1)
            b.text = "Continue"
            
        
    #Challenge card retract. When retractImage is true, the card will move forwards/backwards depending on whether its currently backwards/forwards.
    if retractImage:
        if imgPos == "foreground":
            if imgRet == -200:
                retractImage = False
                imgPos = "background"
            else:
                imgRet-=5
        elif imgPos == "background":
            if imgRet == 0:
                retractImage = False
                imgPos = "foreground"
            else:
                imgRet+=5

    #Card
    pushMatrix()
    translate(0, height/2, imgRet*baseScale)
    base = 400
    imgHeight = base*baseScale
    imgWidth = ((base/4)*3)*baseScale
    rotateY(radians(imgRot))
    image(imgIndex[currentCard["back"]], 0, 0, imgWidth, imgHeight)
    rotateY(radians(180))
    scale(-1, 1) #Yes, this IS necessary.
    translate(0, 0, -1)
    image(imgIndex["card-"+currentCard["id"]], 0, 0, imgWidth, imgHeight)
    popMatrix()
    
    #Floor box thing
    pushMatrix()
    translate(0, height, 0)
    fill(255, 255, 255, 255)
    box(1000*baseScale, 10*baseScale, 1000*baseScale)
    popMatrix()
    
    # Reset the translate at the top of the draw()
    popMatrix()
    
    # Scale the buttons based on the current base scale
    scale(*globals.baseScaleXY)

    if currentCard["showStart"]:
        for o in minigameButtons:
            o.update()
    else:
        for o in defaultButtons:
            o.update()
    for o in miscButtons:
        o.update()
    
def newCard():
    global pool
    cardConfig = globals.cardConfig
    
    if pool == {}:
        pool = {}
        for deck in globals.userConfig["settings"]["useDecks"]:
            pool.update(cardConfig[deck])
    chosenCard = choice(pool.keys())
    setCard(chosenCard)
    del pool[chosenCard]
    
def setCard(card):
    global currentCard
    
    deck = card.split("-")[0]
    showStart = True
    if globals.cardConfig[deck][card] == None:
        showStart = False
    currentCard = {
        "id": card,
        "deck": deck,
        "back": "card-"+deck+"-back",
        "showStart": showStart,
        "minigame": globals.cardConfig[deck][card]
    }
    
def gotoMainMenu(*args):
    if args[1] == LEFT:
        globals.currentMenu = "mainMenu"
def gotoMinigame(*args):
    global currentCard
    if args[1] == LEFT:
        minigame.currentCard = currentCard
        minigame.init()
        globals.currentMenu = "minigame"
