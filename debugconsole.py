import globals

class Console:
    def __init__(self):
        self.showConsole = False
        self.consoleText = ""
        self.consoleHistory = []
        self.consoleTextColor = color(255, 255, 255, 128)
        
    def draw(self):
        #Get base scale
        baseScale = globals.baseScale
        pushMatrix()
        translate(0, width/2)
        
        #Create console box
        pushMatrix()
        translate(0, height, 0)
        fill(0, 0, 0, 128)
        rect(0, 0, 1000*baseScale, 100*baseScale)

        #Write console text, if any.
        translate(0, -12*baseScale, 0)
        textSize(30*baseScale)
        fill(self.consoleTextColor)
        text(self.consoleText, 0, 0)
        popMatrix()
        
        popMatrix()
    
    #Toggles the console on/off.
    def toggleConsole(self):
        self.showConsole = not self.showConsole
        
    #Input a key. Will execute valid commands if the last key is enter ("\n")
    def input(self, input):
        #Backspace
        if input == "" and self.showConsole:
            #Make text white if it isn't already.
            self.consoleTextColor = color(255, 255, 255, 128)
            self.consoleText = self.consoleText[:-1]
            
        #Execute command
        elif input == "\n":
            command = self.consoleText.split(" ")
            
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
                self.consoleTextColor = color(255, 0, 0, 128)
                return None
            
            self.consoleHistory.append(self.consoleText)
            self.consoleText = ""
            
        #Command history
        #Up
        elif input == 38:
            self.consoleText = self.consoleHistory[len(self.consoleHistory)-self.consoleHistoryInt-1]
            if self.consoleHistoryInt < len(consoleHistory):
                self.consoleHistoryInt+=1
        
        #Down
        elif input == 40: 
            self.consoleText = self.consoleHistory[len(self.consoleHistory)-self.consoleHistoryInt-1]
            if self.consoleHistoryInt > 0:
                self.consoleHistoryInt-=1
                if self.consoleHistory == 0:
                    self.consoleText = ""
        
        #Type a character
        elif type(input) == unicode:
            self.consoleText+=input
