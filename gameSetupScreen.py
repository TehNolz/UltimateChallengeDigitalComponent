import globals

def init():
    global buttons
    
    Object.startGroup()
    
    #Play button
    playButton = Button(width*0.75, height*0.75, r.copy())
    playButton.releaseAction = gotoGame
    playButton.text = "Play"
    
    buttons = Object.endGroup()
    
def draw():
    global buttons
    for o in buttons:
        o.update()
    
    
def gotoGameScreen(*args):
    if args[1] == LEFT:
        globals.currentMenu = "gameScreen"
