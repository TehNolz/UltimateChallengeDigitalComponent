import data
import globals
import gameSetupScreen
import gameScreen
import mainMenu
import manual
import console
import test
import textInput
from Object import Object
from util import *

#Hello world!
log = globals.log
log.info("Hello world!")

def setup():
    #log.info("Running setup!")
    global imgIndex
    global font
    global gameScreen
    global mainMenu
    global font
    size(1133, 600, P3D)
    smooth(8)

    #Load the loading screen (so meta)
    image(loadImage("misc-loadingscreen.png"), 0, 0, 1133, 600)
    
    #Start the game.
    log.info("Starting!")
    
    data.loadData()
    gameScreen.init()
    gameSetupScreen.init()
    mainMenu.init()
    test.init()
    console.init()
    manual.init()
    
    hint(DISABLE_OPTIMIZED_STROKE)

def draw():
    # Update the mousePress value in Object
    # Necessary because when 'mousePressed()' is used, the field 'mousePressed' for some reason starts raising errors
    Object.mousePress = mousePressed
    #textFont(font)
    
    # Set the cursor to the arrow by default
    cursor(0)
    
    #Change background color            
    background(globals.backgroundColor)
    
    #Center ALL THE THINGS!
    imageMode(CENTER)
    rectMode(CENTER)
    
    #Calculate base scale
    globals.baseScale = float(height) / 600
    globals.baseScaleXY.X = float(width) / 1133
    globals.baseScaleXY.Y = float(height) / 600
    
    #Switch to a different menu.
    if globals.currentMenu == "gameSetupScreen":
        gameSetupScreen.draw()
    elif globals.currentMenu == "gameScreen":
        gameScreen.draw()
    elif globals.currentMenu == "mainMenu":
        mainMenu.draw()
    elif globals.currentMenu == "manual":
        manual.draw(mousePressed)
    elif globals.currentMenu == "test":
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
    textInput.check()
    Object.clickPos = Vector2(mouseX, mouseY)

def mouseReleased():
    Object.mouseRelease = True
    
def keyPressed():
    #Open console
    if key == "`":
        console.toggleConsole()

    #Send key to active text box, if any exist.
    elif globals.activeTextBox != None:
        textBox = globals.activeTextBox
        textBox.input(key, keyCode)
        
    # Easy screen switchers
    if keyCode == UP:
        globals.currentMenu = 'test'
    if keyCode == LEFT:
        globals.currentMenu = 'gameScreen'
    if keyCode == DOWN:
        globals.currentMenu = 'mainMenu'
    if keyCode == RIGHT:
        globals.currentMenu = 'gameSetupScreen'
