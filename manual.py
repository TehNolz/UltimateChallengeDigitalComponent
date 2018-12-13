import globals
from util import *
from Button import Button
from Object import Object

def init():
    global manual1, manual2
    
    imgIndex = globals.imgIndex
    manual1 = imgIndex["manual-1"]
    manual2 = imgIndex["manual-2"]

button_x = 165
button_y = 525
button_w = 50
button_h = 50






def draw(mousePressed):
    
    global manual1, manual2, button_x, button_y, button_w, button_h
    
    
    
    if mousePressed and (mouseButton == LEFT) and (mouseX > button_x and button_x + button_w > mouseX) and (mouseY > button_y and button_y + button_h > mouseY):
        fill(255,0,0)
        rect(button_x, button_y, button_w, button_h)
    
    
    
    rect(button_x, button_y, button_w, button_h)
    
    
    
    image(manual1, width/3, height/2)
    manual1.resize(350,500)
    
    #image(manual2, width/2 , height/2)
    #manual2.resize(350,500)
    
