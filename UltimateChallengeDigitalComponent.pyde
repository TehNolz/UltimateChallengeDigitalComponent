import os
import logging
import json
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

#gameconfig
gameconfig = {
    "useDecks": {
        "base",
        "expansion1",
        "expansion2"
    }
}

def newCard():
    global gameconfig
    global cardconfig
    global currentCard
    
    pool = {}
    for deck in gameconfig["useDecks"]:
        pool.update(cardconfig[deck])
    chosenCard = choice(pool.keys())
    
    deck = chosenCard.split("-")[0]
    showStart = cardconfig[deck][chosenCard]["dice"] or cardconfig[deck][chosenCard]["timer"]
    
    currentCard = {
        "id": chosenCard,
        "back": deck+"-back",
        "showStart": showStart
    }

def setup():
    log.info("Running setup!")
    global currentImage
    global backImage
    global cardconfig
    global imgIndex
    size(1133, 600, P3D)
    
    #Load the loading screen (so meta)
    image(loadImage("misc-loadingscreen.png"), 0, 0, 1133, 600)
    
    #Load game images
    imgIndex = {}
    for file in os.listdir("data"):
        type = file.split("-")[0]
        if  type != "card":
            name = file.split("-")[1].split(".")[0]
            imgIndex[name] = requestImage(file)
        
    #Load card images
    log.info("Loading images...")
    cardconfig = json.loads(open("cardconfig.json").read())
    for category in cardconfig:
        for card in cardconfig[category]:
            imgIndex[card] = requestImage(cardconfig[category][str(card)]["file"])
        imgIndex[category+"-back"] = requestImage("card-"+category+"-back.png")
    
    #Wait for all images to finish loading.
    while True:
        var = True
        for img in imgIndex:
            imgWidth = imgIndex[img].width
            if imgWidth == 0:
                var = False
            elif imgWidth == -1:
                log.error("Failed to load image: "+str(img))
                var = False
        if var:
            break
    log.info("Finished loading images.")
        
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
    global imgIndex
    global cardconfig
    global baseScale
    
    #Calculate scaling. This assumes the normal screen resolution is 1133x600
    baseScale = (height/6)/100.0
    
    background(180, 180, 180, 128)
    translate(width/2, 0, 0)
    
    imageMode(CENTER)
    rectMode(CENTER)
    
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
        
        pushMatrix()
        translate(0, 0, 0)
        translate(0, height*0.90, 0)
        image(imgIndex["nextcard"], 0, 0, imgWidth, imgWidth/5)
        popMatrix()
        
        pushMatrix()
        translate(0, height/2, 0)
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
    elif mouseButton == RIGHT:
        if not turnImage:
            retractImage = True
