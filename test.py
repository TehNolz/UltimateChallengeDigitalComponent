import globals
from Object import Object
from Button import Button
from util import *
import prime_number_menu


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
    b.description = 'very looooooooooooooooooooooong placeholder\ntext because I want to show that this is a really neat feature'
    b.descBoxTextSize = b.textSize
    
    buttons = Object.endGroup()
    
    Object.startGroup()
    
    r *= 0.5
    b1 = Button(width/2, 205 - 80, r.copy()*0.2)
    b1.applyStyle('radio')
    b1.radioGroup = 'testScreen_radiobuttons'
    
    b1 = Button(width/2, 205 - 40, r.copy()*0.2)
    b1.applyStyle('radio')
    b1.radioGroup = 'testScreen_radiobuttons'
    
    b1 = Button(width/2, 205 + 40, r.copy()*0.2)
    b1.applyStyle('radio')
    b1.radioGroup = 'testScreen_radiobuttons'
    
    b1 = Button(width/2, 205 + 80, r.copy()*0.2)
    b1.applyStyle('radio')
    b1.radioGroup = 'testScreen_radiobuttons'
    
    b1 = Button(width/2, 205, r.copy()*0.2)
    b1.applyStyle('checkbox')
    b1.boxColor = color(255,0,0, 0)
    
    bGroup2 = Object.endGroup()

def draw():
    scale(globals.baseScale)
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
