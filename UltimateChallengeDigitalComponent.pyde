import data
import globals
import settingsScreen
import gameSetupScreen
import gameScreen
import mainMenu
import manual
import console
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
loadDuration = 7
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
        loadText = 'Initializing console...'
    elif stage == 6:
        console.init()
        loadText = 'Initializing manual screen...'
    elif stage == 7:
        manual.init()
        loadText = 'Congfiguring renderer...'
    else:
        hint(DISABLE_OPTIMIZED_STROKE)
        hint(ENABLE_KEY_REPEAT)
        #textMode(SHAPE)
        return True
    loadBar()
    loadStage += 1
    return False

def showErrorMessage():
    import javax.swing.JOptionPane as JOptionPane
    import javax.swing.JDialog as JDialog
    import java.awt.Toolkit as Toolkit
    import java.awt.Font as Font
    import os, traceback
    
    Toolkit.getDefaultToolkit().beep()
    
    custom_tb = ''
    bare_tb = ''
    tb_lines = traceback.format_exc().split('\n')
    counter = 0
    for line in tb_lines[:-1]:
        counter += 1
        _line = line.replace(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '')

        bare_tb += _line + '\n'
    
        _line = _line.replace(' ', '&nbsp;')
        if counter != 1 and counter % 2 != 0:
            # Apply the monospaced font face
            _line = '<font face=\'Monospaced\' style=\'font-weight:normal\'>' + _line + '</font>'
        elif counter != 1 and line.strip().startswith('File'):
            _line = '&nbsp;&nbsp;&nbsp;&nbsp;'+_line.strip()
        custom_tb += ('\n' if tb_lines.index(line) != 0 else '') + _line
    
    globals.log.critical(bare_tb[:-1])
    
    custom_tb = custom_tb.replace('\n', '<br>')
    custom_tb = custom_tb = '<html>' + custom_tb + '</html>'
    
    pane = JOptionPane(custom_tb, JOptionPane.ERROR_MESSAGE)
    
    dialog = pane.createDialog('Traceback')
    dialog.setAlwaysOnTop(True)
    dialog.show()
    exit(1)

lastScreen = ''
activeKeys = set()
activeKeyCodes = set()
def draw():
    try:
        global lastScreen
        # This loadscreen loads stuff in the draw so we can update the loading bar
        if not loadScreen(): return
        
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
        lastScreen = globals.currentMenu
        popStyle()
        popMatrix()
            
        #Show console, when necessary.
        if console.showConsole:
            console.draw(mousePressed)
        
        # Reset the mouseRelease value
        Object.mouseRelease = False
        
        # Reset the click position if the mouse is not pressed
        if not Object.mousePress:
            Object.clickPos = Vector2()
    except:
        showErrorMessage()

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
    try:
        textInput.check()
        Object.clickPos = Vector2(mouseX, mouseY)
    except:
        showErrorMessage()
    
def mouseReleased():
    try:
        Object.mouseRelease = True
    except:
        showErrorMessage()
    
def keyPressed():
    try:
        global activeKeys
        global activeKeyCodes
    
        if not key == CODED:
            if key.isalnum() or key in ' ./\()"\'-:,.;<>~!@#$%^&*|+=[]{}`~?':
                newActiveKeys = set()
                for k in activeKeys:
                    if not k == CODED and not k.isalnum() and not isWordDelimiter(k):
                        newActiveKeys.add(k)
                activeKeys = newActiveKeys
        activeKeys.add(key)
        activeKeyCodes.add(keyCode)
        
        #Send key to active text box, if any exist.
        if globals.activeTextBox != None:
            textBox = globals.activeTextBox
            textBox.input(activeKeys, activeKeyCodes)
            
        #Open console with F12
        if keyCode == 108 and globals.userConfig['settings']['enable_debug_console']:
            console.toggleConsole()
    except:
        showErrorMessage()

def keyReleased():
    try:
        global activeKeys
        global activeKeyCodes
        if key in activeKeys: activeKeys.remove(key)
        if keyCode in activeKeyCodes: activeKeyCodes.remove(keyCode)
    except:
        showErrorMessage()
