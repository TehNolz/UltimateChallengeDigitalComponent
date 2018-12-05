import globals
from Object import Object
from Button import Button
from util import *

class mainMenu:
    def __init__(self):
        global buttontest
        r = RoundRect(-150, -150, 300, 300, 50)
        r *= 0.5
        buttontest = Button(width/2, height/2, r.copy())
        buttontest.releaseAction = setMenu
    
    def draw(self):
        buttontest.update()

def setMenu(*args):
    globals.currentMenu = 'gamescreen'
