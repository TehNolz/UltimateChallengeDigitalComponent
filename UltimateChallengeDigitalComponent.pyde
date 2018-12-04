import os
import logging
import loaddata
import globals
from random import randint
from random import choice

#Setup logging
logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger("LOG")
log.info("Hello world!")

#####Declare globals
#Images
imgRot = 0
imgRet = 0
imgPos = "foreground"
turnImage = False
retractImage = False

#Menus
currentMenu = "gamescreen"

#Console
showConsole = False
consoleText = ""
consoleHistory = []
consoleHistoryInt = 0

#gameconfig
gameconfig = {
    "useDecks": {
        "base",
        "expansion1",
        "expansion2"
    }
}

def newCard():
    cardConfig = globals.cardConfig
    
    global currentCard
    pool = {}
    for deck in gameconfig["useDecks"]:
        pool.update(cardConfig[deck])
    chosenCard = choice(pool.keys())
    
    deck = chosenCard.split("-")[1]
    showStart = cardConfig[deck][chosenCard]["dice"] or cardConfig[deck][chosenCard]["timer"]
    
    currentCard = {
        "id": chosenCard,
        "back": "card-"+deck+"-back",
        "showStart": showStart
    }

def setup():
    log.info("Running setup!")
    global cardConfig
    global imgIndex
    global font
    size(1133, 600, P3D)
    
    #Load the loading screen (so meta)
    image(loadImage("misc-loadingscreen.png"), 0, 0, 1133, 600)
    
    log.info("Loading assets.")
    loaddata.loadData()
    font = globals.fonts["OpenSans"]
    textFont(font)
        
    #Pick a random card to show.
    newCard()
    
def draw():
    global currentCard
    global backImage
    global imgRot
    global imgRet
    global imgPos
    global turnImage
    global retractImage
    global baseScale
    global consoleText
    
    imgIndex = globals.imgIndex
    cardConfig = globals.cardConfig
        
    #Calculate scaling. This assumes the normal screen resolution is 1133x600
    baseScale = (height/6)/100.0
    
    background(180, 180, 180, 128)
    translate(width/2, 0, 0)
    
    imageMode(CENTER)
    rectMode(CENTER)
    textAlign(CENTER)
    
    if currentMenu == "gamescreen":
        #Challenge card flip. When turnImage is true, the card will flip and show a new challenge.
        if turnImage:
            imgRot+=10
            if imgRot == 360:
                imgRot = 0
        if turnImage and (imgRot == 0):
            turnImage = False
        elif imgRot == 180:
            newCard()
            
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
        base = 400
        imgHeight = base*baseScale
        imgWidth = ((base/4)*3)*baseScale
        translate(0, height/2, imgRet*baseScale)
        rotateY(radians(imgRot))
        image(imgIndex[currentCard["back"]], 0, 0, imgWidth, imgHeight)
        rotateY(radians(180))
        scale(-1, 1) #Yes, this IS necessary.
        translate(0, 0, -1)
        image(imgIndex[currentCard["id"]], 0, 0, imgWidth, imgHeight)
        popMatrix()
        
        #Next card button
        pushMatrix()
        translate(0, height*0.90, 0)
        image(imgIndex["gamescreen-nextcard"], 0, 0, imgWidth, imgWidth/5)
        popMatrix()
        
        #Floor box thing
        pushMatrix()
        translate(0, height, 0)
        fill(255, 255, 255, 255)
        box(1000*baseScale, 10*baseScale, 1000*baseScale)
        popMatrix()
        
        if showConsole:
            #Console box
            pushMatrix()
            translate(0, height, 0)
            fill(0, 0, 0, 128)
            rect(0, 0, 1000*baseScale, 100*baseScale)

            #Console text
            translate(0, -12*baseScale, 0)
            textSize(30*baseScale)
            fill(255, 255, 255, 128)
            text(consoleText, 0, 0)
            popMatrix()
            
def mousePressed():
    global currentImage
    global challengeCards
    global retractImage
    global turnImage
    
    if mouseButton == LEFT:
        if (416*baseScale <= mouseX <= 716*baseScale) and (510*baseScale <= mouseY <= 570*baseScale):
            if not retractImage:
                turnImage = True
        
            
def keyPressed():
    global showConsole
    global consoleText
    global currentCard
    global consoleHistory
    global consoleHistoryInt
    global turnImage
    global retractImage
    
    #Open console
    if key == "`":
        showConsole = not showConsole
        if not showConsole:
            consoleText = ""
            
    elif showConsole:
        #Backspace
        if key == "" and showConsole:
            consoleText = consoleText[:-1]
            
        #Execute command
        elif key == "\n":
            command = consoleText.split(" ")
            if command[0] == "setcard":
                exists = False
                for deck in cardConfig:
                    if command[1] in cardConfig[deck]:
                        exists = True
                if exists:
                    deck = command[1].split("-")[0]
                    showStart = cardConfig[deck][command[1]]["dice"] or cardConfig[deck][command[1]]["timer"]
                    
                    currentCard = {
                        "id": command[1],
                        "back": deck+"-back",
                        "showStart": showStart
                    }
            elif command[0] == "retractcard":
                if not turnImage:
                    retractImage = True
            elif command[0] == "flipcard":
                if not retractImage:
                    turnImage = True
            else:
                consoleText = ""
                return None
            
            consoleHistory.append(consoleText)
            consoleText = ""
            
        #Command history
        #Up
        elif keyCode == 38:
            consoleText = consoleHistory[len(consoleHistory)-consoleHistoryInt-1]
            if consoleHistoryInt < len(consoleHistory):
                consoleHistoryInt+=1
        
        #Down
        elif keyCode == 40: 
            consoleText = consoleHistory[len(consoleHistory)-consoleHistoryInt-1]
            if consoleHistoryInt > 0:
                consoleHistoryInt-=1
                if consoleHistory == 0:
                    consoleText = ""
        
        #Type a character
        elif type(key) == unicode:
            consoleText+=key
