import globals
import gameScreen
import textInput

showConsole = False
consoleTextColor = color(255, 255, 255)

def init():
    global consoleTextBox
    baseScale = globals.baseScale
    consoleTextBox = textInput.textBox(height*0.1, 0, 1000*baseScale, 50*baseScale, boxColor=color(0, 0, 0, 128), textColor=color(255, 255, 255), command=command)
    globals.textBoxDict["global"].append(consoleTextBox)

def draw():
    global consoleTextBox
    consoleTextBox.draw()
    
    text(frameRate, width*0.9, height*0.9)
    
#Toggles the console on/off.
def toggleConsole():
    global consoleTextBox
    global showConsole
    global consoleText
    showConsole = not showConsole
    if not showConsole:
        consoleText = ""
        globals.activeTextBox = None
    else:
        globals.activeTextBox = consoleTextBox
    
#Input a key. Will execute valid commands if the last key is enter ("\n")
def command(input):
    global consoleText
    global consoleTextColor

    command = input.split(" ")
    
    #setcard <id>
    #Changes the current challenge card to <id>
    if globals.currentMenu == "gameScreen":
        if command[0] == "setcard":
            exists = False
            for deck in globals.cardConfig:
                if command[1] in globals.cardConfig[deck]:
                    exists = True
            if exists:
                gameScreen.setCard(command[1])
        
        #retractcard
        #Switches the card between background/foreground
        elif command[0] == "retractcard":
            if not gameScreen.turnImage:
                gameScreen.retractImage = True
                
        #flipcard
        #Flips the card
        elif command[0] == "flipcard":
            if not gameScreen.retractImage:
                gameScreen.turnImage = True
    
    consoleTextBox.text = ""
