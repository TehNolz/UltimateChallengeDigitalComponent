import globals
from util import *
from Button import Button
from Object import Object
from random import choice

class gameScreen:
    def __init__(self):
        self.turnImage = False
        self.imgRot = 0
        self.imgPos = "foreground"
        self.imgRet = 0
        self.retractImage = False
        self.newCard()
        transition(self, 'turnCard', 5, 0)
        
    once = False
    def draw(self):
        
        baseScale = globals.baseScale
        imgIndex = globals.imgIndex
        
        #Challenge card flip. When turnImage is true, the card will flip and show a new challenge.
        if self.turnImage:
            transition(self, 'turnCard', 500, 359)+10
            print(self.imgRot)
            self.imgRot += 10
            if self.imgRot == 360:
                transition(self, 'turnCard', 5, 0, EXP)
                self.imgRot = 0
        if self.turnImage and (self.imgRot == 0):
            print('dead')
            self.turnImage = False
        elif self.imgRot == 180:
            self.newCard()
            
        #Challenge card retract. When retractImage is true, the card will move forwards/backwards depending on whether its currently backwards/forwards.
        if self.retractImage:
            if self.imgPos == "foreground":
                if self.imgRet == -200:
                    self.retractImage = False
                    self.imgPos = "background"
                else:
                    self.imgRet-=5
            elif self.imgPos == "background":
                if self.imgRet == 0:
                    self.retractImage = False
                    self.imgPos = "foreground"
                else:
                    self.imgRet+=5

        #Card
        pushMatrix()
        base = 400
        imgHeight = base*baseScale
        imgWidth = ((base/4)*3)*baseScale
        translate(0, height/2, self.imgRet*baseScale)
        rotateY(radians(self.imgRot))
        image(imgIndex[self.currentCard["back"]], 0, 0, imgWidth, imgHeight)
        rotateY(radians(180))
        scale(-1, 1) #Yes, this IS necessary.
        translate(0, 0, -1)
        image(imgIndex["card-"+self.currentCard["id"]], 0, 0, imgWidth, imgHeight)
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
        
    def newCard(self):
        cardConfig = globals.cardConfig
        
        pool = {}
        for deck in globals.gameconfig["useDecks"]:
            pool.update(cardConfig[deck])
        self.setCard(choice(pool.keys()))
        
        
    def setCard(self, card):
        deck = card.split("-")[0]
        showStart = globals.cardConfig[deck][card]["dice"] or globals.cardConfig[deck][card]["timer"]
        
        self.currentCard = {
            "id": card,
            "back": "card-"+deck+"-back",
            "showStart": showStart
        }
