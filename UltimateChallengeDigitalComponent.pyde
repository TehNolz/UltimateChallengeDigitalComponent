import os
import data
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
    data.loadData()
    font = globals.fonts["OpenSans"]
    textFont(font)
    
    #Start the game.
    log.info("Starting!")
    
    gameScreen.init()
    gameSetupScreen.init()
    mainMenu.init()
    test.init()

def draw():
    # Update the mousePress value in Object
    # Necessary because when 'mousePressed()' is used, the field 'mousePressed' for some reason starts raising errors
    Object.mousePress = mousePressed
    
    # Set the cursor to the arrow by default
    cursor(0)
    
    #Change background color            
    background(180)
    
    #Center ALL THE THINGS!
    imageMode(CENTER)
    rectMode(CENTER)
    
    #Calculate base scale
    globals.baseScale = float(height) / 600
    globals.baseScaleXY.X = float(width) / 1133
    globals.baseScaleXY.Y = float(height) / 600
    
    # We can either do a scale x and y base approach (currently used by the buttons), or
    # we go for a single baseScale and translate the missing height
    # downward. That way, things aren't elongated.
    # BTW, the scaling on gameScreen seems really unnecessary; why not
    # just use a single scale transformation at the start?
    
    ## Example of the translating the missing height
    # globals.baseScale = float(width) / 1133
    # heightAdjust = height - 600 * globals.baseScale
    # translate(0, heightAdjust/2)
    ## This scales everything to match the width, and centers everything
    ## vertically with a translate so that nothing is elongated.
    
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
    
    # Reset the mouseRelease value
    Object.mouseRelease = False
    
    # Reset the click position if the mouse is not pressed
    if not Object.mousePress:
        Object.clickPos = Vector2()

def mousePressed():
    baseX = globals.baseScaleXY.X
    baseY = globals.baseScaleXY.Y
    if globals.currentMenu in globals.textBoxDict:
        isInsideBox = False
        for textBox in globals.textBoxDict[globals.currentMenu]:
            if (textBox.x*baseX <= mouseX <= (textBox.x+textBox.boxWidth)*baseX) and (textBox.y*baseY <= mouseY <= (textBox.y+textBox.boxHeight)*baseY):
                isInsideBox = True
                textBox.active()
        if not isInsideBox:
            globals.activeTextBox = None
        
    Object.clickPos = Vector2(mouseX, mouseY)

def mouseReleased():
    Object.mouseRelease = True
    
def keyPressed():
    #Open console
    if key == "`":
        console.toggleConsole()
    
    #If the console is open, send every key as input.
    elif console.showConsole:
        console.input(key)
        
    #Send key to active text box, if any exist.
    elif globals.activeTextBox != None:
        textBox = globals.activeTextBox
        textBox.input(key)
        
    # Easy screen switchers
    if keyCode == UP:
        globals.currentMenu = 'test'
    if keyCode == LEFT:
        globals.currentMenu = 'gameScreen'
    if keyCode == DOWN:
        globals.currentMenu = 'mainMenu'
    if keyCode == RIGHT:
        globals.currentMenu = 'gameSetupScreen'
