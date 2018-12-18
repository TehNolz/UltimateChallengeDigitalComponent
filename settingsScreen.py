import globals
from util import *
from Button import Button
from Object import Object

def init():
    global buttons, categories
    
    categories = dict()
    
    Object.startGroup()

    backButton = Button(37, 37, RoundRect(-25, -25, 50, 50) * 0.75)
    backButton.releaseAction = gotoMainMenu
    backButton.textSize *= 3
    backButton.applyStyle('compact')
    backButton.description = 'Main menu'
    backButton.icon = globals.imgIndex['back'].copy()
    backButton.iconScale = 0.75
    backButton.iconColor = color(0,0)
    
    backButton = Button(37, 37 + 67, RoundRect(-25, -25, 50, 50) * 0.75)
    backButton.releaseAction = gotoMainMenu
    backButton.textSize *= 3
    backButton.applyStyle('compact')
    backButton.description = 'Quit'
    backButton.icon = globals.imgIndex['tictactoe-cross'].copy()
    backButton.iconScale = 0.5
    backButton.iconColor = color(0,0)
    
    buttons = Object.endGroup()

def draw():
    width = 1133
    height = 600
    scale(*globals.baseScaleXY)
    
    for o in buttons:
        o.update()
    
def gotoMainMenu(*args):
    if args[1] == LEFT:
        globals.currentMenu = "mainMenu"
