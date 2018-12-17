import globals
from util import *
from Button import Button
from Object import Object

button_x = 160
button_y = 525
button_x1 = 975
button_y1 = 525
forward = 0
backward = 0

def init():
    global manual1, manual2, manual3, manual4, manual5, manual6,  buttons, forward, backward
    
    imgIndex = globals.imgIndex
    manual1 = imgIndex["manual-1"]
    manual2 = imgIndex["manual-2"]
    manual3 = imgIndex["manual-3"]
    manual4 = imgIndex["manual-4"]
    manual5 = imgIndex["manual-5"]
    manual6 = imgIndex["manual-6"]
    
    

    Object.startGroup()
    
    r = RoundRect(-25, -25, 50, 50)
    manualBack = Button(button_x, button_y, r.copy())
    manualBack.releaseAction = pageBack
    manualBack.applyStyle('simple')
    manualBack.hoverStroke = color(128, 64, 0)
    # This is the unicode character for an arrow pointing to the left (ALT+27)
    manualBack.text = u'\u2190'
    manualBack.textSize *= 2
    
    manualForward = Button(button_x1, button_y1, r.copy())
    manualForward.releaseAction = pageForward
    manualForward.applyStyle('simple')
    manualForward.hoverStroke = color(128, 64, 0)
    # This is the unicode character for an arrow pointing to the right (ALT+26)
    manualForward.text = u'\u2192'
    manualForward.textSize *= 2
    
    backButton = Button(width*0.95, height*0.1, r.copy())
    backButton.releaseAction = gotoMainMenu
    backButton.text = "Back"

    buttons = Object.endGroup()

def draw(mousePressed):
    width = 1133
    height = 600
    
    scale(*globals.baseScaleXY)
    
    global manual1, manual2, manual3, manual4, manual5, manual6, button_x, button_y, button_w, button_h, forward, backward
    
   
    
    textSize(50)
    fill(0)
    text("The Ultimate Challenge manual", width/6, 40)
    
    
    image(manual1, width*(1.0/3), height/2)
    manual1.resize(370,500)
    image(manual2, width*(2.0/3), height/2)
    manual2.resize(370,500)
        
    if forward == 1:
        image(manual3, width*(1.0/3), height/2)
        manual3.resize(370,500)
        image(manual4, width*(2.0/3), height/2)
        manual4.resize(370,500)
    
    if forward == 2:
        image(manual5, width*(1.0/3), height/2)
        manual5.resize(370,500)
        image(manual6, width*(2.0/3), height/2)
        manual6.resize(370,500)
    
    if backward == 1:
        image(manual1, width*(1.0/3), height/2)
        manual1.resize(370,500)
        image(manual2, width*(2.0/3), height/2)
        manual2.resize(370,500)
        
    if backward == 2:
        image(manual3, width*(1.0/3), height/2)
        manual3.resize(370,500)
        image(manual4, width*(2.0/3), height/2)
        manual4.resize(370,500)

            
    
    for o in buttons:
        o.update()


def pageForward(*args):
    global forward, backward
    if forward == 0:
        forward = 1
        backward = 0
        
    elif forward == 1:
        forward = 2

    elif forward == 2:
        pass
                    
def pageBack(*args):
    global backward, forward
    if backward == 0:
        backward = 1
        forward = 0
        
    elif backward == 1:
        pass
       
def gotoMainMenu(*args):
    if args[1] == LEFT:
        globals.currentMenu = "mainMenu"
    
        
    
    

    
    
    
        
        
    
        
        
        

            
        
    
    

        
        
        
        
