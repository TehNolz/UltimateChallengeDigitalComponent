import os
import loaddata
import globals
import gameSetupScreen
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
    #printAttributes(g.matrix, 6)
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
    
    gameScreen.init()
    gameSetupScreen.init()
    mainMenu.init()
    test.init()

def draw():
    Object.mousePress = mousePressed
    if mousePressed:
        setClickPos(Vector2(mouseX,mouseY), mouseButton)
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
    if keyCode == RIGHT:
        globals.currentMenu = 'gameSetupScreen'
    
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
    Object.mouseRelease = False

def mousePressed():
    if globals.currentMenu in globals.textBoxDict:
        isInsideBox = False
        for textBox in globals.textBoxDict[globals.currentMenu]:
            if (textBox.x <= mouseX <= textBox.x+textBox.boxWidth) and (textBox.y <= mouseY <= textBox.y+textBox.boxHeight):
                isInsideBox = True
                textBox.active()
        if not isInsideBox:
            globals.activeTextBox = None
        

def mouseReleased():
    Object.mouseRelease = True
    
def keyPressed():
    #Open console
    if key == "`":
        console.toggleConsole()
    
    #If the console is open, send every key as input.
    elif console.showConsole:
        console.input(key)
        
    #Send key to active text bot, if any exist.
    elif globals.activeTextBox != None:
        textBox = globals.activeTextBox
        textBox.input(key)
