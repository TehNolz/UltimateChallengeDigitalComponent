import globals
import gameScreen

showConsole = False
consoleText = ""
consoleHistory = []
consoleTextColor = color(255, 255, 255)

def draw():
    rectMode(CENTER)
    
    #Get base scale
    baseScale = globals.baseScale
    
    #Create console box
    pushMatrix()
    textAlign(CENTER, CENTER)
    translate(width/2, width/2, 0)
    fill(0, 0, 0, 128)
    rect(0, 0, 1000*baseScale, 100*baseScale)

    #Write console text, if any.
    translate(0, -12*baseScale, 0)
    textSize(30*baseScale)
    fill(consoleTextColor)
    text(consoleText, 0, 0)
    popMatrix()
    
#Toggles the console on/off.
def toggleConsole():
    global showConsole
    global consoleText
    showConsole = not showConsole
    if not showConsole:
        consoleText = ""
    
#Input a key. Will execute valid commands if the last key is enter ("\n")
def input(input):
    global consoleText
    global consoleTextColor
    
    #Backspace
    if input == "":
        #Make text white if it isn't already.
        consoleTextColor = color(255, 255, 255)
        consoleText = consoleText[:-1]
        
    #Execute command
    elif input == "\n":
        command = consoleText.split(" ")
        
        #setcard <id>
        #Changes the current challenge card to <id>
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
                
        #If an invalid command is entered, change the color to red instead of adding it to history and clearing text.
        else:
            consoleTextColor = color(255, 0, 0)
            return None
        
        consoleHistory.append(consoleText)
        consoleText = ""
        
    #Command history
    #Up
    elif input == 38:
        consoleText = consoleHistory[len(consoleHistory)-consoleHistoryInt-1]
        if consoleHistoryInt < len(consoleHistory):
            consoleHistoryInt+=1
    
    #Down
    elif input == 40: 
        consoleText = consoleHistory[len(consoleHistory)-consoleHistoryInt-1]
        if consoleHistoryInt > 0:
            consoleHistoryInt-=1
            if consoleHistory == 0:
                consoleText = ""
    
    #Type a character
    elif type(input) == unicode:
        consoleText+=input
