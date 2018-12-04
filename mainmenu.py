import globals
from Object import Object
from Button import Button
from util import *

class mainMenu:
    def __init__(self):
        r = RoundRect(-150, -150, 300, 300, 50)
        r *= 1
        buttontest = Button(0, 0, r.copy())
    
    def draw(self):
        Object.updateAll()
        
