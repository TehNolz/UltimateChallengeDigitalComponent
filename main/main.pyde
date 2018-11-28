import os
from random import randint

def setup():
    global currentImage
    global challengeCards
    global backImage
    
    size(600, 600)
    background(0)
    backImage = loadImage("..\Assets\Challenge Cards\challenge-back.png")
    
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
    imageMode(CENTER)
    #scale(0.4)
    image(currentImage, width/2, height/2, currentImage.width*0.4, currentImage.height*0.4)
    
def mousePressed():
    global currentImage
    global challengeCards
    currentImage = challengeCards[randint(0, len(challengeCards)-1)]
    
    print(width/2, height/2)
    print(mouseX, mouseY)
