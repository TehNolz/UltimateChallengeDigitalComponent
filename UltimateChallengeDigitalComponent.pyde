import os
import loaddata
import globals
log = globals.log
import gamescreen
import debugconsole
log.info("Hello world!")

console = debugconsole.Console()

def setup():
    log.info("Running setup!")
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
    
    log.info("Starting!")
    gameScreen = gamescreen.gameScreen()
    
def draw():    
    imgIndex = globals.imgIndex
    cardConfig = globals.cardConfig
        
    #Calculate scaling. This assumes the normal screen resolution is 1133x600
    globals.baseScale = (height/6)/100.0
    
    background(180, 180, 180, 128)
    translate(width/2, 0, 0)
    
    imageMode(CENTER)
    rectMode(CENTER)
    textAlign(CENTER)
    
    if globals.currentMenu == "gamescreen":
        gameScreen.drawScreen()
        
    if console.showConsole:
            console.draw()
            
def mousePressed():
    baseScale = globals.baseScale
    
    if mouseButton == LEFT:
        if (416*baseScale <= mouseX <= 716*baseScale) and (510*baseScale <= mouseY <= 570*baseScale):
            if not gameScreen.retractImage:
                gameScreen.turnImage = True
        
def keyPressed():    
    #Open console
    if key == "`":
        console.toggleConsole()
            
    elif console.showConsole:
        console.input(key)
