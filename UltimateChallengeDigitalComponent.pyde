import data
import globals
import settingsScreen
import gameSetupScreen
import gameScreen
import mainMenu
import manual
import console
import test
import textInput
import minigame
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
    background(204)
    
    
def loadScreen():
    global loadStage
    global loadDuration
    stage = loadStage
    # Shows a progress bar
    
    loadText = ''
    def loadBar():
        width = 1133
        height = 600
        pushStyle()
        amount = float(stage) / loadDuration
        stroke(0)
        strokeWeight(2)
        fill(255)
        rect(width/2-100, height*0.55, 200, 30, 5)
        fill(0, 187, 255)
        noStroke()
        rect(width/2-100, height*0.55, 200 * amount, 30, 5)
        fill(0)
        textSize(20)
        textAlign(CENTER)
        if textWidth(loadText) + textAscent() > 200:
            textSize(20 * (200 / float(textWidth(loadText) + textAscent())))
        text(loadText, width/2, height*0.55 + 15 + textHeight(loadText) / 2)
        popStyle()
    
    if stage == 0:
        fill(0)
        textSize(30)
        text('Loading...', (width - textWidth('Loading'))/2, height/2)
        log.info("Starting!")
        loadText = 'Loading assets...'
    elif stage == 1:
        data.loadData()
        loadText = 'Initializing settings screen...'
    elif stage == 2:
        settingsScreen.init()
        loadText = 'Initializing game screen...'
    elif stage == 3:
        gameScreen.init()
        loadText = 'Initializing game setup screen...'
    elif stage == 4:
        gameSetupScreen.init()
        loadText = 'Initializing main menu...'
    elif stage == 5:
        mainMenu.init()
        loadText = 'Initializing misc assets...'
    elif stage == 6:
        test.init()
        loadText = 'Initializing console...'
    elif stage == 7:
        console.init()
        loadText = 'Initializing manual screen...'
    elif stage == 8:
        manual.init()
        loadText = 'Congfiguring renderer...'
    else:
        hint(DISABLE_OPTIMIZED_STROKE)
        textMode(SHAPE)
        return True
    loadBar()
    loadStage += 1
    return False

loadStage = 0
loadDuration = 8
def draw():
    if not loadScreen(): return
    
    # Update the mousePress value in Object
    # Necessary because when 'mousePressed()' is used, the field 'mousePressed' for some reason starts raising errors
    Object.mousePress = mousePressed
    #textFont(font)
    
    applySettings()
    
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
        manual.draw()
    elif globals.currentMenu == "minigame":
        minigame.draw(mousePressed)
    elif globals.currentMenu == "settings":
        settingsScreen.draw()
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

def applySettings():
    # Load background from globals
    backgroundImg = globals.backgroundImg
    # In case it is None, use a white background instead and load a new image
    if backgroundImg == None:
        background(255)
        globals.backgroundImg = globals.imgIndex[globals.backgroundImgName].copy()
    else:
        # Reload and resize the background image if the dimensions don't match the screen
        # All this reloading nonsense is to prevent heapspace errors. Basically we're trying
        # to reload the image as little as possible.
        if not backgroundImg.width == width and not backgroundImg.height == height:
            del globals.backgroundImg
            globals.backgroundImg = globals.imgIndex[globals.backgroundImgName].copy()
            globals.backgroundImg.resize(width, height)
            backgroundImg = globals.backgroundImg
        background(backgroundImg)

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
        gameScreen.newCard()
        globals.currentMenu = 'gameScreen'
    if keyCode == RIGHT:
        globals.currentMenu = 'gameSetupScreen'
