import os
import logging
import loaddata
import globals
import gamescreen

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

def setup():
    log.info("Running setup!")
    global cardConfig
    global imgIndex
    global font
    global gameScreen
    size(1133, 600, P3D)
    
    #Load the loading screen (so meta)
    image(loadImage("misc-loadingscreen.png"), 0, 0, 1133, 600)
    
    log.info("Loading assets.")
    loaddata.loadData()
    font = globals.fonts["OpenSans"]
    textFont(font)
        
    gameScreen = gamescreen.gameScreen()
    
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
    globals.baseScale = (height/6)/100.0
    
    background(180, 180, 180, 128)
    translate(width/2, 0, 0)
    
    imageMode(CENTER)
    rectMode(CENTER)
    textAlign(CENTER)
    
    if currentMenu == "gamescreen":
        gameScreen.drawScreen()
            
def mousePressed():
    global globalScreen
    baseScale = globals.baseScale
    
    if mouseButton == LEFT:
        if (416*baseScale <= mouseX <= 716*baseScale) and (510*baseScale <= mouseY <= 570*baseScale):
            if not gameScreen.retractImage:
                gameScreen.turnImage = True
        
            
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
