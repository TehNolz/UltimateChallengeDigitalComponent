import globals
from util import *
from Button import Button
from Object import Object

def init():
    
    Object.startGroup()
    
    r = RoundRect(-25, -25, 50, 50)
    
    backButton = Button(width*0.95, height*0.1, r.copy())
    backButton.releaseAction = gotoMainMenu
    backButton.text = "Back"
    
    buttons = Object.endGroup()
    

def draw():
    pass
    
    
    
def gotoMainMenu(*args):
    if args[1] == LEFT:
        globals.currentMenu = "mainMenu"
