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
    global retractImage
    global b
    global buttons
    
    turnImage = False
    imgRot = 0
    imgPos = "foreground"
    imgRet = 0
    retractImage = False
    newCard()
    
    Object.startGroup()
    b = Button(width/2, height*0.90, RoundRect(-570/2,-114/2,570,114)*0.5)
    b.clickAction = startTurn
    #transition(None, 'turnCard', 5, 0)
    buttons = Object.endGroup()
    
def startTurn(*args):
    print("a")
    global turnImage
    if args[1] == LEFT:
        turnImage = True

def draw():
    global turnImage
    global imgRot
    global imgPos
    global imgRet
    global retractImage
    global b
    global buttons
    global currentCard
    
    pushMatrix()
    translate(width/2, 0, 0)
    
    baseScale = globals.baseScale
    imgIndex = globals.imgIndex
    
    #Challenge card flip. When turnImage is true, the card will flip and show a new challenge.
    if turnImage:
        print(transition(None, 'turnCard', 500, 359)+10)
        print(imgRot)
        imgRot += 10
        if imgRot == 360:
            transition(None, 'turnCard', 5, 0, EXP)
            imgRot = 0
    if turnImage and (imgRot == 0):
        print('dead')
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
    
    for o in buttons:
        o.update()
    
def newCard():
    cardConfig = globals.cardConfig
    
    pool = {}
    for deck in globals.gameconfig["useDecks"]:
        pool.update(cardConfig[deck])
    setCard(choice(pool.keys()))
    
    
def setCard(card):
    global currentCard
    
    deck = card.split("-")[0]
    showStart = globals.cardConfig[deck][card]["dice"] or globals.cardConfig[deck][card]["timer"]
    
    currentCard = {
        "id": card,
        "back": "card-"+deck+"-back",
        "showStart": showStart
    }
