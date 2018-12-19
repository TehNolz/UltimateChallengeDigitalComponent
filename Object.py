from util import *
import globals

class Object:
    activeKeys = set()
    keyCodes = set()
    
    buttons = {'UP': UP,
               'DOWN': DOWN,
               'LEFT': LEFT,
               'RIGHT': RIGHT}
    
    DEFAULT_FPS = 30
    LOCK_FPS = False
    BOUNDED_CANVAS = True
    disabledControls = False
    
    mousePress = False
    mouseRelease = False
    clickPos = Vector2()
    
    def __init__(self, x = None, y = None):
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
        self.localScale = 1
        self.baseScale = 1
    
    def __repr__(self):
        return '<' + self.__class__.__name__ + ('#%06x' % id(self)) + '>'
    
    def update(self):
        fps = self.getFPS()
        self.controls()
        pushStyle()
        pushMatrix()
        if not globals.userConfig['settings']['objectAnims_OnOff']:
            translate(*self.pos)
            rotate(self.rotation)
            scale(self.baseScale)
        else:
            translate(*self.pos+self.localTranslation)
            rotate(self.rotation + self.localRotation)
            scale(self.baseScale * self.localScale)
        self.drawImage()
        popMatrix()
        popStyle()
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

    def getFPS(self): return frameRate if not Object.LOCK_FPS else Object.DEFAULT_FPS

    def getMousePos(self):
        """Get the mouse position based on the current transformation matrix"""
        return self.getOOP(Vector2(mouseX, mouseY))
    
    # OOP stands for Object-Oriented-Point
    def getOOP(self, pos):
        """Take a coordinate on the screen and transform it to a point relative to this button"""
        # This is only useful for coordinates positioned on the screen, so to convert from one
        # relative coordinate to the other requires applying the transformation matrix first
        # and then passing it through here.
        
        # Momentarily use an the inverse of the current transformation matrix and do calculations
        pushMatrix()
        g.setMatrix(getCurrentInvMatrix())
        pos = pos.getModelPos()
        popMatrix()
        return pos
    
    groupingObjects = False
    _group = None
    @staticmethod
    def startGroup():
        Object.groupingObjects = True
        Object._group = list()
    @staticmethod
    def endGroup():
        Object.groupingObjects = False
        return list(Object._group)
    
    @staticmethod
    def toggleAllControls(b):
        Object.disabledControls = not b
        for o in Object.allObjects:
            if not o.__class__ == Object: continue
            o.disableControls = not b
    
    def translateLocal(self, x, y):
        # Disable the animations/transformations
        if not globals.userConfig['settings']['objectAnims_OnOff']:
            return
        translate(*-self.localTranslation)
        self.localTranslation.X += x
        self.localTranslation.Y += y
        translate(x, y)
    def resetTranslation(self):
        translate(*-self.localTranslation)
        self.localTranslation = Vector2()
    def rotateLocal(self, r):
        if not globals.userConfig['settings']['objectAnims_OnOff']:
            return
        rotate(-self.localRotation)
        self.localRotation = r
        rotate(r)
    def resetRotation(self):
        rotate(-self.localRotation)
        self.localRotation = 0
    def scaleLocal(self, s):
        if not globals.userConfig['settings']['objectAnims_OnOff']:
            return
        scale(1/self.localScale)
        self.localScale = s
        scale(s)
    def resetScale(self):
        scale(1/self.localScale)
        self.localScale = 1
    def scale(self, s):
        self.baseScale *= s
