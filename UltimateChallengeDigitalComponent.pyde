import os
import loaddata
import globals
import gameScreen
import gameSetupScreen
import mainMenu
import console
import test
from Object import Object
from util import *

#Hello world!
log = globals.log
log.info("Hello world!")

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
    font = globals.fonts["OpenSans"] # is that sans from undertale?
    textFont(font)
    
    #Start the game.
    log.info("Starting!")
    
    gameSetupScreen.init()
    gameScreen.init()
    mainMenu.init()
    test.init()

def draw():
    #Change background color            
    background(180, 180, 180)
    
    #Center ALL THE THINGS!
    imageMode(CENTER)
    rectMode(CENTER)
    
    if keyCode == UP:
        globals.currentMenu = 'test'
    if keyCode == LEFT:
        globals.currentMenu = 'gameScreen'
    if keyCode == DOWN:
        globals.currentMenu = 'mainMenu'
    
    #Calculate base scale
    globals.baseScale = (height/6)/100.0
    
    #Switch to a different menu.
    if globals.currentMenu == "gameSetupScreen":
        gameSetupScreen.draw()
    elif globals.currentMenu == "gameScreen":
        gameScreen.draw()
    elif globals.currentMenu == "mainMenu":
        mainMenu.draw()
    elif globals.currentMenu == 'test':
        test.draw()
        
    #Show console, when necessary.
    if console.showConsole:
        console.draw()
    
    if not Object.mousePress:
        setClickPos(Vector2(), -1)
        Object.mousePress = False
        Object.mouseRelease = False

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
