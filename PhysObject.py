from Object import Object
from util import *

class PhysObject(Object):
    allPhysObjects = list()
    
    buttons = {'UP': UP,
               'DOWN': DOWN,
               'LEFT': LEFT,
               'RIGHT': RIGHT}
    
    HIT_EDGE = True
    STOP_AT_EDGE = True
    disabledControls = False
    
    @staticmethod
    def updateCollisions():
        for o in PhysObject.allPhysObjects:
            o.collisions()
    
    def __init__(self, x = None, y = None):
        Object.__init__(self, x, y)
        PhysObject.allPhysObjects.append(self)
        self.vel = Vector2()
        self.accel = 150
        self.decay = 50
        self.scanbox = Vector2()
        self.nearbyObjects = set()
        self.bounceEfficiency = 1
    
    def update(self):
        fps = self.getFPS()
        self.move(self.vel.X / fps, self.vel.Y / fps)
        self.decayVel()
        Object.update(self)
    
    def collisions(self):
        fps = self.getFPS()
        self.nearbyObjects = set()
        vel = self.vel.size() / fps
        self.scanbox = Vector2(self.radius+vel, self.radius+vel)

    def push(self, x, y):
        fps = self.getFPS()
        self.vel.X += x / fps
        self.vel.Y += y / fps

    def pushUp(self): self.push(0, -self.accel)
    def pushDown(self): self.push(0, self.accel)
    def pushLeft(self): self.push(-self.accel, 0)
    def pushRight(self): self.push(self.accel, 0)
    
    def controls(self):
        if self.disableControls or PhysObject.disabledControls: return
        fps = self.getFPS()
        c = self.buttons
        for val in self.keyCodes:
            if val == c['UP']: self.pushUp()
            elif val == c['DOWN']: self.pushDown()
            elif val == c['LEFT']: self.pushLeft()
            elif val == c['RIGHT']: self.pushRight()
        
    def decayVel(self):
        if self.decay == 0: return
        fps = self.getFPS()
        if self.vel.X == 0 and self.vel.Y == 0: return
        elif self.vel.X == 0: xDecay = 0; yDecay = float(self.decay)
        elif self.vel.Y == 0: xDecay = float(self.decay); yDecay = 0
        else:
            angle = atan2(self.vel.X, self.vel.Y)
            xDecay = sin(angle) * self.decay
            yDecay = cos(angle) * self.decay
        self.vel.X = decayVal(self.vel.X, xDecay / fps)
        self.vel.Y = decayVal(self.vel.Y, yDecay / fps)
    
    def drawImage(self):
        fill(255, 0, 0)
        stroke(0,0,0,0)
        ellipse(0, 0, 10, 10)
    
    def setPosition(self, x, y):
        if PhysObject.BOUNDED_CANVAS:
            b = self.bounds
            s = self.shape
            if x < b.X-s.X:
                x *= -1 * self.bounceEfficiency
                self.vel.X = abs(self.vel.X) * self.bounceEfficiency
            elif x > b.X + b.width - s.width - s.X:
                x = b.X + b.width - (b.X + b.width - x) * self.bounceEfficiency
                self.vel.X = abs(self.vel.X) * -1 * self.bounceEfficiency
            if y < b.Y-s.Y:
                y *= -1 * self.bounceEfficiency
                self.vel.Y = abs(self.vel.Y) * self.bounceEfficiency
            elif y > b.Y + b.height - s.height - s.Y:
                y = b.Y + b.height - (b.Y + b.height - y) * self.bounceEfficiency
                self.vel.Y = abs(self.vel.Y) * -1 * self.bounceEfficiency
        Object.setPosition(self, x, y)
    
    @staticmethod
    def toggleAllControls(b):
        PhysObject.diabledControls = not b
        for o in PhysObject.allPhysObjects:
            o.disableControls = not b
