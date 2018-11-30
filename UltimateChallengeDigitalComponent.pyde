import os
from random import randint

imgRot = 0
turnImage = False

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
        print(var)
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
    global turnImage
    
    if turnImage:
        imgRot+=10
        if imgRot == 360:
            imgRot = 0
    if turnImage and (imgRot == 0):
        turnImage = False
    elif imgRot == 180:
        currentImage = challengeCards[randint(0, len(challengeCards)-1)]
    
    background(180, 180, 180, 128)
    translate(width/2, 0, 0)
    
    imageMode(CENTER)
    rectMode(CENTER)
    
    pushMatrix()
    translate(0, height/2, 0)
    imgScale = 0.3
    rotateY(radians(imgRot))
    image(backImage, 0, 0, backImage.width*imgScale, backImage.height*imgScale)
    rotateY(radians(180))
    scale(-1, 1)
    translate(0, 0, -1)
    image(currentImage, 0, 0, currentImage.width*imgScale, currentImage.height*imgScale)
    popMatrix()
    
    pushMatrix()
    translate(0, 0-height/4, 0)
    color(0, 255, 0)
    rect(0, 0, 300, 100)
    popMatrix()
     
def mousePressed():
    global currentImage
    global challengeCards
    
    global turnImage
    turnImage = True
