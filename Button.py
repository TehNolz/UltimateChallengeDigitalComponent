from Object import Object
from util import *

class Button(Object):
    allButtons = list()
    mousePressPos = Vector2()
    BOUNDED_CANVAS = False
    
    def __init__(self, x, y, r):
        Button.allButtons.append(self)
        Object.__init__(self, x, y)
        self.shape = r
        self.baseShape = self.shape.copy()
        self.color = color(255)
        self.hoverColor = color(240)
        self.pressColor = color(220)
        if False: ##debugging
            self.color = color(255,255,255,100)
            self.hoverColor = color(240,240,240,100)
            self.pressColor = color(220,220,220,100)
        self.mouseEntered = False
        self.clickedInside = False
        self.clickArea = None
        self.rotation = 0
        self.resetWave = False
        self.disableControls = True
        self.text = 'placeholder'
        
        # Placeholders for functions called in their respective mouse event function
        self.leaveAction = None
        self.enterAction = None
        
        self.nothingAction = None
        self.hoverAction = None
        self.clickAction = None
        self.pressAction = None
        self.releaseAction = None
    
    @staticmethod
    def initFromArgs(x, y, w, h): self = Button(x, y, Rectangle(0, 0, w, h)); return self
    @staticmethod
    def initFromRect(r): self = Button(r.X, r.Y, r.placeAtZero()); return self
    
    def setPosition(self, x, y): Object.setPosition(self, x, y)
    def drawImage(self):
        textAlign(LEFT)
        colorMode(HSB,255,255,255)
        stroke((millis()/float(20))%255, 255,150)
        colorMode(RGB)
        strokeJoin(ROUND)
        strokeWeight(max(sin(millis()/float(200)) +1, 0)+3)
        
        self.updateCursor()
        if (self.mousePress or self.mouseRelease):
            b = self.clickArea.contains(*self.getAAP(getClickPos(), False))
            if b and not self.clickedInside: self.onClick(mouseButton)
            self.clickedInside = b
        else: self.clickedInside = False
        
        if self.mouseRelease and self.clickedInside and self.mouseEntered: self.onRelease(mouseButton)
        if self.mousePress and self.clickedInside and self.mouseEntered: self.onPress(mouseButton)
        elif not self.mousePress and self.mouseEntered: self.onHover()
        else: self.onNothing()
        
        self.shape.fill()
        colorMode(HSB,255,255,255)
        fill((float(millis())/20)%255, 255,75)
        colorMode(RGB)
        textSize(self.shape.maxRadius()/3)
        s = 'is going to be changed dipshit'
        #self.resetRotation()
        rotate(-self.rotation-self.localRotation)
        text(s, -textWidth(s)/2,textDescent()*1.3)

    def updateCursor(self):
        if (self.mousePress or self.mouseRelease) and self.clickArea == None:
            self.clickArea = self.area.copy() * self.localScale
        elif not (self.mousePress or self.mouseRelease): self.clickArea = None
        if not self.isHighestPriorityClick(): b = False
        elif (self.mousePress or self.mouseRelease): b = self.clickArea.contains(*self.getMousePos(False))
        else:
            b = self.area.contains(*self.getMousePos())
            if b and not self.mouseEntered: self.onEnter()
        if self.mouseEntered and not b:
            cursor(0)
            self.onLeave()
        self.mouseEntered = b
        if b: cursor(HAND)

    def onNothing(self):
        transitionFill(self, 100, self.color, EXP)
        wave = sin(PI * (float(millis()) / 1000))*0.05
        #self.rotateLocal(transition(self, 'rotate', 250, radians(0), SQRT))
        self.shape.radius = transition(self, 'radius', 250, self.shape.maxRadius()*0.5, EXP)
        self.scaleLocal(transition(self, 'scale', 250, 1+wave, EXP, self.resetWave))
        self.resetWave = False
        if self.nothingAction != None:
            self.nothingAction(self)
    def onHover(self):
        transitionFill(self, 100, self.hoverColor, EXP)
        #self.rotateLocal(transition(self, 'rotate', 250, radians(45), SQRT))
        self.shape.radius = transition(self, 'radius', 150, self.shape.maxRadius()*0.25, SQRT)
        self.scaleLocal(transition(self, 'scale', 250, 1.1, SQRT))
        self.resetWave = True
        if self.hoverAction != None:
            self.hoverAction(self)
    def onPress(self, button):
        transitionFill(self, 50, self.pressColor, SQRT)
        #self.rotateLocal(transition(self, 'rotate', 75, radians(0), SQRT))
        self.shape.radius = transition(self, 'radius', 75, self.shape.maxRadius()*0.75, SQRT)
        self.scaleLocal(transition(self, 'scale', 75, 0.8, SQRT))
        self.resetWave = True
        if self.pressAction != None:
            self.pressAction(self, button)
    def onRelease(self, button):
        #info(str(self) + ' activated. (MB'+str(button)+')')
        self.disableControls = not self.disableControls
        if self.releaseAction != None:
            self.releaseAction(self, button)
    def onClick(self, button):
        if self.clickAction != None:
            self.clickAction(self, button)
    def onEnter(self):
        if self.enterAction != None:
            self.enterAction(self)
    def onLeave(self):
        if self.leaveAction != None:
            self.leaveAction(self)
    
    def getButtonsAbove(self): return Button.allButtons[Button.allButtons.index(self)+1:]
    def isHighestPriorityClick(self):
        """Checks is the cursor isn't inside any buttons above it's priority"""
        for o in self.getButtonsAbove():
            if o.mouseEntered: return False
        return True
