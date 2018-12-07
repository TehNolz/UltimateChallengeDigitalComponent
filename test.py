import globals
from Object import Object
from Button import Button
from util import *


buttons = None
b = None
def init():
    global buttons, b
    Object.startGroup()
    r = RoundRect(-150, -150, 300, 300, 50)
    b = Button(150,150,r.copy())
    buttons = Object.endGroup()

m = None
once = False
def draw():
    global m, once
    rectMode(CORNER)

    r = radians(float(millis()) / 100)
    
    pushMatrix()
    scale(globals.baseScale)
    translate(300,300)
    scale(0.5)
    rotate(QUARTER_PI)
    
    if not once or True:
        m = g.getMatrix()
        m.invert()
        m.translate(-width/2, -height/2)
        once = True
    g.setMatrix(m)
    
    mousePos1 = Vector2(mouseX, mouseY)
    mousePos2 = mousePos1.modelPos()
    print(mousePos1, mousePos2)
    popMatrix()
    
    strokeWeight(5)
    fill(0)
    stroke(0)
    
    point(*mousePos1)
    point(*mousePos2)
    
    fill(255,0,0)
    
    pushMatrix()
    translate(*b.pos)
    b.shape.fill()
    popMatrix()

    scale(globals.baseScale)
    translate(300,300)
    scale(0.5)
    rotate(QUARTER_PI)

    for o in buttons:
        o.update()
