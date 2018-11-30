import os
from random import randint

imgRot = 0
turnImage = False

def setup():
    global currentImage
    global challengeCards
    global backImage
    size(600, 600, P3D)
    
    challengeCards = []
    for file in os.listdir("data"):
        if file == "challenge-back.png":
            backImage = loadImage(file)
        else:
            challengeCards.append(loadImage(file))
            
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
    pushMatrix()
    translate(0, height/2, 0)
    imgScale = 0.4
    rotateY(radians(imgRot))
    image(backImage, 0, 0, backImage.width*imgScale, backImage.height*imgScale)
    rotateY(radians(180))
    scale(-1, 1)
    translate(0, 0, -1)
    image(currentImage, 0, 0, currentImage.width*imgScale, currentImage.height*imgScale)
    popMatrix()
     
def mousePressed():
    global currentImage
    global challengeCards
    
    global turnImage
    turnImage = True
