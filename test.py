import globals
from Object import Object
from Button import Button
from util import *


buttons = None
def init():
    global buttons
    Object.startGroup()
    r = RoundRect(-150, -150, 300, 300, 50)
    r *= 1
    b1 = Button(0,0,r.copy())
    b1.setPosition(width/2-350, height-200)
    b = Button(0,0,r.copy()*0.5)
    b.setPosition(width/2-200, height-237.5)
    b.pos = b.pos.rotateAround(b1.pos, radians(-45))
    
    b1 = Button(0,0,r.copy())
    b1.setPosition(width/2+350, height-200)
    b = Button(0,0,r.copy()*0.5)
    b.setPosition(width/2+200, height-237.5)
    b.pos = b.pos.rotateAround(b1.pos, radians(45))
    buttons = Object.endGroup()
    for o in buttons:
        o.rotation = QUARTER_PI
        o.scale(0.5)

def draw():
    rectMode(CORNER)
    pushMatrix()
    mousePos1 = Vector2(mouseX, mouseY)
    translate(50,50)
    mousePos2 = Vector2(modelX(mouseX, mouseY, 0), modelY(mouseX, mouseY, 0))
    popMatrix()
    print(mousePos1, mousePos2)
    strokeWeight(5)
    fill(0)
    stroke(0)
    #rect(mousePos1.X, mousePos1.Y, mousePos2.X, mousePos2.Y)
    point(*mousePos1)
    point(*mousePos2)
    
    #for o in buttons:
    #    o.update()
