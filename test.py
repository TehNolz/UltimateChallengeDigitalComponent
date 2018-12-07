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
    r *= 1
    b1 = Button(150,150,r.copy())
    #b1.setPosition(width/2-350, height-200)
    b = b1
    #b = Button(0,0,r.copy()*0.5)
    #b.setPosition(width/2-200, height-237.5)
    #b.pos = b.pos.rotateAround(b1.pos, radians(-45))
    
    #b1 = Button(0,0,r.copy())
    #b1.setPosition(width/2+350, height-200)
    #b = Button(0,0,r.copy()*0.5)
    #b.setPosition(width/2+200, height-237.5)
    #b.pos = b.pos.rotateAround(b1.pos, radians(45))
    buttons = Object.endGroup()
    for o in buttons:
        o.rotation = QUARTER_PI
        #o.scale(0.5)

def draw():
    scale(globals.baseScale)
    rectMode(CORNER)
    pushMatrix()
    mousePos1 = Vector2(mouseX, mouseY)
    scale(1.5)
    translate(width/2,50)
    rotate(b.localRotation)
    b.shape.fill()
    #mousePos2 = Vector2(modelX(mouseX, mouseY, 0), modelY(mouseX, mouseY, 0))
    mousePos2 = b.getMousePos()
    popMatrix()
    strokeWeight(5)
    fill(0)
    stroke(0)
    point(*mousePos1)
    point(*mousePos2)
    fill(255,0,0)
    pushMatrix()
    translate(*-b.shape.getPos())
    popMatrix()
    
    
    r = b.area.copy()
    scale(1.5)
    translate(width/2,50)
    rotate(b.localRotation)

    for o in buttons:
        o.update()
