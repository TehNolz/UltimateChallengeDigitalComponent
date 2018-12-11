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

def draw():
    pushStyle()
    rectMode(CORNER)
    
    pushMatrix()
    scale(globals.baseScale)
    translate(300,300)
    scale(0.5)
    rotate(QUARTER_PI)

    m = g.getMatrix()
    m.invert()
    m.translate(-width/2, -height/2)
    g.setMatrix(m)
    
    mousePos1 = Vector2(mouseX, mouseY)
    mousePos2 = mousePos1.getModelPos()
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
    
    popStyle()
