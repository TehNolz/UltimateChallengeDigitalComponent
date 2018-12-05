import time
import __builtin__

__builtin__.VERSION = 'v1.0a'

LIN = lambda x:x
EXP = lambda x:x**2
SQRT = lambda x:x**0.5

transitionCache = dict()
def cacheTransition(self, id, value): transitionCache[id+str(self)] = value
def getTransition(self, id, default): return transitionCache[id+str(self)] if (id+str(self)) in transitionCache else default

transitions = dict()
def transition(self, id, time, value, mod=LIN, autoReset=True):
    _id = id+str(self)
    if time == 0 or not _id in transitions or autoReset and not transitions[_id][1] == value:
        transitions[_id] = (millis()+time, value)
        nv = getTransition(self, id+'#MEM', value)
        cacheTransition(self,id,nv)
        return nv
    v = transitions[_id]
    x = constrain(float(millis()),0,v[0])
    t = constrain(mod(abs(1 - (v[0] - x)/float(time))), 0, 1)
    nv = lerp(getTransition(self, id, value), value, t)
    cacheTransition(self, id+'#MEM', nv)
    return nv

colorCache = dict()
def cacheColor(self, id, c): colorCache[id+str(self)] = c
def getColor(self, id, default): return colorCache[id+str(self)] if (id+str(self)) in colorCache else default

colorTransitions = dict()
def transitionColor(self, id, time, c, mod=LIN, autoReset=True):
    _id = id+str(self)
    if not _id in colorTransitions or not colorTransitions[_id][1] == c:
        colorTransitions[_id] = (millis()+time, c)
        nc = getColor(self, id+'#MEM', c)
        cacheColor(self,id,nc)
        return nc
    v = colorTransitions[_id]
    x = constrain(float(millis()),0,v[0])
    t = constrain(mod(abs(1 - (v[0] - x)/float(time))), 0, 1)
    nc = lerpColor(getColor(self, id, c), c, t)
    cacheColor(self, id+'#MEM', nc)
    return nc

def transitionFill(self, time, c, mod=LIN, autoReset=True): fill(transitionColor(self, '<fill>', time, c, mod, autoReset))
def transitionStroke(self, time, c, mod=LIN, autoReset=True): stroke(transitionColor(self, '<stroke>', time, c, mod, autoReset))

def decayVal(val, rate, neutral = 0):
    rate = abs(rate)
    if abs(val - neutral) < rate:
        return neutral
    elif val < neutral: return val + rate
    return val - rate

class Vector2:
    def __init__(self, x = 0, y = 0):
        self.X = x
        self.Y = y

    def __add__(self, other): return Vector2(self.X+other.X, self.Y+other.Y)
    def __sub__(self, other): return self + (-other)
    def __neg__(self): return self*-1
    def __repr__(self): return '{X:' + str(self.X) + ',Y:' + str(self.Y) + '}'
    def __mul__(self, other): return Vector2(self.X * other, self.Y * other)
    def __truediv__(self, other): return Vector2(self.X / other, self.Y / other)
    def __div__(self, other): return Vector2(self.X / other, self.Y / other)
    def __iter__(self): return (self.__dict__[item] for item in sorted(self.__dict__))

    def rotateAround(self, axis, rotation):
        p = self - axis
        d = p.size()
        a = atan2(*p) + rotation
        p.X = sin(a) * d
        p.Y = cos(a) * d
        return p+axis

    def size(self): return (self.X * self.X + self.Y * self.Y)**0.5
    def copy(self): return Vector2(self.X, self.Y)

class Rectangle:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.X = x
        self.Y = y
        self.width = w
        self.height = h
    
    def __mul__(self, other): return Rectangle(self.X * other, self.Y * other, self.width * other, self.height * other)
    def copy(self): return Rectangle(self.X, self.Y, self.width, self.height)
    def contains(self, x, y): return x >= self.X and x <= self.X + self.width and y >= self.Y and y <= self.Y + self.height
    def __repr__(self): return '{X:'+str(round(self.X,1))+',Y:'+str(round(self.Y,1))+',W:'+str(round(self.width,1))+',H:'+str(round(self.height,1))+'}'

    def move(self, x, y): return self.move(Vector2(x,y))
    def fill(self): rect(self.X, self.Y, self.width, self.height)
    def placeAtZero(self): return Rectangle(0, 0, self.width, self.height)
    def getCenter(self): return Vector2(self.X+self.width/2, self.Y+self.height/2)
    def getPos(self): return Vector2(self.X, self.Y)
    
class RoundRect(Rectangle):
    def __init__(self, x=0, y=0, w=0, h=0, r=0):
        self.X = x
        self.Y = y
        self.width = w
        self.height = h
        self.radius = r
    
    def __mul__(self, other): return RoundRect(self.X + (self.width - self.width*other)/2, self.Y + (self.height - self.height*other)/2, self.width * other, self.height * other, self.radius * other)
    def copy(self): return RoundRect(self.X, self.Y, self.width, self.height, self.radius)
    def move(self, pos): return RoundRect(self.X + pos.X, self.Y + pos.Y, self.width, self.height, self.radius)
    
    def contains(self, x, y):
        if not Rectangle.contains(self, x, y): return False
        r1 = Rectangle(self.X, self.Y+self.radius, self.width, self.height-self.radius*2)
        r2 = Rectangle(self.X+self.radius, self.Y, self.width-self.radius*2, self.height)
        if r1.contains(x,y) or r2.contains(x,y):
            del r1, r2
            return True
        del r1, r2
        v = Vector2(x,y)
        v1 = v - Vector2(self.X+self.radius, self.Y+self.radius)
        v2 = v - Vector2(self.X+self.radius, self.Y+self.height-self.radius)
        v3 = v - Vector2(self.X+self.width-self.radius, self.Y+self.radius)
        v4 = v - Vector2(self.X+self.width-self.radius, self.Y+self.height-self.radius)
        if v1.size() <= self.radius or v2.size() <= self.radius or v3.size() <= self.radius or v4.size() <= self.radius:
            del v, v1, v2, v3, v4
            return True
        return False
    
    def fill(self):
        pushStyle()
        strokeJoin(MITER)
        rectMode(CORNER)
        arc(self.X+self.radius, self.Y+self.radius, self.radius*2, self.radius*2, PI, PI+HALF_PI)
        arc(self.X+self.radius, self.Y+self.height-self.radius, self.radius*2, self.radius*2, HALF_PI, PI)
        arc(self.X+self.width-self.radius, self.Y+self.radius, self.radius*2, self.radius*2, PI+HALF_PI, TAU)
        arc(self.X+self.width-self.radius, self.Y+self.height-self.radius, self.radius*2, self.radius*2, 0, HALF_PI)
        noStroke()
        #rect(self.X, self.Y+self.radius, self.width, self.height-self.radius*2)
        #rect(self.X+self.radius, self.Y, self.width-self.radius*2, self.height)
        rect(self.X-1, self.Y+self.radius-1, self.width+2, self.height-self.radius*2+2)
        rect(self.X+self.radius-1, self.Y-1, self.width-self.radius*2+2, self.height+2)
        popStyle()
        line(self.X+self.radius, self.Y, self.X+self.width-self.radius, self.Y)
        line(self.X+self.radius, self.Y+self.height, self.X+self.width-self.radius, self.Y+self.height)
        line(self.X, self.Y+self.radius, self.X, self.Y+self.height-self.radius)
        line(self.X+self.width, self.Y+self.radius, self.X+self.width, self.Y+self.height-self.radius)
    
    def maxRadius(self): return self.width/2 if self.width < self.height else self.height/2

clickPos = Vector2()
_clickButton = -1
def setClickPos(pos, button):
    global clickPos, _clickButton
    if _clickButton == button: return
    _clickButton = button
    clickPos = pos
def getClickPos():
    global clickPos
    return clickPos

def info(s): print('['+str(millis())+'] '+str(s))

def printAttributes(c, colums, types=False):
    import os
    os.chdir('data')
    file = open('attributes.txt', 'w+')
    l = 0
    d = dir(c) if not c == None else list(globals())
    b = 0
    columns = list()
    n = len(str(c))
    file.write('='+'='*n+'=\n')
    file.write(str(c)+'|\n')
    file.write('='+'='*n+'=\n\n')
    for i in range(colums):
        yee = list()
        for j in range(b, int(b+len(d)/colums)):
            yee.append((str(type(c.__getattribute__(d[j]))) + '  ' if types else '') + d[j])
            b+=1
        columns.append(yee)
    sizes = list()
    for x in columns:
        s = 0
        for y in x:
            if s < len(str(y)): s = len(str(y))
        sizes.append(s)
    columns = list(map(list, zip(*columns)))
    for x in columns:
        i = 0
        for y in x:
            file.write(str(y) + ' '*(sizes[i] - len(str(y))) + '  ')
            i+=1
        file.write('\r\n')
    file.close()
    print(file.name)
    os.system('cmd /c "' + file.name + '"')
    os.chdir('..')
