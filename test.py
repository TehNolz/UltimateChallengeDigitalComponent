import globals
from Object import Object
from Button import Button
from util import *


buttons = None
b = None
bGroup2 = None
def init():
    global buttons, b, bGroup2, b1
    Object.startGroup()
    
    globals.bgColor = color(204)
    
    r = RoundRect(-150, -150, 300, 300, 50)
    b = Button(150,300,r.copy()*0.5)
    b.applyStyle('compact')
    b.text = 'test\nbutton'
    b.description = 'placeholder\ntext'
    
    buttons = Object.endGroup()
    
    Object.startGroup()

    def bgRed(*args):
        if args[0].activated:
            globals.bgColor = color(128,0,0)
    def bgBlue(*args):
        if args[0].activated:
            globals.bgColor = color(0,128,0)
    def bgGreen(*args):
        if args[0].activated:
            globals.bgColor = color(0,0,128)
    def bgYellow(*args):
        if args[0].activated:
            globals.bgColor = color(175, 175, 0)
    def bgGrey(*args):
        if args[0].activated:
            globals.bgColor = color(204)
    
    r *= 0.5
    b1 = Button(width/2, 205 - 80, r.copy()*0.2)
    b1.applyStyle('radio')
    b1.radioGroup = 'testScreen_radiobuttons'
    b1.releaseAction = bgRed
    b1.idleAction = bgRed
    
    b1 = Button(width/2, 205 - 40, r.copy()*0.2)
    b1.applyStyle('radio')
    b1.radioGroup = 'testScreen_radiobuttons'
    b1.releaseAction = bgBlue
    b1.idleAction = bgBlue
    
    b1 = Button(width/2, 205 + 40, r.copy()*0.2)
    b1.applyStyle('radio')
    b1.radioGroup = 'testScreen_radiobuttons'
    b1.releaseAction = bgGreen
    b1.idleAction = bgGreen
    
    b1 = Button(width/2, 205 + 80, r.copy()*0.2)
    b1.applyStyle('radio')
    b1.radioGroup = 'testScreen_radiobuttons'
    b1.releaseAction = bgYellow
    b1.idleAction = bgYellow
    
    b1 = Button(width/2, 205, r.copy()*0.2)
    b1.applyStyle('checkbox')
    b1.boxColor = color(255,0,0, 0)
    b1.idleAction = bgGrey
    b1.hoverAction = bgGrey
    b1.pressAction = bgGrey
    
    bGroup2 = Object.endGroup()

def draw():
    scale(globals.baseScale)
    background(globals.bgColor)
    pushStyle()
    rectMode(CORNER)
    textMode(LEFT)
    
    for o in bGroup2:
        o.update()
    
    fill(0)
    textSize(25)
    for o in bGroup2:
        s = "This button is: " + str(o.activated)
        text(s, 1133/2+20, o.pos.Y + textHeight(s)/2)

    for o in buttons:
        o.update()