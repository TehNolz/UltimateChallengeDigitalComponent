import globals
from util import *
from Button import Button
from Object import Object

button_x = 165
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
    manualForward = Button(button_x1, button_y1, r.copy())
    manualForward.releaseAction = pageForward

    buttons = Object.endGroup()

def draw(mousePressed):
    
    global manual1, manual2, manual3, manual4, manual5, manual6, button_x, button_y, button_w, button_h, forward, backward
    
    

    
    image(manual1, width*(1.0/3), height/2)
    manual1.resize(350,500)
    
    image(manual2, width*(2.0/3), height/2)
    manual2.resize(350,500)
    
    
    if forward == 1:
        image(manual3, width*(1.0/3), height/2)
        manual3.resize(350,500)
        image(manual4, width*(2.0/3), height/2)
        manual4.resize(350,500)
    if forward == 2:
        image(manual5, width*(1.0/3), height/2)
        manual5.resize(350,500)
        image(manual6, width*(2.0/3), height/2)
        manual6.resize(350,500)
    if backward == 1:
        image(manual1, width*(1.0/3), height/2)
        manual1.resize(350,500)
        image(manual2, width*(2.0/3), height/2)
        manual2.resize(350,500)
    
    
    
    
    
    #image(manual4, width*(1.0/3), height/2)
    #manual4.resize(350,500)
    
    #image(manual5, width*(1.0/3), height/2)
    #manual5.resize(350,500)
    
    #image(manual6, width*(1.0/3), height/2)
    #manual6.resize(350,500)
    
    
    
    for o in buttons:
        o.update()



def pageBack(*args):
    global backward
    if backward == 0:
        backward = 1
    elif backward == 1:
        backward = 2
        forward = 1
    elif backward == 2:
        pass
        
    
    
def pageForward(*args):
    global forward
    if forward == 0:
        forward = 1
    elif forward == 1:
        forward = 2
    elif forward == 2:
        pass
        
        
        
        
