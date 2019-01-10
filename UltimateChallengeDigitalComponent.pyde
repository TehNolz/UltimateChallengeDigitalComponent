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
    
    
loadStage = 0
loadDuration = 8
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
        background(204)
        fill(0)
        textSize(30)
        text('Loading...', (width - textWidth('Loading'))/2, height/2)
        log.info("Starting!")
        loadText = 'Loading assets...'
    elif stage == 1:
        fill(0)
        textSize(30)
        text('Loading...', (width - textWidth('Loading'))/2, height/2)
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
        #textMode(SHAPE)
        return True
    loadBar()
    loadStage += 1
    return False

lastScreen = ''
keySpeed = 1 # 1 frame, or 60 times a second
keySpeedCounter = 0
keyRepeatDelay = 30 # 30 frames, or 500 milliseconds
keyRepeatCounter = 0
lastKeyEvent = None
lastKeyCode = None
activeKeys = set()
activeKeyCodes = set()

def draw():
    try:
        _draw()
    except Exception, e:
        import javax.swing.JOptionPane as JOptionPane
        import java.awt.Toolkit as Toolkit
        import os
        Toolkit.getDefaultToolkit().beep()
        if len(e.args) < 2:
            e.args = (e.args[0], '')
        message = ''
        if e.message != '':
            message = '\nERROR:  - Message: \''+e.message+'\''
        JOptionPane.showMessageDialog(None, 
            'ERROR: Caught '+e.__class__.__name__+message+'\nERROR:  - Cause: '+ e.args[1] + '\nERROR:  - Line:  '+ str(sys.exc_info()[2].tb_lineno) + ' at file '+ os.path.basename(__file__),
            "Traceback", 
            JOptionPane.WARNING_MESSAGE);
        raise e
def _draw():
    global lastScreen
    # This loadscreen loads stuff in the draw so we can update the loading bar
    if not loadScreen(): return
    
    global keySpeed
    global keySpeedCounter
    global keyRepeatDelay
    global keyRepeatCounter
    global lastKeyEvent
    global lastKeyCode
    global activeKeys
    global activeKeyCodes
    
    
    # This is to force key repeats because P3D is gay and disables that for some fucking reason
    # mind you key repeats work fucking fine in P2D
    if keyPressed:
        if keyRepeatCounter < keyRepeatDelay:
            keyRepeatCounter += 1
        else:
            if keySpeedCounter < keySpeed:
                keySpeedCounter += 1
            else:
                keySpeedCounter = 0
                _keyPressed(lastKeyEvent, lastKeyCode)
    else:
        keySpeedCounter = 0
        keyRepeatCounter = 0
        activeKeys = set()
        activeKeyCodes = set()
        lastKeyEvent = None
        lastKeyCode = None
    
    
    # Update the mousePress value in Object
    # Necessary because when 'mousePressed()' is used, the field 'mousePressed' for some reason starts raising errors
    Object.mousePress = mousePressed
    
    applySettings()
    
    #Center ALL THE THINGS!
    imageMode(CENTER)
    rectMode(CENTER)
    textAlign(LEFT)
    
    #Calculate base scale
    globals.baseScale = float(height) / 600
    globals.baseScaleXY.X = float(width) / 1133
    globals.baseScaleXY.Y = float(height) / 600
    
    #Switch to a different menu.
    pushStyle()
    pushMatrix()
    if globals.currentMenu == "gameSetupScreen":
        gameSetupScreen.draw(mousePressed)
    elif globals.currentMenu == "gameScreen":
        # Hides the prime number menu when you toggle to the gamescreen
        if not lastScreen == globals.currentMenu:
            gameScreen.showPrimeNumbers = False
        gameScreen.draw(mousePressed)
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
    lastScreen = globals.currentMenu
    popStyle()
    popMatrix()
        
    #Show console, when necessary.
    if console.showConsole:
        console.draw()
    
    # Reset the mouseRelease value
    Object.mouseRelease = False
    
    # Reset the click position if the mouse is not pressed
    if not Object.mousePress:
        Object.clickPos = Vector2()

def applySettings():
    updateFont()
    
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
    
def _keyPressed(key, keyCode): # This one is for key repeats
    global lastKeyEvent
    global lastKeyCode
    global keySpeedCounter
    global keyRepeatCounter
    global activeKeys
    global activeKeyCodes
    
    if not lastKeyEvent == key or not lastKeyCode == keyCode:
        keySpeedCounter = 0
        keyRepeatCounter = 0
    
    lastKeyEvent = key
    lastKeyCode = keyCode
    
    #Send key to active text box, if any exist.
    if globals.activeTextBox != None:
        textBox = globals.activeTextBox
        textBox.input(activeKeys, activeKeyCodes)
    
def keyPressed(): #This one is for single key strokes
    global activeKeys
    global activeKeyCodes

    if not key == CODED:
        if key.isalnum() or key in ' ./\()"\'-:,.;<>~!@#$%^&*|+=[]{}`~?':
            newActiveKeys = set()
            for k in activeKeys:
                if not k == CODED and not k.isalnum():
                    newActiveKeys.add(k)
            activeKeys = newActiveKeys
    activeKeys.add(key)
    activeKeyCodes.add(keyCode)
    _keyPressed(key, keyCode)
    
    #Open console
    if key == "`" and globals.debug:
        console.toggleConsole()

def keyReleased():
    global activeKeys
    global activeKeyCodes
    global lastKeyEvent
    global lastKeyCode
    if key in activeKeys: activeKeys.remove(key)
    if keyCode in activeKeyCodes: activeKeyCodes.remove(keyCode)
    if lastKeyEvent == key:
        lastKeyEvent = None
    if lastKeyCode == keyCode:
        lastKeyCode = None
