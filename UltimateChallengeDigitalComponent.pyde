import os
import loaddata
import globals
log = globals.log
import gamescreen
import mainmenu
import debugconsole
from Object import Object
from util import *
log.info("Hello world!")

print('eat my ass')

console = debugconsole.Console()

def setup():
    log.info("Running setup!")
    global imgIndex
    global font
    global gameScreen
    global mainMenu
    size(1133, 600, P3D)
    
    #Load the loading screen (so meta)
    image(loadImage("misc-loadingscreen.png"), 0, 0, 1133, 600)
    
    log.info("Loading assets.")
    loaddata.loadData()
    font = globals.fonts["OpenSans"]
    textFont(font)
    
    log.info("Starting!")
    mainMenu = mainmenu.mainMenu()
    gameScreen = gamescreen.gameScreen()
    
def draw():
    imgIndex = globals.imgIndex
    cardConfig = globals.cardConfig
        
    #Calculate scaling. This assumes the normal screen resolution is 1133x600
    
    background(180, 180, 180, 128)
    
    imageMode(CENTER)
    rectMode(CENTER)
    textAlign(CENTER)

    if globals.currentMenu == "gamescreen":
        globals.baseScale = (height/6)/100.0
        gameScreen.draw()
    elif globals.currentMenu == "mainmenu":
        mainMenu.draw()
        
    if console.showConsole:
        console.draw()
    if not Object.mousePress: setClickPos(Vector2(), -1)

def mousePressed():
    Object.mouseRelease = False
    if not Object.mousePress: setClickPos(Vector2(mouseX,mouseY), mouseButton)
    Object.mousePress = True
    baseScale = globals.baseScale

def mouseReleased():
    Object.mousePress = False
    Object.mouseRelease = True
        
def keyPressed():    
    #Open console
    if key == "`":
        console.toggleConsole()
            
    elif console.showConsole:
        console.input(key)
