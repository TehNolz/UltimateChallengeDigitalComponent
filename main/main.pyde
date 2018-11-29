import os
from random import randint

rot = 0

def setup():
    global currentImage
    global challengeCards
    global backImage
    size(600, 600, P3D)
    
    
    dir = "..\Assets\Challenge Cards"
    challengeCards = []
    for file in os.listdir(dir):
        if file == "challenge-back.png":
            backImage = loadImage(dir+"\\"+file)
        else:
            challengeCards.append(loadImage(dir+"\\"+file))
            
    print(challengeCards)
    currentImage = backImage
    
def draw():
    global currentImage
    global rot
    
    background(0)
    imageMode(CENTER)
    translate(width/2, height/2)
    imgScale = 0.4
    rotateY(radians(rot))
    image(currentImage, 0, 0, currentImage.width*imgScale, currentImage.height*imgScale)
     
def mousePressed():
    global currentImage
    global challengeCards
    
    currentImage = challengeCards[randint(0, len(challengeCards)-1)]
    
def mouseWheel(event):
    global rot
    
    rot+= event.getCount()*5
    print(radians(rot))
