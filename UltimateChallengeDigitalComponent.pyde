import os
from random import randint

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
    global currentImage
    global challengeCards
    global backImage
    size(600, 600, P3D)
    
    #Load the loading screen (so meta)
    loadingImage = loadImage("image-misc-loadingscreen.png")
    image(loadingImage, 0, 0)
    
    #Load all images in another thread.
    challengeCards = []
    for file in os.listdir("data"):
        var = file.split("-")
        if var[0] == "card":
            if var[1] == "challenge":
                if var[2] == "back.png":
                    backImage = requestImage(file)
                else:
                    challengeCards.append(requestImage(file))
    
    #Hold the script until all images have been loaded.
    var = True
    while True:
        if backImage.width == 0:
            for img in challengeCards:
                if img.width != 0:
                    var = False
        if var:
            break
        
    #Pick a random card to show.
    currentImage = challengeCards[randint(0, len(challengeCards)-1)]
    
def draw():
    global currentImage
    global backImage
    global imgRot
    global imgRet
    global imgPos
    global turnImage
    global retractImage
    
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
            currentImage = challengeCards[randint(0, len(challengeCards)-1)]
            
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
        image(backImage, 0, 0, imgWidth, imgHeight)
        rotateY(radians(180))
        scale(-1, 1)
        translate(0, 0, -1)
        image(currentImage, 0, 0, imgWidth, imgHeight)
        popMatrix()
        
        pushMatrix()
        translate(0, 0-height/4, 0)
        color(0, 255, 0)
        rect(0, 0, 300, 100)
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
