import globals
from util import *
from Button import Button
from Object import Object

def init():
    global manual1, manual2, manual3, manual4, manual5, manual6,  buttons, forward
    
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

button_x = 160
button_y = 525
button_x1 = 975
button_y1 = 525
forward = 1

def draw(mousePressed):
    
    global manual1, manual2, manual3, manual4, manual5, manual6, button_x, button_y, button_w, button_h, forward
    
    

    
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
    print('inquisition')
    # Code to go one page back
    pass
    
def pageForward(*args):

    if forward == 1:
        image(manual3, width*(1.0/3), height/2)
        manual3.resize(350,500)
        image(manual4, width*(2.0/3), height/2)
        manual4.resize(350,500)
        forward = 2
    if forward == 2:
        image(manual5, width*(1.0/3), height/2)
        manual5.resize(350,500)
        image(manual6, width*(1.0/3), height/2)
        manual6.resize(350,500)
        

        
    
    
    
