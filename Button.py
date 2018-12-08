from Object import Object
from util import *
import globals

class Button(Object):
    allButtons = list()
    BOUNDED_CANVAS = False
    
    def __init__(self, x, y, r):
        Button.allButtons.append(self)
        Object.__init__(self, x, y)
        self.shape = r
        self.baseShape = self.shape.copy()
        self.color = color(255)
        self.hoverColor = color(240)
        self.pressColor = color(220)
        if False: # Transparent colors for when I am debugging based on visuals
            self.color = color(255,100)
            self.hoverColor = color(240,100)
            self.pressColor = color(220,100)
        self.mouseEntered = False
        self.clickedInside = False
        
        self.clickArea = None
        self.clickMatrix = None
        
        self.rotation = 0
        self.disableControls = True
        self.text = 'placeholder'
        
        # A set containing the mouseButton values that this button will respond to.
        self.activators = {LEFT}

        self.applyStyle('default')
    
    @staticmethod
    def initFromArgs(x, y, w, h): self = Button(x, y, Rectangle(0, 0, w, h)); return self
    @staticmethod
    def initFromRect(r): self = Button(r.X, r.Y, r.placeAtZero()); return self
    
    def setPosition(self, x, y): Object.setPosition(self, x, y)
    def drawImage(self):
        textAlign(LEFT)
        rectMode(CORNER)
        colorMode(HSB,255,255,255)
        stroke((millis()/float(20))%255, 255,150)
        colorMode(RGB)
        strokeJoin(ROUND)
        strokeWeight(max(sin(millis()/float(200)) +1, 0)+3)
        
        # Update various field that effect how the button responds to the cursor
        self.updateCursor()
        
        # Check if a click happened inside the mouse
        if (self.mousePress or self.mouseRelease) and mouseButton in self.activators:
            # Momentarily apply the cached matrix and do calculations.
            # This is part of the shape caching when clicking.
            pushMatrix()
            g.setMatrix(self.clickMatrix)
            clickInside = self.clickArea.contains(*self.getOOP(self.clickPos))
            popMatrix()
            if clickInside and not self.clickedInside:
                # This is the moment the button is clicked
                self.onClick(mouseButton)
            self.clickedInside = clickInside
        else:
            # Reset the field value
            self.clickedInside = False
        
        # Button state checks; idle, hover, press and click
        if self.mouseRelease and self.clickedInside and self.mouseEntered:
            # When the mouse is released and the click and cursor are inside the button
            # It also does onPress for the sake of the button style
            self.onPress(mouseButton)
            self.onRelease(mouseButton)
            
            # Resetting these values is a must because if the button does not idly update,
            # other buttons stop responding to input
            self.clickedInside = False
            self.mouseEntered = False
        if self.mousePress and self.clickedInside and self.mouseEntered:
            # If the mouse is pressed while the cursor is inside the button
            self.onPress(mouseButton)
        elif not self.mousePress and self.mouseEntered:
            # If the cursor is inside the button but doesn't press it
            self.onHover()
        else:
            # Run onNothing() when the button is idle
            self.onNothing()
        
        point(0,0)
        
        fill(0)
        # Reset rotation to keep text horizontal
        rotate(-self.rotation-self.localRotation)
        textSize(self.shape.maxRadius()/3)
        text(self.text, -textWidth(self.text)/2,textDescent()*1.3)

    def updateCursor(self):
        # Shape caching
        #  - Makes it so that if the button transforms away from the cursor
        #    after clicking don't matter
        # TL;DR - Makes buttons respond better
        if (self.mousePress or self.mouseRelease) and self.clickArea == None:
            self.clickArea = self.shape.copy()
            self.clickMatrix = g.getMatrix()
        elif not (self.mousePress or self.mouseRelease):
            self.clickArea = None
            self.clickMatrix = None
        
        # Check if button contains cursor
        if not self.isHighestPriorityClick():
            # If any higher priority button also contains the cursor, this button
            # won't even consider checking.
            mouseInside = False
        elif (self.mousePress or self.mouseRelease):
            # In case the mouse is pressed or released, use the cached button shape and matrix.
            # This streamlines button response.
            
            # Momentarily apply the cached matrix and do calculations.
            pushMatrix()
            g.setMatrix(self.clickMatrix)
            mouseInside = self.clickArea.contains(*self.getMousePos())
            popMatrix()
        else:
            # Check if the current shape contains the cursor.
            mouseInside = self.shape.contains(*self.getMousePos())
            if mouseInside and not self.mouseEntered: self.onEnter()
        
        if self.mouseEntered and not mouseInside:
            # This is the moment the mouse leaves the button
            self.onLeave()
        
        self.mouseEntered = mouseInside

    def onNothing(self):
        self.idleStyle(self, -1)
        self.idleAction(self, -1)
    def onHover(self):
        self.hoverStyle(self, -1)
        self.hoverAction(self, -1)
    def onClick(self, button):
        print('click')
        self.clickStyle(self, button)
        self.clickAction(self, button)
    def onPress(self, button):
        self.pressStyle(self, button)
        self.pressAction(self, button)
    def onRelease(self, button):
        log = globals.log
        log.debug(str(self) + ' activated. (MB'+str(button)+')')
        self.releaseStyle(self, button)
        self.releaseAction(self, button)
    def onEnter(self):
        self.enterStyle(self, -1)
        self.enterAction(self, -1)
    def onLeave(self):
        self.leaveStyle(self, -1)
        self.leaveAction(self, -1)
    
    # Placeholders for styles
    @staticmethod
    def idleStyle(self, button): pass
    @staticmethod
    def hoverStyle(self, button): pass
    @staticmethod
    def clickStyle(self, button): pass
    @staticmethod
    def pressStyle(self, button): pass
    @staticmethod
    def releaseStyle(self, button): pass
    @staticmethod
    def enterStyle(self, button): pass
    @staticmethod
    def leaveStyle(self, button): pass
    
    # Placeholders for actions
    @staticmethod
    def idleAction(self, button): pass
    @staticmethod
    def hoverAction(self, button): pass
    @staticmethod
    def clickAction(self, button): pass
    @staticmethod
    def pressAction(self, button): pass
    @staticmethod
    def releaseAction(self, button): pass
    @staticmethod
    def enterAction(self, button): pass
    @staticmethod
    def leaveAction(self, button): pass
    
    def applyStyle(self, name):
        """Apply a style to this button"""
        ButtonStyles.applyStyle(self, name)
    
    def getButtonsAbove(self):
        """Returns a list containing buttons with a higher draw priority"""
        return Button.allButtons[Button.allButtons.index(self)+1:]
    def isHighestPriorityClick(self):
        """Checks is the cursor isn't inside any buttons above it's priority"""
        for o in self.getButtonsAbove():
            if o.clickedInside: return False
        return True

class ButtonStyles:
    """
    Button styles are functions that give buttons their appearance based on what
    action is performed on the button.
    Styles can be merged. The most recently applied style only overwrites some
    parts of a previous style.
    """
    
    @staticmethod
    def applyStyle(button, name):
        """Applies a style to a button. Style names are case sensitive."""
        # Check if the style exists
        if not name in ButtonStyles.styles.keys():
            raise ButtonStyles.NoSuchStyleException('Style \'' + name + '\' does not exist.')
            
        # Cast the style to a field
        style = ButtonStyles.styles[name]
        
        # Cast all action styles to fields
        idle    = style('idle')
        hover   = style('hover')
        click   = style('click')
        press   = style('press')
        release = style('release')
        enter   = style('enter')
        leave   = style('leave')
        
        # Apply action styles if they are defined in the style
        if not idle    == None: button.idleStyle    = idle
        if not hover   == None: button.hoverStyle   = hover
        if not click   == None: button.clickStyle   = click
        if not press   == None: button.pressStyle   = press
        if not release == None: button.releaseStyle = release
        if not enter   == None: button.enterStyle   = enter
        if not leave   == None: button.leaveStyle   = leave

    def default(action):
        def idle(self, button):
            transitionFill(self, 100, self.color, EXP)
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            self.scaleLocal(transition(self, 'scale', 250, 1, EXP))
            self.shape.fill()
            
        def hover(self, button):
            transitionFill(self, 100, self.hoverColor, EXP)
            self.shape.radius = transition(self, 'radius', 150, self.shape.maxRadius()*0.25, SQRT)
            self.scaleLocal(transition(self, 'scale', 250, 1.1, SQRT))
            self.shape.fill()
        
        def press(self, button):
            transitionFill(self, 50, self.pressColor, SQRT)
            self.shape.radius = transition(self, 'radius', 75, self.shape.maxRadius()*0.75, SQRT)
            self.scaleLocal(transition(self, 'scale', 75, 0.8, SQRT))
            self.shape.fill()
        
        action = action.lower()
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        return None

    def default_pulsate(action):
        def idle(self, button):
            try: self.resetWave
            except: self.resetWave = False
            try: self.pulseAmplitude
            except: self.pulseAmplitude = 0.05
            transitionFill(self, 100, self.color, EXP)
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            wave = sin(PI * (float(millis()) / 1000))*self.pulseAmplitude
            self.scaleLocal(transition(self, 'scale', 250, 1+wave, EXP, self.resetWave))
            self.resetWave = False
            self.shape.fill()
            
        def hover(self, button):
            try: self.resetWave
            except: self.resetWave = False
            transitionFill(self, 100, self.hoverColor, EXP)
            self.shape.radius = transition(self, 'radius', 150, self.shape.maxRadius()*0.25, SQRT)
            self.scaleLocal(transition(self, 'scale', 250, 1.1, SQRT))
            self.resetWave = True
            self.shape.fill()
        
        def press(self, button):
            try: self.resetWave
            except: self.resetWave = False
            transitionFill(self, 50, self.pressColor, SQRT)
            self.shape.radius = transition(self, 'radius', 75, self.shape.maxRadius()*0.75, SQRT)
            self.scaleLocal(transition(self, 'scale', 75, 0.8, SQRT))
            self.resetWave = True
            self.shape.fill()
        
        action = action.lower()
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        return None
    
    def default_rotate(action):
        def idle(self, button):
            try: self.idleRotation
            except: self.idleRotation = 0
            transitionFill(self, 100, self.color, EXP)
            self.rotateLocal(transition(self, 'rotate', 250, self.idleRotation, SQRT))
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            self.scaleLocal(transition(self, 'scale', 250, 1, EXP))
            self.shape.fill()
            
        def hover(self, button):
            try: self.hoverRotation
            except: self.hoverRotation = QUARTER_PI
            transitionFill(self, 100, self.hoverColor, EXP)
            self.rotateLocal(transition(self, 'rotate', 250, self.hoverRotation, SQRT))
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.25, SQRT)
            self.scaleLocal(transition(self, 'scale', 250, 1.1, SQRT))
            self.shape.fill()
        
        def press(self, button):
            try: self.pressRotation
            except: self.pressRotation = 0
            transitionFill(self, 50, self.pressColor, SQRT)
            self.rotateLocal(transition(self, 'rotate', 75, self.pressRotation, SQRT))
            self.shape.radius = transition(self, 'radius', 75, self.shape.maxRadius()*0.75, SQRT)
            self.scaleLocal(transition(self, 'scale', 75, 0.8, SQRT))
            self.shape.fill()
        
        action = action.lower()
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        return None

    # A dictionary containing all styles and their name
    styles = {
        'default': default,
        'pulsate': default_pulsate,
        'rotate' : default_rotate
    }
    
    class NoSuchStyleException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
            
