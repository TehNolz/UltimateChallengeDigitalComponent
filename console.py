import globals
import gameScreen
import textInput

showConsole = False
consoleTextColor = color(255, 255, 255)

def init():
    width = 1133
    height = 600
    global consoleTextBox
    baseScale = globals.baseScale
    consoleTextBox = textInput.textBox(height*0.1, 0, 1000*baseScale, 50*baseScale, boxColor=color(0, 0, 0, 128), textColor=color(255, 255, 255), command=command)
    globals.textBoxDict["global"].append(consoleTextBox)

def draw(mousePressed=False):
    width = 1133
    height = 600
    textSize(30)
    global consoleTextBox
    scale(globals.baseScale)
    consoleTextBox.draw(mousePressed)
    
    pushStyle()
    fill(0, 0, 0, 255)
    s = nfc(frameRate, 3)
    text(s, 1133 - textWidth(s), 600 - (textAscent() - textDescent()/2)/2)
    popStyle()
    
#Toggles the console on/off.
def toggleConsole():
    global consoleTextBox
    global showConsole
    showConsole = not showConsole
    if not showConsole:
        consoleTextBox.text[0] = ""
        globals.activeTextBox = None
    else:
        globals.activeTextBox = consoleTextBox
    
#Runs commands
def command(input):
    global consoleText
    global consoleTextColor

    command = input.split(" ")
    
    #setcard <id>
    #Changes the current challenge card to <id>
    if globals.currentMenu == "gameScreen":
        if command[0] == "setcard" or command[0] == "sc":
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
        elif command[0] == "flipcard" or command[0] == "fc":
            if not gameScreen.retractImage:
                gameScreen.turnImage = True
    
    if command == "changemenu" or command[0] == "cm":
        globals.currentMenu = str(command[1])
    
    consoleTextBox.text = ['', '', '']
