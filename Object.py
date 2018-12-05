from util import *

class Object:
    activeKeys = set()
    keyCodes = set()
    allObjects = list()
    
    mousePress = False
    buttons = {'UP': UP,
               'DOWN': DOWN,
               'LEFT': LEFT,
               'RIGHT': RIGHT}
    
    DEFAULT_FPS = 30
    LOCK_FPS = False
    BOUNDED_CANVAS = True
    disabledControls = False
    mouseRelease = False
    
    @staticmethod
    def updateAll():
        pushStyle()
        pushMatrix()
        for o in Object.allObjects: o.update()
        popMatrix()
        popStyle()
        Object.mouseRelease = False
    
    def __init__(self, x = None, y = None):
        #Object.allObjects.append(self)
        if Object.groupingObjects:
            Object._group.append(self)
        if x == None: x = width/2
        if y == None: y = height/2
        self.pos = Vector2(x, y)
        self.rotation = 0
        self.speed = 100
        self.shape = Rectangle(-5,-5,10,10)
        self.bounds = Rectangle(20,20,width-40,height-40)
        self.disableControls = False
        self.localTranslation = Vector2()
        self.localRotation = 0
        self.localScale = float(1)
        self.baseScale = 1
    
    def __repr__(self):
        return '<' + self.__class__.__name__ + ('#%06x' % id(self)) + '>'
    
    def update(self):
        fps = self.getFPS()
        self.controls()
        pushMatrix()
        translate(*self.pos)
        rotate(self.rotation)
        scale(self.baseScale)
        self.drawImage()
        #self.resetRotation()
        self.resetTranslation()
        popMatrix()
        self.setPosition(self.pos.X, self.pos.Y)
    
    def setRotation(self, angle): self.rotation = angle % TAU
    def setRotationDeg(self, angle): self.setRotation(radians(angle))
    def turn(self, angle): self.setRotation(self.rotation + angle)
    def turnDeg(self, angle): self.turn(radians(angle))

    def setPosition(self, x, y):
        if self.BOUNDED_CANVAS:
            b = self.bounds
            s = self.shape.copy()
            s *= self.localScale * self.baseScale
            x = constrain(x, b.X-s.X, b.X + b.width - s.width - s.X)
            y = constrain(y, b.Y-s.Y, b.Y + b.height - s.height - s.Y)
        self.pos.X = x
        self.pos.Y = y

    def move(self, x, y): self.setPosition(self.pos.X + x, self.pos.Y + y)
    def up(self, y): self.setPosition(self.pos.X, self.pos.Y - y)
    def down(self, y): self.setPosition(self.pos.X, self.pos.Y + y)
    def left(self, x): self.setPosition(self.pos.X - x, self.pos.Y)
    def right(self, x): self.setPosition(self.pos.X + x, self.pos.Y)
    
    def controls(self):
        if self.disableControls or Object.disabledControls: return
        fps = self.getFPS()
        c = self.buttons
        for val in self.keyCodes:
            if val == c['UP']: self.up(self.speed / fps)
            elif val == c['DOWN']: self.down(self.speed / fps)
            elif val == c['LEFT']: self.left(self.speed / fps)
            elif val == c['RIGHT']: self.right(self.speed / fps)

    def drawImage(self):
        fill(255)
        stroke(0,0,0,0)
        ellipse(0, 0, 10, 10)

    @property
    def area(self):
        #return self.shape.move(Vector2(modelX(0,0,0), modelY(0,0,0)))
        return self.shape.move(self.pos+self.localTranslation)
    def getFPS(self): return frameRate if not Object.LOCK_FPS else Object.DEFAULT_FPS
    
    def setLoadOrder(self, i):
        index = Object.allObjects.index(self)
        Object.allObjects.pop(index)
        newindex = constrain(i, 0, len(Object.allObjects)-1)
        Object.allObjects.insert(newindex, self)
    
    def raiseItem(self): self.setLoadorder(Object.allObjects.index(self) + 1)
    def lowerItem(self): self.setLoadorder(Object.allObjects.index(self) - 1)

    def getMousePos(self, includeScale=True, axisOriented=True):
        """Only orient it to the axis after all rotation transforms are done"""
        
        if not axisOriented: return Vector2(mouseX,mouseY)
        return self.getAAP(Vector2(mouseX,mouseY),includeScale)
    def getAAP(self, pos, includeScale=True):
        """Returns an axis-aligned point. This means it will be rotated with the objects rotation
        Useful for checking if a point entered an oriented rectangle."""
        p = pos.rotateAround(self.pos, self.rotation)
        p = (p - self.pos) / self.baseScale + self.pos
        p = p.rotateAround(self.pos + self.localTranslation, self.localRotation)
        if includeScale: return (p - self.pos - self.localTranslation) / self.localScale + self.pos + self.localTranslation
        return p
    
    groupingObjects = False
    _group = None
    @staticmethod
    def startGroup():
        Object.groupingObjects = True
        Object._group = list()
    @staticmethod
    def endGroup():
        Object.groupingObjects = False
        return Object._group[:]
    
    @staticmethod
    def toggleAllControls(b):
        Object.disabledControls = not b
        for o in Object.allObjects:
            if not o.__class__ == Object: continue
            o.disableControls = not b
    
    def translateLocal(self, x, y):
        self.localTranslation.X += x
        self.localTranslation.Y += y
        translate(x, y)
    def resetTranslation(self):
        translate(-self.localTranslation.X, -self.localTranslation.Y)
        self.localTranslation = Vector2()
    def rotateLocal(self, r):
        #rotate(-self.localRotation)
        self.localRotation = r
        rotate(r)
    def resetRotation(self):
        rotate(-self.localRotation)
        self.localRotation = 0
    def scaleLocal(self, s):
        scale(s)
        self.localScale = s
    def resetScale(self):
        scale(1/self.localScale)
        self.localScale = 1
    def scale(self, s):
        self.baseScale *= s
