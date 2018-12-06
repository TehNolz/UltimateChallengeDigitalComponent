import os
import loaddata
import globals
import gamescreen
import mainmenu
import debugconsole
from Object import Object
from util import *

#Hello world!
log = globals.log
log.info("Hello world!")

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
    
    #Load assets
    log.info("Loading assets.")
    loaddata.loadData()
    font = globals.fonts["OpenSans"]
    textFont(font)
    
    #Start the game.
    log.info("Starting!")
    mainMenu = mainmenu.mainMenu()
    gameScreen = gamescreen.gameScreen()

def draw():
    #Change background color            
    background(180, 180, 180, 255)
    
    #Center ALL THE THINGS!
    imageMode(CENTER)
    rectMode(CENTER)
    textAlign(CENTER)

    #Calculate base scale, then store it in globals.
    #This assumes a base resolution of 600x1133. Scale is a float (eg. 1.65).
    #Multiply values by baseScale to make them scale properly when the window size changes.
    
    #Switch to a different menu.
    if globals.currentMenu == "gamescreen":
        globals.baseScale = (height/6)/100.0
        gameScreen.draw()
    elif globals.currentMenu == "mainmenu":
        mainMenu.draw()
        
    #Show console, when necessary.
    if console.showConsole:
        console.draw()

def mousePressed():
    Object.mouseRelease = False
    if not Object.mousePress: 
        setClickPos(Vector2(mouseX,mouseY), mouseButton)
    Object.mousePress = True
    baseScale = globals.baseScale

def mouseReleased():
    Object.mousePress = False
    Object.mouseRelease = True
        
def keyPressed():    
    #Open console
    if key == "`":
        console.toggleConsole()
    
    #If the console is open, send every key as input.
    elif console.showConsole:
        console.input(key)
