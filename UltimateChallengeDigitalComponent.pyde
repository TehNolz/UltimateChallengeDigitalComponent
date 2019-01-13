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
    def loadBar(progress=stage, duration=loadDuration, yOffset=0):
        width = 1133
        height = 600
        translate(0, yOffset)
        pushStyle()
        amount = float(progress) / duration
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
    elif stage == 1:
        fill(0)
        textSize(30)
        loadText = 'Loading assets...'
        loadBar()
        totalRequests, finishedRequests = data.loadData(True)
        if finishedRequests != totalRequests:
            loadText = 'Progress: '+scaleMemory(finishedRequests, 2) + '/'+scaleMemory(totalRequests, 2)
            loadBar(finishedRequests, totalRequests, 45)
            return False
        loadText = 'Progress: '+scaleMemory(finishedRequests, 2) + '/'+scaleMemory(totalRequests, 2)
        loadBar(finishedRequests, totalRequests, 45)
        loadText = 'Initializing settings screen...'
    elif stage == 2:
        pushStyle()
        stroke(204)
        strokeWeight(5)
        fill(204)
        rect(width/2-100, height*0.55+45, 200, 30)
        popStyle() 
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
    elif stage == 8:
        hint(DISABLE_OPTIMIZED_STROKE)
        hint(ENABLE_KEY_REPEAT)
        #textMode(SHAPE)
        loadStage += 1
        globals.log.info('Finished Loading!\t['+str(millis())+' ms]')
        return True
    else:
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
    tb_lines.append('\n\nSee \'logs\\ucdc_app.log\' for more details.')
    for line in tb_lines:
        lineno = tb_lines.index(line)+1
        _line = line.replace(os.path.dirname(os.path.realpath(__file__))+'\\', '')

        bare_tb += _line + '\n'
        _line = _line.replace(' ', '&nbsp;')
        
        colorTags = []
        def addTag(fontTag, start, end, endTag='</font>'):
            for tag, _start, _end, endTag in colorTags:
                if isWithin(start, _start, _end) or isWithin(end, _start, _end):
                    return # Enclosed tags are skipped
            colorTags.append((fontTag, start, end, endTag))
    
        pendingTags = list()
        for c in ('\'', '"'):
            if c in _line:
                searchOffset = 0
                newString = _line
                counter = 0
                tagStart = 0
                tagEnd = len(_line)
                while searchOffset != -1:
                    searchOffset = _line.find(c, searchOffset)
                    if searchOffset != 0 and _line[searchOffset-1] == '\\':
                        searchOffset += 1
                        continue
                    if searchOffset != -1:
                        if counter % 2 == 0:
                            tagStart = searchOffset
                        else:
                            tagEnd = searchOffset+1
                            addTag('<font color=#a31515>', tagStart, tagEnd)
                            tagStart = 0
                            tagEnd = len(_line)
                        counter += 1
                        searchOffset += 1
                    elif counter % 2 != 0:
                        pendingTags.append(('<font color=#a31515>', tagStart, tagEnd))
        for tag in pendingTags:
            addTag(*tag)
        
        if '#' in _line and lineno != 1 and lineno % 2 != 0:
            addTag('<font color=#008052>', _line.find('#'), len(_line))
            
        if '@' in _line and lineno != 1 and lineno % 2 != 0:
            addTag('<font color=#a31515>', _line.find('#'), len(_line))
        
        counter = 0
        words = list()
        for w in _line.split('&nbsp;'):
            words.extend(split_multiDelim(w, ' /\()"\'-:,;<>~!@#$%^&*|+=[]{}`~?'))
        
        occurrences = dict()
        import keyword
        kwlist = keyword.kwlist
        kwlist.extend(['True', 'False', 'None'])
        for kw in kwlist: 
            occurrences[kw] = _line.count(kw)
        
        for w in words:
            isNumber = False
            try:
                float(w)
                isNumber = True
            except:
                if len(w) == 0 or lineno == 1 or lineno % 2 == 0:
                    continue
                if True in [(w == _) for _ in kwlist]:
                    modStr = _line.replace(w, ' '*len(w), occurrences[w]-1)
                    index = modStr.find(w)
                    addTag('<font color=#0000ff>', index, index+len(w))
                
            if isNumber: 
                occurrences[w] = occurrences.get(w, 0) + 1
                modStr = _line.replace(w, ' '*len(w), occurrences[w]-1)
                
                index = modStr.find(w)
                addTag('<font color=#008052>', index, index+len(w))
            counter += 1

        # Sort the tags based on the closing index, because the string is modified back to front
        colorTags = sorted(colorTags, key=lambda tup: tup[2]) 
        for tag, start, end, endTag in colorTags[::-1]:
            _line = _line[:end] + endTag + _line[end:] 
            _line = _line[:start] + tag + _line[start:]
        
        if lineno != 1 and lineno % 2 != 0 and not _line.strip().startswith('File') and not _line.startswith('See'):
            # Apply the monospaced font face
            _line = '<font face=\'Monospaced\' style=\'font-weight:normal\'>' + _line + '</font>'
        elif lineno != 1 and line.strip().startswith('File'):
            _line = '&nbsp;&nbsp;&nbsp;&nbsp;'+_line.strip()
        custom_tb += ('\n' if tb_lines.index(line) != 0 else '') + _line
    
    globals.log.critical(bare_tb[:-1])
    
    custom_tb = custom_tb.replace('\n', '<br>')
    custom_tb = '<html>' + custom_tb + '</html>'
    
    pane = JOptionPane(custom_tb, JOptionPane.ERROR_MESSAGE)
    
    dialog = pane.createDialog('Traceback')
    dialog.setAlwaysOnTop(True)
    dialog.show()
    exit(1)

lastScreen = ''
activeKeys = set()
activeKeyCodes = set()
lastUpdate = 0
def draw():
    global lastUpdate
    try:
        updateDelay = millis() - lastUpdate
        lastUpdate = millis()
        global lastScreen
        # This loadscreen loads stuff in the draw so we can update the loading bar
        if not loadScreen(): return
        
        if updateDelay > 1000:
            globals.log.warning('Detected abnormally high update latency. ['+str(updateDelay)+' ms]')
        
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
        
        if not lastScreen == globals.currentMenu:
            globals.log.info('Screen changed to ' + globals.currentMenu + '.')
        lastScreen = str(globals.currentMenu)
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
            globals.log.info('Reloading background image')
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
