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
        self.stroke = color(0)
        self.color = color(255)
        self.hoverColor = color(240)
        self.pressColor = color(220)
        self.textColor = color(0)
        self.textSize = self.shape.getMaxTextSize() / 5
        self.font = createFont('Sans Serif', self.shape.getMaxTextSize()*0.75)
        self.mouseEntered = False
        self.clickedInside = False
        
        self.clickArea = None
        self.clickMatrix = None
        
        self.rotation = 0
        self.disableControls = True
        self.text = ''
        
        # A set containing the mouseButton values that this button will respond to.
        self.activators = {LEFT}

        self.applyStyle('default')
    
    @staticmethod
    def initFromArgs(x, y, w, h): self = Button(x, y, Rectangle(0, 0, w, h)); return self
    @staticmethod
    def initFromRect(r): self = Button(r.X, r.Y, r.placeAtZero()); return self
    
    def setPosition(self, x, y): Object.setPosition(self, x, y)
    def drawImage(self):
        textAlign(CENTER)
        rectMode(CORNER)
        colorMode(HSB,255,255,255)
        self.stroke = color((float(millis())/20)%255, 255, 150)
        colorMode(RGB)
        strokeJoin(ROUND)
        strokeWeight(3)
        textFont(self.font)
        
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
        elif self.mousePress and self.clickedInside and self.mouseEntered:
            # If the mouse is pressed while the cursor is inside the button
            self.onPress(mouseButton)
        elif not self.mousePress and self.mouseEntered:
            # If the cursor is inside the button but doesn't press it
            self.onHover()
        else:
            # Run onNothing() when the button is idle
            self.onNothing()
    
        # Reset rotation to keep text horizontal

    def updateCursor(self):
        """Update various field that effect how the button responds to the cursor"""
        # Shape caching
        #  - Makes it so that if the button transforms away from the cursor
        #    after clicking, the cursor isn't registered as having left the button.
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
    
    radioButtons = set()
    
    @staticmethod
    def applyStyle(button, name):
        """Applies a style to a button. Style names are case sensitive."""
        # Check if the style exists
        if not name in ButtonStyles.styles.keys():
            raise ButtonStyles.NoSuchStyleException('Style \'' + name + '\' does not exist.')
            
        # Cast the style to a field
        style = ButtonStyles.styles[name]
        
        # Cast all action styles to fields
        setup   = style('setup')
        idle    = style('idle')
        hover   = style('hover')
        click   = style('click')
        press   = style('press')
        release = style('release')
        enter   = style('enter')
        leave   = style('leave')
        
        # Run style setup if defined
        if not setup   == None: setup(button)
        
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
            stroke(self.stroke)
            transitionFill(self, 100, self.color)
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            self.scaleLocal(transition(self, 'scale', 250, 1, EXP))
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            
        def hover(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.hoverColor)
            self.shape.radius = transition(self, 'radius', 150, self.shape.maxRadius()*0.25, SQRT)
            self.scaleLocal(transition(self, 'scale', 250, 1.1, SQRT))
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            cursor(HAND)
        
        def press(self, button):
            stroke(self.stroke)
            transitionFill(self, 50, self.pressColor)
            self.shape.radius = transition(self, 'radius', 75, self.shape.maxRadius()*0.75, SQRT)
            self.scaleLocal(transition(self, 'scale', 75, 0.8, SQRT))
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            cursor(HAND)
        
        action = action.lower()
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        return None

    def default_pulsate(action):
        # Setup initializes style-specific fields
        def setup(self):
            self.resetWave = False
            self.pulseAmplitude = 0.025
        
        def idle(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.color)
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            wave = sin(PI * (float(millis()) / 1000))*self.pulseAmplitude
            self.scaleLocal(transition(self, 'scale', 250, 1+wave, EXP, self.resetWave))
            self.resetWave = False
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            
        def hover(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.hoverColor)
            self.shape.radius = transition(self, 'radius', 150, self.shape.maxRadius()*0.25, SQRT)
            self.scaleLocal(transition(self, 'scale', 250, 1.1, SQRT))
            self.resetWave = True
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            cursor(HAND)
        
        def press(self, button):
            stroke(self.stroke)
            transitionFill(self, 50, self.pressColor)
            self.shape.radius = transition(self, 'radius', 75, self.shape.maxRadius()*0.75, SQRT)
            self.scaleLocal(transition(self, 'scale', 75, 0.8, SQRT))
            self.resetWave = True
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            cursor(HAND)
        
        action = action.lower()
        if action == 'setup': return setup
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        return None
    
    def default_rotate(action):
        def setup(self):
            self.idleRotation = 0
            self.hoverRotation = QUARTER_PI
            self.pressRotation = 0
        
        def idle(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.color)
            self.rotateLocal(transition(self, 'rotate', 250, self.idleRotation, SQRT))
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            self.scaleLocal(transition(self, 'scale', 250, 1, EXP))
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            
        def hover(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.hoverColor)
            self.rotateLocal(transition(self, 'rotate', 250, self.hoverRotation, SQRT))
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.25, SQRT)
            self.scaleLocal(transition(self, 'scale', 250, 1.1, SQRT))
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            cursor(HAND)
        
        def press(self, button):
            stroke(self.stroke)
            transitionFill(self, 50, self.pressColor)
            self.rotateLocal(transition(self, 'rotate', 75, self.pressRotation, SQRT))
            self.shape.radius = transition(self, 'radius', 75, self.shape.maxRadius()*0.75, SQRT)
            self.scaleLocal(transition(self, 'scale', 75, 0.8, SQRT))
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            cursor(HAND)
        
        action = action.lower()
        if action == 'setup': return setup
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        return None
    
    def default_rotate_pulsate(action):
        def setup(self):
            self.idleRotation = 0
            self.hoverRotation = QUARTER_PI
            self.pressRotation = 0
            self.pulseAmplitude = 0.025
            self.resetWave = True
        
        def idle(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.color)
            self.rotateLocal(transition(self, 'rotate', 250, self.idleRotation, SQRT))
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            wave = sin(PI * (float(millis()) / 1000))*self.pulseAmplitude
            self.scaleLocal(transition(self, 'scale', 250, 1+wave, EXP, self.resetWave))
            self.resetWave = False
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            
        def hover(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.hoverColor)
            self.rotateLocal(transition(self, 'rotate', 250, self.hoverRotation, SQRT))
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.25, SQRT)
            self.scaleLocal(transition(self, 'scale', 250, 1.1, SQRT))
            self.resetWave = True
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            cursor(HAND)
        
        def press(self, button):
            stroke(self.stroke)
            transitionFill(self, 50, self.pressColor)
            self.rotateLocal(transition(self, 'rotate', 75, self.pressRotation, SQRT))
            self.shape.radius = transition(self, 'radius', 75, self.shape.maxRadius()*0.75, SQRT)
            self.scaleLocal(transition(self, 'scale', 75, 0.8, SQRT))
            self.resetWave = True
            self.shape.fill()
            fill(self.textColor)
            rotate(-self.rotation-self.localRotation)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
            cursor(HAND)
        
        action = action.lower()
        if action == 'setup': return setup
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        return None

    def default_radio(action):
        def setup(self):
            ButtonStyles.radioButtons.add(self)
            # Force the button to become round
            if not self.shape.width == self.shape.height:
                # Scale height to match width
                if self.shape.width < self.shape.height:
                    self.shape.Y += (h - w) / 2
                    self.shape.height = self.shape.width
                # Scale width to match height
                else:
                    self.shape.X += (w - h) / 2
                    self.shape.width = self.shape.height
            self.radioGroup = ''
            self.activated = False
            self.radioColor = color(0, 75)
            # ColorTransition tells the transitionFill when it should cache it's color. (Hard to explain, it's important trust me)
            self.colorTransition = True
            self.shape.radius = self.shape.maxRadius()
            self.indicatorScale = 0.5
        
        def idle(self, button):
            # This is the color of the indicator. Part of me still wanted to be able to use the rainbow stroke color.
            # This scales based on the alpha of the box color: <stroke|0] alpha [255|radio_color>
            c = lerpColor(self.stroke, removeAlpha(self.radioColor), float(alpha(self.radioColor)) / 255)
            stroke(self.stroke)
            self.scaleLocal(transition(self, 'scale', 100, 1, EXP))
            transitionFill(self, 100, self.color)
            self.shape.fill()
            if self.activated:
                transitionFill(self, 100, c, LIN, self.colorTransition, 'radio')
                self.colorTransition = False
            else:
                transitionFill(self, 100, self.color, LIN, True, 'radio')
                # This prevents the transitionFill from thinking it needs to reset
                self.colorTransition = True
            noStroke()
            pushMatrix()
            scale(self.indicatorScale)
            ellipse(0,0,self.shape.width, self.shape.height)
            popMatrix()
        
        def hover(self, button):
            c = lerpColor(self.stroke, removeAlpha(self.radioColor), float(alpha(self.radioColor)) / 255)
            stroke(self.stroke)
            self.scaleLocal(transition(self, 'scale', 100, 1.1, SQRT))
            transitionFill(self, 100, self.hoverColor)
            self.shape.fill()
            if self.activated:
                transitionFill(self, 100, c, LIN, self.colorTransition, 'radio')
                self.colorTransition = False
            else:
                transitionFill(self, 100, self.hoverColor, LIN, True, 'radio')
                self.colorTransition = True
            noStroke()
            pushMatrix()
            scale(self.indicatorScale)
            ellipse(0,0,self.shape.width, self.shape.height)
            popMatrix()
            cursor(HAND)
        
        def press(self, button):
            c = lerpColor(self.stroke, removeAlpha(self.radioColor), float(alpha(self.radioColor)) / 255)
            stroke(self.stroke)
            self.scaleLocal(transition(self, 'scale', 50, 0.9, SQRT))
            transitionFill(self, 50, self.pressColor)
            self.shape.fill()
            if self.activated:
                transitionFill(self, 50, c, LIN, self.colorTransition, 'radio')
                self.colorTransition = False
            else:
                transitionFill(self, 50, self.pressColor, LIN, True, 'radio')
                self.colorTransition = True
            noStroke()
            pushMatrix()
            scale(self.indicatorScale)
            ellipse(0,0,self.shape.width, self.shape.height)
            popMatrix()
            cursor(HAND)
        
        def release(self, button):
            otherButtons = [x for x in ButtonStyles.radioButtons if x.radioGroup == self.radioGroup and not x == self]
            for x in otherButtons: x.activated = False
            self.activated = True
        
        action = action.lower()
        if action == 'setup': return setup
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        if action == 'release': return release
        return None

    def default_checkbox(action):
        def setup(self):
            self.boxColor = color(0, 75)
            self.activated = False
            self.colorTransition = True
            self.indicatorScale = 0.5
        
        def idle(self, button):
            # This is the color of the indicator. Part of me still wanted to be able to use the rainbow stroke color.
            # This scales based on the alpha of the box color: <stroke|0] alpha [255|box_color>
            c = lerpColor(self.stroke, removeAlpha(self.boxColor), float(alpha(self.boxColor)) / 255)
            stroke(self.stroke)
            self.scaleLocal(transition(self, 'scale', 100, 1, EXP))
            transitionFill(self, 100, self.color)
            self.shape.fill()
            if self.activated:
                transitionFill(self, 100, c, LIN, self.colorTransition, 'box')
                self.colorTransition = False
            else:
                transitionFill(self, 100, self.color, LIN, True, 'box')
                self.colorTransition = True
            # Apply the cached fill color to stroke because otherwise the borders are missing
            stroke(getColor(self, '<fill>box#MEM', self.color))
            (self.shape * self.indicatorScale).fill()
            
        def hover(self, button):
            c = lerpColor(self.stroke, removeAlpha(self.boxColor), float(alpha(self.boxColor)) / 255)
            stroke(self.stroke)
            self.scaleLocal(transition(self, 'scale', 100, 1.1, SQRT))
            transitionFill(self, 100, self.hoverColor)
            self.shape.fill()
            if self.activated:
                transitionFill(self, 100, c, LIN, self.colorTransition, 'box')
                self.colorTransition = False
            else:
                transitionFill(self, 100, self.hoverColor, LIN, True, 'box')
                self.colorTransition = True
            stroke(getColor(self, '<fill>box#MEM', self.color))
            (self.shape * self.indicatorScale).fill()
            cursor(HAND)
            
        def press(self, button):
            c = lerpColor(self.stroke, removeAlpha(self.boxColor), float(alpha(self.boxColor)) / 255)
            stroke(self.stroke)
            self.scaleLocal(transition(self, 'scale', 50, 1, SQRT))
            transitionFill(self, 50, self.pressColor)
            self.shape.fill()
            if self.activated:
                transitionFill(self, 50, c, LIN, self.colorTransition, 'box')
                self.colorTransition = False
            else:
                transitionFill(self, 50, self.pressColor, LIN, True, 'box')
                self.colorTransition = True
            stroke(getColor(self, '<fill>box#MEM', self.color))
            (self.shape * self.indicatorScale).fill()
            cursor(HAND)
        
        def release(self, button):
            self.activated = not self.activated
            
        action = action.lower()
        if action == 'setup': return setup
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        if action == 'release': return release
        return None

    def custom_dice(action):
        def setup(self):
            self.throwdice = False
            self.rolled = 0
            self.Rolldice = 2
        
        def throw(self):
            Width = self.shape.width
            Height = self.shape.height
            
            # Calculate the size of the dots  (smallest dimension * (2/15))
            if Width > Height:
                dotSize = Height * (float(2)/15)
            else:
                dotSize = Width * (float(2)/15)
            
            import random
            if self.throwdice:
                self.Rolldice = random.randint(1,6)
                self.rolled+=1
                if self.rolled == 25:
                    self.throwdice = False
                    self.rolled = 0
            
            if self.Rolldice==1:
                ellipse(0, 0, dotSize, dotSize)
                        
            elif self.Rolldice==2:
                ellipse(0, 0, dotSize, dotSize)
                ellipse(Width/6, 0, dotSize, dotSize)
                ellipse(-Width/6, 0, dotSize, dotSize)
                    
            elif self.Rolldice==3:
                ellipse(0, 0, dotSize, dotSize)
                ellipse(Width/6, Height/6, dotSize, dotSize)
                ellipse(-Width/6, -Height/6, dotSize, dotSize)
                        
            elif self.Rolldice==4:
                ellipse(-Width/6, Width/6, dotSize, dotSize)
                ellipse(Width/6, -Width/6, dotSize, dotSize)
                ellipse(Width/6, Width/6, dotSize, dotSize)
                ellipse(-Width/6, -Width/6, dotSize, dotSize)
                        
            elif self.Rolldice==5:
                ellipse(0, 0, dotSize, dotSize)
                ellipse(-Width/6, Width/6, dotSize, dotSize)
                ellipse(Width/6, -Width/6, dotSize, dotSize)
                ellipse(Width/6, Width/6, dotSize, dotSize)
                ellipse(-Width/6, -Width/6, dotSize, dotSize)
                    
            elif self.Rolldice==6:
                ellipse(-Width/6, Width/6, dotSize, dotSize)
                ellipse(Width/6, -Width/6, dotSize, dotSize)
                ellipse(Width/6, 0, dotSize, dotSize)
                ellipse(-Width/6, 0, dotSize, dotSize)
                ellipse(Width/6, Width/6, dotSize, dotSize)
                ellipse(-Width/6, -Width/6, dotSize, dotSize)
            
        def idle(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.color)
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            self.scaleLocal(transition(self, 'scale', 250, 1, EXP))
            self.shape.fill()
            throw(self)
        
        def hover(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.hoverColor)
            self.shape.radius = transition(self, 'radius', 150, self.shape.maxRadius()*0.25, SQRT)
            self.scaleLocal(transition(self, 'scale', 250, 1.1, SQRT))
            self.shape.fill()
            cursor(HAND)
            throw(self)
        
        def press(self, button):
            stroke(self.stroke)
            transitionFill(self, 50, self.pressColor)
            self.shape.radius = transition(self, 'radius', 75, self.shape.maxRadius()*0.75, SQRT)
            self.scaleLocal(transition(self, 'scale', 75, 0.8, SQRT))
            self.shape.fill()
            cursor(HAND)
            throw(self)
        
        def release(self, button):
            self.throwdice = True
        
        action = action.lower()
        if action == 'setup': return setup
        if action == 'idle': return idle
        if action == 'hover': return hover
        if action == 'press': return press
        if action == 'release': return release
        return None

    def default_compact(action):
        def setup(self):
            self.description = ''
        
        def idle(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.color)
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            self.scaleLocal(transition(self, 'scale', 250, 1, EXP))
            self.shape.fill()
            
            rotate(-self.rotation-self.localRotation)
            descBox = self.shape.copy()
            descBox.setPos(0, -self.shape.height*0.8/2)
            descBox.height *= 0.8
            descBox.width = transition(self, 'resize_desc', 250, 0, SQRT)
            descBox.radius = descBox.maxRadius()
            descBox.radius = constrain(descBox.radius, 0, self.shape.radius)
            descBox.fill()
            
            fill(self.textColor)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
        
        def hover(self, button):
            stroke(self.stroke)
            transitionFill(self, 100, self.hoverColor)
            self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
            self.scaleLocal(transition(self, 'scale', 250, 1, EXP))
            self.shape.fill()
            
            rotate(-self.rotation-self.localRotation)
            descBox = self.shape.copy()
            descBox.setPos(0, -self.shape.height*0.8/2)
            descBox.height *= 0.8
            descBox.width = transition(self, 'resize_desc', 250, 250, SQRT)
            descBox.radius = descBox.maxRadius()
            descBox.radius = constrain(descBox.radius, 0, self.shape.radius)
            descBox.fill()
            
            fill(self.textColor)
            textSize(self.textSize)
            text(self.text, 0, textHeight(self.text) / 2)
        
        action = action.lower()
        if action == 'setup': return setup
        if action == 'idle': return idle
        if action == 'hover': return hover
        return None

    # A dictionary containing all styles and their name
    styles = {
        'default': default,
        'pulsate': default_pulsate,
        'rotate' : default_rotate,
        'rotate_pulsate': default_rotate_pulsate,
        'radio': default_radio,
        'checkbox': default_checkbox,
        'dice': custom_dice,
        'compact': default_compact
    }
    
    class NoSuchStyleException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
            
