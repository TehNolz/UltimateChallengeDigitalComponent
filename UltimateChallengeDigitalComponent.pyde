import os
import logging
import json
from random import randint

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

def setup():
    log.info("Running setup!")
    global currentImage
    global backImage
    global cardconfig
    global imgIndex
    size(1133, 600, P3D)
    
    #Load the loading screen (so meta)
    loadingImage = loadImage("misc-loadingscreen.png")
    image(loadingImage, 0, 0, 1133, 600)
    
    #Load all images
    imgIndex = {}
    log.info("Loading images...")
    cardconfig = json.loads(open("cardconfig.json").read())
    for category in cardconfig:
        imgIndex[category] = {}
        for card in cardconfig[category]:
            if card != "back":
                card = int(card)
            imgIndex[category][card] = requestImage(cardconfig[category][str(card)]["file"])
    
    
    #Wait for all images to finish loading.
    while True:
        var = True
        for category in imgIndex:
            for card in imgIndex[category]:
                imgWidth = imgIndex[category][card].width
                if imgWidth == 0:
                    var = False
        if var:
            break
    log.info("Finished loading images.")
        
    #Pick a random card to show.
    currentImage = imgIndex["base"][randint(1, len(imgIndex["base"])-1)]
    backImage = imgIndex["base"]["back"]
    
def draw():
    global currentImage
    global backImage
    global imgRot
    global imgRet
    global imgPos
    global turnImage
    global retractImage
    global imgIndex
    global cardconfig
    
    #Calculate scale.
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
            currentImage = imgIndex["base"][randint(1, len(imgIndex["base"])-1)]
            
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
        print(imgWidth, imgHeight)
        translate(0, height/2, imgRet*baseScale)
        rotateY(radians(imgRot))
        image(backImage, 0, 0, imgWidth, imgHeight)
        rotateY(radians(180))
        scale(-1, 1)
        translate(0, 0, -1)
        image(currentImage, 0, 0, imgWidth, imgHeight)
        popMatrix()
        
        pushMatrix()
        translate(0, 0, 0)
        fill(0, 255, 0)
        translate(0, height*0.90, 0)
        rect(0, 0, imgWidth, imgWidth/5)
        popMatrix()
     
def mousePressed():
    global currentImage
    global challengeCards
    global retractImage
    global turnImage
    
    if mouseButton == LEFT:
        if not retractImage:
            turnImage = True
    elif mouseButton == RIGHT:
        if not turnImage:
            retractImage = True
