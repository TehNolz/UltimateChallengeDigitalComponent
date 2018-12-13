import globals
from util import *
from Button import Button
from Object import Object
from random import choice

def init():
    global turnImage
    global imgRot
    global imgPos
    global imgRet
    global toggleChallengeField
    global b
    global challengeNextCard
    global startChallengeButton
    global buttons
    global challengeFieldPos
    
    turnImage = False
    imgRot = 0
    imgPos = "foreground"
    imgRet = 0
    toggleChallengeField = False
    challengeFieldPos = 0
    
    Object.startGroup()
    #New card
    b = Button(width*0.5, height*0.90, RoundRect(-285,-57,570,114)*0.5)
    b.releaseAction = startTurn
    b.text = "Pick a new card."
    
    r = RoundRect(-140,-57,280,114)
    challengeNextCard = Button(width*0.57, height*0.9, r.copy()*0.5)
    challengeNextCard.releaseAction = startTurn
    challengeNextCard.text = "Pick a new card."
    
    startChallengeButton = Button(width*0.43, height*0.9, r.copy()*0.5)
    startChallengeButton.releaseAction = startChallenge
    startChallengeButton.text = "Start challenge."
    
    #Back button
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 0.5
    backButton = Button(width*0.95, height*0.1, r.copy()*0.5)
    backButton.releaseAction = gotoMainMenu
    backButton.text = "Quit"
    
    buttons = Object.endGroup()
    
def startTurn(*args):
    global turnImage
    if args[1] == LEFT:
        turnImage = True

def draw():
    global turnImage
    global imgRot
    global imgPos
    global imgRet
    global toggleChallengeField
    global b
    global startChallengeButton
    global challengeNextCard
    global buttons
    global currentCard
    global challengeFieldPos
    
    pushMatrix()
    translate(width/2, 0, 0)
    
    baseScale = globals.baseScale
    imgIndex = globals.imgIndex
    
    #Challenge card flip. When turnImage is true, the card will flip and show a new challenge.
    if turnImage:
        imgRot += 10
        if imgRot == 360:
            imgRot = 0
    if turnImage and (imgRot == 0):
        turnImage = False
    elif imgRot == 180:
        newCard()
        
    #Challenge card retract. When retractImage is true, the card will move forwards/backwards depending on whether its currently backwards/forwards.
    if toggleChallengeField:
        if imgPos == "foreground":
            if imgRet == -100:
                toggleChallengeField = False
                imgPos = "background"
            else:
                imgRet-=5
                challengeFieldPos-=1
        elif imgPos == "background":
            if imgRet == 0:
                toggleChallengeField = False
                imgPos = "foreground"
            else:
                imgRet+=5
                challengeFieldPos+=1
                
                
    pushMatrix()
    fill(255, 255, 255)
    print(challengeFieldPos/100.0)
    translate(0, 0-height*(challengeFieldPos/100), 0)
    rect(0, 0, width+100, height+100)
    
    popMatrix()

    #Card
    pushMatrix()
    base = 400
    imgHeight = base*baseScale
    imgWidth = ((base/4)*3)*baseScale
    translate(0, height/2, imgRet*baseScale)
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
        startChallengeButton.update()
        challengeNextCard.update()
    else:
        b.update()
    
def newCard():
    cardConfig = globals.cardConfig
    
    pool = {}
    for deck in globals.userConfig["settings"]["useDecks"]:
        pool.update(cardConfig[deck])
    setCard(choice(pool.keys()))
    
    
def setCard(card):
    global currentCard
    
    deck = card.split("-")[0]
    showStart = True
    if globals.cardConfig[deck][card] == None:
        showStart = False
    currentCard = {
        "id": card,
        "back": "card-"+deck+"-back",
        "showStart": showStart,
        "minigame": globals.cardConfig[deck][card]
    }
    
def gotoMainMenu(*args):
    if args[1] == LEFT:
        globals.currentMenu = "mainMenu"
        
def startChallenge(*args):
    if args[1] == LEFT:
        global toggleChallengeField
        global challengeActive
        
        toggleChallengeField = True
        challengeActive = True
    
